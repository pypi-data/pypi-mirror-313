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
import os
import numpy as np
import sys

from .physconst import eovereps0
from .potentialbc import eval_boundary_conditions
from .integrate import integrate_arr, special_diff
from .config import get_config

### AUXILIARY FUNCTIONS ###


def vector_norm(arr, norm = 'max'):
	"""Apply array/vector norm according to given norm type"""
	if norm == 'max':
		return np.amax(np.abs(arr))
	elif norm == 'rms':
		return np.sqrt(np.mean(arr**2))
	else:
		raise ValueError("Invalid value for argument norm")

def symmetrized_distance(arr, center, norm = 'max'):
	"""Difference of array and its symmetrized version according to given norm type"""
	symm_arr = symmetrize_array(arr, center)
	return vector_norm(symm_arr - arr, norm)

def antisymmetrized_distance(arr, center, norm = 'max'):
	"""Difference of array and its antisymmetrized version according to given norm type"""
	antisymm_arr = antisymmetrize_array(arr, center)
	return vector_norm(antisymm_arr - arr, norm)

def isint(x):
	"""Test is value is integer"""
	return np.round(x) == x

def symmetrize_array(arr, center = None):
	"""Symmetrize array around symmetry center.

	Arguments:
	arr      Numpy 1d-array. Array to be symmetrized.
	center   Integer. Index of symmetry center.

	Returns:
	symmetric_array   Numpy 1d-array. Symmetrized array.
	"""
	if arr.ndim != 1:
		raise ValueError("Argument arr must be a 1-dimensional array")
	size = len(arr)
	if center is None:
		center = (size - 1) / 2  # calculate result below
	if not isint(2 * center):
		raise ValueError("Argument center must be an integer value or integer + 0.5")
	if center < 0 or center > size - 1:
		raise ValueError(f"Argument center out of range for array of size {size}")

	# Find start/end index of left and right parts that compose the result
	n_left = int(np.ceil(center))
	n_right = n_left + 1 if isint(center) else n_left

	if center < (size - 1) / 2:
		symmetric_array = np.append(np.flip(arr[n_left:]), arr[n_right:])[-size:]
	elif center > (size - 1) / 2:
		symmetric_array = np.append(arr[:n_left], np.flip(arr[:n_right]))[:size]
	else:
		symmetric_array = 0.5 * (arr + arr[::-1])

	return symmetric_array


def antisymmetrize_array(arr, center = None):
	"""Antisymmetrize array around (c, arr[c]) with c as symmetry center.

	Arguments:
	arr      Numpy 1d-array. Array to be antisymmetrized.
	center   Integer. Index of symmetry center.

	Returns:
	antisymmetric_array   Numpy 1d-array. Antisymmetrized array.
	"""
	if arr.ndim != 1:
		raise ValueError("Argument arr must be a 1-dimensional array")
	size = len(arr)
	if center is None:
		center = (size - 1) / 2  # calculate result below
	if not isint(2 * center):
		raise ValueError("Argument center must be an integer value or integer + 0.5")
	if center < 0 or center > size - 1:
		raise ValueError(f"Argument center out of range for array of size {size}")

	# Find start/end index of left and right parts that compose the result
	n_left = int(np.ceil(center))
	n_right = n_left + 1 if isint(center) else n_left

	# Get offset (central value) and shift offset to zero
	offset = arr[n_left] if isint(center) else (arr[n_left - 1] + arr[n_left]) / 2
	arr_shift = arr - offset

	# Antisymmetrize accordingly; mind possibly offsets in antisymmetric "function"
	if center < (size - 1) / 2:
		antisymmetric_array = np.append(-np.flip(arr_shift[n_left:]), arr_shift[n_right:])[-size:]
	elif center > (size - 1) / 2:
		antisymmetric_array = np.append(arr_shift[:n_left], -np.flip(arr_shift[:n_right]))[:size]
	else:
		antisymmetric_array = 0.5 * (arr_shift - arr_shift[::-1])

	# Re-apply (i.e., add) offset to the result
	antisymmetric_array += offset

	return antisymmetric_array


def auto_symmetrize(arr, center, threshold = 1e-12, verbose = False):
	"""Symmetrize or antisymmetrize array if the result is sufficiently close to the original

	Arguments:
	arr         Numpy 1d-array. Array which will be checked for symmetry and
	            (anti-)symmetrized.
	center      Integer or float, being integer-valued or integer + 0.5. Index
	            of symmetry center.
	threshold   Float. Maximum distance between the (anti-)symmetrized array and
	            the original. If the actual distance is lower than threshold,
	            return the (anti-)symmetrized array, otherwise return the
	            original.
	verbose     True or False. If True, print what the function does.

	Returns:
	arr_new     Numpy 1d-array. (Anti-)symmetrized array or input array
                depending on threshold.
	"""
	if arr.ndim != 1:
		raise ValueError("Argument arr must be a 1-dimensional array")

	if symmetrized_distance(arr, center) < threshold:
		action = "Symmetrize"
		arr_new = symmetrize_array(arr, center)
	elif antisymmetrized_distance(arr, center) < threshold:
		action = "Antisymmetrize"
		arr_new = antisymmetrize_array(arr, center)
	else:
		action = "No symmetrization"
		arr_new = arr
	if verbose:
		print(action)
		print("symmetry_before     =", symmetrized_distance(arr, center))
		print("symmetry_after      =", symmetrized_distance(arr_new, center))
		print("antisymmetry_before =", antisymmetrized_distance(arr, center))
		print("antisymmetry_after  =", antisymmetrized_distance(arr_new, center))
	return arr_new


