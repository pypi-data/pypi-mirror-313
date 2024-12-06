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
from scipy.sparse import dia_matrix, csc_matrix, coo_matrix, issparse
from .physparams import PhysParams
from .hamiltonian import parity_x, parity_y, parity_z, hexchange, hzeeman, hstrain, hz_block_diag
from .phystext import format_unit
from . import spinmat

### HELPER FUNCTION ###
indexed_obs_regex = r"([A-Za-z0-9_]+)\[([+-]?[0-9]+)\]$"  # used below several times
def get_index_from_obs_string(s):
	m = re.match(indexed_obs_regex, s)
	return None if m is None else int(m.group(2))

def obsid_to_tex(obsid, dimful = None):
	"""Get quantity and unit string in TeX style from observable id

	Arguments:
	obsid   String
	dimful  True, False, or None. Whether to get the quantity and unit strings
	        for dimensionful observables. If None, take the value from
	        all_observables.

	Returns:
	qstr    String. TeX formatted string for physical quantity.
	ustr    String. TeX formatted string for unit.
	"""
	if dimful is None:
		dimful = all_observables.dimful is True
	if obsid not in all_observables:
		sys.stderr.write("Warning (obsid_to_tex): Observable '%s' not defined.\n" % obsid)
		return None, None
	obs = all_observables[obsid]
	qstr = obs.to_str(style = 'tex', dimful = dimful)
	ustr = obs.get_unit_str(style = 'tex', dimful = dimful)
	if '%i' in qstr:
		idx = get_index_from_obs_string(obsid)
		if idx is not None:
			qstr = qstr % idx
		else:
			sys.stderr.write("ERROR (obsid_to_tex): No index value for indexed observable.\n")
			qstr = qstr.replace('%i', '?')
	return (qstr, ustr)

### MATRIX TOOLS ###
def blockdiag(mat, nblocks, offset = 0):
	"""Construct a sparse block matrix in COO format
	This function is faster than scipy.sparse.block_diag() for larger matrices
	It is also more restricted though, as all blocks are identical

	Arguments:
	mat      Numpy array of two dimensions, or scipy sparse matrix. The matrix
	         that constitutes one block.
	nblocks  Integer. The number of blocks.
	offset   Integer. If nonzero, the blocks will be placed off-diagonally; +1
	         means one position below the diagonal, -1 one position above; the
	         absolute value must be smaller than nblocks.

	Note:
	For larger input matrices (argument 'mat'), it is advisable to use a sparse
	format for better performance.

	Returns:
	A sparse matrix of type scipy.sparse.coo_matrix.
	"""
	cols = []
	rows = []
	data = []
	nx, ny = mat.shape
	if not isinstance(offset, (int, np.integer)):
		raise TypeError("Argument offset must be an integer")
	if abs(offset) >= nblocks:
		raise ValueError("Absolute value of argument offset must be smaller than nblocks")
	if offset > 0:
		rowidx = np.arange(offset, nblocks) * nx
		colidx = np.arange(0, nblocks - offset) * ny
	elif offset < 0:
		rowidx = np.arange(0, nblocks + offset) * nx
		colidx = np.arange(-offset, nblocks) * ny
	else:
		rowidx = np.arange(0, nblocks) * nx
		colidx = np.arange(0, nblocks) * ny
	ndata = len(rowidx)
	if issparse(mat):
		coomat = mat.tocoo()
		for i, j, v in zip(coomat.row, coomat.col, coomat.data):
			rows.append(i + rowidx)
			cols.append(j + colidx)
			data.append(np.full(ndata, v))
	else:
		for i in range(0, nx):
			for j in range(0, ny):
				if mat[i, j] != 0.0:
					rows.append(i + rowidx)
					cols.append(j + colidx)
					data.append(np.full(nblocks, mat[i, j]))
	if len(rows) == 0 or len(cols) == 0 or len(data) == 0:
		return coo_matrix((nx * nblocks, ny * nblocks), dtype = mat.dtype)
	rows = np.concatenate(rows)
	cols = np.concatenate(cols)
	data = np.concatenate(data)
	return coo_matrix((data, (rows, cols)), shape = (nx * nblocks, ny * nblocks))

### OBSERVABLES CLASS ###
class Observable:
	"""Observable object.

	Attributes:
	obsid          String. The observable id.
	obsfun         Function (callable object) or None. None is appropriate for
	               observables that are calculated elsewhere (i.e., not a
	               function in observables.py).
	obsfun_type    String, one of 'none', 'mat', 'params', 'params_magn',
	               'eivec', 'kwds', and 'overlap'. This determines which
	               arguments will be passed to obsfun and how the eigenvectors
	               are applied.
	unit_dimless   String or None. Unit of the dimensionless variety
	               (unformatted).
	unit_dimful    String or None. Unit of the dimensionful variety
	               (unformatted).
	dimful_qty     String or None. What quantity determines the scaling factor
	               for conversion between dimensionful and dimensionless
	               observable.
	dimful_factor  Float or None. Scaling factor for conversion between
	               dimensionful and dimensionless observable.
	obsid_alias    String or list of strings. Alias(es) for the observable id.
	str_dimless    Dict instance, whose keys are formatting styles and whose
	               values are the string representations of the dimensionless
	               observable in these styles.
	str_dimful     Dict instance, whose keys are formatting styles and whose
	               values are the string representations of the dimensionful
	               observable in these styles.
	minmax         List of 2 floats or None. If set, this determines the range of
	               of the colour legends in the plots.
	colordata      String or None. If set, which colormap should be used for this
	               observable.
	"""
	def __init__(self, obsid, obsfun, obsfun_type = None, unit_dimless = None, unit_dimful = None, dimful_qty = None, obsid_alias = None, str_dimless = None, str_dimful = None, minmax = None, colordata = None):
		##
		if not isinstance(obsid, str):
			raise TypeError("Argument obsid must be a string instance")
		self.obsid = obsid
		self.obsfun = obsfun  # TODO: test
		if obsfun_type is None:
			self.obsfun_type = "none" if obsfun is None else "mat"
		elif obsfun_type in ['none', 'mat', 'mat_indexed', 'params', 'params_indexed', 'params_magn', 'eivec', 'kwds', 'overlap']:
			self.obsfun_type = obsfun_type
		else:
			raise ValueError("Invalid value for argument 'obsfun_type'.")
		if isinstance(unit_dimless, str) or unit_dimless is None:
			self.unit_dimless = unit_dimless
		else:
			raise TypeError("Argument unit_dimless must be a string instance or None")
		if dimful_qty is None:
			self.dimful_qty = None
			self.dimful_factor = 1.0
		elif isinstance(dimful_qty, str):
			self.dimful_qty = dimful_qty
			self.dimful_factor = None
		else:
			raise TypeError("Argument dimful_qty must be a string instance or None")
		if isinstance(unit_dimful, str) or unit_dimful is None:
			self.unit_dimful = unit_dimful
		else:
			raise TypeError("Argument unit_dimful must be a string instance or None")
		if obsid_alias is None:
			self.obsid_alias = []
		elif isinstance(obsid_alias, str):
			self.obsid_alias = [obsid_alias]
		elif isinstance(obsid_alias, list) and all(isinstance(alias, str) for alias in obsid_alias):
			self.obsid_alias = obsid_alias
		else:
			raise TypeError("Argument obsid_alias must be a string or list of strings")
		if str_dimless is None:
			str_dimless = {}
		elif not isinstance(str_dimless, dict):
			raise TypeError("Argument str_dimless must be a dict instance or None")
		if str_dimful is None:
			str_dimful = {}
		elif not isinstance(str_dimful, dict):
			raise TypeError("Argument str_dimful must be a dict instance or None")
		self.str_dimless = str_dimless
		if len(str_dimful) == 0 and len(str_dimless) > 0:
			self.str_dimful = str_dimless
		else:
			self.str_dimful = str_dimful
		if minmax is None:
			self.minmax = [-1.0, 1.0]
		elif isinstance(minmax, (int, float, np.integer, np.floating)):
			self.minmax = [-abs(minmax), abs(minmax)]
		elif isinstance(minmax, list) and len(minmax) == 2:
			self.minmax = [float(minmax[0]), float(minmax[1])]
		else:
			raise TypeError("Argument minmax must be a number or a list of two numbers")
		if colordata is None:
			self.colordata = 'symmobs'  # default
		elif isinstance(colordata, str):
			self.colordata = colordata
		else:
			raise TypeError("Argument colordata must be a string instance or None")

	def to_str(self, style = None, dimful = False, index_from = None):
		"""Get string representation of the observable

		Arguments:
		style       String or None. If set, one of the formatting styles. If
		            None, return the observable id.
		dimful      True or False. Whether to use the dimensionful (True) or
		            dimensionless (False) variety.
		index_from  None or string. If set, extract a replacement value for '%i'
		            from the string. This is applied to observables of types
		            mat_indexed and params_indexed only.

		Returns:
		String.
		"""
		if dimful and isinstance(style, str) and style in self.str_dimful:
			s = self.str_dimful[style]
		elif not dimful and isinstance(style, str) and style in self.str_dimless:
			s = self.str_dimless[style]
		else:
			s = self.obsid
		if self.obsfun_type in ['mat_indexed', 'params_indexed']:
			idx = None if index_from is None else get_index_from_obs_string(index_from)
			if '%i' in s:
				return s.replace('%i', '?') if idx is None else (s % idx)
			elif '[]' in s:
				return s.replace('[]', '[?]') if idx is None else s.replace('[]', '[%i]' % idx)
			else:
				return s
		else:
			return s

	def get_unit(self, dimful = False):
		"""Get unit of the observable (unformatted).

		Arguments:
		dimful  True or False. Whether to use the dimensionful (True) or
		        dimensionless (False) variety.

		Returns:
		String.
		"""
		return self.unit_dimful if dimful and self.unit_dimful is not None else self.unit_dimless

	def get_unit_str(self, style = None, dimful = False, negexp = True):
		"""Get unit of the observable (formatted).

		Arguments:
		style   String or None. If set, one of the formatting styles. If None,
		        return the observable id.
		dimful  True or False. Whether to use the dimensionful (True) or
		        dimensionless (False) variety.
		negexp  True or False. If True, style quotients using negative exponents
		        (e.g., 'm s^-1'). If False, use a slash notation (e.g., 'm/s').

		Returns:
		String.
		"""
		raw_unit_str = self.get_unit(dimful = dimful)
		return format_unit(raw_unit_str, style = style, negexp = negexp)

	def get_range(self, dimful = False):
		"""Get minimum and maximum value for a colormap.

		Argument:
		dimful  True or False. Whether to use the dimensionful (True) or
		        dimensionless (False) variety.

		Returns:
		List of two numbers.
		"""
		if dimful:
			if self.dimful_factor is None:
				sys.stderr.write("Warning (Observable.get_range): Dimensional factor has not been initialized (for observable %s).\n" % self.obsid)
				return self.minmax
			return [self.minmax[0] * self.dimful_factor, self.minmax[1] * self.dimful_factor]
		else:
			return self.minmax

	def __str__(self):
		"""String: Observable id"""
		return self.obsid

	def __repr__(self):
		"""Representation with type 'Observable'"""
		return "<Observable '%s'>" % self.obsid

	def set_dimful_factor(self, param = None, value = None):
		"""Set dimensional factor for conversion between dimensionless and dimensionful observable.

		Arguments:
		param   PhysParams instance. Set conversion factor by extracting the
		        value from the PhysParams instance based on the string that is
		        set in self.dimful_qty.
		value   Float. Set conversion factor to this value.

		Note:
		Either param or value should be set, but not both.

		Returns:
		self.dimful_factor   Value of the conversion factor.
		"""
		if value is not None:
			if param is not None:
				raise ValueError("Either argument 'param' or argument 'value' must be specified, not both.")
			if self.dimful_qty is not None or self.dimful_factor is not None:
				pass  # show warning
			if not isinstance(value, (int, float, np.integer, np.floating)):
				raise TypeError("Argument 'value' must be numeric")
			self.dimful_factor = float(value)
			self.dimful_qty = 'value'
		elif param is not None:
			if not isinstance(param, PhysParams):
				raise TypeError("Argument 'param' must be a PhysParams instance.")
			if self.dimful_qty is None:
				self.dimful_factor = 1.0
				return 1.0
			paramdict = param.to_dict()
			# Parse values and parameters
			matches = re.findall(r"\s*([/\*]?)\s*([0-9.e+-]+|[a-z_]+)(\s*(\^|\*\*)\s*([+-]?[0-9]+))?", self.dimful_qty.lower())
			self.dimful_factor = 1.0
			if matches is None or len(matches) == 0:
				sys.stderr.write("Warning (Observable.set_dimful_factor): Attribute 'dimful_qty' has invalid contents (for observable '%s').\n" % self.obsid)
				return 1.0
			for m in matches:
				try:
					value = float(m[1])
				except:
					if m[1] in paramdict:
						try:
							value = float(paramdict[m[1]])
						except:
							value = 1.0
							sys.stderr.write("Warning (Observable.set_dimful_factor): Parameter '%s' is not numeric (for observable '%s').\n" % (m[1], self.obsid))
					else:
						sys.stderr.write("Warning (Observable.set_dimful_factor): '%s' is neither a value nor a valid parameter name (for observable '%s').\n" % (m[1], self.obsid))
						self.dimful_factor = 1.0
						return 1.0
				power = int(m[4]) if m[3] in ['**', '^'] else 1
				if m[0] == '/':
					power *= -1
				self.dimful_factor *= (value ** power)
				# print (value, "**", power, "=", value ** power, "-->", self.dimful_factor)
		else:
			raise ValueError("Either argument 'param' or argument 'value' must be specified.")
		return self.dimful_factor


