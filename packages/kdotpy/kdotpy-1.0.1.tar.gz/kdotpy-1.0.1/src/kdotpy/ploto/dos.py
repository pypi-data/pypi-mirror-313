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
import warnings

from matplotlib import use as mpluse
mpluse('pdf')
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle

from ..config import get_config, get_config_bool, get_config_int, get_config_num
from .colortools import get_colormap, indexed_color_auto_range
from .tools import get_fignum, get_plot_size, plot_energies
from .toolslegend import add_colorbar, get_legend_file
from .toolstext import format_axis_unit, set_xlabel, set_ylabel
from .toolsticks import add_frequency_ticks, set_ticks
from ..phystext import format_value

from ..density import DensityScale, DensityData
from ..physconst import eoverhbar
from ..momentum import Vector, VectorGrid


def is_range_uniform(val):
	"""Detect whether array is uniform (linear).
	Returns True if second discrete derivative (differences of differences) is
	zero or length is 0, 1, 2."""
	return len(val) < 3 or np.amax(np.abs(np.diff(np.diff(val)))) < 1e-10

def extend_by_one(arr):
	"""Extend array by one element.
	Use [arr[0], (arr[i] + arr[i+1]) / 2, arr[-1]]."""
	arr = np.asarray(arr)
	return np.concatenate(((arr[0],), 0.5 * (arr[1:] + arr[:-1]), (arr[-1],)))

def shorten_by_one(arr):
	"""Shorten array by one element.
	Use [(arr[i] + arr[i+1]) / 2]."""
	arr = np.asarray(arr)
	return 0.5 * (arr[1:] + arr[:-1])

def add_contours(xval, yval, zval, levels, xminmax = None, linewidths = None):
	"""Add contours to current figure.
	Used to equal integrated DOS contours to a plot of (local) integrated DOS.

	Arguments:
	xval, yval   Grid variables
	zval         Data array
	levels       z values at which contours are to be drawn.
	xminmax      None or a 2-tuple. Horizontal extent of the plot. If None,
	             determine automatically.
	linewidths   A list of the same length as levels. The line widths of the
	             individual contours. If None, use default value for all
	             contours.
	"""
	rcParams['contour.negative_linestyle'] = 'solid'
	levels = np.asarray(levels)
	if xminmax is None:
		xmin0, xmax0 = min(xval), max(xval)
	else:
		xmin0, xmax0 = tuple(xminmax)
	if not is_range_uniform(xval):
		xx1, yy1 = np.meshgrid(xval, yval)
		contours = plt.contour(xx1, yy1, zval.transpose(), levels, origin = 'lower', extent = (xmin0, xmax0, min(yval), max(yval)), linewidths = 0.75, colors='k')  # removed: aspect = 'auto'
	else:
		contours = plt.contour(zval.transpose(), levels, origin = 'lower', extent = (xmin0, xmax0, min(yval), max(yval)), linewidths = 0.75, colors='k')  # removed: aspect = 'auto'

	if isinstance(linewidths, (list, np.ndarray)):
		if len(linewidths) != len(levels):
			raise ValueError("Argument linewidths must have the same length as argument levels")
		if len(contours.collections) != len(levels):
			levels1 = contours.levels
			linewidths1 = [linewidths[np.argsort(np.abs(levels - l))[0]] for l in levels1]
		else:
			levels1 = levels
			linewidths1 = linewidths
		for ci in range(0, len(levels1)):
			if linewidths1[ci] is not None:
				plt.setp(contours.collections[ci], linewidth = linewidths1[ci])

def valrange_patch(xmin, xmax, ymin, ymax, vertical=True):
	"""Wrapper around Rectangle for validity range patch"""
	patch_style = {'facecolor': '#c02000', 'edgecolor': None, 'alpha': 0.5, 'zorder': -5}
	if vertical:
		return Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, **patch_style)
	else:
		return Rectangle((ymin, xmin), ymax - ymin, xmax - xmin, **patch_style)

def valrange_edge(xmin, xmax, y, vertical=True):
	"""Wrapper around plt.plot for a validity range edge"""
	edge_color = 'r'
	if vertical:
		plt.plot([xmin, xmax], [y, y], ':', color=edge_color)
	else:
		plt.plot([y, y], [xmin, xmax], ':', color=edge_color)

def add_valrange(ee, idosmin, idosmax, vrmin = None, vrmax=None, vertical=True):
	ax = plt.gca()
	if vrmin is not None:
		if vrmin > min(ee):
			patch = valrange_patch(idosmin, idosmax, min(ee), vrmin, vertical=vertical)
			ax.add_patch(patch)
		valrange_edge(idosmin, idosmax, vrmin, vertical=vertical)
	if vrmax is not None:
		if vrmax < max(ee):
			patch = valrange_patch(idosmin, idosmax, max(ee), vrmax, vertical=vertical)
			ax.add_patch(patch)
		valrange_edge(idosmin, idosmax, vrmax, vertical=vertical)

def dos_idos(params, densitydata, outputid = "", filename = "", title = None, density_range = None, **plotopts):
	"""Density of states (DOS) and integrated density of states (IDOS) plots; wrapper function

	Arguments:
	params          PhysParams instance.
	densitydata     DensityData instance. Container for IDOS vs energy values.
	outputid        String that is inserted into the filenames.
	filename        NOT USED
	title           Plot title
	density_range   None or 2-tuple. If set, then use the values in order to
	                determine the coorect scale for the density axis.
	**plotopts      Additional plot options, which are ignored by this function.
	"""
	# Extract data from DensityData container (shortcuts)
	if not isinstance(densitydata, DensityData):
		raise TypeError("Argument densitydata must be a DensityData instance")

	fig_idos = None
	if densitydata.get_idos() is not None:
		fig_idos = integrated_dos(
			params, densitydata, outputid=outputid, title=title,
			density_range=density_range, **plotopts
		)
	fig_dos = None
	if densitydata.get_dos() is not None:
		fig_dos = dos(
			params, densitydata, outputid=outputid, title=title,
			density_range=density_range, **plotopts
		)
	return fig_idos, fig_dos

