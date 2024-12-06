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

from math import sqrt, ceil, tanh, pi
import sys
import numpy as np

from .physconst import kB, muB, eoverhbar
from .materials import Material
from .layerstack import LayerStack, default_layer_names
from .latticetrans import lattice_transform
from .strain import lattice_const_from_strain, strain_epsilondiag, strain_automatic

### GENERAL FUNCTIONS

def material_param(layer_material, substrate_material, a_lattice = None, strain = None, angle = 0.0, hide_strain_warning = False):
	"""Calculate and store derived material parameters

	Arguments:
	layer_material       Material instance
	substrate_material   Material instance or None.
	a_lattice            Number or None. The lattice constant of the strained
	                     material.
	angle                Number. For a strip in a non-trivial orientation, the
	                     angle between the longitudinal direction and the
	                     crystal direction a.
	hide_strain_warning  True or False. If True, hide the warning issued when
	                     lattice constant and substrate material are both given
	                     explicitly.

	Return:
	A dict instance with the parameters of the layer material, appropriately
	amended with the strain(ed) values.
	"""
	if not isinstance(layer_material, Material):
		raise ValueError("layer_material must be a Material instance")
	if substrate_material is not None and not isinstance(substrate_material, Material):
		raise ValueError("substrate_material must be None or a Material instance")

	mparam = layer_material.param.copy()
	mparam['material'] = layer_material
	# mparam['compound'] = layer_material.name
	mparam['aFree'] = 1. * layer_material['a']
	if 'a' in mparam:
		del mparam['a']
	
	mparam['epsilonxx'], mparam['epsilonyy'], mparam['epsilonzz'] = strain_epsilondiag(layer_material, substrate_material, strain = strain, a_lattice = a_lattice, hide_strain_warning = hide_strain_warning)
	mparam['epsilonyz'], mparam['epsilonxz'], mparam['epsilonxy'] = 0.0, 0.0, 0.0   # for now, no off-diagonal strain
	mparam['epsilon_par'] = (mparam['epsilonxx'] + mparam['epsilonyy']) / 2
	return mparam




### EXCHANGE COUPLING ###

def brillouin52(x):
	"""Brillouin function with an approximation near x = 0.
	The approximation is better than the numerical noise (~1e-11) for |x| < 1e-5
	A series expansion would be:
	  B_{5/2}(x) ~ (7/15)x - (259/5625)x^3 + (2666/421875)x^5 - (47989/52734375)x^7 + ...
	The radius of convergence of this expansion is R = (5/6) pi ~ 2.6.
	"""
	return x * 7 / 15 if (abs(x) < 1e-5) else (6 / 5) / tanh(x * 6 / 5) - (1 / 5) / tanh(x * 1 / 5)

def Aexchange(magn, temperature, g=0.0, TK0=0.0):
	"""Aexchange / nbeta as function of magnetic field and temperature"""
	if g == 0.0:
		return 0.0
	elif isinstance(magn, (float, np.floating, int, np.integer)):
		return (-1 / 6) * (-5 / 2) * brillouin52( (5 / 2) * g * muB * magn / kB / (temperature + TK0) )
	elif isinstance(magn, tuple) and len(magn) == 3:
		bb = np.sqrt(magn[0]**2 + magn[1]**2 + magn[2]**2)
		if bb == 0.0:
			return 0.0, 0.0, 0.0
		else:
			Aexabs = (-1 / 6) * (-5 / 2) * brillouin52( (5 / 2) * g * muB * bb / kB / (temperature + TK0) )
			return Aexabs * magn[0] / bb, Aexabs * magn[1] / bb, Aexabs * magn[2] / bb
	else:
		raise TypeError("Input must be float or 3-tuple")

### PhysParams CLASS ###