def write_to_temp_file(filename, z, vz, new = False):
	"""Write potential to temporary file (for debugging)

	Arguments:
	filename  String. Filename in the current working directory
	z         List of axis values (e.g. z/growth direction)
	vz        List of values along the axis
	new       True or False. If True, write new file, overwriting if a file
	          with the same name already exists. If False, append to an existing
	          file.

	No return value
	"""
	try:
		f = open(filename, 'w' if new else 'a')
	except:
		return
	if new and z is not None:
		f.write(', '.join(["%s" % z1 for z1 in z]) + '\n')
	f.write(', '.join(["%s" % v1 for v1 in vz]) + '\n')
	f.close()


def solve_potential(zval, densz, epsilonz, /, z1 = 0.0, z2 = 0.0, z3 = 0.0, v1 = None, v2 = None, v3 = None, v12 = None, dv1 = None, dv2 = None, dz = 1.0, verbose = False, well_center = None):
	"""Solve potential based on density and dielectric constant as function of z.
	That is, solve the potential V(z) from the Poisson equation
	   d_z [epsilon(z) d_z V(z)] = rho(z) e / epsilon0
	where epsilon(z) and rho(z) are the dielectric constant and charge density,
	respectively, as function of z. Here, d_z denotes the derivative in z.

	Arguments:
	zval        Numpy array. The z coordinates where densz and epsilonz are
	            defined.
	densz       Numpy array. The density as function of z.
	epsilonz    Numpy array. The dielectric constant epsilon as function of z.
	z1, z2, z3  Integers or floats. Indices where boundary conditions act. They
	            must be unequal.
	v1, v2, v3  Floats. Potential values at z1, z2, and z3.
	v12         Float. Difference V(z2) - V(z1).
	dv1, dv2    Floats. Derivatives of the potential at z1 or z2.
	dz          Float. The resolution of the z coordinate in nm.
	verbose     True or False. If True, print diagnostic information to stdout.
	well_center Integer. Index of center of well layer.

	Returns:
	vz          Numpy array. The potential that solves the Poisson equation.
	"""
	symmetrization_constraint = get_config('selfcon_symmetrization_constraint', choices = ['strict', 'loose', 'never'])

	if symmetrization_constraint == 'strict':
		symmetrize = True
		symmetry_center = (len(densz) - 1) / 2
	elif symmetrization_constraint == 'loose':
		symmetrize = True
		symmetry_center = well_center
	elif symmetrization_constraint == 'never':
		symmetrize = False
		symmetry_center = None  # Won't be used

	# We need to keep the density at the edges equal to 0; otherwise, the
	# integrals may not always yield the expected values.
	densz[1] += densz[0]
	densz[0] = 0.0
	densz[-2] += densz[-1]
	densz[-1] = 0.0

	if symmetrize:
		# Symmetrize input arrays, but only if they are "sufficiently" symmetric already
		if verbose:
			print('densz:', end=' ')
		densz = auto_symmetrize(densz, symmetry_center, verbose=verbose)

	int_densz = integrate_arr(densz) * dz
	if symmetrize:
		if verbose:
			print('intdensz:', end=' ')
		int_densz = auto_symmetrize(int_densz, symmetry_center, verbose=verbose)

	int_invepsilonz = integrate_arr(1. / epsilonz) * dz

	int_dens_over_epsz = integrate_arr(int_densz / epsilonz) * dz
	if symmetrize:
		if verbose:
			print('int_dens_over_epsz:', end=' ')
		int_dens_over_epsz = auto_symmetrize(int_dens_over_epsz, symmetry_center, verbose=verbose)

	if verbose:
		print("solve_potential: Every 4th point from first and last z...")
		print("int dens:")
		print(int_densz[:40:4])
		print("...")
		print(int_densz[-40::4])
		print()
		print("int 1/eps")
		print(int_invepsilonz[:40:4])
		print("...")
		print(int_invepsilonz[-40::4])
		print()
		print("int n/eps")
		print(int_dens_over_epsz[:40:4])
		print("...")
		print(int_dens_over_epsz[-40::4])
		print()

	# Extract values from arrays
	int_dens_over_eps_z1, int_dens_over_eps_z2, int_dens_over_eps_z3 = \
		np.interp([z1, z2, z3], zval, int_dens_over_epsz)
	int_invepsilon_z1, int_invepsilon_z2, int_invepsilon_z3 = \
		np.interp([z1, z2, z3], zval, int_invepsilonz)
	epsilon_z1, epsilon_z2 = np.interp([z1, z2], zval, epsilonz)
	int_dens_z1, int_dens_z2 = np.interp([z1, z2], zval, int_densz)
	int_dens_over_epsz_1_2 = int_dens_over_eps_z2 - int_dens_over_eps_z1
	int_invepsilonz_1_2 = int_invepsilon_z2 - int_invepsilon_z1

	# Define solutions
	if v1 is not None and v2 is not None:
		int_const = ((v2 - v1) - eovereps0 * int_dens_over_epsz_1_2) / int_invepsilonz_1_2
		vz = v1 + eovereps0 * (int_dens_over_epsz - int_dens_over_eps_z1) + int_const * (int_invepsilonz - int_invepsilon_z1)

	elif v12 is not None and v3 is not None:
		int_const = (v12 - eovereps0 * int_dens_over_epsz_1_2) / int_invepsilonz_1_2
		vz = v3 + eovereps0 * (int_dens_over_epsz - int_dens_over_eps_z3) + int_const * (int_invepsilonz - int_invepsilon_z3)

	elif v1 is not None and dv2 is not None:
		int_const = epsilon_z2 * dv2 - eovereps0 * int_dens_z2
		vz = v1 + eovereps0 * (int_dens_over_epsz - int_dens_over_eps_z1) + int_const * (int_invepsilonz - int_invepsilon_z1)

	elif v2 is not None and dv1 is not None:
		int_const = epsilon_z1 * dv1 - eovereps0 * int_dens_z1
		vz = v2 + eovereps0 * (int_dens_over_epsz - int_dens_over_eps_z2) + int_const * (int_invepsilonz - int_invepsilon_z2)

	elif v1 is not None and dv1 is not None:
		int_const = epsilon_z1 * dv1 - eovereps0 * int_dens_z1
		vz = v1 + eovereps0 * (int_dens_over_epsz - int_dens_over_eps_z1) + int_const * (int_invepsilonz - int_invepsilon_z1)

	elif v2 is not None and dv2 is not None:
		int_const = epsilon_z2 * dv2 - eovereps0 * int_dens_z2
		vz = v2 + eovereps0 * (int_dens_over_epsz - int_dens_over_eps_z2) + int_const * (int_invepsilonz - int_invepsilon_z2)

	else:  # we should not end up here anyway
		raise ValueError("Invalid combination of boundary conditions")

	if symmetrize:
		if verbose:
			print('vz:', end=' ')
		vz = auto_symmetrize(vz, symmetry_center, threshold=1e-10, verbose=verbose)

	return vz