def integrated_dos(params, densitydata, outputid = "", filename = "", title = None, density_range = None, **plotopts):
	"""Integrated density of states (IDOS) plot.

	See dos() for more information.
	"""
	unit_negexp = get_config_bool('plot_dos_units_negexp')
	vertical = get_config_bool('plot_dos_vertical')
	valrange = get_config_bool('plot_dos_validity_range')
	idos_fill = get_config_bool('plot_idos_fill')
	dos_color = get_config('plot_dos_color')
	dens_qty = get_config('dos_quantity')
	dens_unit = get_config('dos_unit')
	e0_color = rcParams.get('lines.color')

	# Extract data from DensityData container (shortcuts)
	if not isinstance(densitydata, DensityData):
		raise TypeError("Argument densitydata must be a DensityData instance")
	ee = densitydata.ee
	energies = densitydata.get_special_energies()
	vrmin, vrmax = densitydata.get_validity_range()

	# Scale automatically and determine the units (but do not set plot limits)
	if isinstance(density_range, list) and len(density_range) == 2:
		densrange = [-density_range[1], density_range[1]] if density_range[0] is None else density_range
	else:
		densrange = None
	densitydata.set_scale(dens_qty, dens_unit, scaled_limits = densrange)
	dscale = densitydata.get_scale()
	idos = densitydata.get_idos(scaled = True)
	if idos is None:
		sys.stderr.write("Warning (ploto.integrated_dos): No IDOS data.\n")
		return None
	qstr = densitydata.qstr(style = 'tex', integrated = True, scaled = True)
	ustr = densitydata.unitstr(style = 'tex', integrated = True, scaled = True, negexp = unit_negexp)
	idosmin, idosmax = (idos[0], idos[-1]) if densrange is None else densrange if dscale is None else (dscale.scaledmin, dscale.scaledmax)

	# IDOS figure
	fig = plt.figure(get_fignum(), figsize = get_plot_size('s'))
	plt.subplots_adjust(**get_plot_size('subplot'))
	ax = fig.add_subplot(1, 1, 1)

	if vertical:
		if idos_fill:
			plt.fill_betweenx(ee, idos, 0, edgecolor=None, facecolor=dos_color, alpha=0.5, zorder=-7)
		plt.plot(idos, ee, '-', color=dos_color, zorder=-6)
		plt.plot([0.0, 0.0], [min(ee), max(ee)], ':', color=e0_color)
		if valrange:
			add_valrange(ee, idosmin, idosmax, vrmin=vrmin, vrmax=vrmax, vertical=vertical)
		plt.axis([idosmin, idosmax, min(ee), max(ee)])
		if get_config_bool('plot_dos_energies'):
			plot_energies(energies, xval = [idosmin, idosmax])
		set_ylabel('$E$', '$\\mathrm{meV}$')
		set_xlabel(qstr, ustr)
		set_ticks()
	else:
		if idos_fill:
			plt.fill_between(ee, idos, 0, edgecolor=None, facecolor=dos_color, alpha=0.5, zorder=-7)
		plt.plot(ee, idos, '-', color=dos_color, zorder=-6)
		plt.plot([min(ee), max(ee)], [0.0, 0.0], ':', color=e0_color)
		if valrange:
			add_valrange(ee, idosmin, idosmax, vrmin=vrmin, vrmax=vrmax, vertical=vertical)
		plt.axis([min(ee), max(ee), idosmin, idosmax])
		if get_config_bool('plot_dos_energies'):
			plot_energies(energies, yval = [idosmin, idosmax])
		set_xlabel('$E$', '$\\mathrm{meV}$')
		set_ylabel(qstr, ustr)
		set_ticks()

	if (title is not None) and (title != ""):
		ax.text(0.5, 0.98, title, ha='center', va='top', transform=ax.transAxes)

	plt.savefig("dos-integrated%s.pdf" % outputid)

	return fig

def dos(params, densitydata, outputid = "", filename = "", title = None, density_range = None, **plotopts):
	"""Density of states (DOS) plot.

	See dos() for more information.
	"""
	unit_negexp = get_config_bool('plot_dos_units_negexp')
	vertical = get_config_bool('plot_dos_vertical')
	valrange = get_config_bool('plot_dos_validity_range')
	dos_fill = get_config_bool('plot_dos_fill')
	dos_color = get_config('plot_dos_color')
	dens_qty = get_config('dos_quantity')
	dens_unit = get_config('dos_unit')

	# Extract data from DensityData container (shortcuts)
	if not isinstance(densitydata, DensityData):
		raise TypeError("Argument densitydata must be a DensityData instance")
	ee = densitydata.ee
	energies = densitydata.get_special_energies()
	vrmin, vrmax = densitydata.get_validity_range()

	# Scale automatically and determine the units (but do not set plot limits)
	if isinstance(density_range, list) and len(density_range) == 2:
		densrange = [-density_range[1], density_range[1]] if density_range[0] is None else density_range
	else:
		densrange = None
	densitydata.set_scale(dens_qty, dens_unit, scaled_limits = densrange)
	dscale = densitydata.get_scale()

	# DOS figure
	fig = plt.figure(get_fignum(), figsize = get_plot_size('s'))
	plt.subplots_adjust(**get_plot_size('subplot'))
	ax = fig.add_subplot(1, 1, 1)

	# Get (scaled) DOS values
	ee1 = (ee[1:] + ee[:-1]) / 2.0
	dos = densitydata.get_dos(derivative = 'diff', scaled = True)
	if dos is None:
		sys.stderr.write("Warning (ploto.dos): No DOS data.\n")
		return None
	qstr = densitydata.qstr(style = 'tex', integrated = False, scaled = True)
	ustr = densitydata.unitstr(style = 'tex', integrated = False, scaled = True, negexp = unit_negexp)
	dosmin, dosmax = 0.0, 1.1 * max(dos)
	# Round dosmax up to a * 10**b wbere a and b are integer values
	dosmax_exp = np.floor(np.log10(dosmax))
	dosmax_val = np.ceil(dosmax / 10**dosmax_exp)
	dosmax = dosmax_val * 10**dosmax_exp

	if vertical:
		if dos_fill:
			plt.fill_betweenx(ee1, dos, 0, edgecolor=None, facecolor=dos_color, alpha=0.5, zorder=-7)
		plt.plot(dos, ee1, '-', color=dos_color, zorder=-6)
		if valrange:
			add_valrange(ee, 0.0, 1.1 * dosmax, vrmin=vrmin, vrmax=vrmax, vertical=vertical)
		plt.axis([dosmin, dosmax, min(ee), max(ee)])
		if get_config_bool('plot_dos_energies'):
			plot_energies(energies, xval = [dosmin, dosmax])
		set_ylabel('$E$', '$\\mathrm{meV}$')
		set_xlabel(qstr, ustr)
		set_ticks()
	else:
		if dos_fill:
			plt.fill_between(ee1, dos, 0, edgecolor=None, facecolor=dos_color, alpha=0.5, zorder=-7)
		plt.plot(ee1, dos, '-', color=dos_color, zorder=-6)
		if valrange:
			add_valrange(ee, 0.0, 1.1 * dosmax, vrmin=vrmin, vrmax=vrmax, vertical=vertical)
		plt.axis([min(ee), max(ee), dosmin, dosmax])
		if get_config_bool('plot_dos_energies'):
			plot_energies(energies, yval = [dosmin, dosmax])
		set_xlabel('$E$', '$\\mathrm{meV}$')
		set_ylabel(qstr, ustr)
		set_ticks()

	if (title is not None) and (title != ""):
		ax.text(0.5, 0.98, title, ha='center', va='top', transform=ax.transAxes)

	plt.savefig("dos%s.pdf" % outputid)

	return fig

def local_density(params, densitydata, integrated = False, **kwds):
	"""Wrapper around density_plot() for densitydata input"""
	kwds['ll'] = densitydata.ll
	kwds['zunit'] = 'nm' if densitydata.scale is None else densitydata.scale
	kwds['energies'] = densitydata.special_energies
	plotdata = densitydata.xyz_idos() if integrated else densitydata.xyz_dos()
	if any(d is None for d in plotdata):
		sys.stderr.write("Warning (ploto.local_density): " + ("IDOS" if integrated else "DOS") + " is not defined.\n")
		return None
	return density2d(params, *plotdata, integrated = integrated, **kwds)

def densityz_energy(params, zval, eeval, densityz, integrated = False, **kwds):
	"""Wrapper around density2d() for 'densityz' input
	
	TODO: densityz will become its own class in the future
	"""
	return density2d(
		params, zval, eeval, densityz, integrated = integrated, **kwds)

