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
import numpy as np

from .config import get_config_int, get_config_bool
from .observables import observables
from .momentum import Vector, VectorGrid, locations_index
from . import ploto
from . import tableo


def twodim_ddp(diagdatapoint, params, style = None, filename = "", erange = None, **kwds):
	"""Plot wave function for a DiagDataPoint in a 2D or LL calculation.

	Arguments:
	diagdatapoint  DiagDataPoint instance. Contains the data. The instance must
	               contain eigenvector data, i.e., diagdatapoint.eivec is not
	               None.
	params         PhysParams instance.
	style          'all', 'separate', 'default', or 'together'. Style of the
	               output; for the first three options, plot psi(z) for all wave
	               functions in separate plots (which may be bundled as a single
	               pdf). For 'together', plot a fixed number of |psi(z)|^2 in a
	               single plot.
	filename       String. Filename for the wave functions without extension.
	erange         List or array of two numbers. Energy range for wave function
	               plots. Do not include states with energy eigenvalue outside
	               this range.
	**kwds         Further keyword arguments are passed to the plot function.
	               (Not to the table/csv function.)

	"""
	if not isinstance(filename, str):
		raise TypeError("Argument filename must be a string instance.")
	elif (filename.lower().endswith(".pdf") or filename.lower().endswith(".csv")) and len(filename) > 4:
		fname = filename[:-4]
	elif filename == "":
		fname = "wfs"
	else:
		fname = filename

	if style.lower() in ["all", "separate", "default"]:
		fig = ploto.wavefunction_z(
			params, diagdatapoint, filename = fname + ".pdf", eivalrange = erange,
			**kwds)
		tableo.wavefunction_z(
			params, diagdatapoint, filename = fname + ".csv", eivalrange = erange)
	elif style.lower() == "together":
		n_states = get_config_int('plot_wf_together_num', minval = 1)
		fig = ploto.abs_wavefunctions_z(
			params, diagdatapoint, filename = fname + ".pdf", eivalrange = erange,
			num = n_states, **kwds)
		tableo.abs_wavefunctions_z(
			params, diagdatapoint, filename = fname + ".csv", eivalrange = erange)
	else:
		raise ValueError("Invalid value for argument style")

	if fig is not None:
		diagdatapoint.wffigure = fig
	sys.stderr.write("(wave function plot to %s.pdf)\n" % fname)
	sys.stderr.write("(wave function data to %s.csv)\n" % fname)
	return

def twodim(
	data, params, wfstyle = None, wflocations = None, filename = "",
	erange = None, remember_eivec = True, dependence = 'b',
	set_eivec_phase = False, ll_full = False):
	"""
	Iterate over all data points and plot wave functions (2D and LL modes)

	Arguments:
	data             DiagData instance.
	params           PhysParams instance.
	wfstyle          None or string. Determines the type of wave function plot.
	wflocations      List, array, or VectorGrid instance. Contains the momenta
	                 or magnetic field values where wave functions should be
	                 saved (plot and table).
	filename         String. Filename for the wave functions without extension.
	erange           List or array of two numbers. Energy range for wave
		             function plots.
	remember_eivec   True or False. If True (default), keep the eigenvector data
	                 in memory If False, delete it afterwards.
	dependence       'k' or 'b'. Whether to match the argument wflocations to
	                 momenta (k) or magnetic field (b).
	set_eivec_phase  True or False. If True, fix complex phase of the wave to a
	                 sensible value. If False (default), take wave functions as
	                 given.
	ll_full          True or False. Whether we are in the full LL mode. See
	                 documentation for ploto.wavefunction_z() for more
	                 information.

	Returns:
	status  Integer or None. On success, return the number of successful wave
	        function plots. On error, return None.
	"""
	if wfstyle is None:
		sys.stderr.write("ERROR (wf.twodim): Wave function style should not be None.\n")
		return None
	if wfstyle.lower() not in ["all", "separate", "default", "together"]:
		sys.stderr.write("ERROR (wf.twodim): Invalid wave function plot style '%s'.\n" % wfstyle)
	if not isinstance(wflocations, (list, np.ndarray, VectorGrid)):
		sys.stderr.write("ERROR (wf.twodim): Invalid or missing value for wflocations.\n")
		return None
	if dependence not in ['k', 'b']:
		raise ValueError("Argument dependence must be 'k' or 'b'")

	n_success = 0
	n_loc = len(wflocations)
	sys.stderr.write("Saving wave function plots and data...\n")
	for ddp in data:
		if dependence == 'b':
			if ddp.paramval is None:
				sys.stderr.write("ERROR (wf.twodim): Missing values for magnetic field.\n")
				return None
			k_b_vector = ddp.paramval if isinstance(ddp.paramval, Vector) else Vector(ddp.paramval, astype = 'z')
			k_b_numeric = k_b_vector.z()
		elif dependence == 'k':
			k_b_vector = ddp.k if isinstance(ddp.k, Vector) else Vector(ddp.k, astype = 'x')
			k_b_numeric = k_b_vector.len()
		else:
			raise ValueError("Value for dependence must be either 'k' or 'b'.")
		j = locations_index(wflocations, vec = k_b_vector, vec_numeric = k_b_numeric)
		if j is not None:
			wfloc = wflocations[j]
			if ddp.eivec is None:
				sys.stderr.write("ERROR (wf.twodim): At %s, wave functions are requested, but eigenvector data is missing.\n" % k_b_vector)
				continue
			if set_eivec_phase:
				ddp = ddp.set_eivec_phase(inplace = False)
			if ddp.bindex is None:
				bandlabels = ["" for _ in ddp.eival]
			elif ddp.llindex is None:
				bandlabels = ["%i" % b for b in ddp.bindex]
			else:
				bandlabels = ["(%i, %i)" % lb for lb in zip(ddp.llindex, ddp.bindex)]
			if ddp.char is not None:
				bandlabels = [("[%s]" % c) if len(b) == 0 else ("%s [%s]" % (b, c)) for b, c in zip(bandlabels, ddp.char)]

			display_k = {'B': k_b_vector} if dependence == 'b' else {'k': k_b_vector}
			file_id = ("_" + ddp.file_id()) if get_config_bool('wf_locations_filename') else ('-%i' % (j+1))
			twodim_ddp(
				ddp, params = params, style = wfstyle,
				filename = filename + file_id, erange = erange,
				display_k = display_k, bandlabels = bandlabels, ll_full = ll_full,
				phase_rotate = (not set_eivec_phase))
			n_success += 1
			if not remember_eivec:
				ddp.delete_eivec()
			sys.stderr.write("%i / %i\n" % (n_success, n_loc))

	if n_success == 0 and n_loc > 0:
		sys.stderr.write("Warning (wf.twodim): No wave function files written.\n")
	elif n_success < n_loc:
		sys.stderr.write("Warning (wf.twodim): Fewer wave function files written than requested.\n")
	return n_success

