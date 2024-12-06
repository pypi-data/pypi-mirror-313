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
import os

import numpy as np

from ..config import get_config_int, get_config
from ..phystext import orbital_labels
from .auxil import q_z
from .simple import simple, simple2d
from .postwrite import create_archive

### HELPER FUNCTION ###

def get_unique_filenames(filenames, fmt="_%i"):
	"""Make a list of unique filenames by appending fmt (containing an integer number)"""
	unique_filenames = []
	counter = {}
	for fn in filenames:
		if filenames.count(fn) > 1:
			if fn in counter:
				counter[fn] += 1
			else:
				counter[fn] = 1
			unique_filenames.append(fn + (fmt % counter[fn]))
		else:
			unique_filenames.append(fn)
	return unique_filenames

### WAVE FUNCTION TABLES ###

def wavefunction_z(params, diagdatapoint, filename = "", absval = False, title = None, eivalrange = None, bandlabels = None, display_k = None, precision = None):
	"""Table of wave functions psi(z), wrapper version.
	For each state, provide a separate file. In each file, the first column is
	the z value, the subsequent ones the real and imaginary parts of the wave
	function value in each orbital.

	Note:
	The configuration setting 'table_wf_files' may be used to disable this
	function or to gather all csv files into a tar or a zip file.

	Arguments:
	params         PhysParams instance. Used to extract nz, ny, resolutions and
	               number of orbitals.
	diagdatapoint  DiagDataPoint instance.
	filename       String. The output file name.
	absval         NOT USED
	title          NOT USED
	eivalrange     2-tuple or None. If set, write wave function data only for
	               states with eigenvalue in that range.
	bandlabels     NOT USED
	display_k      Vector or None. If set, test whether the vector is zero. If
	               not, suppress character warning. (NOT USED?)
	precision      Integer or None. Number of digits for floating point numbers.
	               If None, use the configuration value.

	No return value.
	"""
	if precision is None:
		precision = get_config_int('table_wf_precision', minval = 2)
	nz = params.nz
	ny = params.ny
	norb = params.norbitals
	# suppress_character_warning = (isinstance(display_k, Vector) and not display_k == 0)
	ddp1 = diagdatapoint.sort_by_eival()
	wf_format = get_config('table_wf_files', choices = ['none', 'csv', 'tar', 'gz', 'gzip', 'targz', 'tar.gz', 'zip', 'zipnozip'])
	fname, fext = os.path.splitext(filename)
	all_files = []
	if wf_format == 'none':  # skip writing csv files
		return
	if isinstance(eivalrange, (list, tuple)) and len(eivalrange) == 2:
		emin, emax = min(eivalrange), max(eivalrange)
	else:
		emin, emax = -np.inf, np.inf

	if ddp1.neig != ddp1.eivec.shape[1]:
		raise ValueError(f"Invalid shape for ddp.eivec. It does not match ddp.neig = {ddp1.neig}.")
	if ddp1.eivec.shape[0] == norb * ny * nz:  # for 1D
		dim = 1
	elif ddp1.eivec.shape[0] == norb * nz:  # for 2D
		dim = 2
		ny = 1
	else:
		raise ValueError("Eigenvectors have incorrect number of components.")

	filenames = []
	for j in range(0, ddp1.neig):
		energy = ddp1.eival[j]
		if energy < emin or energy > emax:
			filenames.append("")
			continue
		if ddp1.llindex is not None and ddp1.char is not None and '?' not in ddp1.char[j]:
			bandlabel = "%s.%i" % (ddp1.char[j], ddp1.llindex[j])
		elif ddp1.char is not None and '?' not in ddp1.char[j]:
			bandlabel = ddp1.char[j]
		elif ddp1.llindex is not None and ddp1.bindex is not None:
			bandlabel = "%i.%i" % (ddp1.llindex[j], ddp1.bindex[j])
		elif ddp1.bindex is not None:
			bandlabel = "%i" % ddp1.bindex[j]
		else:
			bandlabel = "(%i)" % j
		filenames.append(f"{fname}.{bandlabel}")
	filenames = [f"{fn}{fext}" for fn in get_unique_filenames(filenames)]

	for j in range(0, ddp1.neig):
		eivec = ddp1.eivec[:, j]
		energy = ddp1.eival[j]
		if energy < emin or energy > emax:
			continue

		if dim == 1 and ny > 1:  # for 1D
			eivec0 = np.reshape(eivec, (ny, norb * nz))
			eivec = eivec0[ny // 2, :]  # take a section in the middle
			nrm = np.vdot(eivec, eivec)
			eivec /= np.sqrt(nrm)
			# print (eivec.shape)

		wfdata = []
		orblabels = orbital_labels(style = 'unicode', norb = norb)
		heading = []
		subheading = []
		# Try to make largest component purely real
		psimax = eivec[np.argmax(np.abs(eivec))]
		phase = psimax / abs(psimax)

		for b in range(0, norb):
			psi = eivec[b::norb]
			psi2 = np.vdot(psi, psi)
			if precision is not None and np.sum(psi2) < 10**-precision:
				continue
			wfdata.append(np.real(psi / phase))
			wfdata.append(np.imag(psi / phase))
			heading.append(orblabels[b])
			heading.append(orblabels[b])
			subheading.append("Re \u03c8_i")  # Re psi_i
			subheading.append("Im \u03c8_i")  # Im psi_i

		wfdata = np.array(wfdata)
		q_z(filenames[j], params, wfdata, clabel = heading, units = subheading, precision = precision)
		all_files.append(filenames[j])

	if len(all_files) == 0:
		sys.stderr.write("Warning (tableo.wavefunction_z): No output files have been written.\n")
	elif wf_format in ['tar', 'gz', 'gzip', 'targz', 'tar.gz', 'zip', 'zipnozip']:
		archive_file = fname + ("--csv.zip" if 'zip' in wf_format else "--csv.tar.gz" if 'gz' in wf_format else "--csv.tar")
		create_archive(archive_file, all_files, fmt = wf_format)
	return


def abs_wavefunctions_z(params, diagdatapoint, filename = "", absval = False, title = None, eivalrange = None, num = None, bandlabels = None, display_k = None, precision = None):
	"""Table of wave functions |psi(z)|^2, wrapper version.
	Each column represents a wave function, i.e., its probability density at z.
	(This function provides a single file, unlike wavefunctions_z().)

	Arguments:
	params         PhysParams instance. Used to extract nz, ny, resolutions and
	               number of orbitals.
	diagdatapoint  DiagDataPoint instance.
	filename       String. The output file name.
	absval         NOT USED
	title          NOT USED
	eivalrange     2-tuple or None. If set, write wave function data only for
	               states with eigenvalue in that range.
	num            Integer or None. If set, write wave function data only for
	               this many states near the middle of the eivalrange.
	bandlabels     NOT USED
	display_k      Vector or None. If set, test whether the vector is zero. If
	               not, suppress character warning. (NOT USED?)
	precision      Integer or None. Number of digits for floating point numbers.
	               If None, use the configuration value.

	No return value.
	"""
	if precision is None:
		precision = get_config_int('table_wf_precision', minval = 2)
	nz = params.nz
	ny = params.ny
	dz = params.zres
	norb = params.norbitals
	ddp1 = diagdatapoint.sort_by_eival()
	if isinstance(eivalrange, (list, tuple)) and len(eivalrange) == 2:
		emin, emax = min(eivalrange), max(eivalrange)
	else:
		emin, emax = -np.inf, np.inf

	if ddp1.neig != ddp1.eivec.shape[1]:
		raise ValueError(f"Invalid shape for ddp.eivec. It does not match ddp.neig = {ddp1.neig}.")
	if ddp1.eivec.shape[0] == norb * ny * nz:  # for 1D
		dim = 1
	elif ddp1.eivec.shape[0] == norb * nz:  # for 2D
		dim = 2
		ny = 1
	else:
		raise ValueError("Eigenvectors have incorrect number of components.")

	if eivalrange is None:
		e0 = 0.0
		sel = np.argsort(np.abs(ddp1.eival - e0))  # [:min(neig, num)]
		if num < len(sel):
			sel = sel[:num]   # restrict to maximum number
		order = np.argsort(ddp1.eival[sel])
		sel = sel[order]
	else:
		e0 = (emin + emax) / 2
		sel = np.argsort(np.abs(ddp1.eival - e0))  # sort by distance to e0
		sel = sel[(ddp1.eival[sel] >= emin) & (ddp1.eival[sel] <= emax)]  # restrict to eigenvalue range
		if num is not None and num < len(sel):
			sel = sel[:num]   # restrict to maximum number
		order = np.argsort(ddp1.eival[sel])
		sel = sel[order]

	if len(sel) == 0:
		sys.stderr.write("Warning (tableo.abs_wavefunctions_z): No eigenstates to be output.\n")
		return

	wfdata = []
	heading = []
	subheading = []

	for j in sel:
		eivec = ddp1.eivec[:, j]
		energy = ddp1.eival[j]

		if dim == 1 and ny > 1:  # for 1D
			eivec0 = np.reshape(eivec, (ny, norb * nz))
			eivec = eivec0[ny // 2, :]  # take a section in the middle
			nrm = np.vdot(eivec, eivec)
			eivec /= np.sqrt(nrm)

		eivec2 = np.real(eivec.conjugate() * eivec)  # Not a matrix multiplication!
		eivec2a = eivec2.reshape(nz, norb, order = 'C')
		psi2 = np.sum(eivec2a, axis = 1) / dz

		wfdata.append(psi2)
		bandlabel = ddp1.char[j] if ddp1.char is not None and '?' not in ddp1.char[j] else ddp1.bindex[j] if ddp1.bindex is not None else ("(%i)" % j)
		heading.append("%s (%.1f meV)" % (bandlabel, energy))
		subheading.append("|\u03c8|\u00b2")  # |psi|^2

	wfdata = np.array(wfdata)
	q_z(filename, params, wfdata, clabel = heading, units = subheading, precision = precision)
	return


def abs_wavefunctions_y(params, diagdatapoint, filename = "", absval = False, title = None, eivalrange = None, bandlabels = None, overlap_eivec = None, precision = None):
	"""Table of wave functions |psi(y)|^2, wrapper version.
	Each column represents a wave function, i.e., its probability density at y.
	This function also saves additional files per eigenstate with the wave
	functions split by orbital (and optionally, by subband).

	Arguments:
	params         PhysParams instance
	diagdatapoint  DiagDataPoint instance.
	filename       String. The output file name for the file where all total
	               probability densities are saved. The same string is also used
	               for generating the per-state data file.
	eivalrange     None or a 2-tuple. If set, do not plot wave functions for the
	               states whose eigenvalues lie outside this range.
	bandlabels     NOT USED
	overlap_eivec  A dict instance. The keys are the subband labels, the values
	               are arrays representing the eigenvector. If given, include
	               the decomposition into subbands in the per-state data file.
	precision      Integer or None. Number of digits for floating point numbers.
	               If None, use configuration value.

	No return value.
	"""
	if precision is None:
		precision = get_config_int('table_wf_precision', minval = 2)
	wf_format = get_config('table_wf_files', choices = ['none', 'csv', 'tar', 'gz', 'gzip', 'targz', 'tar.gz', 'zip', 'zipnozip'])
	fname, fext = os.path.splitext(filename)
	all_files = []
	if wf_format == 'none':  # skip writing csv files
		return
	if isinstance(eivalrange, (list, tuple)) and len(eivalrange) == 2:
		emin, emax = min(eivalrange), max(eivalrange)
	else:
		emin, emax = -np.inf, np.inf

	nz = params.nz
	ny = params.ny
	dy = params.yres
	norb = params.norbitals
	ddp1 = diagdatapoint.sort_by_eival()

	if ddp1.neig != ddp1.eivec.shape[1]:
		raise ValueError(f"Invalid shape for ddp.eivec. It does not match ddp.neig = {ddp1.neig}.")
	if ddp1.eivec.shape[0] == norb * ny * nz:  # for 1D
		dim = 1
	elif ddp1.eivec.shape[0] == norb * nz:  # for 2D
		dim = 2
		ny = 1
	else:
		raise ValueError("Eigenvectors have incorrect number of components.")

	if ny <= 1 or dim == 2:
		sys.stderr.write("Warning (tableo.abs_wavefunctions_y): No y dimension.\n")
		return

	filenames = []
	for j in range(0, ddp1.neig):
		energy = ddp1.eival[j]
		if energy < emin or energy > emax:
			filenames.append("")
			continue
		energy_int = int(round(energy))
		filenames.append(f"{fname}.{energy_int:+d}meV")
	filenames = [f"{fn}{fext}" for fn in get_unique_filenames(filenames)]

	wf_alldata = []
	wf_energies = []
	y = params.yvalues_nm()
	for j in range(0, ddp1.neig):
		eivec = ddp1.eivec[:, j]
		energy = ddp1.eival[j]
		if energy < emin or energy > emax:
			continue

		eivec = np.reshape(eivec, (ny, nz, norb))
		thisdata = [y]
		columns = ['y', 'sum']

		# Full wave function (for a separate file)
		wf_energies.append(energy)
		psi2_sum = np.sum(np.abs(eivec)**2, axis = (1, 2)) / dy
		wf_alldata.append(psi2_sum)
		thisdata.append(psi2_sum)

		# Orbital overlap
		columns += orbital_labels(style = 'unicode', norb = norb)
		for b in range(0, norb):
			psi = eivec[:, :, b]
			psi2 = np.sum(np.abs(psi)**2, axis = 1)
			thisdata.append(psi2 / dy)

		if overlap_eivec is not None:  # Subband overlap
			eivec = np.reshape(eivec, (ny, nz * norb))
			absv2 = np.sum(np.abs(eivec)**2)
			total_ei = np.sum(np.abs(eivec)**2, axis=1) / absv2
			total_ov = np.zeros_like(total_ei)
			for ov in overlap_eivec:      # overlap_eivec should be a dict
				ovec = overlap_eivec[ov]  # this is the data; argument ov is the label
				absw2 = np.sum(np.abs(ovec)**2)
				psi = np.inner(eivec.conjugate(), ovec)
				# print ('%i (%s):' % (jj+1, ov), eivec.shape, ovec.shape, '->', psi.shape, '->')
				psi2 = np.abs(psi)**2 / absv2 / absw2
				total_ov += psi2
				thisdata.append(psi2 / dy)
				columns.append(ov)
			other_ov = total_ei - total_ov
			thisdata.append(other_ov / dy)
			columns.append('other')

		subheading = ['nm'] + ["|\u03c8|\u00b2" for c in columns[1:]]  # |psi|^2
		simple(filenames[j], thisdata, float_precision = precision, clabel = columns, cunit = subheading)
		all_files.append(filenames[j])

	if len(wf_alldata) == 0:
		sys.stderr.write("Warning (tableo.wavefunction_y): No output files have been written.\n")
		return

	alldata = np.concatenate(([y], np.array(wf_alldata)))
	heading = ['y'] + ["%.2f meV" % e for e in wf_energies]
	subheading = ['nm'] + ["|\u03c8|\u00b2" for e in wf_energies]  # |psi|^2
	simple(filename, alldata, float_precision = precision, clabel = heading, cunit = subheading)
	all_files.append(filename)

	if wf_format in ['tar', 'gz', 'gzip', 'targz', 'tar.gz', 'zip', 'zipnozip']:
		archive_file = fname + ("--csv.zip" if 'zip' in wf_format else "--csv.tar.gz" if 'gz' in wf_format else "--csv.tar")
		create_archive(archive_file, all_files, fmt = wf_format)
	return


def wavefunction_zy(params, diagdatapoint, filename = "", absval = True, separate_bands = False, title = None, eivalrange = None, precision = None):
	"""Table of wave functions |psi(z, y)|^2, wrapper version.
	For each eigenstate, compose a two-dimensional table with the y coordinates
	in the columns and z coordinates in the rows.

	Arguments:
	params         PhysParams instance
	diagdatapoint  DiagDataPoint instance.
	filename       String. The output file name for the file where all total
	               probability densities are saved. The same string is also used
	               for generating the per-state data file.
	absval         NOT USED
	separate_bands  If False, sum absolute value squared over the orbitals.
	                If True, provide data for each orbital separately.
	title          NOT USED
	eivalrange     None or a 2-tuple. If set, do not plot wave functions for the
	               states whose eigenvalues lie outside this range.
	precision      Integer or None. Number of digits for floating point numbers.
	               If None, use configuration value.

	No return value.
	"""
	if precision is None:
		precision = get_config_int('table_wf_precision', minval = 2)
	wf_format = get_config('table_wf_files', choices = ['none', 'csv', 'tar', 'gz', 'gzip', 'targz', 'tar.gz', 'zip', 'zipnozip'])
	fname, fext = os.path.splitext(filename)
	all_files = []
	if wf_format == 'none':  # skip writing csv files
		return
	if isinstance(eivalrange, (list, tuple)) and len(eivalrange) == 2:
		emin, emax = min(eivalrange), max(eivalrange)
	else:
		emin, emax = -np.inf, np.inf

	nz = params.nz
	ny = params.ny
	dz = params.zres
	dy = params.yres
	z = params.zvalues_nm()
	y = params.yvalues_nm()
	norb = params.norbitals
	labels = {'axislabels': ['z', 'y'],	'axisunits': ['nm', 'nm'], 'datalabel': '|psi|^2', 'dataunit': 'nm^-2'}

	ddp1 = diagdatapoint.sort_by_eival()
	if ddp1.neig != ddp1.eivec.shape[1]:
		raise ValueError(f"Invalid shape for ddp.eivec. It does not match ddp.neig = {ddp1.neig}.")
	if ddp1.eivec.shape[0] == norb * ny * nz:  # for 1D
		dim = 1
	elif ddp1.eivec.shape[0] == norb * nz:  # for 2D
		dim = 2
		ny = 1
	else:
		raise ValueError("Eigenvectors have incorrect number of components.")

	if ny <= 1 or dim == 2:
		sys.stderr.write("Warning (tableo.wavefunction_zy): No y dimension.\n")
		return

	filenames = []
	for j in range(0, ddp1.neig):
		energy = ddp1.eival[j]
		if energy < emin or energy > emax:
			filenames.append("")
			continue
		energy_int = int(round(energy))
		filenames.append(f"{fname}.{energy_int:+d}meV")
	filenames = [f"{fn}{fext}" for fn in get_unique_filenames(filenames)]

	wf_energies = []
	for j in range(0, ddp1.neig):
		energy = ddp1.eival[j]
		if energy < emin or energy > emax:
			continue
		wf_energies.append(energy)

		# Full wave function
		eivec = np.reshape(ddp1.eivec[:, j], (ny, nz, norb))
		if separate_bands:
			eivecdata = np.abs(eivec)**2 / dy / dz
			eivecdata = eivecdata.transpose(2, 0, 1).reshape(ny * norb, nz)
			oval = np.repeat(np.arange(0, norb), ny)  # TODO: For future use.
			yval = np.tile(y, norb)
		else:
			eivecdata = np.sum(np.abs(eivec)**2, axis = 2).T / dy / dz
			yval = y

		clabel = "%.3f meV" % energy
		# TODO: For separate_bands = True, the data now appears as norb tables
		# in succession, with the orbital DOF unlabelled. As of now, simple2d
		# does not support multi-indexing for row and column headers. An
		# alternative solution would be to put each orbital on a different
		# worksheet (infrastructure is also not available).
		simple2d(
			filenames[j], z, yval, eivecdata, float_precision = precision,
			clabel = clabel, **labels)
		all_files.append(filenames[j])

	if len(all_files) == 0:
		sys.stderr.write("Warning (tableo.wavefunction_zy): No output files have been written.\n")
	elif wf_format in ['tar', 'gz', 'gzip', 'targz', 'tar.gz', 'zip', 'zipnozip']:
		archive_file = fname + ("--csv.zip" if 'zip' in wf_format else "--csv.tar.gz" if 'gz' in wf_format else "--csv.tar")
		create_archive(archive_file, all_files, fmt = wf_format)
	return