def density2d(
		params, xval, yval, zval, outputid = "", energies = None, filename = "",
		title = None, interpolate = True, xlabel = None, ylabel = None,
		yunit = None, zunit = None, xrange = None, zrange = None,
		colormap = "Blues", legend = False, posneg = False, contours = False,
		contoursdata = None, contoursval = None, ll = False, integrated = False,
		frequency_ticks = False, **plotopts):
	"""Generic function used for local density of states (DOS) plots and the like.
	The horizontal and vertical axis can be any quantity, as can be the data.

	Arguments:
	params          PhysParams instance.
	xval            Array of values on the horizontal axis.
	yval            Array of values on the vertical axis.
	zval            Data array. The size should correspond to the lengths of
	                xval and yval.
	outputid        String that is inserted into the filename. Only meaningful
	                if filename is None.
	energies        A dict instance with special energies. This is used to show
	                dashed lines at the Fermi energy, charge neutrality point,
	                etc. See tools.plot_energies(). If None, do not plot
	                special energies.
	filename        Output filename. If None, use dos-localxxx.pdf, where xxx is
	                the outputid.
	title           Plot title
	interpolate     Whether to apply interpolation to the data. If xval is a
	                uniform array, then use the interpolation method as
	                specified (interpolate being a string) or the 'bilinear'
	                method if interpolate is True or no interpolation if
	                interpolate is False or None. If xval is a non-uniform
	                array, use 'flat' if interpolate is False or None, otherwise
	                use 'gouraud'. See matplotlib documentation for functions
	                pcolormesh() and imshow() for more information on the
	                interpolation methods.
 	xlabel          Set label on the x axis. Use 'k_x' if it is not set.
	ylabel          Set label on the y axis. Use 'E' (energy) if it is not set.
	yunit           If a string, use this density unit for the y axis. If True,
	                use the density unit from the DensityData instance. If
	                False, do not scale.
	zunit           If a string, use this density unit for the data ('z
	                values'). If True, use the density unit from the DensityData
	                instance. If False, do not scale.
	xrange          None or 2-tuple. Extent of the horizontal axis. If None,
	                determine automatically.
	zrange          None or 2-tuple. Minimum and maximum value of the colour
	                scale. If None, determine automatically.
	colormap        A matplotlib or kdotpy colormap id. Used for the colour
	                scale.
	legend          If True, draw a legend. If it is a string, draw a legend and
	                use this string as its label. If False, do not draw a
	                legend.
	posneg          Indicates whether the data is a strictly positive quantity
	                (posneg = False) or can also take negative values (posneg =
	                True).
	contours        If True, draw contours at automatically determined values.
	contoursdata    An array that contains the coordinates of one or more
	                contours (containing the y values as function of the x
	                values in xval). The array may be one-dimensional (single
	                contour) or two-dimensional (multiple contours).
	contoursval     NOT USED
	ll              Indicate whether one is plotting Landau levels (if so, set
	                it to True). This affects the density scaling.
	integrated      Indicate whether the quantity is an integrated density (if
	                so, set it to True). This affects the displayed units that
	                correspond to density.
	frequency_ticks  If True, add frequency ticks at the inner edge of the
	                 left-hand axis, like in the transitions plot.
	**plotopts      Additonal plot options, which are ignored by this function.

	Note:
	The options contours and contoursdata can be used at the same time.

	Returns:
	A matplotlib figure instance.
	"""
	if zval is None:
		sys.stderr.write("ERROR (ploto.local_dos): No data (argument zval).\n")
		return

	fig = plt.figure(get_fignum(), figsize = get_plot_size('s', legend = legend))
	plt.subplots_adjust(**get_plot_size('subplot', legend = legend))
	ax = fig.add_subplot(1, 1, 1)
	colormap = get_colormap(colormap)
	unit_negexp = get_config_bool('plot_dos_units_negexp')
	dens_qty = get_config('dos_quantity')
	dens_unit = get_config('dos_unit')

	if not isinstance(xval, (VectorGrid, list, np.ndarray)) and len(xval) > 0:
		sys.stderr.write("ERROR (ploto.local_dos): Argument xval must be a non-empty list or array.\n")
		return

	if isinstance(xval, VectorGrid):
		xval1 = xval.get_values(None)
	elif isinstance(xval, (list, np.ndarray)) and len(xval) > 0 and isinstance(xval[0], Vector):
		xval1 = np.array([k.len() for k in xval])
	else:  # list/array of numbers
		xval1 = xval
	xmin0 = min(xval1)
	xmax0 = max(xval1)
	if isinstance(xrange, (list, tuple)) and len(xrange) == 2:
		xmin = min(xrange)
		xmax = max(xrange)
	elif xrange is None:
		extend_xaxis = get_config_num('fig_extend_xaxis', minval = 0)
		xmin = xmin0 - extend_xaxis * (xmax0 - xmin0) if extend_xaxis > 0 else xmin0
		xmax = xmax0 + extend_xaxis * (xmax0 - xmin0) if extend_xaxis > 0 else xmax0
	else:
		raise TypeError("Argument xrange must be a list/tuple of length 2 or None")

	z90 = np.percentile(np.abs(zval), 90.0) if posneg else np.percentile(zval, 95.0)
	if isinstance(zunit, DensityScale):
		zscale = zunit
		zval = zscale.scaledvalues(zval)
	elif zunit is True:
		zscale = DensityScale(zval, dens_qty, dens_unit, ll = ll, kdim = 2 if ll else params.kdim)
		zval = zscale.scaledvalues()
	else:
		zscale = None

	if isinstance(yunit, DensityScale):
		yscale = yunit
		yval = yscale.scaledvalues(yval)
	elif yunit is True:
		yscale = DensityScale(yval, dens_qty, dens_unit, ll = ll, kdim = 2 if ll else params.kdim)
		yval = yscale.scaledvalues()
	else:
		yscale = None

	if zrange is not None:
		vmin = -max(abs(zrange[0]), abs(zrange[1])) if posneg else zrange[0]
		vmax = max(abs(zrange[0]), abs(zrange[1])) if posneg else zrange[1]
	else:  # automatic scaling
		absvmax = 1.0
		for vmax in [0.0001, 0.0002, 0.0004, 0.0006, 0.001, 0.002, 0.004, 0.006, 0.01, 0.02, 0.04, 0.06, 0.1, 0.2, 0.4, 0.6]:
			if 1.2 * z90 < vmax:
				absvmax = vmax
				break
		vmax = absvmax if zscale is None else zscale.scaledvalues(absvmax)
		vmin = -vmax if posneg else 0.0

	## Draw colour (background)
	if not is_range_uniform(xval1):
		if interpolate:
			shading_method = 'gouraud'
			pxval = shorten_by_one(xval1) if len(xval1) == zval.shape[0] + 1 else xval1
			pyval = shorten_by_one(yval) if len(yval) == zval.shape[1] + 1 else yval
		else:
			shading_method = 'flat'
			pxval = xval1 if len(xval1) == zval.shape[0] + 1 else extend_by_one(xval1)
			pyval = yval if len(yval) == zval.shape[1] + 1 else extend_by_one(yval)
		rasterized = get_config_bool('plot_rasterize_pcolormesh')
		plt.pcolormesh(
			pxval, pyval, zval.transpose(), cmap = colormap, vmin = vmin,
			vmax = vmax, shading = shading_method, rasterized = rasterized)
	else:
		interpolation_method = None if interpolate is False else 'bilinear' if interpolate is True else interpolate
		dx = 0.5 * (xval1[1] - xval1[0])
		left = xmin0 if len(xval1) == zval.shape[0] + 1 else xmin0 - dx
		right = xmax0 if len(xval1) == zval.shape[0] + 1 else xmax0 + dx
		dy = 0.5 * (yval[1] - yval[0])
		bottom = min(yval) if len(yval) == zval.shape[1] + 1 else min(yval) - dy
		top = max(yval) if len(yval) == zval.shape[1] + 1 else max(yval) + dy
		plt.imshow(np.clip(zval.transpose(), vmin, vmax), cmap = colormap, origin = 'lower', extent = (left, right, bottom, top), aspect = 'auto', vmin = vmin, vmax = vmax, interpolation = interpolation_method)

	## Draw contours (preset)
	if contours:
		if vmax <= 0.03:
			levels = np.arange(-0.015, 0.0151, 0.001) if posneg else np.arange(0.002, vmax + 0.0001, 0.002)
		elif vmax <= 0.3:
			levels = np.arange(-0.15, 0.151, 0.01) if posneg else np.arange(0.02, vmax + 0.0001, 0.02)
		elif vmax <= 1.5:
			levels = np.arange(-1.0, 1.01, 0.1) if posneg else np.arange(0.2, vmax + 0.0001, 0.2)
		else:
			levels = np.arange(-np.ceil(vmax) - 0.5, np.ceil(vmax) + 0.51, 1.0) if posneg else np.arange(0.5, np.ceil(vmax) + 0.51, 1.0)
		c0 = np.argmin(np.abs(levels))
		if levels[0] > 0:
			linewidths = [2.0 if (ci + 1) % 10 == 0 else 1.25 if (ci + 1) % 5 == 0 else 0.75 for ci in range(0, len(levels))]
		elif np.abs(levels[c0]) > 0.1:
			linewidths = [2.0 if np.abs(lv) < 0.9 else 0.75 for lv in levels]
		else:
			linewidths = [2.0 if (ci - c0) % 10 == 0 else 1.25 if (ci - c0) % 5 == 0 else 0.75 for ci in range(0, len(levels))]
		add_contours(xval1, yval, zval, levels, xminmax = [xmin0, xmax0], linewidths = linewidths)
	## Draw contours (from input)
	if isinstance(contoursdata, np.ndarray) and len(contoursdata.shape) == 1:
		plt.plot(xval1, contoursdata, 'r-')
	elif isinstance(contoursdata, np.ndarray) and len(contoursdata.shape) == 2:
		for cdata in contoursdata:
			plt.plot(xval1, cdata, 'r-')
	if get_config_bool('plot_dos_energies'):
		plot_energies(energies, xval = [xmin, xmax])
	plt.axis([xmin, xmax, min(yval), max(yval)])
	if isinstance(xlabel, str) and len(xlabel) > 0:
		plt.xlabel(xlabel)
	else:
		set_xlabel('$k_x$', '$\\mathrm{nm}^{-1}$')
	if isinstance(ylabel, str) and len(ylabel) > 0:
		plt.ylabel(ylabel)
	elif isinstance(yscale, DensityScale):  # i.e., it is an IDOS
		yqstr = yscale.qstr(style = 'tex', integrated = True)
		yunitstr = yscale.unitstr(style = 'tex', integrated = True, negexp = unit_negexp)
		set_ylabel(str(yqstr), yunitstr)
	else:
		set_ylabel('$E$', '$\\mathrm{meV}$')
	set_ticks()
	if frequency_ticks:
		add_frequency_ticks()

	if legend:
		legend_filename = get_legend_file(filename)
		if zscale is not None:
			zqstr = zscale.qstr(style = 'tex', integrated = integrated)
			zunitstr = zscale.unitstr(style = 'tex', integrated = integrated, negexp = unit_negexp)
		legend_label = legend if isinstance(legend, str) else None if zscale is None else zqstr if zunitstr is None else "%s\n%s" % (zqstr, format_axis_unit(zunitstr))
		add_colorbar(vmin, vmax, cmap = colormap, label = legend_label, label_y1 = -0.05, label_y2 = -0.05, filename = legend_filename)

	if (title is not None) and (title != ""):
		ax.text(0.5, 0.98, title, ha='center', va='top', transform=ax.transAxes)

	if filename is None or len(filename) == 0:
		filename = "dos-local%s.pdf" % outputid
	plt.savefig(filename)
	# plt.close()
	return fig