class PhysParams:
	"""Container class for physical parameters.
	The parameters may be returned as a function of z.

	Attributes (arguments):
	kdim
	norbitals
	zres
	yres
	linterface
	ly_width (width)
	yconfinement
	strain_direction
	strip_angle (strip_direction)
	magn
	temperature
	substrate_material
	a_lattice
	- (rel_strain)
	- (strain_angle)
	- (layer_types)
	layer_material (m_layers)
	layer_stack
	cache_param
	cache_z
	lz_thick
	nz
	zInterface
	nlayer
	c_dz, c_dz2
	c_dy, c_dy2
	ny
	ymid
	ninterface
	dzinterface
	"""
	def __init__(
		self, kdim = None, l_layers = None, m_layers = None, layer_types = None,
		layer_density = None, zres = None, linterface = None, width = None,
		yres = None, magn = None, temperature = None, yconfinement = None,
		substrate_material = None,	strain_direction = None, a_lattice = None,
		rel_strain = None, norbitals = None, lattice_orientation = None,
		matdef_renorm = True, hide_yconfinement_warning = False,
		hide_strain_warning = False):
		# Default values (l_layers, m_layers)
		if l_layers is None:
			l_layers = []
		if m_layers is None:
			m_layers = []

		# Number of k dimensions
		if kdim in [1, 2, 3]:
			self.kdim = kdim
		else:
			sys.stderr.write("ERROR: The number of momentum dimensions must be 1, 2, or 3.\n")
			exit(1)

		# Number of orbitals
		if norbitals is None:
			self.norbitals = 6
		elif norbitals in [6, 8]:
			self.norbitals = norbitals
		else:
			sys.stderr.write("ERROR: The number of orbitals must be either 6 or 8.\n")
			exit(1)

		# Resolution (discretization of the derivatives)
		if zres is None and kdim <= 2:
			sys.stderr.write("ERROR: Resolution zres is required explicitly for 1D and 2D.\n")
			exit(1)
		elif zres is None:
			zres = 0.25  # resolution in z direction -- default value for kdim >= 3
		if zres <= 0.0:
			sys.stderr.write("ERROR: Resolution zres must be positive\n")
			exit(1)
		self.zres = zres

		if yres is None and kdim <= 1:
			sys.stderr.write("ERROR: Resolution yres is required explicitly for 1D.\n")
			exit(1)
		elif yres is None:
			yres = 0.25  # resolution in y direction -- default value for kdim >= 2
		if yres <= 0.0:
			sys.stderr.write("ERROR: Resolution yres must be positive\n")
			exit(1)
		self.yres = yres

		# Interface thickness
		if linterface is None:
			linterface = 0.075  # nm -- default value
		if linterface <= 0.0 or linterface > 10.0:
			sys.stderr.write("ERROR: Interface thickness out of range\n")
			exit(1)
		self.linterface = linterface

		# Width (y dimension) of the sample
		if width is None and kdim <= 1:
			sys.stderr.write("ERROR: Sample width is required explicitly for 1D.\n")
			exit(1)
		elif width is None:
			width = 1.0    # width -- default value for kdim >= 2
		if width < 0.0:
			sys.stderr.write("ERROR: Sample width must be positive\n")
			exit(1)
		self.ly_width = width

		# Confinement potential in y direction
		if yconfinement is None:
			yconfinement = 1e5
		if self.kdim >= 2:
			self.yconfinement = 0
		elif yconfinement < 0:
			sys.stderr.write("ERROR: Confinement in y direction should not be negative.\n")
			exit(1)
		elif yconfinement == 0:
			if not hide_yconfinement_warning:
				sys.stderr.write("Warning: No confinement in y direction is not recommended. Choose a value >= 50000 meV.\n")
		elif yconfinement <= 1000:
			if not hide_yconfinement_warning:
				sys.stderr.write("Warning: Confinement in y direction < 50000 meV can lead to strange results. Did you mean %s meV?\n" % (1000 * yconfinement))
		elif yconfinement < 5e4:
			if not hide_yconfinement_warning:
				sys.stderr.write("Warning: Confinement in y direction < 50000 meV can lead to strange results.\n")
		elif yconfinement > 1e6:
			sys.stderr.write("ERROR: Confinement in y direction exceeds maximum 10^6 meV.\n")
			exit(1)
		self.yconfinement = yconfinement

		# Strain
		if strain_direction is not None:
			sys.stderr.write("Warning: Argument strain_direction is deprecated, and is ignored. In order to replicate the behaviour for strain axis other than z, use 'strain' with the appropriate numerical inputs.\n")
		if isinstance(rel_strain, tuple) and len(rel_strain) == 3:
			rel_strain = strain_automatic(rel_strain)

		# Orientation
		self.lattice_orientation = None
		self.lattice_trans = None
		if isinstance(lattice_orientation, (int, np.integer, float, np.floating)):
			self.lattice_orientation = [lattice_orientation]
			self.lattice_trans = [lattice_orientation]
		elif isinstance(lattice_orientation, tuple) and len(lattice_orientation) == 3 and all([isinstance(x, int) for x in lattice_orientation]):
			if lattice_orientation[2] != 0:
				sys.stderr.write("ERROR: Third component of the strip direction must be 0.\n")
				exit(1)
			if lattice_orientation[0] == 0 and lattice_orientation[1] == 0:
				sys.stderr.write("ERROR: Strip direction must not be (0,0,0).\n")
				exit(1)
			self.lattice_orientation = [lattice_orientation]
			self.lattice_trans = np.arctan2(lattice_orientation[1], lattice_orientation[0]) * 180 / np.pi
		else:
			try:
				self.lattice_trans = lattice_transform(lattice_orientation)
			except:
				sys.stderr.write("ERROR: Not a valid lattice transformation.\n")
				raise
			self.lattice_orientation = lattice_orientation
		if isinstance(self.lattice_trans, (int, np.integer, float, np.floating)) and np.abs(self.lattice_trans) > 1e-6 and kdim != 1:
			sys.stderr.write("Warning: Strip direction is irrelevant for momentum dimension %i.\n" % kdim)
			self.lattice_trans = None
		if 'verbose' in sys.argv:
			str_matrix = " (matrix)" if self.lattice_transformed_by_matrix() else ""
			str_angle = " (angle)" if self.lattice_transformed_by_angle() else ""
			print(f"Lattice transformation{str_matrix}{str_angle}:")
			print(self.lattice_orientation)
			print(self.lattice_trans)

		### EXTERNAL ENVIRONMENT
		if magn is None:
			magn = 0.0    # Magnetic field in T -- default value
		self.magn = magn

		if temperature is None:
			temperature = 0.0   # Temperature in K -- default value
		if temperature < 0.0:
			sys.stderr.write("ERROR: Temperature must be positive\n")
			exit(1)
		self.temperature = temperature

		## LAYER STACK, MATERIAL PARAMETERS ##

		# Layer types/names
		if layer_types is None:
			lnames = None
		elif isinstance(layer_types, str):
			lnames1 = []
			for l in layer_types.lower():
				if l not in default_layer_names:
					sys.stderr.write("ERROR: Invalid layer type '%s'.\n" % l)
					exit(1)
				lnames1.append(default_layer_names[l])
			lnames = []
			for j, l in enumerate(lnames1):
				if lnames1.count(l) == 1:
					lnames.append(l)
				else:
					c = lnames1[:j].count(l) + 1
					lnames.append(l + ("%i" % c))
		else:  # TODO: list
			raise TypeError("Argument layer_types must be a string or None.")
		if lnames is not None and len(lnames) != len(m_layers):
			sys.stderr.write("ERROR: List of layer names has incorrect length.\n")
			exit(1)

		# Lattice parameter (set by substrate)
		self.substrate_material = substrate_material
		ref_layer_index = None
		if rel_strain == 'none':
			if a_lattice is not None:
				sys.stderr.write("Warning: Strain is ignored, so 'a_lattice' does not have an effect.\n")
			a_lattice = None
			self.a_lattice = 0.65
		elif a_lattice is None and rel_strain is None:
			if substrate_material is None:
				sys.stderr.write("ERROR: For determination of strain, one of the following three arguments is required:\n\'msubst\' (substrate material), \'a_lattice\' (lattice constant), or \'strain\' (relative strain).\n")
				exit(1)
			else:
				self.a_lattice = self.substrate_material['a']
		elif a_lattice is not None and rel_strain is None:
			self.a_lattice = a_lattice
		elif a_lattice is None and rel_strain is not None:
			# The reference material is the well layer:
			# second layer if 2 or 3 layers, first if 1 layer, otherwise raise an error
			if lnames is not None:
				if 'well' in lnames:
					ref_layer_index = lnames.index('well')
				else:
					sys.stderr.write("ERROR: Layer names are given, but the 'well' could not be identified uniquely.\n")  # Second error message will follow below
			elif len(m_layers) <= 3:
				ref_layer_index = 0 if len(m_layers) == 1 else 1
			if ref_layer_index is None:
				sys.stderr.write("ERROR: Cannot determine the well layer for calculation of lattice constant from relative strain.\nPlease input strain using \'a_lattice\' or \'msubst\'.\n")
				exit(1)
			m_ref = m_layers[ref_layer_index]
			a_lattice = lattice_const_from_strain(rel_strain, m_ref)
			self.a_lattice = a_lattice
		else:
			sys.stderr.write("Warning: Relative strain is ignored if lattice constant is given.\n")
			self.a_lattice = a_lattice

		# Material parameters
		strain_angle = self.lattice_trans if kdim == 1 and isinstance(self.lattice_trans, (int, np.integer, float, np.floating)) and np.abs(self.lattice_trans) > 1e-6 else 0.0
		m_param = []
		for j, mat in enumerate(m_layers):
			strain_arg = rel_strain if j == ref_layer_index or rel_strain == 'none' else None
			m_param.append(material_param(mat, self.substrate_material, a_lattice = a_lattice, strain = strain_arg, angle = strain_angle, hide_strain_warning = hide_strain_warning))
		self.layer_material = m_layers  # this is not stored in the LayerStack instance, so save it here

		# Layer data
		self.layerstack = LayerStack(tuple(m_param), l_layers, zres = self.zres, names = lnames)
		if matdef_renorm:
			self.layerstack.renormalize_to(norbitals)
		elif norbitals != self.layerstack.matdef_orbitals:
			sys.stderr.write("Warning: Using parameters for %i-orbital model in %i-orbital model without renormalization.\n" % (self.layerstack.matdef_orbitals, norbitals))
		self.cache_param = None
		self.cache_z = None
		if layer_density is not None and layer_density != []:
			self.layerstack.set_density(layer_density)

		# Geometry (z dimension)
		self.lz_thick = self.layerstack.lz_thick      # Total thickness (nm)
		self.nz = self.layerstack.nz                  # Lattice points
		self.zinterface = self.layerstack.zinterface  # Interfaces (z coordinates in lattice points
		self.nlayer = self.layerstack.nlayer          # Number of layers

		## OTHER DERIVED QUANTITIES ##

		## Coefficients of discretisation of derivatives
		self.c_dz = -1.j / (2 * self.zres)
		self.c_dz2 = -1. / (self.zres**2)
		self.c_dy = -1.j / (2 * self.yres)
		self.c_dy2 = -1. / (self.yres**2)

		# Lattice points (y dimension)
		self.ny = int(ceil(self.ly_width / self.yres - 1e-10))  # small offset to avoid rounding errors

		# Center in y dimension
		self.ymid = (self.ny - 1) / 2.

		# Interface (width)
		self.ninterface = int(ceil(self.linterface / self.zres)) + 1
		self.dzinterface = self.linterface / self.zres

		# Exchange coupling
		self.has_exchange = self.layerstack.has_exchange()

	def to_dict(self, material_format = 'sub'):
		"""Return a dict composed of the class's attributes."""
		paramdict = {
			'norbitals': self.norbitals,
			'norb': self.norbitals,
			'zres': self.zres,
			'yres': self.yres,
			'linterface': self.linterface,
			'zinterface': self.zinterface,
			'ninterface': self.ninterface,
			'nzinterface': self.ninterface,
			'dzinterface': self.dzinterface,
			'yconfinement': self.yconfinement,
			'a': self.a_lattice,
			'b': self.magn,
			'magn': self.magn,
			't': self.temperature,
			'temp': self.temperature,
			'l': self.lz_thick,
			'd': self.lz_thick,
			'thickness': self.lz_thick,
			'w': self.ly_width,
			'width': self.ly_width,
			'ny': self.ny,
			'nz': self.nz,
			'nlayer': self.nlayer,
			'ymid': self.ymid,
		}
		if isinstance(self.substrate_material, Material):
			paramdict['msubst'] = self.substrate_material.format(fmt = material_format)
		elif isinstance(self.substrate_material, str):
			paramdict['msubst'] = self.substrate_material
		# Layerstack variables:
		for i in range(0, self.layerstack.nlayer):
			paramdict['layername(%i)' % (i+1)] = self.layerstack.names[i]
			paramdict['lname(%i)' % (i+1)] = self.layerstack.names[i]
			paramdict['layernz(%i)' % (i+1)] = self.layerstack.thicknesses_n[i]
			paramdict['nzlayer(%i)' % (i+1)] = self.layerstack.thicknesses_n[i]
			paramdict['layerl(%i)' % (i+1)] = self.layerstack.thicknesses_z[i]
			paramdict['llayer(%i)' % (i+1)] = self.layerstack.thicknesses_z[i]
			paramdict['dlayer(%i)' % (i+1)] = self.layerstack.thicknesses_z[i]
			paramdict['layermater(%i)' % (i+1)] = self.layer_material[i].format(fmt = material_format)
			paramdict['mlayer(%i)' % (i+1)] = self.layer_material[i].format(fmt = material_format)
			paramdict['nzminlayer(%i)' % (i+1)] = self.layerstack.zinterface[i]
			paramdict['nzmaxlayer(%i)' % (i+1)] = self.layerstack.zinterface[i + 1]
			paramdict['zminlayer(%i)' % (i+1)] = self.layerstack.zinterface_nm[i]
			paramdict['zmaxlayer(%i)' % (i+1)] = self.layerstack.zinterface_nm[i + 1]
		return paramdict

	def diff(self, other):
		"""For a pair of PhysParams instances, find their differences

		Arguments:
		other   PhysParams instance

		Returns:
		A dict instance. The keys are where the two parameter dicts (obtained by
		method to_dict()) differ. The values are 2-tuples of the values. If the
		key is missing in one of the PhysParams instances, then the
		corresponding member of the tuple is None.
		"""
		params_dict1 = self.to_dict()
		params_dict2 = other.to_dict()
		diff_dict = {}
		for p in params_dict1:
			if p not in params_dict2:
				diff_dict[p] = (params_dict1[p], None)
			elif params_dict1[p] != params_dict2[p]:
				diff_dict[p] = (params_dict1[p], params_dict2[p])
		for p in params_dict2:
			if p not in params_dict1:
				diff_dict[p] = (None, params_dict2[p])
		return diff_dict

	def print_diff(self, arg, style = None):
		"""Print differences between a pair of PhysParams instances.

		Arguments:
		arg     PhysParams or dict instance. If a PhysParams instance, find the
		        difference between the two by using self.diff(arg). If a dict
		        instance, it should be the result of a 'diff' between PhysParams
		        instances, i.e., the values should be 2-tuples.
		style   Determines the format. Possible values are None or 'full',
		        'table' or 'align', 'short' or 'summary'.

		No return value.
		"""
		if isinstance(arg, PhysParams):
			diff = self.diff(arg)
		elif isinstance(arg, dict):
			diff = arg
		else:
			raise TypeError("Argument must be another PhysParams instance or a dict instance [from diff()]")
		if style is None or style == "full":
			for p in sorted(diff):
				print("  %s: %s vs %s" % (p, diff[p][0], diff[p][1]))
			print()
		if style == "table" or style == "align":
			l0, l1, l2 = 0, 0, 0
			for p in diff:
				l0 = max(l0, len(p))
				l1 = max(l1, len(str(diff[p][0])))
				l2 = max(l2, len(str(diff[p][1])))
			fmt = "  %%-%is: %%-%is vs %%-%is" % (l0, l1, l2)
			for p in sorted(diff):
				print(fmt % (p, diff[p][0], diff[p][1]))
			print()
		elif style == "short" or style == "summary":
			print(", ".join(sorted(diff.keys())))

	def check_equal(self, arg, ignore = None):
		"""Check whether two PhysParams instances are equal

		Arguments:
		arg     PhysParams or dict instance. If a PhysParams instance, find the
		        difference between the two by using self.diff(arg). If a dict
		        instance, it should be the result of a 'diff' between PhysParams
		        instances, i.e., the values should be 2-tuples.
		ignore  A list of keys whose values should not be compared.

		Returns:
		False if the 'param dict' of the PhysParams instances have differences,
		otherwise True.
		"""
		if isinstance(arg, PhysParams):
			diff = self.diff(arg)
		elif isinstance(arg, dict):
			diff = arg
		else:
			raise TypeError("Argument must be another PhysParams instance or a dict instance [from diff()]")
		if ignore is None:
			ignore = []  # default value
		for p in diff:
			if p not in ignore:
				return False
		return True

	def lattice_transformed(self):
		"""Check whether the lattice transformation is set"""
		return self.lattice_orientation is not None

	def lattice_transformed_by_matrix(self):
		"""Check whether the lattice transformation is set and is defined as a matrix"""
		return (self.lattice_orientation is not None) and isinstance(self.lattice_trans, np.ndarray)

	def lattice_transformed_by_angle(self):
		"""Check whether the lattice transformation is set and is defined as an angle"""
		return isinstance(self.lattice_orientation, list) and len(self.lattice_orientation) == 1 and isinstance(self.lattice_orientation[0], (float, np.floating, int, np.integer))

	def make_param_cache(self):
		"""Cache z dependence of parameters"""
		self.cache_z = -0.5 + 0.5 * np.arange(2 * self.nz + 1)
		self.cache_param = self.layerstack.make_param_cache(self.cache_z, dz = 1.0, delta_if = self.dzinterface, nm = False, extend = True)

	def clear_param_cache(self):
		"""Clear cached z dependence of parameters"""
		self.cache_z = None
		self.cache_param = None
		# print ("Cleared parameter cache")

	def z(self, z):
		"""Calculate and cache z dependence of parameters.

		Argument:
		z     None, integer, float, or array. If None, return value at centre of
		      range. If integer, return value at z'th position. If float, return
		      value at z'th position; this is especially useful for half-integer
		      values. If array (or list, etc.), return values at all positions
		      in array.

		Note:
		The lattice points are numbered 0, ..., nz-1. Note that the z dependence
		is also calculated at 0.5, 1.5, ...

		Performance warning:
		Calling this function for single numbers z is relatively slow. If one
		needs to iterate over many values, use an array input for z

		Returns:
		A dict instance. Its keys label the z-dependence parameters, its value
		is a float or an array with the parameter value(s) at z.
		"""
		if z is None:
			if self.cache_param is None:
				self.make_param_cache()
			z_idx = self.nz
			return {v: self.cache_param[v][z_idx] for v in self.cache_param}
		elif isinstance(z, (int, np.integer)):
			if self.cache_param is None:
				self.make_param_cache()
			z_idx = 2 * z + 1
			return {v: self.cache_param[v][z_idx] for v in self.cache_param}
		elif isinstance(z, (float, np.floating)) and abs(z * 2 - round(z * 2)) < 1e-9:
			if self.cache_param is None:
				self.make_param_cache()
			z_idx = int(round(2 * z + 1))
			return {v: self.cache_param[v][z_idx] for v in self.cache_param}
		else:
			# Performance warning: Avoid using single numbers z in this case.
			# For z being an array, the warning does not apply.
			return self.layerstack.param_z(z, dz = 1.0, delta_if = self.dzinterface, nm = False, extend = True)

	def zvalues_nm(self, extend = 0):
		"""Return array of z coordinates in nm

		Argument:
		extend   Integer. Add this many values to the return array. Default: 0.

		Returns:
		Numpy array of float type, of dimension 1, and of length nz + extend.
		"""
		if not isinstance(extend, int):
			raise TypeError("Argument extend must be an int instance.")
		return ((np.arange(0, self.nz + extend, dtype = float) - 0.5 * extend) / (self.nz - 1) - 0.5) * self.lz_thick
		## For extend = 0: (np.arange(0, self.nz, dtype = float) / (self.nz - 1) - 0.5) * self.lz_thick

	def interface_z_nm(self):
		"""Return array of the z coordinates in nm of the interfaces"""
		return (np.array(self.zinterface, dtype = float) / (self.nz - 1) - 0.5) * self.lz_thick

	def yvalues_nm(self, extend = 0):
		"""Return array of y coordinates in nm
		Note the slight difference to z coordinates.

		Argument:
		extend   Integer. Add this many values to the return array. Default: 0.

		Returns:
		Numpy array of float type, of dimension 1, and of length ny + extend.
		"""
		if not isinstance(extend, int):
			raise TypeError("Argument extend must be an int instance.")
		return (np.arange(0, self.ny + extend, dtype = float) + 0.5 - 0.5 * extend) * self.yres - 0.5 * self.ly_width
		## For extend = 0: return (np.arange(0, self.ny, dtype = float) + 0.5) * self.yres - 0.5 * self.ly_width

	def well_z(self, extend_nm = 0.0, strict = False):
		"""Return bottom and top z indices of the well layer

		Arguments:
		extend_nm   Float. Subtract and add this length (in nm) to the lower and
		            upper z coordinate, respectively. The actual extension is an
		            integer number of lattice points. Downward rounding is used.
		strict      True or False. If True, raise an exception if the well layer
		            is undefined or ambiguous. If False, return (None, None) in
		            that case.

		Returns:
		i_bottom  Float or None.
		i_top     Float or None.
		"""
		jwell = self.layerstack.layer_index("well")
		if jwell is None:
			if strict:
				raise ValueError("The well layer is undefined or ambiguous")
			return None, None
		i_bottom, i_top = self.zinterface[jwell], self.zinterface[jwell + 1]
		extend = int(np.floor(extend_nm / self.zres + 1e-10))
		return i_bottom - extend, i_top + extend

	def well_z_nm(self, extend_nm = 0.0, strict = False):
		"""Return bottom and top z coordinates (in nm) of the well layer

		See well_z(). Note that rounding to an integer number of lattice points
		also applies here.
		"""
		jwell = self.layerstack.layer_index("well")
		if jwell is None:
			if strict:
				raise ValueError("The well layer is undefined or ambiguous")
			return None, None
		interface_nm = self.interface_z_nm()
		z_bottom, z_top = interface_nm[jwell], interface_nm[jwell + 1]
		extend = self.zres * np.floor(extend_nm / self.zres + 1e-10)
		return z_bottom - extend, z_top + extend

	def symmetric_z(self, strict = False):
		"""Return z coordinates of largest symmetric extension of the well layer

		Arguments:
		strict      True or False. If True, raise an exception if the well layer
		            is undefined or ambiguous. If False, return (None, None) in
		            that case.

		Returns:
		z_bottom  Float or None.
		z_top     Float or None.
		"""
		z_bottom, z_top = self.well_z(strict = strict)
		if z_bottom is None or z_top is None:
			return None, None
		max_extend = min(z_bottom, self.nz - 1 - z_top)
		return z_bottom - max_extend, z_top + max_extend