def init_potential(params, cardens = None, n_depletion = None, l_depletion = None, v_outer = None, v_inner = None, efield = None, verbose = False, custom_bc = None):
	"""Initial potential for the self-consistent calculations.

	Arguments:
	params         PhysParams instance.
	cardens        Float. Initial carrier density, assumed to be uniform over
	               the z direction.
	n_depletion    Float. Density in the depletion layer.
	l_depletion    Float. Thickness of the depletion layer in nm.
	v_inner, v_outer   V_{top} - V_{bottom}; electrostatic potential; use
		               v_outer to apply the potential to the edges of the stack,
		               v_inner to apply the potential to the interfaces of the
		               well
	efield         A list/tuple length 2, where both elements are float or None.
	               Electric field at bottom and top interface. None may be used
	               as shortcut for [None, None].
	verbose     True or False. If True, print diagnostic information to stdout.

	Returns:
	cardens    Float. Carrier density consistent with the density function.
	qdensz     Numpy array. Charge density as function of z.
	qdensz_bg  Numpy array. Density of background charges as function of z.
	bc         Dict instance. The boundary conditions for the potential.
	"""
	nz = params.nz
	dz = params.zres
	zval = params.zvalues_nm()
	epsilonz = np.array([params.z(z)['diel_epsilon'] for z in range(0, nz)])   # this is quite inefficient but will do the job
	try:
		i_bottom, i_top = params.well_z(strict = True)
		z_bottom, z_top = params.well_z_nm(strict = True)
	except:
		sys.stderr.write("ERROR (init_potential): The well layer could not be identified. This is necessary for the SC Hartree calculation to proceed.\n")
		raise
	z_mid = (z_bottom + z_top) / 2  # point centered in the well

	if efield is None:
		efield = [None, None]

	# initial density (zero everywhere)
	qdensz = np.zeros(nz, dtype = float)
	qdensz_bg = params.layerstack.get_density(np.arange(0, nz))

	# handle inner or outer potential
	if v_outer is None and v_inner is None:
		v_tb, vz1, vz2 = None, zval.min(), zval.max()
	elif v_outer is not None and v_inner is None:
		v_tb, vz1, vz2 = v_outer, zval.min(), zval.max()
	elif v_outer is None and v_inner is not None:
		v_tb, vz1, vz2 = v_inner, z_bottom, z_top
	else:
		raise ValueError("At most one of arguments v_outer and v_inner may be given.")

	# boundary conditions / initial potential
	if cardens is not None:
		# initial carrier density (uniformly distributed in well layer)
		for z in range(i_bottom, i_top + 1):
			qdensz[z] += -cardens / dz / ((i_top + 1) - i_bottom)
		if efield[0] is not None and efield[1] is not None:
			sys.stderr.write("ERROR (init_potential): Input of carrier density cannot be combined with two electric-field conditions.\n")
			exit(1)
	elif n_depletion is None and np.sum(np.abs(qdensz_bg)) < 1e-10 and efield[0] is not None and efield[1] is not None:
		cardens = -(efield[1] * epsilonz[-1] - efield[0] * epsilonz[0]) / eovereps0
		for z in range(i_bottom, i_top + 1):
			qdensz[z] += -cardens / dz / ((i_top + 1) - i_bottom)
	if n_depletion is not None:
		if v_tb is not None and v_tb != 0.0:
			sys.stderr.write("ERROR (init_potential): Input of depletion layer charge and background (gate) potential cannot be combined.\n")
			exit(1)
		if l_depletion is None:
			ldep_b, ldep_t = None, None
		elif isinstance(l_depletion, (float, np.floating)):
			ldep_b, ldep_t = l_depletion, l_depletion
		elif isinstance(l_depletion, (int, np.integer)):
			ldep_b, ldep_t = l_depletion * dz, l_depletion * dz
		elif isinstance(l_depletion, (list, tuple)) and len(l_depletion) == 2:
			ldep_b, ldep_t = tuple(l_depletion)
			if isinstance(ldep_b, int):
				ldep_b *= dz
			if isinstance(ldep_t, int):
				ldep_t *= dz
		else:
			sys.stderr.write("ERROR (init_potential): The depletion layer length argument must be a number or a list/tuple of two numbers.\n")
			exit(1)

		if isinstance(n_depletion, (float, np.floating, int, np.integer)):
			ndep_b, ndep_t = 0.5 * n_depletion, 0.5 * n_depletion
		elif isinstance(n_depletion, (list, tuple)) and len(n_depletion) == 2:
			ndep_b, ndep_t = tuple(n_depletion)
		else:
			sys.stderr.write("ERROR (init_potential): The depletion layer charge argument must be a number or a list/tuple of two numbers.\n")
			exit(1)

		# Determine background charge
		if ldep_b is not None:
			nz_dep_b = max(1, int(round(ldep_b / dz)))
			i_dep_b = max(0, i_bottom - nz_dep_b)
			if verbose:
				print("B depl:", i_bottom, ldep_b, nz_dep_b, i_dep_b)
			for z in range(i_dep_b, i_bottom):
				qdensz_bg[z] += ndep_b / dz / nz_dep_b
		if ldep_t is not None:
			nz_dep_t = max(1, int(round(ldep_t / dz)))
			i_dep_t = min(nz, i_top + 1 + nz_dep_t)
			if verbose:
				print("T depl:", i_top + 1, ldep_t, nz_dep_t, i_dep_t)
			for z in range(i_top + 1, i_dep_t):
				qdensz_bg[z] += ndep_t / dz / nz_dep_t
	else:
		ndep_b, ndep_t = 0.0, 0.0

	ndep = ndep_b + ndep_t
	net_charge = (np.sum(qdensz_bg) + np.sum(qdensz)) * dz

	bc = eval_boundary_conditions(
		params, net_charge = net_charge, cardens = cardens, efield = efield,
		v_tb = v_tb, vz1 = vz1, vz2 = vz2, n_depletion = n_depletion,
		ndep = ndep, ndep_b = ndep_b, ndep_t = ndep_t
	)
	if custom_bc is not None:
		bc = bc.apply_custom(custom_bc)

	bc = bc.validate(params)

	if verbose:
		print("Boundary conditions:", bc)
		print(zval.min(), z_bottom, z_mid, z_top, zval.max())

	return cardens, qdensz, qdensz_bg, bc