def dos_ll(
		params, bval, ee, ndos, outputid = "", energies = None, filename = "",
		title = None, interpolate = True, xlabel = None, xrange = None,
		colormap = "Blues", contours = False, contoursdata = False,
		contoursval = None, legend = False, **plotopts):
	"""Plot density of states for LL data

	Arguments:
	params        PhysParams instance.
	bval          Array of magnetic field (b) values (horizontal axis)
	ee            Array of energy values (vertical axis)
	ndos          Numeric density of states (number of filled LLs below, counted
	              from the charge neutrality point). This is a two-dimensional
	              array whose dimensions correspond to the lengths of bval and
	              ee.
	outputid      String inserted into the filename. Only meaningful when
	              filename is None or empty.
	energies      A dict instance with special energies. This is used to show
	              dashed lines at the Fermi energy, charge neutrality point,
	              etc. See tools.plot_energies(). If None, do not plot special
	              energies.
	filename      Output filename. If not set, use dos-numericxxx.pdf, where
	              xxx is the outputid.
	title         Plot title
	interpolate   Whether to apply interpolation to the data. If xval is a
	              uniform array, then use the interpolation method as
	              specified (interpolate being a string) or the 'bilinear'
	              method if interpolate is True or no interpolation if
	              interpolate is False or None. If xval is a non-uniform array,
	              use 'flat' if interpolate is False or None, otherwise use
	              'gouraud'. See matplotlib documentation for functions
	              pcolormesh() and imshow() for more information on the
	              interpolation methods.
	xlabel        Label on the x axis. If None, use 'B' (magnetic field).
	xrange        None or 2-tuple. Extent of the horizontal axis. If None,
	              determine automatically.	
	colormap      A matplotlib or kdotpy colormap.
	contours      If True, draw contours at automatically determined values.
	contoursdata  An array that contains the coordinates of one or more
	              contours (containing the y values as function of the x values
	              in xval). The array may be one-dimensional (single contour) or
	              two-dimensional (multiple contours).
	contoursval   NOT USED
	legend        If True, draw a legend. If it is a string, draw a legend and
	              use this string as its label. If False, do not draw a legend.
	**plotopts    Additonal plot options, which are ignored by this function.

	Returns:
	A matplotlib figure instance.
	"""
	fig = plt.figure(get_fignum(), figsize = get_plot_size('s', legend = legend))
	plt.subplots_adjust(**get_plot_size('subplot', legend = legend))
	ax = fig.add_subplot(1, 1, 1)

	if isinstance(bval, VectorGrid) and len(bval) > 0:
		bval = bval.get_values('b')
	elif isinstance(bval, (list, np.ndarray)) and len(bval) > 0:
		bval = np.asarray(bval)
	else:
		sys.stderr.write("ERROR (ploto.dos_ll): Magnetic-field values bval must be a non-empty list or array.\n")
		return
	bmin0 = min(bval)
	bmax0 = max(bval)
	if isinstance(xrange, (list, tuple)) and len(xrange) == 2:
		bmin = min(xrange)
		bmax = max(xrange)
	elif xrange is None:
		extend_xaxis = get_config_num('fig_extend_xaxis', minval = 0)
		bmin = bmin0 - extend_xaxis * (bmax0 - bmin0) if extend_xaxis > 0 else bmin0
		bmax = bmax0 + extend_xaxis * (bmax0 - bmin0) if extend_xaxis > 0 else bmax0
	else:
		raise TypeError("Argument xrange must be a list/tuple of length 2 or None")
	nmax = min(np.ceil(np.max(np.abs(ndos)[1:, :])), 10)
	colormap = get_colormap(colormap)
	vmin, vmax = indexed_color_auto_range(colormap)
	if vmin is None and vmax is None:
		vmin, vmax = -nmax, nmax

	zdata = np.ma.masked_where(np.isnan(ndos), ndos).transpose()  # prevent warnings that occur if NaN values are present
	## Draw colour (background)
	if not is_range_uniform(bval):
		if interpolate:
			shading_method = 'gouraud'
			pxval = shorten_by_one(bval) if len(bval) == ndos.shape[0] + 1 else bval
			pyval = shorten_by_one(ee) if len(ee) == ndos.shape[1] + 1 else ee
		else:
			shading_method = 'flat'
			pxval = bval if len(bval) == ndos.shape[0] + 1 else extend_by_one(bval)
			pyval = ee if len(ee) == ndos.shape[1] + 1 else extend_by_one(ee)
		rasterized = get_config_bool('plot_rasterize_pcolormesh')
		plt.pcolormesh(
			pxval, pyval, zdata, cmap = colormap, vmin = vmin, vmax = vmax,
			shading = shading_method, rasterized = rasterized)
	else:
		interpolation_method = None if interpolate is False else 'bilinear' if interpolate is True else interpolate
		dx = 0.5 * (bval[1] - bval[0])
		left = bmin0 if len(bval) == ndos.shape[0] + 1 else bmin0 - dx
		right = bmax0 if len(ee) == ndos.shape[0] + 1 else bmax0 + dx
		dy = 0.5 * (ee[1] - ee[0])
		bottom = min(ee) if len(ee) == ndos.shape[1] + 1 else min(ee) - dy
		top = max(ee) if len(ee) == ndos.shape[1] + 1 else max(ee) + dy
		plt.imshow(np.clip(zdata, vmin, vmax), cmap = colormap, origin = 'lower', extent = (left, right, bottom, top), aspect = 'auto', vmin = vmin, vmax = vmax, interpolation = interpolation_method)

	if contours:
		levels = np.arange(-9.5, 9.6, 1.0)
		linewidths = [2.0 if np.abs(lv) < 0.9 else 0.75 for lv in levels]
		add_contours(bval, ee, ndos, levels, linewidths = linewidths)
	if isinstance(contoursdata, np.ndarray) and len(contoursdata.shape) == 1:
		plt.plot(bval, contoursdata, 'r-')
	elif isinstance(contoursdata, np.ndarray) and len(contoursdata.shape) == 2:
		for cdata in contoursdata:
			plt.plot(bval, cdata, 'r-')
	plt.axis([bmin, bmax, min(ee), max(ee)])
	if isinstance(xlabel, str) and len(xlabel) > 0:
		plt.xlabel(xlabel)
	else:
		set_xlabel('$B$', '$\\mathrm{T}$')
	set_ylabel('$E$', '$\\mathrm{meV}$')
	set_ticks()

	if legend:
		legend_filename = get_legend_file(filename)
		legend_label = legend if isinstance(legend, str) else "NDOS\n(# levels)"
		add_colorbar(vmin, vmax, cmap = colormap, label = legend_label, label_y1 = -0.05, label_y2 = -0.05, filename = legend_filename)
	if filename is None or len(filename) == 0:
		filename = "dos-numeric%s.pdf" % outputid

	if (title is not None) and (title != ""):
		ax.text(0.5, 0.98, title, ha='center', va='top', transform=ax.transAxes)

	plt.savefig(filename)
	# plt.close()
	return fig

