# kdotpy - k·p theory on a lattice for simulating semiconductor band structures
# Copyright (C) 2024 The kdotpy collaboration <kdotpy@uni-wuerzburg.de>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of kdotpy.
#
# kdotpy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, version 3.
#
# kdotpy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# kdotpy. If not, see <https://www.gnu.org/licenses/>.
#
# Under Section 7 of GPL version 3 we require you to fulfill the following
# additional terms:
#
#     - We require the preservation of the full copyright notice and the license
#       in all original files.
#
#     - We prohibit misrepresentation of the origin of the original files. To
#       obtain the original files, please visit the Git repository at
#       <https://git.physik.uni-wuerzburg.de/kdotpy/kdotpy>
#
#     - As part of a scientific environment, we believe it is reasonable to
#       expect that you follow the rules of good scientific practice when using
#       kdotpy. In particular, we expect that you credit the original authors if
#       you benefit from this program, by citing our work, following the
#       citation instructions in the file CITATION.md bundled with kdotpy.
#
#     - If you make substantial changes to kdotpy, we strongly encourage that
#       you contribute to the original project by joining our team. If you use
#       or publish a modified version of this program, you are required to mark
#       your material in a reasonable way as different from the original
#       version.

import numpy as np
import sys
import re
import csv

MAX_HEADER_ROWS = 10
MAX_FOOTER_ROWS = 10

def read_aligned_table(filename, spacechar = ' '):
	"""Read CSV file with 'aligned table'

	Algorithm:
	Look for columns with spaces, i.e., positions which contain a space
	character in each line.

	Note:
	The table must be aligned properly. Even if a single line does not align
	properly, this function may fail.

	Arguments:
	filename   String. The input file name.
	spacechar  String. Character that should be considered as space (i.e.,
	           alignment character).

	Returns:
	List of list containing the non-space data, split by the spaces.
	"""
	try:
		f = open(filename, 'r')
	except:
		sys.stderr.write("ERROR (read_aligned_table): File '%s' does not exist or cannot be read.\n" % filename)
		return None
	spaces = []
	for line in f:
		ln = line.strip('\n')
		this_spaces = [x in spacechar for x in ln]
		l1 = len(spaces)
		l2 = len(this_spaces)
		if l1 >= l2:
			spaces = [s1 and s2 for s1, s2 in zip(spaces, this_spaces)] + spaces[l2:]
		else:
			spaces = [s1 and s2 for s1, s2 in zip(spaces, this_spaces)] + this_spaces[l1:]
	f.close()

	col_start = [0] if not spaces[0] else []
	col_end = []
	for j in range(1, len(spaces)):
		if spaces[j-1] and (not spaces[j]):
			col_start.append(j)
		elif (not spaces[j-1]) and spaces[j]:
			col_end.append(j)
	if not spaces[-1]:
		col_end.append(len(spaces))
	if len(col_start) != len(col_end):
		raise ValueError
	if len(col_start) == 1:
		sys.stderr.write("ERROR (read_aligned_table): File '%s' is not a properly aligned table.\n" % filename)
		return None

	try:
		f = open(filename, 'r')
	except:
		sys.stderr.write("ERROR (read_aligned_table): File '%s' does not exist or cannot be read.\n" % filename)
		return None
	rawdata = []
	for line in f:
		ln = line.strip('\n')
		l1 = len(ln)
		thisdata = []
		for s, e in zip(col_start, col_end):
			if s >= l1:
				break
			thisdata.append(ln[s: min(e, l1)].strip())
		rawdata.append(thisdata)
	f.close()
	return rawdata

def read_csv(filename):
	"""Read csv (comma separated value) file.
	We use the csv module from Python. We expect that the separation character
	is a comma. The function uses several heuristics to split into header, data,
	and footer parts. Together (in this order) they form the complete data
	present in the file.

	Note:
	If no columns are detected, then try the read_aligned_table function.

	Argument:
	filename   String. The input file name.

	Returns:
	data    List of list of strings. The raw data for the rows that have been
	        recognised as proper 'data'.
	header  List of list of strings. The column headers. This may consist of 0,
	        1, 2, or more rows (maximally MAX_HEADER_ROWS).
	footer  List of list of strings. The column footers. This may consist of 0,
	        1, 2, or more rows (maximally MAX_HEADER_ROWS).
	"""
	try:
		f = open(filename, 'r', newline='')
	except:
		sys.stderr.write("ERROR (read_csv): File '%s' does not exist or cannot be read.\n" % filename)
		return None, None, None
	csvreader = csv.reader(f)
	rawdata = [row for row in csvreader]
	f.close()
	if max([len(row) for row in rawdata]) < 2:
		rawdata = read_aligned_table(filename)
		if rawdata is None:
			return None, None, None

	# determine number of columns and rows
	ncol = max([len(row) for row in rawdata])
	nrow = len(rawdata)

	re_isfloat = re.compile(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?\s*')
	is_numeric = np.array([[re_isfloat.fullmatch(x) for x in row] + [False] * (ncol - len(row)) for row in rawdata], dtype = bool)
	is_empty = np.array([[len(x) == 0 for x in row] + [True] * (ncol - len(row)) for row in rawdata], dtype = bool)
	is_text = ~is_numeric & ~is_empty
	col_numeric = np.sum(is_numeric, axis = 0)
	col_text = np.sum(is_text, axis = 0)
	col_empty = np.sum(is_empty, axis = 0)
	ncol_numeric = 0
	ncol_text = 0
	for c in range(0, ncol):
		if col_text[c] >= 4:
			ncol_text += 1
		elif col_numeric[c] >= 4:
			ncol_numeric += 1
		coltype = 'text' if col_text[c] >= 4 else 'numeric' if col_numeric[c] >= 4 else 'empty'

	row_numeric = np.sum(is_numeric, axis = 1)
	row_text = np.sum(is_text, axis = 1)
	non_data_rows = []
	for r in range(0, nrow):
		if row_text[r] > ncol_text:
			non_data_rows.append(r)
	header_rows = [r for r in non_data_rows if r < MAX_HEADER_ROWS and r < nrow - 2]
	data_starts = 0 if header_rows == [] else max(header_rows) + 1
	footer_rows = [r for r in non_data_rows if r >= nrow - MAX_FOOTER_ROWS and r > data_starts + 1]
	data_ends = nrow if footer_rows == [] else min(footer_rows)

	return rawdata[data_starts:data_ends], rawdata[:data_starts], rawdata[data_ends:]

def read_csv_dict(filename):
	"""Read csv (comma separated value) file and return a dict with the data.
	This uses read_csv(). See documentation for that function for more
	information on how the file is 'parsed'.

	Argument:
	filename   String. The input file name.

	Returns:
	data_dict   A dict instance, whose keys are the column headers and whose
	            data is a list of strings, representing the raw data. The keys
	            are taken from the first valid header or footer row.
	"""
	try:
		data, header, footer = read_csv(filename)
	except:
		return None
	if data is None or len(data) == 0:
		return None
	data_dict = {}
	if len(header) + len(footer) == 0:
		ncol = max([len(row) for row in data])
		for c in range(0, ncol):
			data_dict[c] = [row[c] for row in data]
	else:
		header_full = header + footer
		if len(header_full) == 1:
			colheadings = header_full[0]
		else:
			colheadings = [h for h in zip(*header_full)]
		for c in range(0, len(colheadings)):
			data_dict[colheadings[c]] = [row[c] for row in data]
	return data_dict

