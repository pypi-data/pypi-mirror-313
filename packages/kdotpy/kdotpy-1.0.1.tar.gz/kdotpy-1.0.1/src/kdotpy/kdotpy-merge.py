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
import os.path
import re

from .config import initialize_config, cmdargs_config
from .materials import initialize_materials
from . import cmdargs
from .bandalign import bandindices
from . import postprocess

from . import ploto
from . import tableo
from . import xmlio

SCRIPT = os.path.basename(__file__)  # the filename of this script, without directory

def main():
	initialize_config()
	initialize_materials()
	ploto.initialize()

	erange = cmdargs.erange()  # plot range (energy)

	filenames = []
	defaultfilename = "output.xml"
	accept_default_files = False
	# If the argument '--' appears in the command line, consider only the arguments
	# after the last '--' as input files
	argstart = 1
	for j in range(1, len(sys.argv)):
		if sys.argv[j] == '--':
			argstart = j
	for a in sys.argv[argstart:]:
		if os.path.isfile(a):
			if a.endswith(".tar.gz") or a.endswith(".tar"):
				tar_contents = xmlio.find_in_tar(a, "output*.xml")
				if tar_contents is not None and tar_contents != []:
					filenames.extend(tar_contents)
			else:
				filenames.append(a)
		elif os.path.isdir(a):
			ls = os.listdir(a)
			filenames_thisdir = []
			for fname in ls:
				m = re.match(r"output.*\.xml(\.gz)?", fname)
				if m is not None:
					filenames_thisdir.append(os.path.join(a, fname))
				m = re.match(r"data.*\.tar\.gz", fname)
				if m is not None:
					tar_contents = xmlio.find_in_tar(os.path.join(a, fname), "output*.xml")
					if tar_contents is not None and tar_contents != []:
						filenames_thisdir.extend(tar_contents)
			if len(filenames_thisdir) > 0:
				filenames.extend(filenames_thisdir)
			else:
				sys.stderr.write("Warning (%s): No data files \"output*.xml\" found in directory %s\n" % (SCRIPT, a))

	if len(filenames) == 0:
		if not accept_default_files:
			sys.stderr.write("ERROR (%s): No data files\n" % SCRIPT)
			exit(2)
		elif os.path.isfile(defaultfilename):
			sys.stderr.write("Warning (%s): No data files specified. Using default \"%s\"\n" % (SCRIPT, defaultfilename))
			filenames = [defaultfilename]
		else:
			ls = os.listdir(".")
			for fname in ls:
				m = re.match(r"output.*\.xml", fname)
				if m is not None:
					filenames.append(fname)
			if len(filenames) == 0:
				sys.stderr.write("ERROR (%s): No data files found.\n" % SCRIPT)
				exit(2)
			else:
				sys.stderr.write("Warning (%s): No data files specified. Using default \"output.##.xml\"; %i files\n" % (SCRIPT, len(filenames)))

	print("Files:")
	for f in filenames:
		print(("%s:%s" % f) if isinstance(f, tuple) else f)

	data, params, dependence = xmlio.readfiles(filenames)
	if len(data) == 0:
		sys.stderr.write("ERROR (%s): No data.\n" % SCRIPT)
		exit(2)
	if not (dependence == 'k' or dependence == 'b' or (isinstance(dependence, list) and dependence[1] == 'b')):
		sys.stderr.write("ERROR (%s): Unexpected dependence type.\n" % SCRIPT)
		exit(1)

	# Reload configuration options from command line, because they may have been
	# overwritten by readfiles.
	cmdargs_config()

	opts = cmdargs.options(axial_automatic = 'ignore')
	vgrid = {} if data.grid is None else data.grid  # VectorGrid for plot title formatting
	plotopts = cmdargs.plot_options(format_args = (params, opts, vgrid))
	curdir, outdir = cmdargs.outdir()  # changes dir as well
	outputid = cmdargs.outputid(format_args = (params, opts, vgrid))  # output filename modifier

	if "select" in sys.argv:
		argn = sys.argv.index("select")
		try:
			sel_component = sys.argv[argn + 1]
			sel_value = float(sys.argv[argn + 2])
		except:
			sys.stderr.write("ERROR (%s): Argument \"select\" must be followed by k, kx, ky, or kphi and a number.\n" % SCRIPT)
			exit(1)
		# sel_idx, sel_kval = k_select(data.get_momenta(), sel_component, sel_value)
		sel_idx, sel_kval = data.get_momentum_grid().select(sel_component, sel_value)
		data = [data[j] for j in sel_idx]

		if len(data) == 0:
			sys.stderr.write("Warning (%s): No data for this selection.\n" % SCRIPT)

	if len(data) == 0:
		sys.stderr.write("ERROR (%s): Nothing to be plotted.\n" % SCRIPT)
		exit(2)

	if "sortdata" in sys.argv:
		data.sort_by_grid()

	if "verbose" in sys.argv:
		if dependence == 'k':
			print("Momentum values:")
			print(", ". join([str(d.k) for d in data]))
		elif dependence == 'b' or isinstance(dependence, list):
			print("Parameter (B) values:")
			print(", ". join([str(d.paramval) for d in data]))
		else:
			raise ValueError("Illegal value for variable dependence")

	e0 = None
	bandalign_opts = cmdargs.bandalign(directory = curdir)
	if bandalign_opts:  # false if None or {}
		if bandalign_opts.get('e0') is None and bandalign_opts.get('from_file') is None:
			sys.stderr.write("Warning (%s): Re-aligning (reconnecting) the states with automatically determined 'anchor energy'. If the result is not satisfactory or if the precise band indices are important, you should define the anchor energy explicitly by 'bandalign -4' (value is energy in meV).\n" % SCRIPT)
		if data.grid is None:
			sys.stderr.write("Warning (%s): Re-aligning (reconnecting) the states may fail if the data is unsorted. Due to absence of a VectorGrid instance in the data, it cannot be determined whether sorting is necessary.\n" % SCRIPT)
		elif not data.grid.is_sorted():
			sys.stderr.write("Warning (%s): For re-aligning (reconnecting) the states, automatically attempt to sort the data.\n" % SCRIPT)
			data.sort_by_grid()
		bandindices(data, **bandalign_opts)

	## Energy shift (TODO: Not very elegant)
	if 'zeroenergy' in opts and opts['zeroenergy']:
		e_ref = 0.0 if 'eshift' not in opts else opts['eshift']
		eshift = data.set_zero_energy(e_ref)
		if eshift is not None:
			sys.stderr.write("Warning (%s): Energy shifted by %.3f meV. Experimental function: Other input and output energies may still refer to the unshifted energy.\n" % (SCRIPT, eshift))
	elif 'eshift' in opts and opts['eshift'] != 0.0:
		data.shift_energy(opts['eshift'])
		sys.stderr.write("Warning (%s): Energy shifted by %.3f meV. Experimental function: Other input and output energies may still refer to the unshifted energy.\n" % (SCRIPT, opts['eshift']))

	if dependence == 'k':
		if 'symmetrytest' in sys.argv:
			data.symmetry_test('x', ignore_lower_dim = True)
			data.symmetry_test('y', ignore_lower_dim = True)
			data.symmetry_test('z', ignore_lower_dim = True)
			data.symmetry_test('xy', ignore_lower_dim = True)
			data.symmetry_test('xyz', ignore_lower_dim = True)
		if 'symmetrize' in sys.argv:
			data = data.symmetrize('xyz')
			if 'symmetrytest' in sys.argv:
				print()
				print("Symmetries after symmetrization:")
				data.symmetry_test('x', ignore_lower_dim = True)
				data.symmetry_test('y', ignore_lower_dim = True)
				data.symmetry_test('z', ignore_lower_dim = True)
				data.symmetry_test('xy', ignore_lower_dim = True)
				data.symmetry_test('xyz', ignore_lower_dim = True)

		if len(data.shape) == 1 and len(data) > 1:
			ploto.bands_1d(data, filename = "dispersion%s.pdf" % outputid, showplot = False, erange = erange, **plotopts)
		elif len(data.shape) == 2 and len(data) > 1:
			ploto.bands_2d(data, filename = "dispersion2d%s.pdf" % outputid, showplot = False, erange = erange, **plotopts)
		elif len(data.shape) > 2 or len(data) == 1:
			sys.stderr.write("Warning (%s): For 0- and 3-dimensional arrays, skip plot.\n" % SCRIPT)
		else:
			sys.stderr.write("ERROR (%s): Array of invalid dimension or size.\n" % SCRIPT)
			exit(1)
	elif isinstance(dependence, list):
		if dependence[1] == 'b':
			paramtex = ploto.format_axis_label("$B$", "$\\mathrm{T}$")
		elif dependence[2] != "":
			paramtex = ploto.format_axis_label("$%s$" % dependence[1], "$\\mathrm{%s}$" % dependence[2])
		else:
			paramtex = "$%s$" % dependence[1]
		if len(data.shape) == 1 and len(data) > 1:
			ploto.bands_1d(data, filename = "%sdependence%s.pdf" % (dependence[1], outputid), showplot = False, erange = erange, paramstr = paramtex, **plotopts)
		elif len(data.shape) >= 2 or len(data) == 1:
			sys.stderr.write("Warning (%s): For 0-, 2-, and 3-dimensional arrays, skip plot.\n" % SCRIPT)
		else:
			sys.stderr.write("ERROR (%s): Array of invalid dimension or size.\n" % SCRIPT)
			exit(1)
	else:
		raise ValueError("Illegal value for variable dependence")

	## Write Table
	if "writecsv" in sys.argv and len(data) > 0:
		dependencestr = "bdependence" if dependence == 'b' else 'dispersion'
		dependencedata = [data.get_paramval(), "b", "T"] if dependence == 'b' else None
		obsids = data[0].obsids
		tableo.disp("%s%s.csv" % (dependencestr, outputid), data, params, observables = obsids, dependence = dependencedata)
		plotobs = plotopts.get('obs')
		if len(data.shape) in [1, 2] and dependence == 'k':
			tableo.disp_byband("%s%s.csv" % (dependencestr, outputid), data, params, erange = erange, observable = plotobs)
		elif len(data.shape) == 1 and dependence == 'b' or (isinstance(dependence, list) and dependence[1] == 'b'):
			b = data.get_paramval()
			tableo.disp_byband("bdependence%s.csv" % outputid, data, params, erange = erange, observable = plotobs, dependence = [b, "b", "T"])
		else:
			sys.stderr.write("Warning (%s): Data shape and/or dependence not suitable for csv output.\n" % SCRIPT)

	try:
		dep = data.gridvar
	except:
		dep = None

	## Density of states
	if "dos" in sys.argv and dep == 'k' and params.kdim in [1, 2]:
		idos, energies = postprocess.dos_k(params, data, erange, outputid, opts, plotopts, energies = {'e0': e0}, onedim = (params.kdim == 1))
	elif "dos" in sys.argv and dep == 'b':
		postprocess.dos_ll(params, data, erange, outputid, opts, plotopts)
	elif "dos" in sys.argv:
		sys.stderr.write("Warning (%s): DOS calculation requires k dependence and momentum dimension = 1 or 2, or b dependence\n" % SCRIPT)
	else:
		idos = None

	# Local DOS (data and plots)
	if "localdos" in sys.argv and dep == 'b':
		postprocess.localdos_ll(params, data, erange, outputid, opts, plotopts)
	elif "localdos" in sys.argv:
		sys.stderr.write("Warning (%s): Local DOS calculation requires b dependence.\n" % SCRIPT)
		idos = None

	exit(0)

if __name__ == '__main__':
	main()