def onedim_ddp(diagdatapoint, params, style = None, filename = "", erange = None, overlap_eivec = None, **kwds):
	"""Plot wave function for a DiagDataPoint in a 1D calculation.

	Arguments:
	diagdatapoint  DiagDataPoint instance. Contains the data. The instance must
	               contain eigenvector data, i.e., diagdatapoint.eivec is not
	               None.
	params         PhysParams instance.
	style          'z' or '1d'; 'y'; 'default' or 'zy'; 'byband' or 'color'.
	               Style of the output. For 'z' or '1d', plot psi(z) for y = 0
	               for all wave functions in separate plots (which may be
	               bundled as a single. For 'y', plot |psi(y)|^2, integrated
	               over z, separated by orbitals (and subbands if requested, see
	               overlap_eivec). For 'zy', plot |psi(z,y)|^2, total over all
	               orbitals. For 'byband' or 'color', plot |psi(z,y)|^2 with
	               colouring depending on local orbital character.
	filename       String. Filename for the wave functions without extension.
	erange         List or array of two numbers. Energy range for wave function
	               plots. Do not include states with energy eigenvalue outside
	               this range.
	overlap_eivec  A dict instance or None. The keys are the subband labels, the
	               values are arrays representing the eigenvector. If style is
	               'y', it will do the following: If given, plot the
	               decomposition of the state into subbands in addition to the
	               decomposition into orbitals. If set to None (default), do the
	               latter only. For other styles, this argument is ignored.
	**kwds         Further keyword arguments are passed to the plot function.
	               (Not to the table/csv function.)
	"""
	if not isinstance(filename, str):
		raise TypeError("Argument filename must be a string instance.")
	elif (filename.lower().endswith(".pdf") or filename.lower().endswith(".csv")) and len(filename) > 4:
		fname = filename[:-4]
	elif filename == "":
		fname = "wfs"
	else:
		fname = filename

	display_k = {'k': diagdatapoint.k}

	if style.lower() in ["z", "1d"]:
		ploto.wavefunction_z(
			params, diagdatapoint, filename = fname + '.pdf', eivalrange = erange,
			display_k = display_k)
	elif style.lower() in ["y"]:
		magn_wf = None if diagdatapoint.paramval is None else diagdatapoint.paramval.z() if isinstance(diagdatapoint.paramval, Vector) else diagdatapoint.paramval
		obsy = observables(diagdatapoint.eivec, params, ['y', 'y2'])
		ploto.abs_wavefunctions_y(
			params, diagdatapoint, filename = fname + '.pdf', eivalrange = erange,
			overlap_eivec = None, obsy = obsy, display_k = display_k, magn = magn_wf)
		tableo.abs_wavefunctions_y(
			params, diagdatapoint, filename = fname + '.csv', eivalrange = erange,
			overlap_eivec = overlap_eivec, precision = 10)
		if overlap_eivec is not None:
			fnamesub = "wfssub" if len(fname) <= 3 else "wfssub" + fname[3:]
			ploto.abs_wavefunctions_y(
				params, diagdatapoint, filename = fnamesub + ".pdf",
				eivalrange = erange, overlap_eivec = overlap_eivec, obsy = obsy,
				display_k = display_k, magn = magn_wf)
	elif style.lower() in ["byband", "by_band", "color", "colour"]:
		ploto.wavefunction_zy(
			params, diagdatapoint, eivalrange = erange, display_k = display_k,
			filename = fname + '.pdf', separate_bands = True)
		tableo.wavefunction_zy(
			params, diagdatapoint, eivalrange = erange,	separate_bands = True,
			filename = fname + '.csv')
	elif style.lower() in ["default", "zy", "yz"]:
		ploto.wavefunction_zy(
			params, diagdatapoint, eivalrange = erange, display_k = display_k,
			filename = fname + '.pdf')
		tableo.wavefunction_zy(
			params, diagdatapoint, eivalrange = erange,	filename = fname + '.csv')
	else:
		sys.stderr.write("ERROR (wf.onedim_ddp): Invalid value '%s' for argument style.\n" % style)
	return

