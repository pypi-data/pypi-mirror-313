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

import sys
import os.path

from multiprocessing import cpu_count as mp_cpu_count
from platform import system
from subprocess import PIPE, Popen
from .cmdargs.tools import isint, isfloat
from . import cmdargs
from .config import get_config


def parse_batch_args(sysargv):
	"""Parse arguments for kdotpy-batch
	
	This function extracts the @-variables and the command to run, plus a few
	auxiliary variables (ncpu, nprocess).
	
	Arguments:
	sysargv  List of strings. The command line arguments, analogous to sys.argv.
	
	Returns:
	allvar   List of strings. The names of the @-variables
	allval   List. The values of the @-variables.
	cmd      List of strings. The command line to execute.
	opts     A dict instance. Contains options: npcu and nprocess.
	"""
	allvar = []
	cmd_at = None
	ncpu = None
	nprocess = None

	# Get arguments specific for 'kdotpy-batch.py'
	for arg in sysargv[1:]:
		if arg.startswith("@"):
			var = arg[1:]
			if "@" in var:
				sys.stderr.write("ERROR (parse_batch_args): No second '@' allowed in variable name\n")
				exit(1)
			elif "{" in var or "}" in var:
				sys.stderr.write("ERROR (parse_batch_args): Variable name cannot contain '{' or '}'.\n")
				exit(1)
			elif var in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
				sys.stderr.write("ERROR (parse_batch_args): Variable name cannot be a single digit.\n")
				exit(1)
			elif var != "" and var in allvar:
				sys.stderr.write("ERROR (parse_batch_args): Variable names must be unique.\n")
				exit(1)
			else:   # zero-length variable identifier is explicitly included
				allvar.append(var)
		elif arg == 'cpu' or arg == 'cpus':
			if nprocess is not None:
				sys.stderr.write("ERROR (parse_batch_args): Specification of number of cpus and number of processes cannot be combined.\n")
				exit(1)
			try:
				ncpu = int(sysargv[sysargv.index(arg) + 1])
			except:
				sys.stderr.write("ERROR (parse_batch_args): Argument '%s' must be followed by a number.\n")
				exit(1)
		elif arg == 'parallel' or arg == 'proc':
			if nprocess is not None:
				sys.stderr.write("ERROR (parse_batch_args): Specification of number of cpus and number of processes cannot be combined.\n")
				exit(1)
			try:
				nprocess = int(sysargv[sysargv.index(arg) + 1])
			except:
				sys.stderr.write("ERROR (parse_batch_args): Argument '%s' must be followed by a number.\n")
				exit(1)
		elif arg == 'do' or arg == '--' or arg == 'cmd':
			cmd_at = sysargv.index(arg)
			break

	if cmd_at is None or cmd_at >= len(sysargv) - 1:
		sys.stderr.write("ERROR (parse_batch_args): No command specified. The command to be run must follow 'do', 'cmd' or '--'.\n")
		exit(1)
	if len(allvar) == 0:
		sys.stderr.write("ERROR (parse_batch_args): No variable ranges specified.\n")

	# Parse arguments. Handle the @ arguments; range and list specifications.
	allval = []
	for v in allvar:
		vrange = cmdargs.grid(args = '@' + v, from_argv = sys.argv[:cmd_at])
		if vrange == [] or vrange is None:
			argn = sys.argv.index("@" + v)
			if cmd_at < argn + 1 or not sys.argv[argn + 1].startswith("["):
				sys.stderr.write("ERROR (parse_batch_args): Variable specification must be followed by range or list.\n")
				exit(1)
			str_to_parse = " ".join(sys.argv[argn + 1: cmd_at])
			str_to_parse = str_to_parse.split('@')[0]
			str_to_parse1 = ""
			j = 0
			for s in str_to_parse:
				if s == '[':
					j += 1
				elif s == ']':
					j -= 1
				str_to_parse1 += s
				if j == 0:
					break

			if str_to_parse1.count('[') != str_to_parse1.count(']'):
				sys.stderr.write("ERROR (parse_batch_args): Unbalanced brackets [ and ].\n")
				exit(1)
			list_of_str = str_to_parse1[1:-1].split(",")
			vrange = [int(x) if isint(x) else float(x) if isfloat(x) else x.strip() for x in list_of_str]
		elif all([x == int(x) for x in vrange]):
			vrange = [int(x) for x in vrange]

		allval.append(vrange)
	
	# Extract command-line template for the program to execute
	cmd = sys.argv[cmd_at + 1:]
	# Define options dict
	opts = {'ncpu': ncpu, 'nprocess': nprocess}
	return allvar, allval, cmd, opts