def subdiv_minmax(xval, yval):
	"""Subdivide an array of y values to match a coarser array of x values, keeping in addition the extrema of y.
	Sometimes, one ends up with an array of y values that has been evaluated at
	a subdivision of the array of x values, but the subdivided array of x values
	is not readily available. As arrays of different lengths cannot be plotted,
	one needs to 'align' the values. This function takes the y values at the
	(coarser) x values, and outputs these. In order to not lose information
	about the extrema, the extrema (x and y values) are inserted where
	necessary. The function returns two (equally long) arrays, slightly longer
	than the input xval.

	Note:
	The function works only if the array yval is a subdivision of the array
	xval, i.e., len(yval) - 1 must be an integer multiple of len(xval) - 1.
	"""
	if len(yval) > len(xval) and (len(yval)-1) % (len(xval)-1) == 0:
		subdiv = (len(yval)-1) // (len(xval)-1)
	else:
		return xval, yval
	if isinstance(xval, VectorGrid):
		xval = xval.get_values(xval.prefix)  # TODO: May not always be the correct choice
	else:
		xval = np.asarray(xval)
	yval = np.asarray(yval)
	xval_ip = np.array([(1. - j / subdiv) * np.array(xval)[:-1] + (j / subdiv) * np.array(xval)[1:] for j in range(0, subdiv)])
	xval_ip = np.concatenate((np.hstack(xval_ip.transpose()), np.array(xval)[-1:]), axis=0)

	threshold_value = 1.05  # setting this value to != 1 is appropriate only if yval >= 0 everywhere
	new_xval = []
	new_yval = []

	xmin = []
	xmax = []
	# Gather extra points at minima and maxima
	for i in range(1, len(xval)-1):
		if yval[subdiv*(i-1)] is None or yval[subdiv*i] is None or yval[subdiv*(i+1)] is None:
			pass
		elif threshold_value * yval[subdiv * (i-1)] < yval[subdiv * i] and threshold_value * yval[subdiv * (i+1)] < yval[subdiv * i]:  # maximum
			j = np.argmax(yval[subdiv * (i-1) + 1:subdiv * (i+1)])
			xmax.append(xval_ip[subdiv * (i-1) + 1 + j])
			if j != subdiv - 1:
				new_xval.append(xval_ip[subdiv * (i-1) + 1 + j])
				new_yval.append(yval[subdiv * (i-1) + 1 + j])
		elif yval[subdiv * (i-1)] > threshold_value * yval[subdiv * i] and yval[subdiv * (i+1)] > threshold_value * yval[subdiv * i]:  # minimum
			j = np.argmin(yval[subdiv * (i-1) + 1:subdiv * (i+1)])
			xmin.append(xval_ip[subdiv * (i-1) + 1 + j])
			if j != subdiv - 1:
				new_xval.append(xval_ip[subdiv * (i-1) + 1 + j])
				new_yval.append(yval[subdiv * (i-1) + 1 + j])

	# Show positions of maxima and minima
	if 'verbose' in sys.argv:
		print("Maxima, 1/B =", np.sort(1. / np.array(xmax)))
		print("Delta(1/B)  =", np.diff(np.sort(1. / np.array(xmax))))
		print("Minima, 1/B =", np.sort(1. / np.array(xmin)))
		print("Delta(1/B)  =", np.diff(np.sort(1. / np.array(xmin))))

	# Put coarse arrays and intermediate values together, and sort
	new_xval = np.concatenate((xval, np.array(new_xval)))
	new_yval = np.concatenate((yval[::subdiv], np.array(new_yval)))
	order = np.argsort(new_xval)
	return new_xval[order], new_yval[order]