class ObservableList:
	"""Container class for Observable instances.

	Attributes:
	observables   List of Observable instances.
	obsids        List of strings. The observable ids in the same order as
	              observables.
	obsids_alias  Dict instance of the form {alias: obs, ...}, where alias is a
	              a string and obs is an Observable instance.
	dimful        True, False, or None. Whether to globally consider
	              dimensionful (True) or dimensionless (False) observables. None
	              means undefined.
	"""
	def __init__(self, observables):
		if not isinstance(observables, list):
			raise TypeError("Argument for ObservableList must be a list of Observable instances")
		if len(observables) > 1 and not all([isinstance(obs, Observable) for obs in observables]):
			raise TypeError("Argument for ObservableList must be a list of Observable instances")
		self.observables = observables
		self.obsids = [obs.obsid for obs in self.observables]
		self.obsids_alias = {}
		for obs in self.observables:
			for alias in obs.obsid_alias:
				self.obsids_alias[alias] = obs.obsid
		self.dimful = None

	def __getitem__(self, key):
		"""Get Observable instance by index (key is int) or observable id (key is str)."""
		if isinstance(key, int):
			return self.observables[key]
		elif isinstance(key, str):
			if '[' in key and ']' in key:  # handle indexed observables
				m = re.match(indexed_obs_regex, key)
				if m is not None:
					key = m.group(1) + '[]'
			if key in self.obsids:
				idx = self.obsids.index(key)
				return self.observables[idx]
			elif key in self.obsids_alias:
				idx = self.obsids.index(self.obsids_alias[key])
				return self.observables[idx]
			else:
				raise KeyError
		else:
			raise TypeError

	def __iter__(self):
		return iter(self.observables)

	def __len__(self):
		return len(self.observables)

	def __contains__(self, item):
		"""The 'in' operator. The item can be an Observable instance or string (observable id)."""
		if isinstance(item, Observable):
			return item in self.observables
		elif isinstance(item, str):
			if '[' in item and ']' in item:  # handle indexed observables
				m = re.match(indexed_obs_regex, item)
				if m is not None:
					item = m.group(1) + '[]'
			return item in self.obsids or item in self.obsids_alias
		else:
			raise TypeError

	def append(self, obs):
		"""Add an Observable instance"""
		if not isinstance(obs, Observable):
			raise TypeError
		if obs.obsid in self.obsids:
			sys.stderr.write("Warning (ObservableList.append): Cannot add an observable with duplicate obsid '%s'.\n" % obs.obsid)
		self.obsids.append(obs.obsid)
		for alias in obs.obsid_alias:
			self.obsids_alias[alias] = obs.obsid

	def extend(self, other):
		"""Extend present instance by another ObservableList instance or by a list of Observable instances."""
		if isinstance(other, ObservableList) or (isinstance(other, list) and all(isinstance(o, Observable) for o in other)):
			for obs in other:
				self.append(obs)  # not the most efficient, but safe
		else:
			raise TypeError("Second argument must be a list of Observables or an ObservableList.")

	def __iadd__(self, other):
		self.extend(other)
		return self

	def set_dimful_factor(self, param = None, value = None):
		"""Set dimensionful factor for all observables.
		See Observable.set_dimful_factor() for more information.
		"""
		return [obs.set_dimful_factor(param = param, value = value) for obs in self.observables]

	def get_dim_factor(self, obs = None, dimful = None):
		"""Get dimensionful factor.

		Arguments:
		obs     Integer, string, or None. If integer, get the value for the
		        observable at that index. If string, get the value for the
		        observable with that observable id. If None, get a list of
		        values for all observables.
		dimful  True, False, or None. Get the value for dimensionful observables
		        (True) or dimensionless observables (False; always yields 1.0).
		        If None, use the value self.dimful set in the present
		        ObservableList instance.

		Returns:
		Float or list of floats.
		"""
		if dimful is None:
			dimful = self.dimful
		if obs is None:
			return [o.dimful_factor if dimful else 1.0 for o in self.observables]
		elif obs in self:
			o = self.__getitem__(obs)
			return o.dimful_factor if dimful else 1.0
		else:
			return 1.0

	def initialize(self, param = None, dimful = None):
		"""Initialize the present ObservableList instance.
		This initializes the dimensionful factors and sets the dimful attribute.

		Arguments:
		param   PhysParams instance. Extract conversion factors from this
		        PhysParams instance. See Observable.set_dimful_factor() for more
		        information.
		"""
		if dimful is True or dimful is False:
			self.dimful = dimful
		elif dimful is None:
			sys.stderr.write("Warning (ObservableList.initialize): Attribute 'dimful' is set to default value False.\n")
			self.dimful = False
		self.set_dimful_factor(param = param)

### OBSERVABLE FUNCTIONS ###