def solve_densityz(zval, vz, epsilonz, z1 = 0.0, z2 = 0.0, z3 = 0.0, v1 = None, v2 = None, v3 = None, v12 = None, dv1 = None, dv2 = None, dz = 1.0, symmetrize = True, verbose = False):
	"""Solve density based on potential and dielectric constant as function of z.
	That is, determine the density rho(z) from the Poisson equation
	   d_z [epsilon(z) d_z V(z)] = rho(z) e / epsilon0
	where epsilon(z) and V(z) are the dielectric constant and potential,
	respectively, as function of z. Here, d_z denotes the derivative in z.

	The arguments z1, z2, z3; v1, v2, v3; v12; dv1, dv2 determine the boundary
	conditions, see solve_potential() for more information. Here, only dv1 and
	dv2 are relevant. The other cases are handled automatically, provided there
	are no charges at the edges of the z range.

	Arguments:
	vz          Numpy array. The potential as function of z.
	epsilonz    Numpy array. The dielectric constant epsilon as function of z.
	z1, z2, z3  Integers. Determine the boundary conditions, see above.
	v1, v2, v3, v12, dv1, dv2
	            Floats. Determine the boundary conditions, see above.
	dz          Float. The resolution of the z coordinate in nm.
	symmetrize  NOT IMPLEMENTED
	verbose     NOT IMPLEMENTED

	Returns:
	densz       Numpy array. The density as found from the Poisson equation.
	"""
	i1 = np.argmin(np.abs(zval - z1))
	i2 = np.argmin(np.abs(zval - z2))
	if np.abs(z1 - zval[i1]) > 1e-6 or np.abs(z2 - zval[i2]) > 1e-6:
		sys.stderr.write("Warning (solve_densityz): Boundary conditions do not align with lattice in z direction. The result may be inaccurate.\n")

	# Calculate dV/dz; use special_diff as inverse of basic_integration
	if dv1 is not None:
		dvz = special_diff(vz, y0 = dv1, i0 = i1) / dz
	elif dv2 is not None:
		dvz = special_diff(vz, y0 = dv2, i0 = i2) / dz
	else:
		dvz = special_diff(vz, automatic = True) / dz
	# Determine density from the Poisson equation
	densz = special_diff(epsilonz * dvz, y0 = 0.0) / dz / eovereps0
	return densz

def cardens_from_potential(vz, epsilonz, dz = 1.0):
	"""Get carrier density from potential V(z)"""
	dvz = np.gradient(vz) / dz
	z1, z2 = 0, -1  # index range; customizable for debugging
	return -(epsilonz[z2] * dvz[z2] - epsilonz[z1] * dvz[z1]) / eovereps0


### FUNCTIONS FOR CALCULATING STATIC POTENTIALS ###