def at_constant_dens_ll(
	xval, densval, zval, filename = "", legend = False, high_resolution = True,
	xlabel = None, ylabel = None, xrange = None, yrange = None,	omit_empty = True,
	is_ldos = True, reciprocal = False, extra_function = None, **plotopts):
	"""Plot quantity at constant density.
	This function provides a single plot (line plot) of a quantity as function
	of an 'x value' (e.g., momentum or magnetic field) for each of the specified
	density values.

	Arguments:
	xval             Array of values on horizontal axis
	densval          Array of density values
	zval             Data array (two-dimensional): Quantity as function of x and
	                 density.
	filename         Output file name
	legend           NOT USED
	high_resolution  If True, use subdivision of x values between the specified,
	                 i.e., insert extra values between existing x values.
	xlabel, ylabel   Labels on the horizontal and vertical axes.
	xrange           Extent of the horizontal axis. If None, determine
	                 automatically.
	yrange           Extent of the vertical axis. If None, use default.
	omit_empty       If True, do not incluse plots at lower and higher density
	                 values for which there is no data (NaN values).
	is_ldos          If True, apply density scaling to the quantity (zval).
	reciprocal       If True, use 1/x as plot variable on the horizontal axis.
	                 If False, use x.
	extra_function   A callable with two arguments. The function is evaluated
	                 as f(x, n) where x and n are substituted from xval and
	                 densval, respectively. An example would be
	                 f(b, n) = b / (n * e) for the classical Hall resistance.
	**plotopts       Additonal plot options, which are ignored by this function.

	No return value.
	"""
	debug = False  # set to True for debug output
	unit_negexp = get_config_bool('plot_dos_units_negexp')
	curve_color = get_config('plot_constdens_color')
	sdh_color = get_config('plot_sdh_markers_color')

	zval = np.array(zval, dtype = float)
	if np.all(np.isnan(zval)):
		sys.stderr.write("ERROR (ploto.at_constant_dens_ll): Data does not contain numerical values.\n")
		return
	pdfpages = PdfPages(filename) if filename is not None and filename != "" else None

	dens_qty = get_config('dos_quantity')
	dens_unit = get_config('dos_unit')
	densval_in = 1.0 * densval  # cache input value (not affected by DensityScale)
	dscale = DensityScale(np.array(densval), dens_qty, dens_unit, kdim = 2, ll = True)
	densval = dscale.scaledvalues()

	if is_ldos:
		zscale = DensityScale(zval, dens_qty, dens_unit, kdim = 2, ll = True)
		zval = zscale.scaledvalues()
	else:
		zscale = None

	if isinstance(xval, VectorGrid):
		xval = xval.get_values(None)  # Not always the right choice
	elif isinstance(xval, (list, np.ndarray)) and len(xval) > 0 and isinstance(xval[0], Vector):
		xval = np.array([x.component(None) for x in xval])
	if reciprocal:
		xmin = 0.0
		xmax = np.max(1. / xval[xval != 0])
		if np.count_nonzero(np.abs(densval) > 1e-5):
			# Find minimum x for which there is data, but do not consider density = 0
			isnumx = np.any(~np.isnan(zval[np.abs(densval) > 1e-5, :]), axis = 0)
			if zval.shape[1] > xval.shape[0] and (zval.shape[1] - 1) % (xval.shape[0] - 1) == 0:
				subdiv = (zval.shape[1] - 1) // (xval.shape[0] - 1)
				sel = isnumx[::subdiv] & (xval != 0.0)
			else:
				sel = isnumx & (xval != 0.0)
			xmin1 = 0.0 if np.count_nonzero(sel) == 0 else np.min(xval[sel])
			if xmin1 > 0.0:
				xmax = 1. / xmin1
	else:
		if isinstance(xrange, (list, tuple)) and len(xrange) == 2:
			xmin = min(xrange)
			xmax = max(xrange)
		elif xrange is None:
			xmin0, xmax0 = min(xval), max(xval)
			extend_xaxis = get_config_num('fig_extend_xaxis', minval = 0)
			xmin = xmin0 - extend_xaxis * (xmax0 - xmin0) if extend_xaxis > 0 else xmin0
			xmax = xmax0 + extend_xaxis * (xmax0 - xmin0) if extend_xaxis > 0 else xmax0
		else:
			raise TypeError("Argument xrange must be a list/tuple of length 2 or None")

	# Do not display the outer values for which there is not data
	if omit_empty:
		sel = ~np.all(np.isnan(zval), axis=1)
		selmin = np.min(densval[sel])
		selmax = np.max(densval[sel])
		sel = (densval >= selmin) & (densval <= selmax)
	else:
		sel = np.ones_like(densval, dtype = bool)

	xmax0 = xmax  # cache value
	sdh_markers = get_config_bool('plot_sdh_markers')
	sdh_scale_amount = get_config_int('plot_sdh_scale_amount', minval = 0)
	for dens, dens0, z in zip(densval[sel], densval_in[sel], zval[sel, :]):
		z = np.array(z, dtype = float)
		with warnings.catch_warnings():  # Suppress warning for all-NaN arrays
			warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')
			zmax = np.nanmax(np.abs(z))
		if zmax is None or np.isnan(zmax):  # no data
			continue
		fig = plt.figure(get_fignum(), figsize = get_plot_size('s'))
		plt.subplots_adjust(**get_plot_size('subplot'))
		ax = fig.add_subplot(1, 1, 1)

		sdh_period = eoverhbar / 2 / np.pi / abs(dens0)
		if len(z) > len(xval) and (len(z) - 1) % (len(xval) - 1) == 0:
			subdiv = (len(z) - 1) // (len(xval) - 1)
			if high_resolution:
				if debug:
					print("For n = %.4f %s:" % (dens, dscale.unitstr(style = 'raw', integrated=True)))
					print("Theoretical value of Delta(1/B) = %.6f / T" % sdh_period)
				xval1, z1 = subdiv_minmax(xval, z)  # Smart subdivision, taking care of minima and maxima
				pxval = 1. / xval1[xval1 != 0] if reciprocal else xval1
				pyval = z1[xval1 != 0] if reciprocal else z1
			else:
				pxval = 1. / xval[xval != 0] if reciprocal else xval
				pyval = z[::subdiv][xval != 0] if reciprocal else z[::subdiv]
		else:
			pxval = 1. / xval[xval != 0] if reciprocal else xval
			pyval = z[xval != 0] if reciprocal else z
		plt.plot(pxval, pyval, '-', color=curve_color)
		xmax = xmax0
		if abs(dens0) > 1e-5 and (sdh_markers or sdh_scale_amount > 0):
			if reciprocal:
				jmax = int(np.floor(xmax0 / sdh_period))
				if sdh_scale_amount > 0:
					if jmax > sdh_scale_amount:
						jmax = sdh_scale_amount
						xmax = jmax * sdh_period
				if sdh_markers:
					for jsdh in range(0, jmax + 1):
						marker = 10 if jsdh % 10 == 0 else 2  # 10: caret up, 2: tick up
						plt.plot(sdh_period * jsdh, 0, color = sdh_color, marker = marker)
			else:  # not reciprocal
				jmax = 20
				for jsdh in range(1, jmax + 1):
					marker = 10 if jsdh % 10 == 0 else 2  # 10: caret up, 2: tick up
					plt.plot(1 / jsdh / sdh_period, 0, color = sdh_color, marker = marker)
			
		if extra_function is not None:
			pyval_extra = extra_function(pxval, 0.0 if abs(dens0) < 1e-9 else dens0)
			linecolor = rcParams['lines.color']
			plt.plot(pxval, pyval_extra, '--', color=linecolor, zorder = 1.9)
		if isinstance(yrange, list) and len(yrange) == 2:
			plt.axis([xmin, xmax, min(yrange), max(yrange)])
		elif zmax is None or np.isnan(zmax):
			plt.axis([xmin, xmax, 0.0, 1.0])
		else:
			yexp = max(-4, np.floor(np.log10(zmax)))
			ymax = zmax * 10**-yexp
			if ymax <= 1.0:
				ymax, tmaj, tmin = 1.0, 0.2, 0.1
			elif ymax <= 3.0:
				ymax, tmaj, tmin = 3.0, 1.0, 0.5
			else:
				ymax, tmaj, tmin = 10.0, 2.0, 1.0
			ax.set_yticks(np.arange(0.0, ymax * 1.01, tmaj) * 10**yexp)
			ax.set_yticks(np.arange(0.0, ymax * 1.01, tmin) * 10**yexp, minor = True)
			plt.axis([xmin, xmax, 0.0, ymax * 10**yexp])

		if xlabel is None:
			set_xlabel("$1/B$" if reciprocal else "$B$", "$\\mathrm{T}^{-1}$" if reciprocal else "$\\mathrm{T}$")
		else:
			plt.xlabel(xlabel)
		if ylabel is not None:
			plt.ylabel(ylabel)
		elif zscale is not None:
			set_ylabel(zscale.qstr(style = 'tex', integrated = False), zscale.unitstr(style = 'tex', integrated = False, negexp = unit_negexp))
		else:
			plt.ylabel("??")
		set_ticks()

		# Density value
		dens_str = "%.4f" % dens
		dens_str = dens_str.rstrip("0")
		if dens_str.endswith("."):
			dens_str += "0"
		if not dens_str.startswith("-"):
			dens_str = "+" + dens_str

		# Density unit
		dens_unit = dscale.unitstr(style = 'tex', integrated=True, negexp = unit_negexp).strip("$ ")
		if dens_unit.startswith("10"):
			dens_unit = r"\times " + dens_unit
		elif dens_unit.startswith("1") and len(dens_unit) > 1:
			dens_unit = dens_unit[1:].strip()

		# Density quantity
		dens_q = dscale.qstr(style = 'tex')
		if '$' in dens_q:
			dens_q = dens_q.strip('$')
		else:
			dens_q = r"\mathrm{%s}" % dens_q

		# Combine into density label, insert at top left of the figure
		dens_space = "" if dens_unit.startswith("/") else r"\,"
		if abs(dens) < 1e-10:
			ax.text(0.03, 0.98, "$%s = 0%s%s$" % (dens_q, dens_space, dens_unit), ha='left', va='top', transform=ax.transAxes)
		else:
			dens_eh = "e" if dens > 0 else "h"
			ax.text(0.03, 0.98, "$%s = %s%s%s$ (%s)" % (dens_q, dens_str, dens_space, dens_unit, dens_eh), ha='left', va='top', transform=ax.transAxes)

		if pdfpages is None:
			file_str = "%.2f" % dens
			file_str.replace('+', 'h_').replace('-', 'e_')
			plt.savefig("dos-constdens-%s.pdf" % file_str)
		else:
			pdfpages.savefig(fig)
		plt.close()

	if pdfpages is not None:
		pdfpages.close()

	return