### MISCELLANEOUS

def print_length_scales(params):
	"""Print length scales.

	Argument:
	params   PhysParams instance.
	"""
	magn = params.magn if isinstance(params.magn, (float, np.floating)) else params.magn.z()
	print()
	print("y resolution: %8.3f nm" % params.yres)
	lB = float('inf') if magn == 0.0 else 1. / sqrt(eoverhbar * abs(magn))
	print("l_B         :", "   inf" if magn == 0.0 else "%8.3f nm" % lB)
	print("2 pi l_B^2  :", "   inf" if magn == 0.0 else "%8.3f nm^2" % (2. * pi / (eoverhbar * abs(magn))))
	print("y width     : %8.3f nm" % params.ly_width)
	print("flux = B*b*c: %8.3f T nm^2" % (magn * params.yres * params.a_lattice))
	print("flux / (h/e) = b * c / (2 pi lB^2)")
	flux = ((eoverhbar / 2 / pi) * magn * params.yres * params.a_lattice)
	if flux > 1e-1:
		print("            : %8.3f" % flux)
	else:
		print("            : %8.3f * 10^-3" % (flux * 1000))

	if magn > 0.0 and params.yres > lB / 4.:
		sys.stderr.write("Warning: y resolution is coarse compared to magnetic length\n")
	if params.ly_width < 4 * lB:
		sys.stderr.write("Warning: Width is small compared to magnetic length\n")
	print()