def gate_potential(v_tb, params, inner = False):
	"""Simulated gate potential

	Apply a voltage difference Vg between "top" and "bottom" of the layer stack.
	The boundary condition V(z0) = 0 fixes the value uniquely; here, z0 is the
	center of the well, or the center of the full layer stack if the well layer
	could not be identified.
	Small values can be used for lifting the degeneracy between top and bottom
	states.

	Arguments:
	v_tb     Float. The potential difference in meV between "top" and "bottom".
	params   PhysParams instance.
	inner    True or False. If True, apply the potential difference between top
	         and bottom surface of the well layer. If False, apply it between
	         top and bottom of the full layer stack.

	Returns:
	vz       Numpy array. The potential as function of z.
	"""
	nz = params.nz
	dz = params.zres
	zval = params.zvalues_nm()

	## Get array of dielectric constants
	# zval = (np.arange(0, nz, dtype = float) / (nz - 1) - 0.5) * params.lz_thick
	epsilonz = np.array([params.z(z)['diel_epsilon'] for z in range(0, nz)])   # this is quite inefficient but will do the job
	zif1, zif2 = params.well_z_nm()
	if zif1 is None or zif2 is None:
		sys.stderr.write("Warning (gate_potential): The well layer could not be identified. The boundary condition for the potential will refer instead to the center of the full layer stack.\n")
		zmid = (zval.min() + zval.max()) / 2
	else:
		zmid = (zif1 + zif2) / 2  # point centered in the well

	# initial density (zero everywhere)
	densz_bg = np.zeros_like(zval)

	# boundary conditions / initial potential
	z1, z2 = zval.min(), zval.max()
	if inner:
		if zif1 is None or zif2 is None:
			sys.stderr.write("Warning (gate_potential): The well layer could not be identified. The boundary condition for the potential will refer instead to the full layer stack.\n")
		else:
			z1, z2 = zif1, zif2
	bc = {'v12': v_tb, 'z1': z1, 'z2': z2, 'v3': 0.0, 'z3': zmid}

	vz = solve_potential(zval, densz_bg, epsilonz, dz = dz, **bc)
	return vz

def gate_potential_from_opts(params, opts):
	"""Initialize gate potential from options

	Argument:
	params   PhysParams instance.
	opts     Dict instance. The options dict from the command line arguments.

	Returns:
	pot      Numpy array or None. Return an array if opts contains any of vgate,
	         vsurf, v_outer, v_inner, and the potential is not initialized from
	         a file. Otherwise return None.
	"""
	if 'potentialfile' in opts:
		return None
	if not any(arg in opts for arg in ['vgate', 'vsurf', 'v_outer', 'v_inner']):
		return None
	v_inner = False
	if 'v_gate' in opts and opts['vgate'] is not None:
		vgate = opts['vgate']
	elif 'v_outer' in opts and opts['v_outer'] is not None:
		vgate = opts['v_outer']
	elif 'v_inner' in opts and opts['v_inner'] is not None:
		vgate = opts['v_inner']
		v_inner = True
	else:
		vgate = 0.0
	pot = gate_potential(vgate, params, inner = v_inner)
	if 'vsurf' in opts and opts['vsurf'] is not None and opts['vsurf'] != 0.0:
		pot += interface_potential(opts['vsurf'], opts['vsurf_l'], params, quadratic=opts['vsurf_quadratic'])
	return pot

def interface_potential(v_surf, vsurf_l, params, quadratic = False):
	"""Interface potential

	Potential that rises to v_surf at the interfaces/surfaces. It decreases
	towards 0 at a distance vsurf_l from the interface.

	Arguments:
	v_surf     Float. Potential value at the interface in meV.
	vsurf_l    Float. Length in nm in which the potential decreases to zero.
	params     PhysParams instance.
	quadratic  True or False. If True, then the potential decreases
	           quadratically to zero, i.e., the potential dependence is a
	           half-parabola at either side of the interface. If False, then the
	           decrease is linear.

	Returns:
	vz       Numpy array. The potential as function of z.
	"""
	nz = params.nz
	dz = params.zres
	zint = params.zinterface

	z = np.arange(0, nz, dtype = float)

	z_if = np.array([(z - zi) * dz for zi in zint])
	d_if = np.amin(np.abs(z_if), axis = 0) / vsurf_l
	if quadratic:
		vz = v_surf * np.maximum(1.0 - d_if, 0.0)**2
	else:
		vz = v_surf * np.maximum(1.0 - d_if, 0.0)
	return vz

def read_potential(params, *args, **kwds):
	"""A wrapper around read_potential_file() that takes care of iteration over multiple arguments"""
	if len(args) == 1 and isinstance(args[0], str):
		return read_potential_file(params, args[0], **kwds)
	if len(args) == 1 and isinstance(args[0], (list, tuple)):  # recursive call: expand list/tuple argument
		return read_potential(params, *tuple(args[0]), **kwds)

	all_mult = []
	all_pot = []
	for a in args:
		if isinstance(a, str):
			all_pot.append(read_potential_file(params, a, **kwds))  # also fine if it is None
			all_mult.append(None)
		elif isinstance(a, (float, int)):
			if len(all_mult) == 0:
				sys.stderr.write("Warning (read_potential): Multiplier without valid potential file.\n")
			elif all_mult[-1] is None:
				all_mult[-1] = float(a)
			else:
				sys.stderr.write("Warning (read_potential): Second and further multipliers are ignored.\n")

	sum_pot = 0
	for v, m in zip(all_pot, all_mult):
		if v is None:
			sys.stderr.write("Warning (read_potential): Invalid potential file.\n")
			continue
		try:
			sum_pot += (1 if m is None else m) * v
		except ValueError:
			sys.stderr.write("ERROR (read_potential): Potentials could not be combined.\n")
			return None
	if not isinstance(sum_pot, np.ndarray):
		sys.stderr.write("Warning (read_potential): No valid potential file.\n")
		return None
	return sum_pot