def add_curves(xval, curvesdata, curvesval = None, fig = None, ax = None, filename = "", linewidth = None):
	"""Add curves to figure. Subdivide the x coordinates if necessary.

	Arguments:
	xval         Array of x values. This array will be subdivided if necessary.
	curvesdata   Array of 'y values'. This array may be one-dimensional (single
	             curve) or two-dimensional (multiple curves).
	curvesval    NOT USED
	fig          None, integer, string, or matplotlib figure instance. If not
	             None, this refers to the figure in which the curves will be
	             drawn. If None, use the current figure.
	ax           A matplotlib axis instance in which the curves will be drawn.
	             If None, use the current axis.
	filename     Output filename. If None or empty, do not save.
	linewidth    Can be None (use default line width), a number (use one line
	             width for all curves) or a list or array (use different line
	             widths for the curves.

	Returns:
	A matplotlib figure instance
	"""
	if fig is None:
		fig = plt.gcf()
	elif isinstance(fig, (int, str)):
		plt.figure(fig)
	else:
		plt.figure(fig.number)
	if ax is None:
		ax = plt.gca()
	else:
		fig.sca(ax)

	if isinstance(xval, VectorGrid):
		xval = xval.get_values(xval.prefix)  # TODO: May not always be the correct choice
	elif isinstance(xval, (list, np.ndarray)) and len(xval) > 0 and isinstance(xval[0], Vector):
		xval = [v.component(None) for v in xval]
	xval = np.array(xval, dtype = float)  # ensure that input is a float array

	if isinstance(curvesdata, list):
		curvesdata = np.array(curvesdata)

	if isinstance(curvesdata, np.ndarray) and len(curvesdata.shape) == 1:
		# stretch (interpolate) x values if necessary
		if len(curvesdata) > len(xval) and (len(curvesdata)-1) % (len(xval)-1) == 0:
			subdiv = (len(curvesdata)-1) // (len(xval)-1)
			xval1 = np.array([(1. - j/subdiv) * np.array(xval)[:-1] + (j / subdiv) * np.array(xval)[1:] for j in range(0, subdiv)])
			xval = np.concatenate((np.hstack(xval1.transpose()), np.array(xval)[-1:]), axis=0)

		if linewidth is None:
			plt.plot(xval, curvesdata, 'k-')
		elif isinstance(linewidth, (float, np.floating, int, np.integer)):
			plt.plot(xval, curvesdata, 'k-', linewidth = linewidth)
		elif isinstance(linewidth, (list, np.ndarray)):
			plt.plot(xval, curvesdata, 'k-', linewidth = linewidth[0])

	elif isinstance(curvesdata, np.ndarray) and len(curvesdata.shape) == 2:
		for cj, cdata in enumerate(curvesdata):
			# stretch (interpolate) x values if necessary
			if len(cdata) > len(xval) and (len(cdata)-1) % (len(xval)-1) == 0:
				subdiv = (len(cdata)-1) // (len(xval)-1)
				xval1 = np.array([(1. - j / subdiv) * np.array(xval)[:-1] + (j / subdiv) * np.array(xval)[1:] for j in range(0, subdiv)])
				xval1 = np.concatenate((np.hstack(xval1.transpose()), np.array(xval)[-1:]), axis=0)
			else:
				xval1 = xval

			if linewidth is None:
				plt.plot(xval1, cdata, 'k-')
			elif isinstance(linewidth, (float, np.floating, int, np.integer)):
				plt.plot(xval1, cdata, 'k-', linewidth = linewidth)
			elif isinstance(linewidth, (list, np.ndarray)):
				plt.plot(xval1, cdata, 'k-', linewidth = linewidth[cj])

	if filename is not None and len(filename) > 0:
		plt.savefig(filename)
	return fig