def ncpu_nprocess(cmd, ncpu = None, nprocess = None, **opts):
	"""Extract number of parallel jobs to be run
	
	Arguments:
	cmd       List of strings. Command line arguments.
	ncpu      None or int. The number of cpus extracted by parse_batch_args().
	nprocess  None or int. The number of processes extracted by
	          parse_batch_args().
	**opts    Unused arguments.
	
	Returns:
	ncpu      Integer. The number of cpus.
	nprocess  Integer. The number of processes.
	"""
	try:
		maxcpu = mp_cpu_count()
	except:
		sys.stderr.write("Warning (kdotpy-batch.py): Could not determine number of CPUs.\n")
		maxcpu = None
	cmd_ncpu = 1 if maxcpu is None else maxcpu
	for j, arg in enumerate(cmd[:-1]):
		if arg in ["cpu", "cpus", "ncpu"]:
			try:
				cmd_ncpu = int(cmd[j+1])
			except:
				pass
			else:
				break

	if nprocess is None:
		if ncpu is not None:
			nprocess = ncpu // cmd_ncpu
		else:
			nprocess = 1 if maxcpu is None else (maxcpu // cmd_ncpu)
	if nprocess < 1:
		nprocess = 1
		sys.stderr.write("Warning (kdotpy-batch.py): Minimum number of processes is one (sequential run).\n")
	if nprocess > 1 and cmd_ncpu > 1:
		ncpu = nprocess * cmd_ncpu
		if maxcpu is not None and ncpu > maxcpu:
			sys.stderr.write("Warning (kdotpy-batch.py): Number of requested parallel processes is larger than the available number of CPUs. This is not recommended, because of a significant performance penalty.\n")
	return ncpu, nprocess

def nice_command(niceness, command):
	"""Provide "niceness" command for "nicing" subprocesses

	Arguments:
	niceness  Integer >= 0. The target 'nice' value of the command.
	command   List of strings. The command line arguments.

	Returns:
	niced_cmd  List of strings. This is the list command prepended by the
	           appropriate 'nice' command.
	"""
	nicecmd = []
	if system() == 'Windows':
		# no nice command
		return command
	if isinstance(niceness, int):
		if niceness < 0:
			sys.stderr.write("Warning (nice_command): Minimum niceness is 0\n")
			nicecmd = ["nice", "-n", "0"]
		elif niceness > 0 and niceness <= 19:
			nicecmd = ["nice", "-n", "%i" % niceness]
		elif niceness >= 20:
			sys.stderr.write("Warning (nice_command): Maximum niceness is 19\n")
			nicecmd = ["nice", "-n", "19"]
		elif niceness == 0:  # let's make this explicit
			pass
	elif niceness is None:
		pass
	else:
		raise TypeError("Niceness must be an integer")
	if not isinstance(command, list):
		raise TypeError("Argument command must be a list")
	return nicecmd + command


def run_and_wait(cmdline_args, niceness = 0, out = None, err = None):
	"""Runs a command without monitoring

	The only way to interrupt the execution is by Ctrl-C (or by sending a signal
	to the external program from somewhere else, e.g., another shell or htop).

	NOTE: It is typically a bad idea to terminate any of the worker processes.
	It should be safe to terminate/abort/interrupt the kdotpy-batch.py parent
	process, but this is currently not the case. (TODO)

	TODO: The exit statuses are not returned correctly in a multithreaded run.
	This can probably be solved only with a dedicated parallelization function
	for kdotpy-batch.py (which is probably a good idea anyway). Try:
	  python3 kdotpy-batch.py cpu 4 @x 0 10 / 10 do sleep -1
	versus
	  python3 kdotpy-batch.py cpu 1 @x 0 10 / 10 do sleep -1
	(sleep -1 is an illegal command that returns exit code 1)

	Arguments:
	cmdline_args  List of strings. The command line arguments.
	niceness      Integer >= 0. The target 'nice' value of the command.
	out           File, PIPE or None. Refers to stdout stream.
	err           File, PIPE or None. Refers to stderr stream.

	Returns:
	exitstatus  Integer. The exit status of the command. This is 0 when
	            successful, nonzero if an error has occurred.
	p_stdout    Contents of stdout output from the command
	p_stderr    Contents of stderr output from the command
	"""

	try:
		nicecmd = nice_command(niceness, command = [])
	except:
		nicecmd = []

	if out is None:
		out = PIPE
	if err is None:
		err = PIPE

	try:
		p = Popen(nicecmd + cmdline_args, stdout=out, stderr=err)
	except OSError as e:
		sys.stderr.write("ERROR (run_and_wait): OSError %i %s\n" % (e.errno, e.strerror))
		return None, None, None
	except:
		sys.stderr.write("ERROR (run_and_wait): Generic error\n")
		return None, None, None

	try:
		p_stdout, p_stderr = p.communicate()
	except KeyboardInterrupt:
		sys.stderr.write("Warning (run_and_wait): Keyboard interrupt\n")
		p.terminate()
		exitstatus = p.poll()
		return exitstatus, None, None
	except:
		sys.stderr.write("Warning (run_and_wait): Abnormal termination. Unhandled exception.\n")
		return None, None, None
	else:
		exitstatus = p.poll()

	if exitstatus != 0:
		sys.stderr.write("Warning (run_and_wait): Termination with exit status %i\n" % exitstatus)

	return exitstatus, p_stdout, p_stderr


def multi_values(*lists):
	"""Give all combinations of the elements of lists as tuples

	For example: multi_values(['a', 'b'], [1, 2, 3]) yields
	  [('a', 1), ('a', 2), ('a', 3), ('b', 1), ('b', 2), ('b', 3)]

	Arguments:
	lists   One or more lists (tuples or other iterables also allowed).

	Returns:
	allval   List of tuples. Tuples containing all combinations of elements from
	         the input lists.
	strides  Tuple. Its i-th element corresponds to the size of one step
	         ('stride') to advance one element corresponding to	the i-th list.
	         In the above example, this would be (3, 1).
	"""
	dim = len(lists)
	if dim == 0:
		return [], ()
	allval = [(x,) for x in lists[0]]
	strides = [1]
	for v in lists[1:]:
		old_allval = allval
		allval = [x + (y,) for x in old_allval for y in v]
		strides = [s * len(v) for s in strides]
		strides.append(1)
	return allval, tuple(strides)

def replace_float(val, fmt = '%s', smart_decimal = True):
	fstr = fmt % val
	if smart_decimal and '.' in fstr:
		fstr = fstr.rstrip('0')
		return fstr + '0' if fstr.endswith(".") else fstr  # strip zeros but keep one after decimal point
	else:
		return fstr

def replace_and_do_command(idx, val, nval, cmd, allvar, strides):
	"""Do '@' replacements and run the command.

	In the list of command arguments, replace indicators with '@' by the
	appropriate input values. Then, execute the resulting command.
	This function is typically iterated over the 'allval' output of
	multi_values().

	The following replacements are done:
	  @@            Total number of values (= nval)
	  @0            Index (= idx)
	  @1, @2, ...   Index of the i-th variable
	  @varname      Value of variable with name 'varname' (specified in 'allvar')
	NOTE: The index outputs @0, @1, @2, ... are 1-based (1, ..., m). The
	arguments to this function use 0-based (0, ..., m-1) indexing, however.

	Arguments:
	idx      Integer. Index (counter) of the run; position in the 'allval' list
	val      n-tuple. Input value (n-tuple)
	nval     Integer. Total number of values (length of 'allval')
	cmd      List of strings. The command line arguments.
	allvar   List of strings. The variable names.
	strides  List or tuple of integers. Step size of i-th variable; output of
		     multi_values().

	Returns:
	exitstatus  Integer. Exit code of the executed command
	"""
	cmd1 = []

	# Numeric multi-index
	ji = []
	ji1 = idx
	for s in strides:
		ji.append(ji1 // s)
		ji1 -= ji[-1] * s

	# Define formatting function for values
	float_format_cfg = get_config('batch_float_format')
	if float_format_cfg.endswith('.'):
		float_format = float_format_cfg.rstrip('.')
		smart_decimal = True
	else:
		float_format = float_format_cfg
		smart_decimal = False
	try:
		float_format % -1.0
	except:
		sys.stderr.write("Warning (replace_and_do_command): Invalid format for float (configuration option 'batch_float_format').\n")
		raise

	# Define replacements as dict
	def fmt(val):
		return replace_float(val, fmt = float_format, smart_decimal = smart_decimal) if isinstance(val, float) else str(val)
	replacements = {'@@': "%i" % nval, '@0': "%i" % (idx + 1)}
	for i, v in enumerate(val):
		replacements["@%i" % (i+1)] = str(ji[i] + 1)
		replacements["@{%s}" % allvar[i]] = fmt(v)
		replacements["@" + allvar[i]] = fmt(v)

	# Perform replacements
	def replace_with_dict(s, d):
		for from_, to in d.items():
			s = s.replace(from_, to)
		return s
	cmd1 = [replace_with_dict(c, replacements) if '@' in c else c for c in cmd]

	# Determine output id; take from the command list
	# Default is the index (counter value)
	outputid = ".%i" % (idx + 1)
	for j, c in enumerate(cmd1[:-1]):
		if c in ["out", "outputid", "outputname", "outid", "outfile"]:
			outputid = cmd1[j+1]

	if 'dryrun' in sys.argv:
		print("%i: " % (idx + 1) + ", ".join(["@%s = %s" % (var, fmt(v)) for var, v in zip(allvar, val)]))
		print(" ".join(cmd1))
		exitstatus = 0
	else:
		curdir, outdir = cmdargs.outdir(do_chdir = False, replacements = replacements)
		fout = open(os.path.join(outdir, "stdout%s.%s" % (outputid, get_config('batch_stdout_extension'))), "w")
		ferr = open(os.path.join(outdir, "stderr%s.%s" % (outputid, get_config('batch_stderr_extension'))), "w")
		exitstatus, stdout, stderr = run_and_wait(cmd1, niceness = 5, out = fout, err = ferr)
		fout.close()
		ferr.close()
	if exitstatus is None:
		raise KeyboardInterrupt

	return exitstatus