def potential_file_overwrite_warning(output_file, input_file, directory = None):
	"""Check if potential file will be overwritten and issue a warning if so.

	Arguments:
	output_file   String. The file name of the target file.
	input_file    String, list/tuple, or None. If a string, the file name of the
	              file from which the potential has been read, for which we
	              check if it will be overwritten. If a list or tuple, iterate
	              over the elements. If None, pass without doing anything.
	directory     String or None. If not None, the directory of the input file
	              (or files). If None, use the current working directory.

	No return value
	"""
	if not isinstance(output_file, str):
		raise TypeError("Argument output_file must be a string instance.")
	if isinstance(input_file, (list, tuple)):
		for fn in input_file:
			if isinstance(fn, str):
				potential_file_overwrite_warning(output_file, fn, directory = directory)
	elif isinstance(input_file, str):
		if directory is not None:
			input_file = os.path.join(directory, input_file)
		if os.path.exists(output_file) and os.path.samefile(output_file, input_file):
			sys.stderr.write("Warning (potential_file_overwrite_warning): The potential file \'%s\' is overwritten.\n" % output_file)

def read_potential_file(params, filename, axis = 'z', directory = None, kbs = None):
	"""Read potential from a file.

	If the input coordinates to not match the coordinates determined by params,
	then use interpolation and/or extrapolation. The result is a function of
	the coordinates defined by params.

	Arguments:
	params      PhysParams instance.
	filename    String. The file name of the input file.
	axis        None, 'z', or 'y'. The axis for which the potential is read.
	kbs         ZippedKB instance.

	Returns:
	pot   Numpy array of dimension 1, if the input is a simple potential as
	      function of z or y, i.e., for an input file which has only two columns
	      (coordinate and potential values).
	      OR
	      Numpy array of dimension 2, if the input file defines a potential
	      split by orbital. The output shape is (nzy, 8) where nzy is the
	      number of coordinates in z or y direction and 8 is the number of
	      orbitals.
	      OR
	      A dict instance, if the input file defines a potential split by
	      subbands. The dict keys are the subband labels, the values are arrays
	      of dimension 1.
	"""
	if directory is not None:
		filename = os.path.join(directory, filename)
	try:
		pf = open(filename, 'r')
	except:
		sys.stderr.write("ERROR (read_potential): File not found.\n")
		exit(1)

	l = pf.readline().strip()
	cols = [c.strip().lstrip().lower() for c in l.split(',')]

	if not (axis is None or axis in ['y', 'z']):
		sys.stderr.write("Warning (read_potential): Potential must be along z or y axis.\n")
		pf.close()
		return None
	if axis is None:
		if 'z' in cols and 'y' not in cols:
			axis = 'z'
		elif 'y' in cols and 'z' not in cols:
			axis = 'y'
		else:
			sys.stderr.write("Warning (read_potential): Wrong file format; the file needs to be a CSV file (with columns separated by \',\') with column headings \'z\' (or \'y\') and \'potential\'.\n")
			pf.close()
			return None

	if cols[0] == "\"potential(b" and cols[1] == "z)\"" and axis == 'z':
		print("Multi-B format detected.")
		pf.close()

		zval = params.zvalues_nm()
		bzs = kbs.b.get_values('bz')
		pot = np.genfromtxt(
			filename, skip_header=1, skip_footer=2,	usecols=range(len(cols) - 3),
			delimiter=",")

		# Check whether the stored potential is for the same z and B values that the calculation uses
		if len(pot[:,0]) == len(zval) and len(cols[2:-2]) == len(bzs):
			if np.allclose(pot[:,0], zval) and np.allclose(np.array(cols[2:-2], dtype=np.float64), bzs):
				return pot[:,1:].T

		sys.stderr.write("Warning (read_potential): Interpolation not implemented for this file format.\n")
		return None

	if axis not in cols or not any([col.startswith('potential') for col in cols]):
		sys.stderr.write("Warning (read_potential): Wrong file format; the file needs to be a CSV file (with columns separated by \',\') with column headings \'z\' (or \'y\') and \'potential\' (or \'potential*\'.\n")
		pf.close()
		return None

	zcol = cols.index(axis)
	pcol = [i for i, col in enumerate(cols) if col.startswith('potential')]

	read_zval = []
	read_pval = []

	for l in pf:
		ldata = [d.strip().lstrip() for d in l.split(',')]
		try:
			z = float(ldata[zcol])
			p = [float(ldata[col]) for col in pcol]
		except:
			continue
		read_zval.append(z)
		read_pval.append(p)

	pf.close()
	if len(read_zval) < 2:
		sys.stderr.write("Warning (read_potential): Insufficient or incorrectly formatted data.\n")
		return None

	read_zval = np.array(read_zval)
	read_pval = np.array(read_pval)

	if axis == 'z':
		zval = params.zvalues_nm()
	elif axis == 'y':
		zval = params.yvalues_nm()
	pval = np.array([np.interp(zval, read_zval, read_pval1) for read_pval1 in read_pval.transpose()])

	read_dz_l = read_zval[1] - read_zval[0]
	read_dz_r = read_zval[-1] - read_zval[-2]
	read_dp_l = read_pval[1] - read_pval[0]
	read_dp_r = read_pval[-1] - read_pval[-2]

	read_zmin = read_zval.min()
	read_zmax = read_zval.max()
	for j in range(0, len(zval)):
		if zval[j] < read_zmin:
			pval[:, j] = read_pval[0] + read_dp_l * (zval[j] - read_zmin) / read_dz_l
		if zval[j] > read_zmax:
			pval[:, j] = read_pval[-1] + read_dp_r * (zval[j] - read_zmax) / read_dz_r
	if zval.min() <= read_zmin - read_dz_l or zval.max() >= read_zmax + read_dz_r:
		sys.stderr.write("Warning (read_potential): Extrapolation was needed.\n")

	if any([cols[col].startswith('potentialsub') for col in pcol]):
		if not all([cols[col].startswith('potentialsub') for col in pcol]):
			sys.stderr.write("ERROR (read_potential): Potential in subband basis cannot be mixed with other types.\n")
			return None
		if axis != 'y':
			sys.stderr.write("ERROR (read_potential): Potential in subband basis must contain data along y direction.\n")
			return None
		subbands_in_cols = [cols[col][12:].lstrip('_-').upper() for col in pcol]
		subbands_pval = {}
		for j, sb in enumerate(subbands_in_cols):
			if len(sb) < 2:
				sys.stderr.write("Warning (read_potential): '%s' is not a valid subband identifier.\n" % sb)
				continue
			if sb[0] not in 'ELHS':
				sys.stderr.write("Warning (read_potential): '%s' is not a valid subband identifier.\n" % sb)
				continue
			if sb.endswith('+') or sb.endswith('-'):
				try:
					sbnum = int(sb[1:-1])
				except:
					sys.stderr.write("Warning (read_potential): '%s' is not a valid subband identifier.\n" % sb)
					continue
				if sbnum <= 0:
					sys.stderr.write("Warning (read_potential): '%s' is not a valid subband identifier.\n" % sb)
					continue
				subbands_pval[sb] = pval[j]
			else:
				try:
					sbnum = int(sb[1:])
				except:
					sys.stderr.write("Warning (read_potential): '%s' is not a valid subband identifier.\n" % sb)
					continue
				if sbnum <= 0:
					sys.stderr.write("Warning (read_potential): '%s' is not a valid subband identifier.\n" % sb)
					continue
				subbands_pval[sb] = pval[j]
		return subbands_pval
	if len(pcol) == 1 and cols[pcol[0]] == 'potential':
		pval = pval.flatten()
	else:
		# pcols = [cols[col] for col in pcol]
		pval_orb = np.zeros((8, pval.shape[1]), dtype = float)
		for pcol_idx, col in enumerate(pcol):
			colname = cols[col]
			if colname == 'potential8':
				for i in [2, 3, 4, 5]:
					pval_orb[i] = pval[pcol_idx]
			if colname == 'potential8h':
				for i in [2, 5]:
					pval_orb[i] = pval[pcol_idx]
			if colname == 'potential8l':
				for i in [3, 4]:
					pval_orb[i] = pval[pcol_idx]
			if colname == 'potential7':
				for i in [6, 7]:
					pval_orb[i] = pval[pcol_idx]
			if colname == 'potential6':
				for i in [0, 1]:
					pval_orb[i] = pval[pcol_idx]
		pval = pval_orb.transpose()
	return pval