def densityz(params, densz, filename = "", title = None, title_val = None, legend = False):
	"""Plot density as function of (the spatial coordinate) z.
	Plot (1) total density, (2) electron, hole, and total density or (3)
	electron, hole, total, and background density.

	Arguments:
	params     PhysParams instance. Used to extract the array of z values.
	densz      dict instance. We extract the values for the keys 'total', 'e',
	           'h', and 'bg'. Each value must be an array of dimension 1 or 2,
	           or None. If one of the arrays has dimension 2, iterate over the
	           first axis and write a multipage PDF as output.
	filename   Output filename
	title      Plot title
	title_val  None, number, tuple, list or array. If a number, print this value
	           in the plot title using % formatting. A tuple can be used for
	           multiple values. If a list or array, take the subsequent values
	           for the subsequent plot.
	legend     If True, plot legend and total surface charges

	No return value.
	"""
	dz = params.zres
	z = params.zvalues_nm()
	zint = params.interface_z_nm()
	fmt_opts = {'style': 'tex', 'fmt': '{:.2g}'}  # format for density values

	if not isinstance(densz, dict):
		raise TypeError("Argument densz must be a dict instance")
	densz_bg = densz.get('bg')
	densz_e = densz.get('e')
	densz_h = densz.get('h')
	densz_t = densz.get('total')
	if densz_bg is not None and np.amax(np.abs(densz_bg)) < 1e-15:
		densz_bg = None
	if densz_t is None and densz_e is not None and densz_h is not None:
		densz_t = densz_e + densz_h
	if densz_t is None and densz_e is None and densz_h is None:
		sys.stderr.write("ERROR (ploto.densz): Nothing to be plotted\n")
		return

	dim_e = densz_e.ndim if isinstance(densz_e, np.ndarray) else 0
	dim_h = densz_h.ndim if isinstance(densz_h, np.ndarray) else 0
	dim_t = densz_t.ndim if isinstance(densz_t, np.ndarray) else 0
	dim_bg = densz_bg.ndim if isinstance(densz_bg, np.ndarray) else 0
	dim = max([dim_e, dim_h, dim_t, dim_bg])
	if dim > 2:
		raise ValueError("Data arrays may not be of dimension > 2.")
	arr_size = densz_t.shape[-1] if densz_t is not None else densz_e.shape[-1] if densz_e is not None else densz_bg.shape[-1]
	npoints = densz_t.shape[0] if dim_t == 2 else densz_e.shape[0] if dim_e == 2 else densz_bg.shape[0] if dim_bg == 2 else 1

	# Determine maximum
	densmax = np.amax(np.abs(densz_t))
	if densz_e is not None:
		densmax = max(densmax, np.amax(np.abs(densz_e)))
	if densz_h is not None:
		densmax = max(densmax, np.amax(np.abs(densz_h)))
	# Background charge does not affect the plot scale, intentionally.

	# Determine unit automatically
	for e in range(-15, 4, 3):
		unit = 10**e
		if densmax <= 30 * unit:
			unitstr = "" if e == 0 else "10^{%i}\\;" % e
			break
	if unit > 1e2:
		unit = 1
		unitstr = ""

	arr_shape = (npoints, arr_size)
	if densz_e is not None:
		densz_e = np.broadcast_to(densz_e, arr_shape)
	if densz_h is not None:
		densz_h = np.broadcast_to(densz_h, arr_shape)
	if densz_t is not None:
		densz_t = np.broadcast_to(densz_t, arr_shape)
	if densz_bg is not None:
		densz_bg = np.broadcast_to(densz_bg, arr_shape)

	pdfpages = PdfPages(filename) if filename is not None and filename != "" else None
	for j in range(0, npoints):
		# Create figure
		fig = plt.figure(get_fignum(), figsize = get_plot_size('s'))
		plt.subplots_adjust(**get_plot_size('subplot'))
		ax = fig.add_subplot(1, 1, 1)
		plt.plot([z.min(), z.max()], [0, 0], 'k--')

		## Plot
		allplots = []
		legendlabels = []
		# holes
		if densz_h is not None:
			thisplot, = plt.plot(z, densz_h[j] / unit, 'r-')
			allplots.append(thisplot)
			legendlabels.append("holes, $\\rho_\\mathrm{h}$")
		# total
		if densz_t is not None:
			thisplot, = plt.plot(z, densz_t[j] / unit, 'b-')
			allplots.append(thisplot)
			legendlabels.append("total, $\\rho$")
		# electrons
		if densz_e is not None:
			thisplot, = plt.plot(z, densz_e[j] / unit, 'g-')
			allplots.append(thisplot)
			legendlabels.append("electrons, $-\\rho_\\mathrm{e}$")
		# background
		if densz_bg is not None:
			thisplot, = plt.plot(z, densz_bg[j] / unit, 'm--')
			allplots.append(thisplot)
			legendlabels.append("backgr., $\\rho_\\mathrm{bg}$")

		# Determine integrals
		int_dens_t = float('nan') if densz_t is None else np.sum(densz_t[j]) * dz
		int_dens_e = float('nan') if densz_e is None else np.sum(densz_e[j]) * dz
		int_dens_h = float('nan') if densz_h is None else np.sum(densz_h[j]) * dz
		int_dens_bg = float('nan') if densz_bg is None else np.sum(densz_bg[j]) * dz

		## Determine min and max
		ymin = -densmax / unit
		ymax = densmax / unit
		if ymax - ymin < 1e-6:
			ymin, ymax = -1e-3, 1e-3

		for zi in zint[1:-1]:
			plt.plot([zi, zi], [ymin, ymax], 'k:')
		plt.axis([z.min() * 1.05, z.max() * 1.05, ymin - 0.05 * (ymax - ymin), ymax + 0.05 * (ymax - ymin)])

		## Determine labels of y and x axis
		set_ylabel('$\\rho(z)$', '$%se/\\mathrm{nm}^3$' % unitstr)
		set_xlabel('$z$', '$\\mathrm{nm}$')
		set_ticks()

		## Plot legend and text (total surface charges)
		if legend:
			ax.legend(handles = allplots, labels = legendlabels, loc='upper right')
			if densz_e is not None:
				if abs(int_dens_e) < abs(int_dens_h) * 1e-3:
					dens_txt = "$n_\\mathrm{e} \\approx 0$"
				else:
					valstr = format_value(-int_dens_e, **fmt_opts).strip('$')
					dens_txt = "$n_\\mathrm{e} = %s\\; e/\\mathrm{nm}^{2}$" % valstr
				ax.text(0.02, 0.05, dens_txt, ha = 'left', va = 'center', transform = ax.transAxes)
			if densz_h is not None:
				if abs(int_dens_h) < abs(int_dens_e) * 1e-3:
					dens_txt = "$n_\\mathrm{h} \\approx 0$"
				else:
					valstr = format_value(int_dens_h, **fmt_opts).strip('$')
					dens_txt = "$n_\\mathrm{h} = %s\\; e/\\mathrm{nm}^{2}$" % valstr
				ax.text(0.02, 0.95, dens_txt, ha = 'left', va = 'center', transform = ax.transAxes)
			if densz_bg is not None:
				if abs(int_dens_bg) < max(abs(int_dens_e), abs(int_dens_h)) * 1e-3:
					dens_txt = "$n_\\mathrm{bg} \\approx 0$"
				else:
					valstr = format_value(int_dens_bg, **fmt_opts).strip('$')
					dens_txt = "$n_\\mathrm{bg} = %s\\; e/\\mathrm{nm}^{2}$" % valstr
				ax.text(0.02, 0.48, dens_txt, ha = 'left', va = 'top', transform = ax.transAxes)

			if densz_e is not None and densz_h is not None and abs(int_dens_t) < max(abs(int_dens_e), abs(int_dens_h)) * 1e-3:
				dens_txt = "$n \\approx 0$"
			elif densz_t is not None:
				dens_txt = "$n = %s\\; e/\\mathrm{nm}^{2}$" % format_value(int_dens_t, **fmt_opts)
			else:
				dens_txt = None
			if dens_txt is not None:
				ax.text(0.02, 0.52, dens_txt, ha = 'left', va = 'bottom', transform = ax.transAxes)

		if (title is not None) and (title != ""):
			if isinstance(title_val, (list, np.ndarray)):
				title_str = title % title_val[j]
			elif isinstance(title_val, (tuple, int, float, np.integer, np.floating)):
				title_str = title % title_val
			else:
				title_str = title
			ax.text(0.5, 0.98, title_str, ha='center', va='top', transform=ax.transAxes)

		if pdfpages is None:
			plt.savefig(filename.replace(".pdf", "-%i.pdf" % (j+1)))
		else:
			pdfpages.savefig(fig)
		plt.close()
	if pdfpages is not None:
		pdfpages.close()

	return