def obs_y(nz, ny, norb = 6):
	"""Observable <y>, function type 'none'."""
	y = np.arange(0, ny, dtype = float) / (ny - 1) - 0.5
	diag = np.repeat(y, norb * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_y2(nz, ny, norb = 6):
	"""Observable <y^2>, function type 'none'."""
	y = np.arange(0, ny, dtype = float) / (ny - 1) - 0.5
	diag = np.repeat(y**2, norb * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_z(nz, ny, norb = 6):
	"""Observable <z>, function type 'none'."""
	z = np.arange(0, nz, dtype = float) / (nz - 1) - 0.5
	diag = np.tile(np.repeat(z, norb), ny)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_z2(nz, ny, norb = 6):
	"""Observable <z^2>, function type 'none'."""
	z = np.arange(0, nz, dtype = float) / (nz - 1) - 0.5
	diag = np.tile(np.repeat(z**2, norb), ny)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_z_if(nz, ny, params):
	"""Observable <z_interface>, function type 'params'."""
	z_if1, z_if2 = params.well_z()
	norb = params.norbitals
	if z_if1 is None or z_if2 is None:
		return csc_matrix((norb * ny * nz, norb * ny * nz))  # zero matrix
	z = np.arange(0, nz, dtype = float)
	z_if = np.minimum(z - z_if1, z_if2 - z) / (nz - 1)
	diag = np.tile(np.repeat(z_if, norb), ny)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_z_if2(nz, ny, params):
	"""Observable <z_interface^2>, function type 'params'."""
	z_if1, z_if2 = params.well_z()
	norb = params.norbitals
	if z_if1 is None or z_if2 is None:
		return csc_matrix((norb * ny * nz, norb * ny * nz))  # zero matrix
	z = np.arange(0, nz, dtype = float)
	z_if = np.minimum(z - z_if1, z_if2 - z) / (nz - 1)
	diag = np.tile(np.repeat(z_if**2, norb), ny)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def in_zrange(nz, ny, z1, z2, norb = 6):
	"""Helper function for defining an observable for getting probability in a range (z1, z2).

	Arguments:
	nz    Integer. Number of lattice points in the z direction. Extract this
	      from a PhysParams instance.
	ny    Integer. Number of lattice points in the y direction. Extract this
	      from a PhysParams instance.
	z1    Integer. Coordinate in lattice points of the lower bound of the
	      interval.
	z2    Integer. Coordinate in lattice points of the upper bound of the
	      interval.
	norb  Integer. Number of orbitals.

	Returns:
	A scipy.sparse.dia_matrix() instance.
	"""
	if z1 is None or z2 is None:
		return csc_matrix((norb * ny * nz, norb * ny * nz))  # zero matrix
	z = np.arange(0, nz, dtype = float)
	z_in_well = np.where((z >= z1) & (z <= z2), np.ones_like(z), np.zeros_like(z))
	diag = np.tile(np.repeat(z_in_well, norb), ny)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def near_z(nz, ny, zval, d, norb = 6, relative = False):
	"""Helper function for defining an observable for getting probability near z.
	'Near z', means the interval [zval - d, zval + d].

	Arguments:
	nz        Integer. Number of lattice points in the z direction. Extract this
	          from a PhysParams instance.
	ny        Integer. Number of lattice points in the y direction. Extract this
	          from a PhysParams instance.
	zval      Integer. Coordinate in lattice points of the center of the
	          interval.
	d         Integer. Width of the interval in lattice points.
	norb      Integer. Number of orbitals.
	relative  True or False. If False, get an observable for the probability
	          density. If True, get an observable for the probability density
	          divided by the uniform probability density.

	Returns:
	A scipy.sparse.dia_matrix() instance.
	"""
	if isinstance(zval, (int, float, np.integer, np.floating)):
		zval = [zval]
	z = np.arange(0, nz, dtype = float)
	open_set = np.any([np.abs(z - z0) < d for z0 in zval], axis = 0)
	edges = np.any([np.abs(z - z0) == d for z0 in zval], axis = 0)
	near_z = np.where(open_set, np.ones_like(z), np.zeros_like(z))
	near_z += 0.5 * np.where(edges & ~open_set, np.ones_like(z), np.zeros_like(z))
	if relative:
		div = np.sum(near_z) / nz
		if div != 0.0:
			near_z /= div
	diag = np.tile(np.repeat(near_z, norb), ny)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_well(nz, ny, params):
	"""Observable <well>, function type 'params'."""
	z_if1, z_if2 = params.well_z()
	norb = params.norbitals
	return csc_matrix((norb * ny * nz, norb * ny * nz)) if z_if1 is None or z_if2 is None else in_zrange(nz, ny, z_if1, z_if2, norb)

def obs_wellext(nz, ny, params):
	"""Observable <well +/- 2 nm>, function type 'params'."""
	z_if1, z_if2 = params.well_z(extend_nm = 2.0)
	norb = params.norbitals
	return csc_matrix((norb * ny * nz, norb * ny * nz)) if z_if1 is None or z_if2 is None else in_zrange(nz, ny, z_if1, z_if2, norb)

def obs_interface_1nm(nz, ny, params):
	"""Observable 'interface density', 1 nm, function type 'params'."""
	return near_z(nz, ny, params.zinterface, 1.0 / params.zres, norb = params.norbitals, relative = False)  # d = 1.0 / params.zres

def obs_interface_char_1nm(nz, ny, params):
	"""Observable 'interface character', 1 nm, function type 'params'."""
	return near_z(nz, ny, params.zinterface, 1.0 / params.zres, norb = params.norbitals, relative = True)  # d = 1.0 / params.zres

def obs_interface_10nm(nz, ny, params):
	"""Observable 'interface density', 10 nm, function type 'params'."""
	return near_z(nz, ny, params.zinterface, 10.0 / params.zres, norb = params.norbitals, relative = False)  # d = 10.0 / params.zres

def obs_interface_char_10nm(nz, ny, params):
	"""Observable 'interface character', 10 nm, function type 'params'."""
	return near_z(nz, ny, params.zinterface, 10.0 / params.zres, norb = params.norbitals, relative = True)  # d = 10.0 / params.zres

def obs_interface_custom(nz, ny, params, length):
	"""Observable 'interface density', 10 nm, function type 'params'."""
	return near_z(nz, ny, params.zinterface, length / params.zres, norb = params.norbitals, relative = False)  # d = 10.0 / params.zres

def obs_interface_char_custom(nz, ny, params, length):
	"""Observable 'interface character', 10 nm, function type 'params'."""
	return near_z(nz, ny, params.zinterface, length / params.zres, norb = params.norbitals, relative = True)  # d = 10.0 / params.zres

def obs_split(nz, ny, norb = 6):
	"""Observable <H_split>, function type 'none'."""
	diag = np.tile(np.array([1., -1., 1., 1., -1., -1., 1., -1.]), ny * nz) if norb == 8 else np.tile(np.array([1., -1., 1., 1., -1., -1.]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_totalspinz(nz, ny, norb = 6):
	"""Observable <Jz>, function type 'none'."""
	diag = np.tile(np.array([0.5, -0.5, 1.5, 0.5, -0.5, -1.5, 0.5, -0.5]), ny * nz) if norb == 8 else np.tile(np.array([0.5, -0.5, 1.5, 0.5, -0.5, -1.5]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_totalspinx(nz, ny, norb = 6):
	"""Observable <Jx>, function type 'none'."""
	return blockdiag(spinmat.jxmat[:norb, :norb], ny * nz).tocsc()

def obs_totalspiny(nz, ny, norb = 6):
	"""Observable <Jy>, function type 'none'."""
	return blockdiag(spinmat.jymat[:norb, :norb], ny * nz).tocsc()

def obs_properspinz(nz, ny, norb = 6):
	"""Observable <Sz>, function type 'none'."""
	return blockdiag(spinmat.szmat[:norb, :norb], ny * nz).tocsc()

def obs_properspinx(nz, ny, norb = 6):
	"""Observable <Sx>, function type 'none'."""
	return blockdiag(spinmat.sxmat[:norb, :norb], ny * nz).tocsc()

def obs_properspiny(nz, ny, norb = 6):
	"""Observable <Sy>, function type 'none'."""
	return blockdiag(spinmat.symat[:norb, :norb], ny * nz).tocsc()

def obs_signspinz(nz, ny, norb = 6):
	"""Observable <sgn(Sz)>, function type 'none'."""
	diag = np.tile(np.array([1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0]), ny * nz) if norb == 8 else np.tile(np.array([1.0, -1.0, 1.0, 1.0, -1.0, -1.0]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_spinz6(nz, ny, norb = 6):
	"""Observable <Jz P_Gamma6>, function type 'none'."""
	diag = np.tile(np.array([0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), ny * nz) if norb == 8 else np.tile(np.array([0.5, -0.5, 0.0, 0.0, 0.0, 0.0]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_spinz8(nz, ny, norb = 6):
	"""Observable <Jz P_Gamma8>, function type 'none'."""
	diag = np.tile(np.array([0.0, 0.0, 1.5, 0.5, -0.5, -1.5, 0.0, 0.0]), ny * nz) if norb == 8 else np.tile(np.array([0.0, 0.0, 1.5, 0.5, -0.5, -1.5]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_spinz7(nz, ny, norb = 6):
	"""Observable <Jz P_Gamma7>, function type 'none'."""
	diag = np.tile(np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, -0.5]), ny * nz) if norb == 8 else np.tile(np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_y_spinz(nz, ny, norb = 6):
	"""Observable <y Jz>, function type 'none'."""
	y = np.arange(0, ny, dtype = float) / (ny - 1) - 0.5
	spinz = np.tile(np.array([0.5, -0.5, 1.5, 0.5, -0.5, -1.5, 0.5, -0.5]), nz) if norb == 8 else np.tile(np.array([0.5, -0.5, 1.5, 0.5, -0.5, -1.5]), nz)
	diag = np.kron(y, spinz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_orbital(nz, ny, norb = 6):
	"""Observable <P_Gamma6 - P_Gamma8>, function type 'none'."""
	diag = np.tile(np.array([1., 1., -1., -1., -1., -1., 0., 0.]), ny * nz) if norb == 8 else np.tile(np.array([1., 1., -1., -1., -1., -1.]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_orbital_gamma6(nz, ny, norb = 6):
	"""Observable <P_Gamma6>, function type 'none'."""
	diag = np.tile(np.array([1., 1., 0., 0., 0., 0., 0., 0.]), ny * nz) if norb == 8 else np.tile(np.array([1., 1., 0., 0., 0., 0.]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_orbital_gamma8(nz, ny, norb = 6):
	"""Observable <P_Gamma8>, function type 'none'."""
	diag = np.tile(np.array([0., 0., 1., 1., 1., 1., 0., 0.]), ny * nz) if norb == 8 else np.tile(np.array([0., 0., 1., 1., 1., 1.]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_orbital_gamma8h(nz, ny, norb = 6):
	"""Observable <P_Gamma8H>, function type 'none'."""
	diag = np.tile(np.array([0., 0., 1.0, 0., 0., 1.0, 0., 0.]), ny * nz) if norb == 8 else np.tile(np.array([0., 0., 1.0, 0., 0., 1.0]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_orbital_gamma8l(nz, ny, norb = 6):
	"""Observable <P_Gamma8L>, function type 'none'."""
	diag = np.tile(np.array([0., 0., 0., 1.0, 1.0, 0., 0., 0.]), ny * nz) if norb == 8 else np.tile(np.array([0., 0., 0., 1.0, 1.0, 0.]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_orbital_gamma7(nz, ny, norb = 6):
	"""Observable <P_Gamma7>, function type 'none'."""
	diag = np.tile(np.array([0., 0., 0., 0., 0., 0., 1., 1.]), ny * nz) if norb == 8 else np.tile(np.array([0., 0., 0., 0., 0., 0.]), ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_orbital_j(nz, ny, norb, j):
	"""Observable <P_orbital(j)>; function type 'mat_indexed'."""
	if j < 1 or j > norb:
		sys.stderr.write("ERROR (obs_orbital_j): Band index out of range [1, ..., norb]\n")
	uvec = np.zeros(norb)
	uvec[j - 1] = 1.0
	diag = np.tile(uvec, ny * nz)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_hdiag(h_block, nz, ny, params, magn = None):
	"""Helper function for block-diagonal observable matrix

	Arguments:
	h_block   Callable from hamiltonian.blocks.
	nz        NOT USED
	ny        Integer. Number of lattice points in y direction.
	params    PhysParams instance.
	magn      Float, Vector instance or None. If None, ignore, otherwise pass it
	          as keyword argument to h_block.

	Returns:
	A scipy.sparse.csc_matrix instance. The full matrix that can be used as
	observable.
	"""
	if magn is None:
		block = hz_block_diag(h_block, params)
	else:
		block = hz_block_diag(h_block, params, magn = magn)
	return blockdiag(block, ny).tocsc()

def obs_hexch(nz, ny, params, magn):
	"""Observable <H_exch>, function type 'params_magn'."""
	return obs_hdiag(hexchange, nz, ny, params, magn = magn)

def obs_hexch1t(nz, ny, params):
	"""Observable <H_exch> at 1T (in z direction), function type 'params'."""
	return obs_hdiag(hexchange, nz, ny, params, magn = 1.0)

def obs_hexchinf(nz, ny, params):
	"""Observable <H_exch> in large field limit (in z direction), function type 'params'."""
	return obs_hdiag(hexchange, nz, ny, params, magn = np.inf)

def obs_hzeeman(nz, ny, params, magn):
	"""Observable <H_zeeman>, function type 'params_magn'."""
	return obs_hdiag(hzeeman, nz, ny, params, magn = magn)

def obs_hzeeman1t(nz, ny, params):
	"""Observable <H_zeeman> at 1T (in z direction), function type 'params'."""
	return obs_hdiag(hzeeman, nz, ny, params, magn = 1.0)

def obs_hstrain(nz, ny, params):
	"""Observable <H_strain>, function type 'params'."""
	return obs_hdiag(hstrain, nz, ny, params)

def obs_llindex(nz, ny, norb):
	"""Observable <LL index> (for full LL mode), function type 'none'."""
	llindex = np.arange(0, ny) - 2
	diag = np.repeat(llindex, nz * norb)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_llindex_mod2(nz, ny, norb):
	"""Observable <LL index mod 2> (for full LL mode), function type 'none'."""
	llindex = np.mod(np.arange(0, ny) - 2, 2)
	diag = np.repeat(llindex, nz * norb)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_llindex_mod4(nz, ny, norb):
	"""Observable <LL index mod 4> (for full LL mode), function type 'none'."""
	llindex = np.mod(np.arange(0, ny) - 2, 4)
	diag = np.repeat(llindex, nz * norb)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def obs_ll_j(nz, ny, norb, j):
	"""Observable <P_ll(j)> (for full LL mode); undefined function type - NOT USED"""
	if j < -2 or j > ny - 3:  # ll_max = ny - 3
		sys.stderr.write("ERROR (obs_llindex_j): LL index out of range [-2, ..., llmax]\n")
	uvec = np.zeros(ny, dtype = float)
	uvec[j + 2] = 1.0
	diag = np.repeat(uvec, nz * norb)
	loc = 0
	return dia_matrix((np.array([diag]), loc), shape = (norb * ny * nz, norb * ny * nz)).tocsc()

def llindex_max(eivec, nz, ny, norb):
	"""Observable LL index 'by maximum', function type 'eivec'."""
	size = nz * norb  # 'average' LL index
	ll_overlap = np.array([np.dot(eivec[size * l:size * (l+1)].conjugate(), eivec[size * l:size * (l+1)]) for l in range(0, ny)])  # ll_max = ny - 3
	return np.argmax(np.abs(ll_overlap)) - 2

def llindex_kwds(nz, ny, llindex = None, **kwds):
	"""Observable LL index, function type 'kwds'."""
	if llindex is None:
		raise ValueError
	return llindex

# IPR-like quantities
# The inverse participation ratio (IPR) is defined in terms of the second and
# fourth moment (m2 and m4, respectively) of the spatial wave functions,
# basically m2**2 / m4.
# Here, we provide a scale and resolution invariant definition. The results are
# dimensionless by definition, but may be multiplied by the sample size (length
# for iprz and ipry, area for ipryz) to get a dimensionful physical quantity.
# Note that here, we (should) always have m2 = 1.
def ipr_z(eivec, nz, ny, norb):
	"""Observable IPR_z, function type 'eivec'."""
	eivec2 = eivec.conjugate() * eivec  # Not a matrix multiplication!
	eivec2z = np.sum(np.sum(eivec2.reshape(ny, nz, norb), axis = 2), axis = 0)
	m2 = np.sum(eivec2z)
	m4 = np.sum(eivec2z**2)
	return m2**2 / m4 / nz

def ipr_y(eivec, nz, ny, norb):
	"""Observable IPR_y, function type 'eivec'."""
	eivec2 = eivec.conjugate() * eivec  # Not a matrix multiplication!
	eivec2y = np.sum(np.sum(eivec2.reshape(ny, nz, norb), axis = 2), axis = 1)
	m2 = np.sum(eivec2y)
	m4 = np.sum(eivec2y**2)
	return m2**2 / m4 / ny

def ipr_yz(eivec, nz, ny, norb):
	"""Observable IPR_yz, function type 'eivec'."""
	eivec2 = eivec.conjugate() * eivec  # Not a matrix multiplication!
	eivec2yz = np.sum(eivec2.reshape(ny * nz, norb), axis = 1)
	m2 = np.sum(eivec2yz)
	m4 = np.sum(eivec2yz**2)
	return m2**2 / m4 / ny / nz

### Derived parity functions
# parity_{x,y,z}() are taken from hamiltonian/parity.py
def isoparity_z(par1, par2 = None, norb = 6):
	"""Isoparity in z. See hamiltonian/parity.py for more information."""
	return parity_z(par1, par2, norb, isoparity = True)

def isoparity_z_well(nz, ny, params):
	"""Isoparity in z applied to the well only. See hamiltonian/parity.py for more information."""
	norb = params.norbitals
	z_if1, z_if2 = params.well_z()
	if z_if1 is None or z_if2 is None:
		return csc_matrix((norb * ny * nz, norb * ny * nz))  # zero matrix
	return parity_z(nz, ny, norb, isoparity = True, zrange = (z_if1, z_if2))

def isoparity_z_symm(nz, ny, params):
	"""Isoparity in z applied to a symmetric region around the well only. See hamiltonian/parity.py for more information."""
	norb = params.norbitals
	z_if1, z_if2 = params.symmetric_z()
	if z_if1 is None or z_if2 is None:
		return csc_matrix((norb * ny * nz, norb * ny * nz))  # zero matrix
	return parity_z(nz, ny, norb, isoparity = True, zrange = (z_if1, z_if2))

def isoparity_x(par1, par2 = None, norb = 6):
	"""Isoparity in x. See hamiltonian/parity.py for more information."""
	return parity_x(par1, par2, norb, isoparity = True)

def isoparity_y(par1, par2 = None, norb = 6):
	"""Isoparity in y. See hamiltonian/parity.py for more information."""
	return parity_y(par1, par2, norb, isoparity = True)

def parity_zy(par1, par2 = None, norb = 6):
	"""Parity in z and y. See hamiltonian/parity.py for more information.
	The result is calculated through matrix multiplication.
	"""
	return parity_z(par1, par2, norb, isoparity = False) @ parity_y(par1, par2, norb, isoparity = False)

def isoparity_zy(par1, par2 = None, norb = 6):
	"""Isoparity in z and y. See hamiltonian/parity.py for more information.
	The result is calculated through matrix multiplication.
	"""
	return parity_z(par1, par2, norb, isoparity = True) @ parity_y(par1, par2, norb, isoparity = True)

### OBSERVABLE DEFINITIONS ###
all_observables = ObservableList([
	Observable(
		'y', obs_y, unit_dimful = 'nm', dimful_qty = 'w',
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "y/w", 'tex': r"$\langle y\rangle/w$", 'unicode': "\u27e8y\u27e9/w"},
		str_dimful = {'plain': "y", 'tex': r"$\langle y\rangle$", 'unicode': "\u27e8y\u27e9"}),
	Observable(
		'y2', obs_y2, unit_dimful = 'nm^2', dimful_qty = 'w^2',
		minmax = [0.0, 0.25], colordata = 'posobs',
		obsid_alias = "y^2",
		str_dimless = {'plain': "(y/w)^2", 'tex': r"$\langle y^2\!\rangle/w^2$", 'unicode': "\u27e8y\xb2\u27e9/w\xb2"},
		str_dimful = {'plain': "y^2", 'tex': r"$\langle y^2\!\rangle$", 'unicode': "\u27e8y\xb2\u27e9"}),
	Observable(
		'sigmay', None, unit_dimful = 'nm^2', dimful_qty = 'w',
		minmax = [0.0, 0.5], colordata = 'posobs',
		obsid_alias = "sigma_y",
		str_dimless = {'plain': "sigma_y/w", 'tex': r"$\sigma_y/w$", 'unicode': "\u03c3_y/w"},
		str_dimful = {'plain': "sigma_y", 'tex': r"$\sigma_y$", 'unicode': "\u03c3_y"}),
	Observable(
		'z', obs_z, unit_dimful = 'nm', dimful_qty = 'd',
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "z/d", 'tex': r"$\langle z\rangle/d$", 'unicode': "\u27e8z\u27e9/d"},
		str_dimful = {'plain': "z", 'tex': r"$\langle z\rangle$", 'unicode': "\u27e8z\u27e9"}),
	Observable(
		'z2', obs_z2, unit_dimful = 'nm^2', dimful_qty = 'd^2',
		minmax = [0.0, 0.25], colordata = 'posobs',
		obsid_alias = "z^2",
		str_dimless = {'plain': "(z/d)^2", 'tex': r"$\langle z^2\!\rangle/d^2$", 'unicode': "\u27e8z\xb2\u27e9/d\xb2"},
		str_dimful = {'plain': "z^2", 'tex': r"$\langle z^2\!\rangle$", 'unicode': "\u27e8z\xb2\u27e9"}),
	Observable(
		'sigmaz', None, unit_dimful = 'nm^2', dimful_qty = 'd',
		minmax = [0.0, 0.5], colordata = 'posobs',
		obsid_alias = "sigma_z",
		str_dimless = {'plain': "sigma_z/d", 'tex': r"$\sigma_z/d$", 'unicode': "\u03c3_z/d"},
		str_dimful = {'plain': "sigma_z", 'tex': r"$\sigma_z$", 'unicode': "\u03c3_z"}),
	Observable(
		'zif', obs_z_if, obsfun_type = 'params', unit_dimful = 'nm', dimful_qty = 'd',
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		obsid_alias = "z_if",
		str_dimless = {'plain': "z_if/d", 'tex': r"$\langle z_\mathrm{if}\rangle/d$", 'unicode': "\u27e8z_if\u27e9/d"},
		str_dimful = {'plain': "z_if", 'tex': r"$\langle z_\mathrm{if}\rangle$", 'unicode': "\u27e8z_if\u27e9"}),
	Observable(
		'zif2', obs_z_if2, obsfun_type = 'params', unit_dimful = 'nm^2', dimful_qty = 'd^2',
		minmax = [0.0, 0.25], colordata = 'posobs',
		obsid_alias = ["z_if2", "zif^2", "z_if^2"],
		str_dimless = {'plain': "(z_if/d)^2", 'tex': r"$\langle z_\mathrm{if}^2\!\rangle/d^2$", 'unicode': "\u27e8z_if\xb2\u27e9/d\xb2"},
		str_dimful = {'plain': "z_if^2", 'tex': r"$\langle z_\mathrm{if}^2\!\rangle$", 'unicode': "\u27e8z_if\xb2\u27e9"}),
	Observable(
		'sigmazif', None, unit_dimful = 'nm^2', dimful_qty = 'w',
		minmax = [0.0, 0.5], colordata = 'posobs',
		obsid_alias = ['sigmaz_if', 'sigma_zif', 'sigma_z_if'],
		str_dimless = {'plain': "sigma_zif/d", 'tex': r"$\sigma_{z_\mathrm{if}}/d$", 'unicode': "\u03c3_zif/d"},
		str_dimful = {'plain': "sigma_zif", 'tex': r"$\sigma_{z_\mathrm{if}}$", 'unicode': "\u03c3_zif"}),
	Observable(
		'well', obs_well, obsfun_type = 'params',
		minmax = [0.0, 1.0], colordata = 'posobs',
		str_dimless = {'plain': "psi^2(well)", 'tex': r"$|\psi_{\mathrm{well}}|^2$", 'unicode': "|\u03c8_well|\xb2"}),  # alternative TeX: r"$\int_{\mathrm{well}}|\psi|^2 dz$"
	Observable(
		'wellext', obs_wellext, obsfun_type = 'params',
		minmax = [0.0, 1.0], colordata = 'posobs',
		obsid_alias = ["extwell", "ext_well", "well_ext"],
		str_dimless = {'plain': "psi^2(well+2nm)", 'tex': r"$|\psi_{\mathrm{well}\pm2\,\mathrm{nm}}|^2$", 'unicode': "|\u03c8_well\xb12nm|\xb2"}),  # alternative TeX: r"$\int_{\mathrm{well}\pm 2\,\mathrm{nm}}|\psi|^2 dz$"
	Observable(
		'interface', obs_interface_1nm, obsfun_type = 'params',
		minmax = [0.0, 1.0], colordata = 'posobs',
		obsid_alias = ["interface1nm", "interface_1nm", "if1nm", "if_1nm"],
		str_dimless = {'plain': "psi^2(if_1nm)", 'tex': r"$|\psi_{\mathrm{if},1\,\mathrm{nm}}|^2$", 'unicode': "|\u03c8_if|\xb2 (1nm)"}),
	Observable(
		'interfacechar', obs_interface_char_1nm, obsfun_type = 'params',
		minmax = [0.0, 3.0], colordata = 'posobs',
		obsid_alias = ["interfacechar1nm", "interface_char", "interface_char_1nm", "ifchar", "if_char", "ifchar1nm", "if_char_1nm"],
		str_dimless = {'plain': "<psi^2(if_1nm)>", 'tex': r"$\langle |\psi_{\mathrm{if},1\,\mathrm{nm}}|^2\rangle$", 'unicode': "\u27e8|\u03c8_if|\xb2\u27e9 (1nm)"}),
	Observable(
		'interface10nm', obs_interface_10nm, obsfun_type = 'params',
		minmax = [0.0, 1.0], colordata = 'posobs',
		obsid_alias = ["interface10nm", "interface_10nm", "if10nm", "if_10nm"],
		str_dimless = {'plain': "psi^2(if_10nm)", 'tex': r"$|\psi_{\mathrm{if},10\,\mathrm{nm}}|^2$", 'unicode': "|\u03c8_if|\xb2 (10nm)"}),
	Observable(
		'interfacechar10nm', obs_interface_char_10nm, obsfun_type = 'params',
		minmax = [0.0, 3.0], colordata = 'posobs',
		obsid_alias = ["interfacechar10nm", "interface_char_10nm", "ifchar", "if_char", "ifchar10nm", "if_char_10nm"],
		str_dimless = {'plain': "<psi^2(if_10nm)>", 'tex': r"$\langle |\psi_{\mathrm{if},10\,\mathrm{nm}}|^2\rangle$", 'unicode': "\u27e8|\u03c8_if|\xb2\u27e9 (10nm)"}),
	Observable(
		'custominterface[]', obs_interface_custom, obsfun_type = 'params_indexed',
		minmax = [0.0, 1.0], colordata = 'posobs',
		str_dimless = {'plain': "psi^2(if_%inm)", 'tex': r"$|\psi_{\mathrm{if},%i\,\mathrm{nm}}|^2$",
		               'unicode': "|\u03c8_if|\xb2 (%inm)"}),
	Observable(
		'custominterfacechar[]', obs_interface_char_custom, obsfun_type = 'params_indexed',
		minmax = [0.0, 3.0], colordata = 'posobs',
		str_dimless = {'plain': "<psi^2(if_%inm)>", 'tex': r"$\langle |\psi_{\mathrm{if},%i\,\mathrm{nm}}|^2\rangle$",
		               'unicode': "\u27e8|\u03c8_if|\xb2\u27e9 (%inm)"}),
	Observable(
		'ipry', ipr_y, obsfun_type = 'eivec', unit_dimful = 'nm', dimful_qty = 'w',
		minmax = [0.0, 1.0], colordata = 'ipr',
		str_dimless = {'plain': "IPR_y", 'tex': r"$\mathrm{IPR}_y$", 'unicode': "IPR_y"},
		str_dimful = {'plain': "IPR_y", 'tex': r"$\mathrm{IPR}_y$", 'unicode': "IPR_y"}),
	Observable(
		'iprz', ipr_z, obsfun_type = 'eivec', unit_dimful = 'nm', dimful_qty = 'd',
		minmax = [0.0, 1.0], colordata = 'ipr',
		str_dimless = {'plain': "IPR_z", 'tex': r"$\mathrm{IPR}_z$", 'unicode': "IPR_z"},
		str_dimful = {'plain': "IPR_z", 'tex': r"$\mathrm{IPR}_z$", 'unicode': "IPR_z"}),
	Observable(
		'ipryz', ipr_yz, obsfun_type = 'eivec', unit_dimful = 'nm^2', dimful_qty = 'd*w',
		minmax = [0.0, 1.0], colordata = 'ipr',
		str_dimless = {'plain': "IPR_yz", 'tex': r"$\mathrm{IPR}_{(y,z)}$", 'unicode': "IPR_yz"},
		str_dimful = {'plain': "IPR_yz", 'tex': r"$\mathrm{IPR}_{(y,z)}$", 'unicode': "IPR_yz"}),
	Observable(
		'sz', obs_properspinz,
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "Sz", 'tex': r"$\langle S^z\!\rangle$", 'unicode': "\u27e8Sz\u27e9"}),
	Observable(
		'sx', obs_properspinx,
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "Sx", 'tex': r"$\langle S^x\!\rangle$", 'unicode': "\u27e8Sx\u27e9"}),
	Observable(
		'sy', obs_properspiny,
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "Sy", 'tex': r"$\langle S^y\!\rangle$", 'unicode': "\u27e8Sy\u27e9"}),
	Observable(
		'jz', obs_totalspinz,
		minmax = [-1.5, 1.5], colordata = 'threehalves',
		obsid_alias = 'spinz',
		str_dimless = {'plain': "Jz", 'tex': r"$\langle J^z\!\rangle$", 'unicode': "\u27e8Jz\u27e9"}),
	Observable(
		'jx', obs_totalspinx,
		minmax = [-1.5, 1.5], colordata = 'threehalves',
		obsid_alias = 'spinx',
		str_dimless = {'plain': "Jx", 'tex': r"$\langle J^x\!\rangle$", 'unicode': "\u27e8Jx\u27e9"}),
	Observable(
		'jy', obs_totalspiny,
		minmax = [-1.5, 1.5], colordata = 'threehalves',
		obsid_alias = 'spiny',
		str_dimless = {'plain': "Jy", 'tex': r"$\langle J^y\!\rangle$", 'unicode': "\u27e8Jy\u27e9"}),
	Observable(
		'jz6', obs_spinz6,
		minmax = [-1.5, 1.5], colordata = 'threehalves',
		obsid_alias = 'spinz6',
		str_dimless = {'plain': "Jz_Gamma6", 'tex': r"$\langle J^z P_{\Gamma_6}\!\rangle$", 'unicode': "\u27e8Jz P_\u03936\u27e9"}),
	Observable(
		'jz8', obs_spinz8,
		minmax = [-1.5, 1.5], colordata = 'threehalves',
		obsid_alias = 'spinz8',
		str_dimless = {'plain': "Jz_Gamma8", 'tex': r"$\langle J^z P_{\Gamma_8}\!\rangle$", 'unicode': "\u27e8Jz P_\u03938\u27e9"}),
	Observable(
		'jz7', obs_spinz7,
		minmax = [-1.5, 1.5], colordata = 'threehalves',
		obsid_alias = 'spinz7',
		str_dimless = {'plain': "Jz_Gamma7", 'tex': r"$\langle J^z P_{\Gamma_7}\!\rangle$", 'unicode': "\u27e8Jz P_\u03937\u27e9"}),
	Observable(
		'yjz', obs_y_spinz,
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		obsid_alias = ["yspinz", "y spinz", "y jz", "y*spinz", "y*jz"],
		str_dimless = {'plain': "y Jz", 'tex': r"$\langle y J^z\!\rangle$", 'unicode': "\u27e8y Jz\u27e9"}),
	Observable(
		'split', obs_split,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		str_dimless = {'plain': "sgn Jz", 'tex': r"$\langle \mathrm{sgn}(J^z)\!\rangle$", 'unicode': "\u27e8sgn Jz\u27e9"}),
	Observable(
		'orbital', obs_orbital,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		str_dimless = {'plain': "orbital", 'tex': r"$\langle P_{\Gamma_6} - P_{\Gamma_8}\rangle$", 'unicode': "\u27e8P_\u03936-P_\u03938\u27e9"}),
	Observable(
		'gamma6', obs_orbital_gamma6,
		minmax = [0.0, 1.0], colordata = 'posobs',
		str_dimless = {'plain': "Gamma6", 'tex': r"$\langle P_{\Gamma_6}\rangle$", 'unicode': "\u27e8P_\u03936\u27e9"}),
	Observable(
		'gamma8', obs_orbital_gamma8,
		minmax = [0.0, 1.0], colordata = 'posobs',
		str_dimless = {'plain': "Gamma8", 'tex': r"$\langle P_{\Gamma_8}\rangle$", 'unicode': "\u27e8P_\u03938\u27e9"}),
	Observable(
		'gamma8l', obs_orbital_gamma8l,
		minmax = [0.0, 1.0], colordata = 'posobs',
		str_dimless = {'plain': "Gamma8L", 'tex': r"$\langle P_{\Gamma_{8};\mathrm{LH}}\rangle$", 'unicode': "\u27e8P_\u03938L\u27e9"}),
	Observable(
		'gamma8h', obs_orbital_gamma8h,
		minmax = [0.0, 1.0], colordata = 'posobs',
		str_dimless = {'plain': "Gamma8H", 'tex': r"$\langle P_{\Gamma_{8};\mathrm{HH}}\rangle$", 'unicode': "\u27e8P_\u03938H\u27e9"}),
	Observable(
		'gamma7', obs_orbital_gamma7,
		minmax = [0.0, 1.0], colordata = 'posobs',
		str_dimless = {'plain': "Gamma7", 'tex': r"$\langle P_{\Gamma_7}$", 'unicode': "\u27e8P_\u03937\u27e9"}),
	Observable(
		'orbital[]', obs_orbital_j, obsfun_type = 'mat_indexed',
		minmax = [0.0, 1.0], colordata = 'posobs',
		str_dimless = {'plain': "orbital[%i]", 'tex': r"$\langle P_{\mathrm{orb}\,%i}\rangle$", 'unicode': "\u27e8P_o%i\u27e9"}),
	Observable(
		'px', parity_x,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = 'parx',
		str_dimless = {'plain': "Px", 'tex': r"$\langle \mathcal{P}_x\rangle$", 'unicode': "\u27e8Px\u27e9"}),
	Observable(
		'isopx', isoparity_x,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = 'isoparx',
		str_dimless = {'plain': "Px (iso)", 'tex': r"$\langle \tilde{\mathcal{P}}_x\rangle$", 'unicode': "\u27e8Px\u27e9 (iso)"}),
	Observable(
		'py', parity_y,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = 'pary',
		str_dimless = {'plain': "Py", 'tex': r"$\langle \mathcal{P}_y\rangle$", 'unicode': "\u27e8Py\u27e9"}),
	Observable(
		'isopy', isoparity_y,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = 'isopary',
		str_dimless = {'plain': "Py (iso)", 'tex': r"$\langle \tilde{\mathcal{P}}_y\rangle$", 'unicode': "\u27e8Py\u27e9 (iso)"}),
	Observable(
		'pz', parity_z,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = 'parz',
		str_dimless = {'plain': "Pz", 'tex': r"$\langle \mathcal{P}_z\rangle$", 'unicode': "\u27e8Pz\u27e9"}),
	Observable(
		'isopz', isoparity_z,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = 'isoparz',
		str_dimless = {'plain': "Pz (iso)", 'tex': r"$\langle \tilde{\mathcal{P}}_z\rangle$", 'unicode': "\u27e8Pz\u27e9 (iso)"}),
	Observable(
		'isopzw', isoparity_z_well, obsfun_type = 'params',
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = 'isoparzw',
		str_dimless = {'plain': "Pz (iso,well)", 'tex': r"$\langle \tilde{\mathcal{P}}_{z,\mathrm{w}}\rangle$", 'unicode': "\u27e8Pz\u27e9 (iso,well)"}),
	Observable(
		'isopzs', isoparity_z_symm, obsfun_type = 'params',
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = 'isoparzs',
		str_dimless = {'plain': "Pz (iso,symm)", 'tex': r"$\langle \tilde{\mathcal{P}}_{z,\mathrm{s}}\rangle$", 'unicode': "\u27e8Pz\u27e9 (iso,symm)"}),
	Observable(
		'pzy', parity_zy,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = ['parzy', 'pzpy', 'pyz', 'paryz', 'pypz'],
		str_dimless = {'plain': "Pzy", 'tex': r"$\langle \mathcal{P}_z\mathcal{P}_y\rangle$", 'unicode': "\u27e8Pz Py\u27e9"}),
	Observable(
		'isopzy', isoparity_zy,
		minmax = [-1.0, 1.0], colordata = 'symmobs',
		obsid_alias = ['isoparzy', 'isopzpy', 'isopyz', 'isoparyz', 'isopypz'],
		str_dimless = {'plain': "Pzy (iso)", 'tex': r"$\langle \tilde{\mathcal{P}}_z\mathcal{P}_y\rangle$", 'unicode': "\u27e8Pz Py\u27e9 (iso)"}),
	Observable(
		'llindex', llindex_kwds, obsfun_type = 'kwds',
		minmax = [-2.5, 17.5], colordata = 'indexed',
		obsid_alias = ['ll_n', 'lln'],
		str_dimless = {'plain': "n (LL)", 'tex': r"LL index $n$", 'unicode': "n (LL)"}),
	Observable(
		'llavg', obs_llindex,
		minmax = [-2.5, 17.5], colordata = 'indexed',
		str_dimless = {'plain': "<n> (LL)", 'tex': r"$\langle n\rangle$", 'unicode': "\u27e8n\u27e9 (LL)"}),
	Observable(
		'llmod2', obs_llindex_mod2,
		minmax = [0.0, 1.0], colordata = 'symmobs',
		str_dimless = {'plain': "<n mod 2> (LL)", 'tex': r"$\langle n\ \mathrm{mod}\  2\rangle$", 'unicode': "\u27e8n mod 2\u27e9 (LL)"}),
	Observable(
		'llmod4', obs_llindex_mod4,
		minmax = [0.0, 3.0], colordata = 'threehalves',
		str_dimless = {'plain': "<n mod 4> (LL)", 'tex': r"$\langle n\ \mathrm{mod}\  4\rangle$", 'unicode': "\u27e8n mod 4\u27e9 (LL)"}),
	Observable(
		'llbymax', llindex_max, obsfun_type = 'eivec',
		minmax = [-2.5, 17.5], colordata = 'indexed',
		str_dimless = {'plain': "n (maj)", 'tex': r"$n$ (majority)", 'unicode': "\u27e8n\u27e9 (maj)"}),
	Observable(
		'll[]', obs_ll_j, obsfun_type = 'mat_indexed',
		minmax = [0.0, 1.0], colordata = 'posobs',
		str_dimless = {'plain': "ll[%i]", 'tex': r"$\langle P_{\mathrm{LL}\,%i}\rangle$", 'unicode': "\u27e8P_LL%i\u27e9"}),
	Observable(
		'berryz', None, unit_dimless = "nm^2",
		minmax = [-400., 400.], colordata = 'symmobs',
		obsid_alias = 'berry',
		str_dimless = {'plain': "Fz (Berry)", 'tex': r"$F_z$ (Berry)", 'unicode': "Fz (Berry)"}),
	Observable(
		'berryx', None, unit_dimless = "nm^2",
		minmax = [-400., 400.], colordata = 'symmobs',
		str_dimless = {'plain': "Fx (Berry)", 'tex': r"$F_x$ (Berry)", 'unicode': "Fx (Berry)"}),
	Observable(
		'berryy', None, unit_dimless = "nm^2",
		minmax = [-400., 400.], colordata = 'symmobs',
		str_dimless = {'plain': "Fy (Berry)", 'tex': r"$F_y$ (Berry)", 'unicode': "Fy (Berry)"}),
	Observable(
		'berryiso', None, unit_dimless = "nm^2",
		minmax = [-400., 400.], colordata = 'symmobs',
		obsid_alias = 'isoberry',
		str_dimless = {'plain': "Fztilde (Berry iso)", 'tex': r"$\tilde{F}_z$ (Berry iso)", 'unicode': "Fztilde (Berry iso)"}),
	Observable(
		'chern', None,
		minmax = [-3., 3.], colordata = 'symmobs',
		str_dimless = {'plain': "C (Chern)", 'tex': r"$C$ (Chern)", 'unicode': "C (Chern)"}),
	Observable(
		'chernsim', None,
		minmax = [-3., 3.], colordata = 'symmobs',
		str_dimless = {'plain': "C (simul. Chern)", 'tex': r"$C$ (simul. Chern)", 'unicode': "C (simul. Chern)"}),
	Observable(
		'dedk', None, unit_dimless = "meV nm",
		minmax = [-300., 300.], colordata = 'symmobs',
		str_dimless = {'plain': "dE / dk", 'tex': r"$dE/dk$", 'unicode': "dE / dk"}),
	Observable(
		'dedkr', None, unit_dimless = "meV nm",
		minmax = [-300., 300.], colordata = 'symmobs',
		str_dimless = {'plain': "nabla E", 'tex': r"$\nabla E\cdot\hat{r}$", 'unicode': "\u2207E \u22c5 r"}),
	Observable(
		'dedkabs', None, unit_dimless = "meV nm",
		minmax = [0., 300.], colordata = 'posobs',
		str_dimless = {'plain': "|nabla E|", 'tex': r"$|\nabla E|$", 'unicode': "|\u2207E|"}),
	Observable(
		'dedkx', None, unit_dimless = "meV nm",
		minmax = [-300., 300.], colordata = 'symmobs',
		str_dimless = {'plain': "dE / dkx", 'tex': r"$dE/dk_x$", 'unicode': "dE / dkx"}),
	Observable(
		'dedky', None, unit_dimless = "meV nm",
		minmax = [-300., 300.], colordata = 'symmobs',
		str_dimless = {'plain': "dE / dky", 'tex': r"$dE/dk_y$", 'unicode': "dE / dky"}),
	Observable(
		'dedkz', None, unit_dimless = "meV nm",
		minmax = [-300., 300.], colordata = 'symmobs',
		str_dimless = {'plain': "dE / dkz", 'tex': r"$dE/dk_z$", 'unicode': "dE / dkz"}),
	Observable(
		'dedkphi', None, unit_dimless = "meV nm",
		minmax = [-300., 300.], colordata = 'symmobs',
		str_dimless = {'plain': "nabla E . phi", 'tex': r"$\nabla E\cdot\hat{\phi}$", 'unicode': "\u2207E \u22c5 \u03d5"}),
	Observable(
		'dedktheta', None, unit_dimless = "meV nm",
		minmax = [-300., 300.], colordata = 'symmobs',
		str_dimless = {'plain': "nabla E . theta", 'tex': r"$\nabla E\cdot\hat{\theta}$", 'unicode': "\u2207E \u22c5 \u03b8"}),
	Observable(
		'v', None, unit_dimless = "10^6 m/s",
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "v", 'tex': r"$v$", 'unicode': "v"}),
	Observable(
		'vr', None, unit_dimless = "10^6 m/s",
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "vr", 'tex': r"$v_r$", 'unicode': "vr"}),
	Observable(
		'vabs', None, unit_dimless = "10^6 m/s",
		minmax = [0.0, 0.5], colordata = 'posobs',
		str_dimless = {'plain': "|v|", 'tex': r"$|v|$", 'unicode': "|v|"}),
	Observable(
		'vx', None, unit_dimless = "10^6 m/s",
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "vx", 'tex': r"$v_x$", 'unicode': "vx"}),
	Observable(
		'vy', None, unit_dimless = "10^6 m/s",
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "vy", 'tex': r"$v_y$", 'unicode': "vy"}),
	Observable(
		'vz', None, unit_dimless = "10^6 m/s",
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "vz", 'tex': r"$v_z$", 'unicode': "vz"}),
	Observable(
		'vphi', None, unit_dimless = "10^6 m/s",
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "vphi", 'tex': r"$v_\phi$", 'unicode': "v\u03d5"}),
	Observable(
		'vtheta', None, unit_dimless = "10^6 m/s",
		minmax = [-0.5, 0.5], colordata = 'symmobs',
		str_dimless = {'plain': "vtheta", 'tex': r"$v_\theta$", 'unicode': "v\u03b8"}),
	Observable(
		'hex', obs_hexch, obsfun_type = 'params_magn', unit_dimless = "meV",
		minmax = [-15., 15.], colordata = 'symmobs',
		obsid_alias = ["h_ex", "hexch", "h_exch"],
		str_dimless = {'plain': "Hexch", 'tex': r"$H_\mathrm{exch}$", 'unicode': "Hexch"}),
	Observable(
		'hex1t', obs_hexch1t, obsfun_type = 'params', unit_dimless = "meV",
		minmax = [-15., 15.], colordata = 'symmobs',
		obsid_alias = ["h_ex_1t", "hexch1t", "h_exch_1t"],
		str_dimless = {'plain': "Hexch(1T)", 'tex': r"$H_\mathrm{exch}(1\,\mathrm{T})$", 'unicode': "Hexch(1T)"}),
	Observable(
		'hexinf', obs_hexchinf, obsfun_type = 'params', unit_dimless = "meV",
		minmax = [-15., 15.], colordata = 'symmobs',
		obsid_alias = ["h_ex_inf", "hexchinf", "h_exch_inf"],
		str_dimless = {'plain': "Hexch(inf)", 'tex': r"$H_\mathrm{exch}(\infty)$", 'unicode': "Hexch(\u221e)"}),
	Observable(
		'hz', obs_hzeeman, obsfun_type = 'params_magn', unit_dimless = "meV",
		minmax = [-5., 5.], colordata = 'symmobs',
		obsid_alias = ["h_z", "hzeeman", "h_zeeman"],
		str_dimless = {'plain': "HZ", 'tex': r"$H_\mathrm{Z}$", 'unicode': "HZ"}),
	Observable(
		'hz1t', obs_hzeeman1t, obsfun_type = 'params', unit_dimless = "meV",
		minmax = [-5., 5.], colordata = 'symmobs',
		obsid_alias = ["h_z1t", "hzeeman1t", "h_zeeman1t"],
		str_dimless = {'plain': "HZ(1T)", 'tex': r"$H_\mathrm{Z}(1\,\mathrm{T})$", 'unicode': "HZ(1T)"}),
	Observable(
		'hstrain', obs_hstrain, obsfun_type = 'params', unit_dimless = "meV",
		minmax = [-15., 15.], colordata = 'symmobs',
		obsid_alias = "h_strain",
		str_dimless = {'plain': "Hstrain", 'tex': r"$H_\mathrm{strain}$", 'unicode': "Hstrain"}),
])

jwell_warning_issued = False
obs_error_issued = False
def observables(eivecs, params, obs, llindex = None, overlap_eivec = None, magn = None):
	"""Calculate observables from eigenvectors

	Arguments:
	eivecs            Numpy array of two dimensions.
	params            PhysParams instance.
	obs               List of strings. Observable ids for which to calculate the
	                  values.
	llindex           Integer or None. Necessary for the llindex observable.
	observable_eivec  Dict instance, whose keys are band labels (characters) and
	                  values are one-dimensional arrays. This is for calculating
	                  overlaps of the current eigenvectors (eivecs) with the
	                  values of observable_eivec.
	magn              Float, Vector instance or None. If not None, the magnetic
	                  field strength.

	Returns:
	Numpy array of complex numbers. The size is (nobs, neig), where nobs is the
	number of observables and neig the number of eigenvectors. The values are
	the observable values for the observables in obs.
	"""
	global obs_error_issued
	nz = params.nz
	ny = params.ny
	norb = params.norbitals
	tp = False
	# tp ('transpose') determines whether eigenvectors are in a transposed
	# configuration in eivec. For the standard returned data of eigsh: tp = True

	if eivecs.shape[0] == norb * ny * nz:  # for 1D
		neig = eivecs.shape[1]
		tp = True
	elif eivecs.shape[1] == norb * ny * nz:  # for 1D, inverted order
		neig = eivecs.shape[0]
	elif eivecs.shape[0] == norb * nz:  # for 2D
		ny = 1
		neig = eivecs.shape[1]
		tp = True
	elif eivecs.shape[1] == norb * nz:  # for 2D, inverted order
		ny = 1
		neig = eivecs.shape[0]
	elif eivecs.shape == (norb, norb):  # for bulk
		ny = 1
		nz = 1
		neig = norb
		tp = True  # transposition is necessary, as in the other cases
	else:
		raise ValueError("Eigenvectors have incorrect number of components")

	# Determine whether there are observables that refer to the quantum well or its interfaces
	# If so, try to determine its layer index. If not found, raise a warning
	well_obs = ["zif", "z_if"] + ["zif2", "z_if2", "zif^2", "z_if^2"] + ["well"] + ["extwell", "wellext", "well_ext"]
	well_obs_present = [o for o in well_obs if o in obs]
	if len(well_obs_present) > 0:
		global jwell_warning_issued
		jwell = params.layerstack.layer_index("well")

		if jwell is None and not jwell_warning_issued:
			sys.stderr.write("Warning: The well layer could not be identified. The requested observables %s have been set to 0.\n" % ", ".join(well_obs_present))
			jwell_warning_issued = True

	# Process observables
	nobs = len(obs)
	obsvals = np.zeros((nobs, neig), dtype = complex)
	obs_error = []
	for i in range(0, nobs):
		if obs[i] in all_observables:
			o = all_observables[obs[i]]
			# print ("OBS", o.obsid, o.obsfun, o.obsfun_type)
			if o.obsfun_type == 'none' or o.obsfun is None:
				obsvals[i, :] = float("nan")
			elif o.obsfun_type == 'mat':
				op = o.obsfun(nz, ny, norb)
				for j in range(0, neig):
					v = eivecs[:, j] if tp else eivecs[j]
					norm2 = np.real(np.vdot(v, v))
					obsval = np.vdot(v, op.dot(v))
					obsvals[i, j] = obsval / norm2
			elif o.obsfun_type == 'mat_indexed':
				idx = get_index_from_obs_string(obs[i])
				op = o.obsfun(nz, ny, norb, idx)
				for j in range(0, neig):
					v = eivecs[:, j] if tp else eivecs[j]
					norm2 = np.real(np.vdot(v, v))
					obsval = np.vdot(v, op.dot(v))
					obsvals[i, j] = obsval / norm2
			elif o.obsfun_type == 'params':
				op = o.obsfun(nz, ny, params)
				for j in range(0, neig):
					v = eivecs[:, j] if tp else eivecs[j]
					norm2 = np.real(np.vdot(v, v))
					obsval = np.vdot(v, op.dot(v))
					obsvals[i, j] = obsval / norm2
			elif o.obsfun_type == 'params_indexed':
				idx = get_index_from_obs_string(obs[i])
				op = o.obsfun(nz, ny, params, idx)
				for j in range(0, neig):
					v = eivecs[:, j] if tp else eivecs[j]
					norm2 = np.real(np.vdot(v, v))
					obsval = np.vdot(v, op.dot(v))
					obsvals[i, j] = obsval / norm2
			elif o.obsfun_type == 'params_magn':
				op = o.obsfun(nz, ny, params, magn = magn)
				for j in range(0, neig):
					v = eivecs[:, j] if tp else eivecs[j]
					norm2 = np.real(np.vdot(v, v))
					obsval = np.vdot(v, op.dot(v))
					obsvals[i, j] = obsval / norm2
			elif o.obsfun_type == 'eivec':
				for j in range(0, neig):
					obsvals[i, j] = o.obsfun(eivecs[:, j] if tp else eivecs[j], nz, ny, norb)
			elif o.obsfun_type == 'kwds':
				obsvals[i, :] = np.array(o.obsfun(nz, ny, llindex = llindex))
			else:
				obs_error.append(obs[i])
		elif overlap_eivec is not None and obs[i] in overlap_eivec:
			# overlap with labeled eigenvector
			w = overlap_eivec[obs[i]]
			normw2 = np.real(np.vdot(w, w))
			for j in range(0, neig):
				v = eivecs[:, j] if tp else eivecs[j]
				normv2 = np.real(np.vdot(v, v))
				if len(w) == nz * norb and ny > 1:
					obsvals[i, j] = 0
					size = nz * norb
					for m in range(0, ny):
						overlap = np.vdot(w, v[m * size: (m+1) * size])
						obsvals[i, j] += np.abs(overlap) ** 2 / normv2 / normw2
				else:
					overlap = np.vdot(w, v)
					obsvals[i, j] = np.abs(overlap) ** 2 / normv2 / normw2
		else:
			obs_error.append(obs[i])
	if len(obs_error) > 0 and not obs_error_issued:
		sys.stderr.write("ERROR (observables): Observables %s could not be calculated.\n" % (", ".join(obs_error)))
		obs_error_issued = True
	return obsvals

def regularize_observable(eival1, eival2, obsval1, obsval2):
	""""Regularize" observable values
	If the observable value suddenly jumps, 'cross over' the eigenvalues and
	observable values if this seems more plausible froma physical perspective.
	The algorithm uses successive linear extrapolation to predict the next value
	of the observable and then selects the actual value that lies closest to it.

	Note:
	Originally, this function was designed for the Berry curvature and
	generalized later.

	Arguments:
	eival1, eival2    One-dimensional arrays. Eigenvalues (as function of
	                  momentum, for example).
	obsval1, obsval2  One-dimensional arrays. Observable values (as function of
	                  momentum, for example).

	Returns:
	eival1new, eival2new    One-dimensional arrays with 'crossed-over'
	                        eigenvalues.
	obsval1new, obsval2new  One-dimensional arrays with 'crossed-over'
	                        observable values.
	"""
	if len(eival1) != len(eival2) or len(obsval1) != len(obsval2) or len(eival1) != len(obsval1):
		raise ValueError("All inputs must have the same length")

	l = len(obsval1)
	if l <= 2:
		return eival1, eival2, obsval1, obsval2

	eival1new = [eival1[0], eival1[1]]
	eival2new = [eival2[0], eival2[1]]
	obsval1new = [obsval1[0], obsval1[1]]
	obsval2new = [obsval2[0], obsval2[1]]

	for j in range(2, l):
		# predict new values
		obsval1pre = 2 * obsval1new[-1] - obsval1new[-2]
		obsval2pre = 2 * obsval2new[-1] - obsval2new[-2]
		diff_11_22 = abs(obsval1pre - obsval1[j]) + abs(obsval2pre - obsval2[j])
		diff_12_21 = abs(obsval1pre - obsval2[j]) + abs(obsval2pre - obsval1[j])
		if diff_11_22 <= diff_12_21:
			eival1new.append(eival1[j])
			eival2new.append(eival2[j])
			obsval1new.append(obsval1[j])
			obsval2new.append(obsval2[j])
		else:
			eival1new.append(eival2[j])
			eival2new.append(eival1[j])
			obsval1new.append(obsval2[j])
			obsval2new.append(obsval1[j])

	if isinstance(eival1, np.ndarray):
		return np.array(eival1new), np.array(eival2new), np.array(obsval1new), np.array(obsval2new)
	else:
		return eival1new, eival2new, obsval1new, obsval2new

def get_all_obsids(kdim=0, ll=False, norb=8, opts=None):
	"""Give all obsids for a given dimension and number of orbitals
	These are the observables that should be calculated and those which end up
	in the output files.

	Arguments:
	kdim    1, 2, or 3. The dimensionality (number of momentum directions).
	ll      True or False. Whether or not a Landau level calculation.
	norb    6 or 8. The number of orbitals in the model
	opts    Dict or None. General options (from the command line).

	Returns:
	obsids  List of strings.
	"""
	if opts is None:
		opts = {}
	if kdim == 3 and not ll:  # bulk
		obsids = ["jz", "jx", "jy", "sz", "sx", "sy", "split", "orbital", "gamma6",
			"gamma8", "gamma8h", "gamma8l", "gamma7", "jz6", "jz8", "jz7", "isopz",
			"hex", "hz"]
	elif kdim == 2 and not ll:  # 2d
		obsids = ["jz", "jx", "jy", "sz", "sx", "sy", "split", "orbital",
			"gamma6", "gamma8", "gamma8h", "gamma8l", "gamma7", "jz6", "jz8", "jz7",
			"z", "z2", "zif", "zif2", "well", "wellext", "interface", "interfacechar",
			"interface10nm", "interfacechar10nm", "iprz", "pz", "isopz", "isopx",
			"isopy", "isopzw", "isopzs", "hex", "hex1t", "hexinf", "hz", "hz1t"]
	elif kdim == 1 and not ll:  # 1d
		obsids = ["y", "y2", "yjz", "jz", "jx", "jy", "sz", "sx", "sy", "split",
			"orbital", "gamma6", "gamma8", "gamma8h", "gamma8l", "gamma7", "jz6",
			"jz8", "jz7", "z", "z2", "zif", "zif2", "iprz", "ipry", "ipryz",
			"pz", "isopz", "px", "isopx", "py", "isopy", "pzy", "isopzy", "hex",
			"hz"]
	elif kdim == 3 and ll:  # bulk-ll
		obsids = ["jz", "jx", "jy", "sz", "sx", "sy", "split", "orbital",
			"gamma6", "gamma8", "gamma8h", "gamma8l", "gamma7", "jz6", "jz8",
			"jz7", "hex", "hz"]
	elif kdim == 2 and ll:  # ll
		obsids = ["jz", "jx", "jy", "sz", "sx", "sy", "split", "orbital",
			"gamma6", "gamma8", "gamma8h", "gamma8l", "gamma7", "jz6",
			"jz8", "jz7", "z", "z2", "zif", "zif2", "well", "wellext",
			"interface", "interfacechar", "interface10nm", "interfacechar10nm",
			"iprz", "pz", "isopz", "hex", "hz"]
	else:
		raise ValueError("Invalid combination of arguments kdim and ll")
	if norb == 6:
		obsids = [oi for oi in obsids if not oi.endswith('7')]

	# Orbital-specific observables
	# TODO: Can the condition be relaxed?
	if opts.get('orbitalobs') and kdim in [1, 2] and not ll:
		obsids.extend(['orbital[%i]' % (j + 1) for j in range(0, norb)])

	# Custom interface length
	# TODO: Can the condition be relaxed?
	if opts.get('custom_interface_length') is not None and kdim in [1, 2] and not ll:
		obsids.extend(["custominterface[%i]" % opts['custom_interface_length'],
		               "custominterfacechar[%i]" % opts['custom_interface_length']])

	return obsids

def plotobs_apply_llmode(plotopts, ll_mode = None):
	"""Set plot observable automatically based on LL mode

	Arguments:
	plotopts  Dict instance with plot options. Note: The instance may be
	          modified if ll_mode is set.
	ll_mode   String. The LL mode.

	Returns:
	plotobs   String or None. The plot observable.
	"""
	if plotopts.get('obs') is None:
		return None
	elif ll_mode is None:
		return plotopts['obs']
	if '.' in plotopts['obs']:
		obs_split = plotopts['obs'].split('.')
		obs1, obs2 = obs_split[0], '.'.join(obs_split[1:])
	else:
		obs1, obs2 = plotopts['obs'], None
	if ll_mode == 'full' and obs1 in ['llindex', 'll_n', 'lln']:
		sys.stderr.write(f"Warning (plotobs_apply_llmode): Observable '{obs1}' cannot be used in 'full' LL mode. Use observable 'llavg' instead.\n")
		plotopts['obs'] = 'llavg' if obs2 is None else 'llavg' + '.' + obs2
	if ll_mode != 'full' and obs1 in ['llavg', 'llmax', 'llbymax']:
		sys.stderr.write(f"Warning (plotobs_apply_llmode): Observable '{obs1}' cannot be used in '{ll_mode}' LL mode. Use observable 'llindex' instead.\n")
		plotopts['obs'] = 'llindex' if obs2 is None else 'llindex' + '.' + obs2
	return plotopts['obs']