def subband_potential(params, subbands_pot, overlap_vectors):
	"""Expand subband potential dict to a potential landscape V(z, y) using the overlap vectors.

	Given the (input) subband potential density v_i(y) where i is a subband
	label, and the overlap eigenvectors psi_i(z), the resulting potential is
	V(z, y) = sum_{i in subbands} |psi_i(z)|^2 v_i(y)
	Note that the inputs v_i(y) have units meV / nm, so that the product with
	the probability density |psi_i(z)|^2 yields a potential in meV.

	Arguments:
	params           PhysParams instance. Used to extract nz, ny, and norbitals.
	subbands_pot     Dict instance, where the keys are the subband labels (see
	                 note below) and the values are arrays of length ny; these
	                 are the values v_i(y) in the equation above.
	overlap_vectors  Dict instance, where the keys are the subband labels (see
	                 note below) and the values are arrays of length
	                 nz * norbitals; these are the eigenvectors psi(z) of the
	                 system in a 2D geometry. We sum over the orbital degrees of
	                 freedom.

	Returns:
	pot   An array of shape (nz, ny); the values V(z, y) in the equation above.

	Notes:
	The subband labels can be of the form H1, E1, etc. or H1+, H1-. We always
	use uppercase labels. If for the subband potential H1 is given and the
	overlap vectors give H1+ and H1-, the summation for V(z, y) will contain the
	contribution
	( |psi_{H1+}(z)|^2 + |psi_{H1-}(z)|^2 ) v_H1(y),
	i.e., we sum over both H1+ and H1- in the same amounts.
	TODO: Is this sensible? Or should we divide by 2?
	"""
	if not isinstance(subbands_pot, dict):
		raise TypeError("Argument subbands_pot must be a dict instance.")
	if overlap_vectors is None:
		sys.stderr.write("ERROR (subband_potential): Overlap vectors are required for potential in subband basis.\n")
		return None
	elif not isinstance(overlap_vectors, dict):
		raise TypeError("Argument overlap_vectors must be a dict instance or None.")

	nz = params.nz
	ny = params.ny
	norb = params.norbitals
	dz = params.zres

	for subband in subbands_pot:
		if subbands_pot[subband].shape != (ny,):
			sys.stderr.write("ERROR (subband_potential): Potential data has invalid shape.\n")
			return None
	for ov in overlap_vectors:
		if overlap_vectors[ov].shape != (nz * norb,):
			sys.stderr.write("ERROR (subband_potential): Overlap vector has invalid shape.\n")
			return None

	pot = np.zeros((nz, ny), dtype = float)
	for sb in subbands_pot:
		if sb in overlap_vectors:
			psiz2 = np.sum(np.reshape(np.abs(overlap_vectors[sb])**2, (nz, norb)), axis = 1)
			pot += np.outer(psiz2 / dz, subbands_pot[sb])  # note factor 1 / dz, to get a proper probability density
		else:
			if sb + '+' in overlap_vectors:
				psiz2 = np.sum(np.reshape(np.abs(overlap_vectors[sb + '+'])**2, (nz, norb)), axis = 1)
				pot += np.outer(psiz2 / dz, subbands_pot[sb])
			if sb + '-' in overlap_vectors:
				psiz2 = np.sum(np.reshape(np.abs(overlap_vectors[sb + '-'])**2, (nz, norb)), axis = 1)
				pot += np.outer(psiz2 / dz, subbands_pot[sb])
			if sb + '+' not in overlap_vectors and sb + '-' not in overlap_vectors:
				sys.stderr.write("Warning (subband_potential): Overlaps vector for subband '%s' is not defined.\n" % sb)
	return pot

