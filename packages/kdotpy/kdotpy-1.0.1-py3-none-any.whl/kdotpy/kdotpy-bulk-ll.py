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

from os import environ
environ['OMP_NUM_THREADS'] = '1'
import sys
import os.path
import numpy as np

from .config import initialize_config, get_config_int, get_config_bool
from .materials import initialize_materials
from . import cmdargs
from .momentum import Vector, VectorGrid, ZippedKB
from .observables import all_observables, get_all_obsids, plotobs_apply_llmode
from .physparams import print_length_scales
from .symbolic import SymbolicHamiltonian
from .hamiltonian import hbulk_split
from .bandalign import bandindices
from .diagonalization import DiagData

from .parallel import set_job_monitor
from .diagonalization import lldiagonalization as lldiag

from . import xmlio
from . import tableo
from . import ploto

sysargv = cmdargs.sysargv

#### MAIN PROGRAM ####
def main():
	SCRIPT = os.path.basename(__file__)  # the filename of this script, without directory
	scriptdir = os.path.dirname(os.path.realpath(__file__))
	initialize_config()
	initialize_materials()
	numpy_printprecision = get_config_int('numpy_printprecision', minval = 0)
	numpy_linewidth = get_config_int('numpy_linewidth', minval = 0)
	np.set_printoptions(precision=numpy_printprecision, linewidth=numpy_linewidth)
	ploto.initialize()

	## Process command line arguments
	ll_mode = 'legacy' if 'lllegacy' in sysargv else 'full' if 'llfull' in sysargv else 'sym'  # possible options: 'legacy', 'sym', 'full'
	params = cmdargs.params(kdim = 3)
	ks = cmdargs.vectorvalues('k', onedim = True, twodim = True, threedim = True)
	bs = cmdargs.vectorvalues('b', onedim = True, twodim = True, threedim = True, defaultaxis = 'z')
	try:
		kbs = ZippedKB(ks, bs)
	except ValueError:
		sys.stderr.write("ERROR (%s): Momentum k and magnetic field b may not both be multi-valued ranges.\n" % SCRIPT)
		exit(1)
	if kbs.dependence() != 'b':
		sys.stderr.write("ERROR (%s): The dependence must be on magnetic field b. Use the argument b followed by a range.\n" % SCRIPT)
		exit(1)
		# Note: Because of this safeguard, we can keep using the VectorGrid instance bs troughout.

	opts = cmdargs.options(axial_automatic = True)
	plotopts = cmdargs.plot_options(format_args = (params, opts, kbs))
	erange = cmdargs.erange()
	curdir, outdir = cmdargs.outdir()  # changes dir as well
	outputid = cmdargs.outputid(format_args = (params, opts, kbs))
	bs = cmdargs.vectorvalues('b', onedim = True, twodim = True, threedim = True, defaultaxis = 'z')
	job_monitor_limit = get_config_int('job_monitor_limit', minval = 0)
	set_job_monitor(len(bs) <= job_monitor_limit)

	## Modify parameters
	params.l_barr = 0.0
	params.nz = 1

	## Define observables
	obsids = get_all_obsids(kdim=3, ll=True, norb=params.norbitals, opts=opts)
	all_observables.initialize(param = params, dimful = 'dimful_obs' in opts and opts['dimful_obs'])

	## Do test on length scales and print warnings if applicable
	print_length_scales(params)

	# Check and manipulate momentum value
	if ks is None or len(ks) == 0:
		sys.stderr.write("Warning: By default, kz = 0\n")
		k0 = Vector(0.0, astype = 'z')
	elif len(ks) > 1:
		sys.stderr.write("Warning: Only at first k value; other values are ignored\n")
		k0 = ks[0]
	else:  # len(ks) == 1
		k0 = ks[0]
	kx, ky, kz = k0.xyz()
	if abs(kx) > 1e-6 or abs(ky) > 1e-6:
		sys.stderr.write("Warning: In LL mode, kx and ky values are ignored.\n")
	k0 = Vector(kz, astype = 'z')

	modelopts_default = {'lattice_reg': False, 'split': 0.0, 'splittype': 'auto', 'ignorestrain': False,
	                     'obs': obsids, 'axial': True, 'bia': False, 'obs_prop': all_observables, 'return_eivec': False}
	mapping = {'targetenergy': 'energy'}
	modelopts = cmdargs.initialize_opts(opts, modelopts_default, mapping)
	num_cpus = opts.get('cpu', 1)
	ll_max = opts.get('ll_max', 30)

	if isinstance(bs, VectorGrid) and not bs.is_vertical():
		sys.stderr.write("Warning (%s): The 'orbital part' of the in-plane magnetic field (Bx, By) is neglected in this calculation mode, unlike Bz. The components Bx and By affect only Zeeman effect, paramagnetic exchange, etc.\n" % SCRIPT)
	# TODO: Anisotropic in-plane strain also requires full mode
	if modelopts['axial'] is False or modelopts['bia'] is True:
		ll_mode = 'full'
	if modelopts['bia'] and modelopts['split'] != 0.0:
		sys.stderr.write("Warning (%s): With BIA, the requested splitting will be applied only to certain momenta in order to lift degeneracies without causing unwanted asymmetries.\n" % SCRIPT)
	modelopts['lattice_reg'] = get_config_bool('lattice_regularization')
	if modelopts['lattice_reg'] is True:
		sys.stderr.write("Warning (%s): It is recommended to disable lattice regularization using the configuration option 'lattice_regularization=false'.\n" % SCRIPT)
	if ll_mode == 'full':
		obsids.extend(["llavg", "llbymax"])
		sys.stderr.write("Warning (%s): For bulk LL, the implementation of Landau-level mode '%s' is experimental. Please double check your results.\n" % (SCRIPT, ll_mode))

	# Process LL mode dependent observables (LL index, etc.)
	plotobs_apply_llmode(plotopts, ll_mode)

	# Calculate symbolic hamiltonian
	if ll_mode in ['sym', 'full']:
		modelopts_hsym = modelopts.copy()
		for k in ['obs', 'obs_prop', 'energy', 'neig', 'cpu', 'pot', 'return_eivec']:
			if k in modelopts_hsym:
				del modelopts_hsym[k]
		kz = 0.0 if ks is None or len(ks) == 0 else ks[0].z() if isinstance(ks[0], Vector) else 0.0
		h_sym = SymbolicHamiltonian(hbulk_split, (params,), modelopts_hsym, hmagn = True, kz = kz)
	else:
		h_sym = None

	# Do diagonalization at k = 0, b = 0 to get CNP (e0)
	data0 = lldiag.hbulk_ll0(params, modelopts, description='Calculating bulk LL dispersion (B=0)')
	bandindices(DiagData([data0]), params=params)  # This stores band indices in data0
	e0 = data0.get_eival0()

	# Do diagonalization for all B values
	data = lldiag.hbulk_ll(ll_mode, kbs, ll_max, h_sym, params, modelopts, list_kwds = {}, description = 'Calculating bulk LL dispersion', num_processes = num_cpus)
	bandindices(data, params=params, e0=e0)

	## Energy shift (TODO: Not very elegant)
	if 'zeroenergy' in opts and opts['zeroenergy']:
		e_ref = 0.0 if 'eshift' not in opts else opts['eshift']
		eshift = data.set_zero_energy(e_ref)
		if eshift is not None:
			sys.stderr.write("Warning (%s): Energy shifted by %.3f meV. Experimental function: Other input and output energies may still refer to the unshifted energy.\n" % (SCRIPT, eshift))
	elif 'eshift' in opts and opts['eshift'] != 0.0:
		data.shift_energy(opts['eshift'])
		sys.stderr.write("Warning (%s): Energy shifted by %.3f meV. Experimental function: Other input and output energies may still refer to the unshifted energy.\n" % (SCRIPT, opts['eshift']))

	table_erange = erange  # if "filtertable" in sysargv else None

	if data is None:
		sys.stderr.write("ERROR (%s): No data.\n" % SCRIPT)
		exit(2)

	## Write Table
	b = data.get_paramval()
	tableo.disp("bdependence%s.csv" % outputid, data, params, erange = table_erange, observables = obsids, dependence = [b, "b", "T"])
	plotobs = plotopts.get('obs')
	tableo.disp_byband("bdependence%s.csv" % outputid, data, params, erange = erange, observable = plotobs)

	## Write XML
	xmlio.writefile("output%s.xml" % outputid, data, params, observables = obsids, caller = SCRIPT, options = opts, dependence = [b, "b", "T"], dependentoptions = [])

	## Write plot
	if len(bs) > 1:
		ploto.bands_1d(data, filename = "bdependence%s.pdf" % outputid, showplot = False, erange = erange, paramstr = ploto.format_axis_label("$B$", "$\\mathrm{T}$"), **plotopts)
	else:
		sys.stderr.write("Warning (%s): For 0-dimensional arrays, skip plot.\n" % SCRIPT)

	## Warning for unparsed arguments
	unparsed = sysargv.unparsed_warning(color = sys.stderr.isatty())
	if unparsed is not None:
		sys.stderr.write("Warning (%s): The following marked command line arguments were not used: %s\n" % (SCRIPT, unparsed))

	exit(0)

if __name__ == '__main__':
	main()