def print_potential(params, pot):
	"""Print potential and electric fields at interfaces and in the layers

	The output is the electrostatic energy in mV and the electric field in
	mV/nm. Note: The electrostatic potential is the opposite (sign-wise) of the
	potential energy.

	Arguments:
	params    PhysParams instance.
	pot       Numpy array. the potential energy in meV.

	No return value.
	"""
	if pot is None:
		sys.stderr.write("Warning (print_potential): Potential is not defined.\n")
		return
	if isinstance(pot, dict):
		sys.stderr.write("Warning (print_potential): Potential in terms of subbands cannot be shown.\n")
		return
	if isinstance(pot, np.ndarray) and pot.ndim == 2 and pot.shape[1] == params.nz:
		for pot1 in pot:
			print_potential(params, pot1)
		return

	nz = params.nz
	dz = params.zres
	zint = np.array(params.zinterface)
	zlay = np.array([0.5 * (zint[j] + zint[j + 1]) for j in range(0, len(zint) - 1)])

	zall = np.empty((zint.size + zlay.size,), dtype=float)
	zall[0::2] = zint
	zall[1::2] = zlay

	zval = (zall - 0.5 * nz + 0.5) * dz

	potval = []
	efield = []
	# For the signs of the potential and E field, see the note above.
	for z in zall:
		zi = int(round(z))
		if zi == 0:
			potval.append(-pot[zi])
			efield.append((pot[zi + 1] - pot[zi]) / dz)
		elif zi == nz - 1:
			potval.append(-pot[zi])
			efield.append((pot[zi] - pot[zi - 1]) / dz)
		elif int(round(2 * z)) % 2 == 1:  # z is a half-integer
			zi1, zi2 = int(round(z - 0.5)), int(round(z + 0.5))
			potval.append(-0.5 * (pot[zi1] + pot[zi2]))
			efield.append((pot[zi2] - pot[zi1]) / dz)
		else:  # z is an integer
			potval.append(-pot[zi])
			efield.append(0.5 * (pot[zi + 1] - pot[zi - 1]) / dz)

	vmax = np.amax(np.abs(pot))
	emax = np.amax(np.abs(np.array(efield)))

	if vmax < 1e-4:
		vmult = 1e-6
		vunit = "nV"
	elif vmax < 1e-1:
		vmult = 1e-3
		vunit = "\u00b5V"
	elif vmax < 1e2:
		vmult = 1.0
		vunit = "mV"
	else:
		vmult = 1e3
		vunit = "V "

	if emax < 1e-4:
		emult = 1e-6
		eunit = "nV/nm"
	elif emax < 1e-1:
		emult = 1e-3
		eunit = "\u00b5V/nm"
	elif emax < 1e2:
		emult = 1.0
		eunit = "mV/nm"
	else:
		emult = 1e3
		eunit = "V/nm "

	if pot.ndim == 1:
		print("   z        V(z)      E(z)")
		unitstr = "  [nm]      [%s]     [%s]" % (vunit, eunit)
	else:
		norb = pot.shape[1]
		print("Split by orbital")
		print(    "   z        V(z)" + " " * (8 * norb - 3) + "E(z)")
		unitstr = "  [nm]      " + "    ".join(["[%s]" % vunit for _ in range(norb)]) + "  " + " ".join(["[%s]" % eunit for _ in range(norb)])
	unicodewarn = False
	try:
		print(unitstr)
	except UnicodeEncodeError:
		sys.stdout.buffer.write(unitstr.encode('utf-8') + b'\n')  # force unicode encoding
		unicodewarn = True
	for z, v, e in zip(zval, potval, efield):
		if pot.ndim == 1:
			print("%7.2f   %7.2f   %7.2f" % (z, v / vmult, e / emult))
		else:
			s = ("%7.2f" % z) + "  "
			s += " ".join(["%7.2f" % x for x in (v / vmult)]) + "  "
			s += " ".join(["%7.2f" % x for x in (e / emult)])
			print(s)
	if unicodewarn:
		sys.stderr.write("Warning (print_potential): Some symbols could not be encoded in the output encoding (%s) and were forcibly converted to UTF-8. You may try to use 'export PYTHONIOENCODING=utf8' to get rid of this warning.\n" % sys.stdout.encoding)
	return
