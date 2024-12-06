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

from math import sin, cos, sqrt, acos, pi
import numpy as np
import sys
import itertools
from .config import get_config_bool

## Parsing momentum values
MomentumFormatError = "Momentum must be in format: k; (kx, ky); (k, phi, \"kphi\"); or (k, phi, \"deg\")"
Momentum3DFormatError = "Momentum must be in format: k; (kx, ky); (k, phi, \"kphi\"); (k, phi, \"deg\"); or (kx, ky, kz)."

degrees_by_default = False

def isrealnum(x):
	return isinstance(x, (float, np.floating, int, np.integer))

def to_polar(x, y, deg = False):
	"""Get polar coordinates (magnitude r, angle phi) from cartesian coordinates (x, y)"""
	return (np.abs(x + 1.j * y), np.angle(x + 1.j * y, deg))

def degstr(x):
	"""Format value in degrees, which may be NaN."""
	return " nan deg" if np.isnan(x) else "%4g" % x

def diff_mod(x, y, m):
	"""Difference of x and y modulo m."""
	diff = np.abs(np.mod(x, m) - np.mod(y, m))
	return np.minimum(diff, m - diff)

def to_spherical(x, y, z, deg = False):
	"""Get spherical coordinates (r, theta, phi) from cartesian coordinates (x, y, z)"""
	rxy2 = x**2 + y**2 + z**2
	if rxy2 == 0.0:
		theta = 0.0 if z >= 0.0 else 180. if deg else pi
		return abs(z), theta, 0.0
	r = np.sqrt(x**2 + y**2 + z**2)
	if deg:
		theta = 90. if z == 0.0 else acos(z / r) * 180. / pi
	else:
		theta = pi / 2 if z == 0.0 else acos(z / r)
	phi = np.angle(x + 1.j * y, deg)
	return r, theta, phi

def polar_fold(r, phi, deg = False, fold = True):
	"""Fold polar coordinates.
	Folding means that a polar coordinate will be brought into a canonical form
	where the angle lies between -90 and +90 degrees (-pi/2 and pi/2), possibly
	with a negative radius. The identity (x, y) = (r cos phi, r sin phi) is
	preserved.

	Arguments:
	r, phi   Float. Radial and angular coordinates.
	deg      True or False. Degrees or radians as angular units, respectively.
	fold     True, False, or None. If True, fold. If False, return non-folded
	         angular coordinate phi between -180 and 180 degrees (-pi and pi).
	         If None, return the input as is.

	Returns:
	r, phi   New set of polar coordinates.
	"""
	if fold is None:
		pass
	elif deg:
		if fold and r < 0.0:
			r = -r
			phi = (phi + 180.) % 360.
		else:
			phi = (phi + 180.) % 360. - 180.
		if fold and phi > 90.:
			r = -r
			phi -= 180.
		elif fold and phi <= -90.:
			r = -r
			phi += 180.
	else:
		if fold and r < 0.0:
			r = -r
			phi = (phi + pi) % (2 * pi)
		else:
			phi = (phi + pi) % (2 * pi) - pi
		if fold and phi > 0.5 * pi:
			r = -r
			phi -= pi
		elif fold and phi <= -0.5 * pi:
			r = -r
			phi += pi
	return r, phi

def spherical_fold(r, theta, phi, deg = False, fold = True):
	"""Fold polar coordinates.
	Folding means that a spherical coordinate will be brought into a canonical
	form where the angle phi lies between -90 and +90 degrees (-pi/2 and pi/2).
	The radius may be negative and the angle theta may be reflected (theta to
	180 degrees minus theta). The identity
	  (x, y, z) = (r sin theta cos phi, r sin theta sin phi, r cos theta)
	is preserved.

	Arguments:
	r, theta, phi   Float. Spherical coordinates.
	deg             True or False. Degrees or radians as angular units,
	                respectively.
	fold            True, False, or None. If True, fold. If False, return
	                non-folded angular coordinate phi between -180 and 180
	                degrees (-pi and pi). If None, return the input as is.

	Returns:
	r, theta, phi   New set of spherical coordinates.
	"""
	if fold is None:
		pass
	elif deg:
		if theta < 0.0 or theta > 180.:
			raise ValueError("Invalid value for theta")
		if fold and r < 0.0:
			r = -r
			phi = (phi + 180.) % 360.
			theta = 180. - theta
		else:
			phi = (phi + 180.) % 360. - 180.
		if fold and theta == 90.:
			r, phi = polar_fold(r, phi, deg, fold)
		elif fold and theta > 90.:
			r = -r
			phi = phi % 360. - 180.
			theta = 180. - theta
	else:
		if theta < 0.0 or theta > pi:
			raise ValueError("Invalid value for theta")
		if fold and r < 0.0:
			r = -r
			phi = (phi + pi) % (2 * pi)
			theta = pi - theta
		else:
			phi = (phi + pi) % (2 * pi) - pi
		if fold and theta == pi:
			r, phi = polar_fold(r, phi, deg, fold)
		elif fold and theta > pi:
			r = -r
			phi = phi % (2 * pi) - pi
			theta = pi - theta
	return r, theta, phi

def add_var_prefix(var, prefix):
	"""Add variable prefix to component var"""
	return 'r' if len(prefix) == 0 and len(var) == 0 else prefix if var == 'r' else prefix + var

# TODO: Check whether reflection functions are still necessary
def no_reflect_array(arr):
	"""Array identity transformation with mapping from new to old array"""
	return arr, np.arange(0, len(arr), dtype = int)

def reflect_array(arr, offset = 0.0):
	"""Array reflections with mapping from new to old array"""
	newval = np.sort(np.concatenate((arr, offset - arr)))
	sel = np.concatenate(([True], np.diff(newval) > 1e-9))
	newval = newval[sel]
	# mapping; we give a slight 'bonus' to the original value
	diff = np.minimum(np.abs(newval[:, np.newaxis] - arr[np.newaxis, :]) - 1e-9, np.abs(newval[:, np.newaxis] + arr[np.newaxis, :] - offset))
	mapping = np.argmin(diff, axis = 1)
	return newval, mapping

def reflect_angular_array(arr, axis = None, deg = True):
	"""Array reflections for angular arrays with mapping from new to old array"""
	if axis is None:
		axis = 'xy'
	phimax = 180.0 if deg else np.pi
	allvalues = (arr, -arr, phimax - arr, -phimax + arr)
	which = np.array([0, 1, 2, 3] if 'x' in axis and 'y' in axis else [0, 2] if 'x' in axis else [0, 1] if 'y' in axis else [0])
	newval = np.sort(np.concatenate(np.array(allvalues)[which]))
	newval = newval[(newval < phimax + 1e-9) & (newval > -phimax - 1e-9)]
	sel = np.concatenate(([True], np.diff(newval) > 1e-9))
	newval = newval[sel]
	# mapping; we give a slight 'bonus' to the original value
	diff = np.amin(np.array((np.abs(newval[:, np.newaxis] - arr[np.newaxis, :]) - 1e-9, np.abs(newval[:, np.newaxis] + arr[np.newaxis, :]), np.abs(newval[:, np.newaxis] + arr[np.newaxis, :] - phimax), np.abs(newval[:, np.newaxis] - arr[np.newaxis, :] + phimax)))[which], axis = 0)
	mapping = np.argmin(diff, axis = 1)
	return newval, mapping

def linear_integration_element(xval, dx = None, xmin = None, xmax = None, fullcircle = True):
	"""Integration elements for linearly spaced grid.

	Arguments:
	xval         Float or array/list. If a float, calculate the size of the
	             integration element [xval - dx/2, xval + dx/2]. If a list, then
	             return the sizes of the intervals.
	dx           Float or None. If set, size of the integration element. Used
	             only if xval is a float.
	xmin, xmax   Float or None. If not None, the minimum/maximum value of the
	             integration interval. Used only if xval is a float.
	fullcircle   True or False. If True, interpret the integration axis as
	             an angular axis, by multiplying by 2 pi / interval size.

	Returns:
	Float or array (like xval)
	"""
	if isinstance(xval, (float, np.floating)) and dx is not None:
		if fullcircle and (xmin is None or xmax is None):
			raise ValueError("Cannot calculate integration element over full circle if minimum and maximum are not given")
		mult = (2. * np.pi) / (xmax - xmin) if fullcircle else 1.0
		if xmin is not None and xval < xmin - 0.5 * dx:
			return 0
		elif xmin is not None and xval < xmin + 0.5 * dx:
			return mult * dx / 2
		elif xmax is not None and xval > xmax + 0.5 * dx:
			return 0
		elif xmax is not None and xval > xmax - 0.5 * dx:
			return mult * dx / 2
		else:
			return mult * dx
	elif isinstance(xval, (np.ndarray, list)) and dx is None:
		if xmin is not None or xmax is not None:
			sys.stderr.write("Warning (linear_integration_element): Arguments xmin and xmax are ignored.\n")
		xval = np.asarray(xval)
		xmin = xval.min()
		xmax = xval.max()
		xbins = np.concatenate(([xmin], 0.5 * (xval[1:] + xval[:-1]), [xmax]))
		mult = (2. * np.pi) / (xmax - xmin) if fullcircle else 1.0
		# For debugging:
		# print(kval, len(kval))
		# print(kbins, len(kbins))
		return (xbins[1:] - xbins[:-1]) * mult
	else:
		raise ValueError("Illegal combination of inputs")

def quadratic_integration_element(kval, dk = None, kmax = None):
	"""Integration elements, quadratic
	Returns the area of the rings between radii [kk - dk/2, kk + dk/2] with a
	lower radius of >= 0 and an upper radius of <= kmax

	Arguments:
	kval   Float or array/list. If a float, calculate the size of the
	       integration element [kval - dk/2, xval + dk/2]. If a list, then
	       return the sizes of the intervals.
	dx     Float or None. If set, size of the integration element. Used only if
	       kval is a float.
	kmax   Float or None. If not None, the maximum value of the integration
	       interval. Used only if kval is a float.

	Returns:
	Float or array (like kval)
	"""
	if isinstance(kval, (float, np.floating)) and dk is not None:
		if kval < 0.5 * dk:
			return (dk**2) / 8
		elif kmax is not None and kval > kmax + 0.5 * dk:
			return 0
		elif kmax is not None and kval > kmax - 0.5 * dk:
			return 0.5 * (kmax**2 - (kval - 0.5 * dk)**2)
		else:
			return kval * dk
	elif isinstance(kval, (np.ndarray, list)) and dk is None:
		if kmax is not None:
			sys.stderr.write("Warning (quadratic_integration_element): Argument kmax is ignored.\n")
		kval = np.asarray(kval)
		kmin = kval.min()
		kmax = kval.max()
		kbins = np.concatenate(([kmin], 0.5 * (kval[1:] + kval[:-1]), [kmax]))
		# For debugging:
		# print(kval, len(kval))
		# print(kbins, len(kbins))
		return 0.5 * (kbins[1:]**2 - kbins[:-1]**2)
	else:
		raise ValueError("Illegal combination of inputs")

def circular_integration_element(kval, dk = None, kmax = None, full = True):
	"""Integration elements, circular extension of one-dimensional array
	Wrapper around quadratic_integration_element that handles the extension of a
	one-dimensional array to the full circle. If this extension is requested
	(full = True), multiply by the correct angular volume element. See also
	documentation for quadratic_integration_element().

	Arguments:
	kval   Float or array/list. If a float, calculate the size of the
	       integration element [kval - dk/2, xval + dk/2]. If a list, then
	       return the sizes of the intervals.
	dx     Float or None. If set, size of the integration element. Used only if
	       kval is a float.
	kmax   Float or None. If not None, the maximum value of the integration
	       interval. Used only if kval is a float.
	full   True or False. Whether to extend to a full circle.

	Returns:
	Array
	"""
	dk2 = quadratic_integration_element(kval, dk, kmax)
	if not full:
		phimult = 1.0
	elif kval.min() < -1e-8:
		if np.amax(np.abs(kval + kval[::-1])) < 1e-8:  # check if array is symmetric around 0
			phimult = np.pi
		else:
			sys.stderr.write("ERROR (circular_integration_element): One-dimensional array is two-sided and not symmetric. Integration element is ill-defined in this case.\n")
			return None
	else:
		phimult = 2.0 * np.pi
	return np.abs(dk2) * phimult

class Vector:
	"""Vector object

	Attributes:
	value     Float or tuple. The vector component(s).
	vtype     String. The vector type, which defines the parametrization of the
	          vector. Is one of: 'x', 'y', 'z', 'xy', 'xyz', 'pol', 'cyl',
	          'sph'.
	degrees   True, False or None. Whether angular units are degrees (True) or
	          radians (False). None means unknown or undefined.
	aunit     Float or None. Multiplier for angular coordinates. This is pi/180
	          for degrees, 1 for radians, and None if the angular unit is
	          unkwown.
	"""
	def __init__(self, *val, astype = None, deg = None):
		if len(val) == 1 and isinstance(val[0], tuple):
			val = val[0]
		self.degrees = None
		if len(val) == 1 and isrealnum(val[0]):
			self.value = val
			if astype in ['x', 'y', 'z']:
				self.vtype = astype
			elif astype is None:
				self.vtype = 'x'
			else:
				raise ValueError("Invalid vector type")
		elif len(val) == 2 and isrealnum(val[0]) and isrealnum(val[1]):
			if astype == 'pol':
				self.value = val
				self.degrees = degrees_by_default if deg is None else deg
			elif astype in ['cyl', 'sph']:
				self.value = (val[0], val[1], 0.0)
				self.degrees = degrees_by_default if deg is None else deg
			elif astype == 'xyz':
				self.value = (val[0], val[1], 0.0)
			elif astype == 'xy' or astype is None:
				self.value = val
			else:
				raise ValueError("Invalid vector type")
			self.vtype = 'xy' if astype is None else astype
		elif len(val) == 3 and isrealnum(val[0]) and isrealnum(val[1]):
			if isrealnum(val[2]):
				if astype in ['cyl', 'sph']:
					self.value = val
					self.degrees = degrees_by_default if deg is None else deg
				elif astype == 'xyz' or astype is None:
					self.value = val
				else:
					raise ValueError("Invalid vector type")
				self.vtype = 'xyz' if astype is None else astype
			elif val[2] in ['deg', 'rad']:
				if astype in ['cyl', 'sph']:
					self.value = (val[0], val[1], 0.0)
				elif astype == 'pol' or astype is None:
					self.value = (val[0], val[1])
				else:
					raise ValueError("Invalid vector type")
				self.degrees = (val[2] == 'deg')
				if deg is not None and self.degrees != deg:
					sys.stderr.write("Warning (Vector): deg keyword is ignored\n")
				self.vtype = 'pol' if astype is None else astype
			else:
				raise ValueError("Invalid vector input")
		elif len(val) == 4 and isrealnum(val[0]) and isrealnum(val[1]) and val[2] in ['deg', 'rad'] and isrealnum(val[3]):
			if astype == 'cyl' or astype is None:
				self.value = val
			else:
				raise ValueError("Invalid vector type")
			self.degrees = (val[2] == 'deg')
			self.vtype = 'cyl'
		elif len(val) == 5 and isrealnum(val[0]) and isrealnum(val[1]) and val[2] in ['deg', 'rad'] and isrealnum(val[3]) and val[4] in ['deg', 'rad']:
			if val[2] != val[4]:
				raise ValueError("Invalid vector input: deg and rad cannot be mixed")
			if astype == 'sph' or astype is None:
				self.value = val
			else:
				raise ValueError("Invalid vector type")
			self.degrees = (val[2] == 'deg')
			if deg is not None and self.degrees != deg:
				sys.stderr.write("Warning (Vector): deg keyword is ignored\n")
			self.vtype = 'cyl'
		else:
			raise ValueError("Invalid vector input. Valid formats: (x), (x,y), (x,y,z),(r,phi,'deg'), (r,phi,'deg',z), (r,theta,'deg',phi,'deg'), where 'deg' may be replaced by 'rad'.")
		self.aunit = None if self.degrees is None else pi / 180. if self.degrees else 1.0  # angle unit

	# component functions
	def len(self, square = False):
		"""Length (magnitude) of the vector.

		Argument:
		square    True or False. If True, return the squared value.
		"""
		if self.vtype in ['x', 'y', 'z', 'pol', 'cyl', 'sph']:
			return self.value[0]**2 if square else abs(self.value[0])
		elif self.vtype == 'xy':
			r2 = self.value[0]**2 + self.value[1]**2
			return r2 if square else np.sqrt(r2)
		elif self.vtype == 'xyz':
			r2 = self.value[0]**2 + self.value[1]**2 + self.value[2]**2
			return r2 if square else np.sqrt(r2)
		else:
			raise TypeError

	def __abs__(self):
		return self.len()

	def x(self):
		"""Get the x component"""
		if self.vtype in ['y', 'z']:
			return 0.0
		elif self.vtype in ['x', 'xy', 'xyz']:
			return self.value[0]
		elif self.vtype in ['pol', 'cyl']:
			return self.value[0] * cos(self.aunit * self.value[1])  # r cos(phi)
		elif self.vtype == 'sph':
			return self.value[0] * sin(self.aunit * self.value[1]) * cos(self.aunit * self.value[2])  # r sin(theta) cos(phi)
		else:
			raise TypeError

	def y(self):
		"""Get the y component"""
		if self.vtype in ['x', 'z']:
			return 0.0
		elif self.vtype == 'y':
			return self.value[0]
		elif self.vtype in ['xy', 'xyz']:
			return self.value[1]
		elif self.vtype in ['pol', 'cyl']:
			return self.value[0] * sin(self.aunit * self.value[1])  # r sin(phi)
		elif self.vtype == 'sph':
			return self.value[0] * sin(self.aunit * self.value[1]) * sin(self.aunit * self.value[2])  # r sin(theta) sin(phi)
		else:
			raise TypeError

	def z(self):
		"""Get the z component"""
		if self.vtype in ['x', 'y', 'xy', 'pol']:
			return 0.0
		elif self.vtype == 'z':
			return self.value[0]
		elif self.vtype in ['xyz', 'cyl']:
			return self.value[2]
		elif self.vtype == 'sph':
			return self.value[0] * cos(self.aunit * self.value[1])  # r cos(theta)
		else:
			raise TypeError

	def xy(self):
		"""Get the x and y component (as tuple)"""
		if self.vtype == 'z':
			return (0.0, 0.0)
		elif self.vtype == 'x':
			return (self.value[0], 0.0)
		elif self.vtype == 'y':
			return (0.0, self.value[0])
		elif self.vtype == 'xy':
			return self.value
		elif self.vtype == 'xyz':
			return (self.value[0], self.value[1])
		elif self.vtype in ['pol', 'cyl']:
			return (self.value[0] * cos(self.aunit * self.value[1]), self.value[0] * sin(self.aunit * self.value[1]))  # r cos(phi), r sin(phi)
		elif self.vtype == 'sph':
			return (self.value[0] * sin(self.aunit * self.value[1]) * cos(self.aunit * self.value[2]), self.value[0] * sin(self.aunit * self.value[1]) * sin(self.aunit * self.value[2]))  # r sin(theta) cos(phi), r sin(theta) sin(phi)
		else:
			raise TypeError

	def xyz(self):
		"""Get the x, y, and z component (as tuple)"""
		if self.vtype == 'x':
			return (self.value[0], 0.0, 0.0)
		elif self.vtype == 'y':
			return (0.0, self.value[0], 0.0)
		elif self.vtype == 'z':
			return (0.0, 0.0, self.value[0])
		elif self.vtype == 'xy':
			return (self.value[0], self.value[1], 0.0)
		elif self.vtype == 'xyz':
			return self.value
		elif self.vtype == 'pol':
			return (self.value[0] * cos(self.aunit * self.value[1]), self.value[0] * sin(self.aunit * self.value[1]), 0.0)  # r cos(phi), r sin(phi), 0
		elif self.vtype == 'cyl':
			return (self.value[0] * cos(self.aunit * self.value[1]), self.value[0] * sin(self.aunit * self.value[1]), self.value[2])  # r cos(phi), r sin(phi), z
		elif self.vtype == 'sph':
			return (self.value[0] * sin(self.aunit * self.value[1]) * cos(self.aunit * self.value[2]), self.value[0] * sin(self.aunit * self.value[1]) * sin(self.aunit * self.value[2]), self.value[0] * cos(self.aunit * self.value[1]))  # r sin(theta) cos(phi), r sin(theta) sin(phi), r cos(theta)
		else:
			raise TypeError

	def pm(self):
		"""Get x + i y and x - i y (as tuple)"""
		x, y = self.xy()
		return x + 1.j * y, x - 1.j * y

	def pmz(self):
		"""Get x + i y, x - i y, and z (as tuple)"""
		x, y, z = self.xyz()
		return x + 1.j * y, x - 1.j * y, z

	def polar(self, deg = True, fold = True):
		"""Get polar coordinates r and phi (as tuple)

		Arguments:
		deg    True or False. Whether the return value of phi should be in
		       degrees (True) or radians (False).
		fold   True or False. Whether to use folding. See polar_fold().

		Returns:
		r, phi   Floats. Polar coordinates
		"""
		if self.vtype == 'z':
			return (0.0, 0.0)
		if self.vtype in ['x', 'y', 'xy', 'xyz']:
			x, y = self.xy()
			r, phi = to_polar(x, y, deg)
		elif self.vtype in ['pol', 'cyl']:
			r, phi = self.value[0], self.value[1]
		elif self.vtype == 'sph':
			r, phi = self.value[0] * sin(self.value[1] * self.aunit), self.value[2]  # r_xy, phi = r sin(theta), phi

		if self.vtype in ['pol', 'cyl', 'sph']:
			if deg and not self.degrees:
				phi *= 180. / pi
			elif not deg and self.degrees:
				phi *= pi / 180.

		return polar_fold(r, phi, deg, fold)

	def cylindrical(self, deg = True, fold = True):
		"""Get cylindrical coordinates r, phi and z (as tuple)

		Arguments:
		deg    True or False. Whether the return value of phi should be in
		       degrees (True) or radians (False).
		fold   True or False. Whether to use folding. See polar_fold().

		Returns:
		r, phi, z   Floats. Cylindrical coordinates
		"""
		if self.vtype in ['x', 'y', 'z', 'xy', 'xyz']:
			x, y, z = self.xyz()
			r, phi = to_polar(x, y, deg)
		elif self.vtype == 'pol':
			r, phi, z = self.value[0], self.value[1], 0.0
		elif self.vtype == 'cyl':
			r, phi, z = self.value
		elif self.vtype == 'sph':
			r, phi, z = self.value[0] * sin(self.value[1] * self.aunit), self.value[2], self.value[0] * cos(self.value[1] * self.aunit)  # r_xy, phi, z = r sin(theta), phi, r cos(theta)

		if self.vtype in ['pol', 'cyl', 'sph']:
			if deg and not self.degrees:
				phi *= 180. / pi
			elif not deg and self.degrees:
				phi *= pi / 180.
		r, phi = polar_fold(r, phi, deg, fold)
		return r, phi, z

	def spherical(self, deg = True, fold = True):
		"""Get spherical coordinates r, theta and phi (as tuple)

		Arguments:
		deg    True or False. Whether the return value of phi should be in
		       degrees (True) or radians (False).
		fold   True or False. Whether to use folding. See spherical_fold().

		Returns:
		r, theta, phi    Floats. Spherical coordinates.
		"""
		if self.vtype in ['x', 'y', 'z', 'xy', 'xyz']:
			x, y, z = self.xyz()
			r, theta, phi = to_spherical(x, y, z, deg)
		elif self.vtype == 'pol':
			r, phi = self.value
			theta = 90. if deg else pi / 2.
			if deg and not self.degrees:  # we only need to rescale phi, not theta
				phi *= 180. / pi
			elif not deg and self.degrees:
				phi *= pi / 180.
		elif self.vtype == 'cyl':
			rxy, phi, z = self.value
			r = sqrt(rxy**2 + z**2)
			if rxy == 0 and z >= 0:
				theta = 0.0
			elif rxy == 0.0 and z < 0:
				theta = 180. if deg else pi
			elif z == 0:
				theta = 90. if deg else pi / 2.
			else:
				theta = acos(z / r) * 180. / pi if deg else acos(z / r)
			if deg and not self.degrees:  # we only need to rescale phi, not theta
				phi *= 180. / pi
			elif not deg and self.degrees:
				phi *= pi / 180.
		elif self.vtype == 'sph':
			r, theta, phi = self.value
			if deg and not self.degrees:  # we rescale phi and theta
				phi *= 180. / pi
				theta *= 180. / pi
			elif not deg and self.degrees:
				phi *= pi / 180.
				theta *= pi / 180.

		return spherical_fold(r, theta, phi, deg, fold)

	def component(self, comp, prefix = ''):
		"""Get component value.

		Argument:
		comp    String. Which component to return.
		prefix  String that matches the first part of the input comp, for
		        example comp = 'kphi', prefix = 'k' is a valid input.

		Returns:
		A float. The value of the component.
		"""
		if comp is None or comp in [prefix, prefix + 'r']:
			if self.vtype in ['pol', 'cyl', 'sph']:
				return self.value[0]
			else:
				return self.len()
		elif comp == prefix + 'x':
			return self.x()
		elif comp == prefix + 'y':
			return self.y()
		elif comp == prefix + 'z':
			return self.z()
		elif comp == prefix + 'phi':
			if self.vtype == 'sph':
				phi = self.value[2]
			elif self.vtype == 'pol':
				phi = self.value[1]
			else:
				_, phi = self.polar(deg = self.degrees, fold = None)
			return phi
		elif comp == prefix + 'theta':
			_, theta, _ = self.spherical(deg = self.degrees, fold = None)
			return theta
		else:
			raise ValueError("Invalid vector component")

	def components(self, prefix = ''):
		"""Get natural components depending on vector type.

		Argument:
		prefix   String that is prepended to the return value.

		Returns:
		List of strings.
		"""
		if self.vtype in ['x', 'y', 'z']:
			return [prefix + self.vtype]
		elif self.vtype == 'xy':
			return [prefix + 'x', prefix + 'y']
		elif self.vtype == 'xyz':
			return [prefix + 'x', prefix + 'y', prefix + 'z']
		elif self.vtype == 'pol':
			return ['r' if prefix == '' else prefix, prefix + 'phi']
		elif self.vtype == 'cyl':
			return ['r' if prefix == '' else prefix, prefix + 'phi', prefix + 'z']
		elif self.vtype == 'sph':
			return ['r' if prefix == '' else prefix, prefix + 'theta', prefix + 'phi']
		else:
			raise TypeError

	def to_dict(self, prefix = '', all_components = False):
		"""Return a dict with components and values

		Argument:
		prefix           String that is prepended to the return value.
		all_components   True or False. If True, give all components x, y, z,
		                 phi, and theta, as well as len and abs. If False, give
		                 the appropriate components for the vtype only.

		Returns:
		vdict   A dict instance, with vector components as keys.
		"""
		vdict = {}
		if all_components:
			for co in ['x', 'y', 'z', 'phi', 'theta']:
				vdict[prefix + co] = self.component(co)
			vdict[prefix + "len"] = self.len()
			vdict[prefix + "abs"] = self.__abs__()  # in fact, identical result to len
		else:
			for co, val in zip(self.components(prefix = prefix), self.value):
				vdict[co] = val
		return vdict

	def get_pname_pval(self, prefix = ''):
		"""Return variable name and value for plot parameter text
		Either a single component like 'kx = 0.1' or a tuple for multiple
		components like '(kx, ky) = (0.1, 0.2)'.
		"""
		comp = self.components(prefix = prefix)
		if len(self.value) == 1:
			return comp[0], self.value[0]
		else:
			return tuple(comp), tuple(self.value)

	def set_component(self, comp, val = None, prefix = '', inplace = True):
		"""Set specific labelled component(s).

		Arguments:
		comp, val  Component and value. Can be one of the following
		           combinations. If None, None, do nothing. If comp is a dict
		           and val is None, set values according to the dict. (This must
		           be of the form {component: value}, where component is a
		           string, like 'x' and value a number. If comp is a string and
		           val a number, set that component to that value. If comp is a
		           list/tuple of strings and val is a list/tuple of number, set
		           the components to the respective values.
		prefix     Prefix for vector components, e.g., 'k'.
		inplace    True or False. If True, return the present Vector instance.
		           If False, return a new instance.

		Returns:
		The present or a new Vector instance.
		"""
		if comp is None and val is None:
			return self
		elif isinstance(comp, dict) and val is None:
			comp_dict = comp
		elif isinstance(comp, str) and isrealnum(val):
			comp_dict = {comp: val}
		elif isinstance(comp, (list, tuple)) and isinstance(val, (list, tuple)) and len(comp) == len(val):
			comp_dict = {c: v for c, v in zip(comp, val)}
		else:
			raise TypeError("Illegal combination of arguments comp and val.")

		value = [v for v in self.value]
		# For debugging:
		# print ("Comp", comp_dict)
		for c in comp_dict:
			if c not in self.components():
				raise ValueError("Invalid vector component '%s' for vector type '%s'" % (c, self.vtype))
			if c in ['x', 'r', '']:
				value[0] = comp_dict[c]
			elif c == 'y' or c == 'theta':
				value[1] = comp_dict[c]
			elif c == 'z':
				value[2] = comp_dict[c]
			elif c == 'phi' and self.vtype in ['pol', 'cyl']:
				value[1] = comp_dict[c]
			elif c == 'phi' and self.vtype == 'sph':
				value[2] = comp_dict[c]
			else:
				raise ValueError
		if inplace:
			self.value = value
			return self
		else:
			return Vector(value, astype = self.vtype, deg = self.degrees)

	def astype(self, astype, inplace = False, deg = None, fold = True, force = False):
		"""Convert Vector to the given vector type.

		Arguments:
		astype   String. Target vector type.
		inplace  True or False. If True, return the present Vector instance. If
		         False, return a new instance.
		deg      True, False, or None. Whether the values of the angles in the
		         target vector should be in degrees (True) or radians (False).
		         If None, use the default.
		fold     True or False. Whether to use folding for angular vector types.
		force    True or False. If True, generate a new vector even if the
		         target vector type is the same as that of the present instance.
		         For angular types, this may involve folding or unfolding. If
		         False, return the same vector if the vector types are the same.

		Returns:
		The present or a new Vector instance.
		"""
		if astype == self.vtype and not force:
			newvalue = self.value
		elif astype == 'x':
			newvalue = self.x()
		elif astype == 'y':
			newvalue = self.y()
		elif astype == 'z':
			newvalue = self.z()
		elif astype == 'xy':
			newvalue = self.xy()
		elif astype == 'xyz':
			newvalue = self.xyz()
		elif astype == 'pol':
			newvalue = self.polar(deg = deg, fold = fold)
		elif astype == 'cyl':
			newvalue = self.cylindrical(deg = deg, fold = fold)
		elif astype == 'sph':
			newvalue = self.spherical(deg = deg, fold = fold)
		else:
			raise TypeError("Invalid vector type")
		if inplace:
			self.value = newvalue
			self.vtype = astype
			if self.vtype in ['pol', 'cyl', 'sph']:
				self.degrees = degrees_by_default if deg is None else deg
			else:
				self.degrees = None
			self.aunit = None if self.degrees is None else pi / 180. if self.degrees else 1.0  # angle unit
			return self
		else:
			return Vector(newvalue, astype = astype, deg = deg)

	def reflect(self, axis = None, inplace = False, deg = None, fold = True):
		"""Reflect Vector to the given vector type.

		Arguments:
		axis     String or None. The axis/axes along which to reflect; one of
		         '', 'x', 'y', 'z', 'xy', 'xz', 'yz', 'xyz'. The empty string is
		         equivalent to the identity transformation. None is equivalent
		         to 'xyz', which is an overall sign flip.
		inplace  True or False. If True, return the present Vector instance. If
		         False, return a new instance.
		deg      True, False, or None. Whether the values of the angles in the
		         target vector should be in degrees (True) or radians (False).
		         If None, use the default.
		fold     True or False. Whether to use folding for angular vector types.

		Returns:
		The present or a new Vector instance.
		"""
		if deg is None:
			deg = self.degrees
		# Default axis (None) is equivalent to 'xyz'
		if axis is None:
			axis = 'xyz'
		elif axis in ['xz', 'yz']:
			return self.reflect('z', inplace = inplace, deg = deg, fold = fold).reflect(axis[0], inplace = inplace, deg = deg, fold = fold)  # composition xz or yz
		elif axis not in ['', 'x', 'y', 'z', 'xy', 'xyz']:
			raise ValueError("Invalid axis")
		if axis == '':  # do nothing
			newvalue = self.value
		elif self.vtype == 'x':
			newvalue = (-self.value[0]) if 'x' in axis else (self.value[0],)
		elif self.vtype == 'y':
			newvalue = (-self.value[0]) if 'y' in axis else (self.value[0],)
		elif self.vtype == 'z':
			newvalue = (-self.value[0]) if 'z' in axis else (self.value[0],)
		elif self.vtype == 'xy':
			x, y = self.xy()
			x1 = -x if 'x' in axis else x
			y1 = -y if 'y' in axis else y
			newvalue = (x1, y1)
		elif self.vtype == 'xyz':
			x, y, z = self.xyz()
			x1 = -x if 'x' in axis else x
			y1 = -y if 'y' in axis else y
			z1 = -z if 'z' in axis else z
			newvalue = (x1, y1, z1)
		elif self.vtype == 'pol':
			r, phi = self.polar(deg = deg, fold = fold)
			if axis == 'xy' or axis == 'xyz':
				newvalue = polar_fold(-r, phi, deg = deg, fold = fold)
			elif axis == 'x':
				phi0 = 180. if deg else np.pi
				newvalue = polar_fold(r, phi0 - phi, deg = deg, fold = fold)
			elif axis == 'y':
				newvalue = polar_fold(r, -phi, deg = deg, fold = fold)
			elif axis == 'z':
				newvalue = (r, phi)
		elif self.vtype == 'cyl':
			r, phi, z = self.cylindrical(deg = deg, fold = fold)
			if axis == 'xy' or axis == 'xyz':
				r, phi = polar_fold(-r, phi, deg = deg, fold = fold)
			elif axis == 'x':
				phi0 = 180. if deg else np.pi
				r, phi = polar_fold(r, phi0 - phi, deg = deg, fold = fold)
			elif axis == 'y':
				r, phi = polar_fold(r, -phi, deg = deg, fold = fold)
			if 'z' in axis:
				z = -z
			newvalue = (r, phi, z)
		elif self.vtype == 'sph':
			r, theta, phi = self.spherical(deg = deg, fold = fold)
			if axis == 'xyz':
				r, theta, phi = spherical_fold(-r, theta, phi, deg = deg, fold = fold)
			elif axis == 'xy':  # composition of xyz and z; other representations possible
				theta0 = 180. if deg else np.pi
				r, theta, phi = spherical_fold(-r, theta0 - theta, phi, deg = deg, fold = fold)
			elif axis == 'x':
				phi0 = 180. if deg else np.pi
				r, theta, phi = spherical_fold(r, theta, phi0 - phi, deg = deg, fold = fold)
			elif axis == 'y':
				r, theta, phi = spherical_fold(r, theta, -phi, deg = deg, fold = fold)
			elif axis == 'z':
				theta0 = 180. if deg else np.pi
				r, theta, phi = spherical_fold(r, theta0 - theta, phi, deg = deg, fold = fold)
			newvalue = (r, theta, phi)
		else:
			raise TypeError("Invalid vector type")
		if inplace:
			self.value = newvalue
			if self.vtype in ['pol', 'cyl', 'sph']:
				self.degrees = degrees_by_default if deg is None else deg
			else:
				self.degrees = None
			self.aunit = None if self.degrees is None else pi / 180. if self.degrees else 1.0  # angle unit
			return self
		else:
			return Vector(newvalue, astype = self.vtype, deg = deg)

	def __neg__(self):
		"""Unary minus.
		The same as self.reflect('xyz').
		"""
		return self.reflect()

	def diff(self, other, square = False):
		"""Distance between two vectors |v1 - v2|.

		Arguments:
		other    Vector instance or zero (0 or 0.0). The second vector. Zero
		         means the zero vector.
		square   True or False. If True, return |v1 - v2|^2 instead.

		Returns:
		A float.
		"""
		x1, y1, z1 = self.xyz()
		if isinstance(other, Vector):
			x2, y2, z2 = other.xyz()
		elif other == 0.0:
			x2, y2, z2 = 0.0, 0.0, 0.0
		else:
			raise TypeError("Comparison must be with another Vector object or 0.")
		sqdiff = (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2
		return sqdiff if square else np.sqrt(sqdiff)

	def __sub__(self, other):
		"""Alias for vector difference, |v1 - v2|"""
		return self.diff(other)

	# equality, inequality, identity
	def equal(self, other, acc = 1e-9):
		"""Test vector equality v1 == v2.
		Equality means that the two instances refer to the same point in (1-,
		2-, or 3-dimensional) space. The representations (vector types and
		values) need not be identical.

		Arguments:
		other    Vector instance or zero (0 or 0.0). The second vector. Zero
		         means the zero vector.
		acc      Float. The maximum Euclidean difference for the vectors to be
		         considered equal. Default value is 1e-9.

		Returns:
		True or False.
		"""
		x1, y1, z1 = self.xyz()
		if isinstance(other, Vector):
			x2, y2, z2 = other.xyz()
		elif other == 0.0:
			x2, y2, z2 = 0.0, 0.0, 0.0
		else:
			raise TypeError("Comparison must be with another Vector object or 0.")
		return abs(x1 - x2) < acc and abs(y1 - y2) < acc and abs(z1 - z2) < acc

	def zero(self, acc = 1e-9):
		"""Test whether vector equals zero vector.

		Arguments:
		acc      Float. The maximum length for the vector to be considered zero.
		         Default value is 1e-9.

		Returns:
		True or False.
		"""
		return self.len(square = True) < acc**2

	def __eq__(self, other):
		"""Test equality with other Vector instance or zero."""
		return self.zero() if other == 0.0 else self.equal(other)

	def __ne__(self, other):
		"""Test inequality with other Vector instance or zero."""
		return (not self.zero()) if other == 0.0 else (not self.equal(other))

	def identical(self, other, acc = 1e-9):
		"""Test vector identity v1 === v2.
		Identity means that the two instances have the same vector type and have
		the same values.

		Arguments:
		other    Vector instance. The second vector.
		acc      Float. The maximum absolute for the values to be considered
		         equal. Default value is 1e-9.

		Returns:
		True or False.
		"""
		if isinstance(other, Vector):
			if self.vtype != other.vtype:
				return False
			return all([abs(vi - wi) < acc for vi, wi in zip(self.value, other.value)])
		else:
			raise TypeError("Comparison must be with another Vector object.")

	def parallel(self, other, acc = 1e-9):
		"""Test whether two vectors are parallel.
		Do so by calculation the cross product. This is equal to zero if and
		only if the vectors are parallel.

		Arguments:
		other    Vector instance or zero. The second vector. If zero, interpret
		         as the zero vector. Then the result is always True.
		acc      Float. The maximum length difference of the cross product for
		         it to be considered zero. Default value is 1e-9.

		Returns:
		True or False.
		"""
		if isinstance(other, Vector):
			if self.zero() or other.zero():
				return True
			else:
				x1, y1, z1 = self.xyz()
				x2, y2, z2 = other.xyz()
				xo, yo, zo = y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - y1 * x2  # outer product
				return abs(xo) < acc and abs(yo) < acc and abs(zo) < acc
		else:
			raise TypeError("Comparison must be with another Vector object.")

	def perpendicular(self, other, acc = 1e-9):
		"""Test whether two vectors are perpendicular.
		Do so by calculation the inner product. This is equal to zero if and
		only if the vectors are perpendicular.

		Arguments:
		other    Vector instance or zero. The second vector. If zero, interpret
		         as the zero vector. Then the result is always True.
		acc      Float. The maximum length difference of the cross product for
		         it to be considered zero. Default value is 1e-9.

		Returns:
		True or False.
		"""
		if isinstance(other, Vector):
			if self.zero() or other.zero():
				return True
			else:
				x1, y1, z1 = self.xyz()
				x2, y2, z2 = other.xyz()
				ip = x1 * x2 + y1 * y2 + z1 * z2  # inner product
				return abs(ip) < acc
		else:
			raise TypeError("Comparison must be with another Vector object.")

	def __str__(self, formatstr='%6.3f'):
		"""String representation"""
		try:
			if self.vtype in ['x', 'y', 'z']:
				return formatstr % self.value
			elif self.vtype == 'xy':
				return ("(" + formatstr + ", " + formatstr + ")") % self.value
			elif self.vtype == 'xyz':
				return ("(" + formatstr + ", " + formatstr + ", " + formatstr + ")") % self.value
			elif self.vtype == 'pol':
				return (("(" + formatstr + ", %s)") % (self.value[0], degstr(self.value[1]))) if self.degrees else (("(" + formatstr + ", " + formatstr + " rad)") % self.value)
			elif self.vtype == 'cyl':
				return (("(" + formatstr + ", %s, " + formatstr + ")") % (self.value[0], degstr(self.value[1]), self.value[2])) if self.degrees else (("(" + formatstr + ", " + formatstr + " rad, " + formatstr + ")") % self.value)
			elif self.vtype == 'sph':
				return (("(" + formatstr + ", %s, %s)") % (self.value[0], degstr(self.value[1]), degstr(self.value[2]))) if self.degrees else (("(" + formatstr + ", " + formatstr + " rad, " + formatstr + " rad)") % self.value)
			else:
				raise TypeError("Invalid Vector type")
		except:
			raise ValueError("Error printing Vector")

	def __repr__(self):
		return str(self)

	def xmlattr(self, prefix = ''):
		"""XML output (attributes and values)

		Attributes:
		prefix   String that is prepended to the vector components to form the
		         attributes.

		Returns:
		A dict of the form {attribute: value, ...}, where attribute is the
		XML attribute for an XML <vector> tag or similar.
		"""
		attr = {}
		if self.vtype in ['x', 'y', 'z']:
			attr[prefix + self.vtype] = self.value[0]
		elif self.vtype == 'xy':
			attr[prefix + 'x'] = self.value[0]
			attr[prefix + 'y'] = self.value[1]
		elif self.vtype == 'xyz':
			attr[prefix + 'x'] = self.value[0]
			attr[prefix + 'y'] = self.value[1]
			attr[prefix + 'z'] = self.value[2]
		elif self.vtype == 'pol':
			if len(prefix) == 0:
				attr['r'] = self.value[0]
			else:
				attr[prefix + ''] = self.value[0]
			attr[prefix + 'phi'] = self.value[1]
			x, y = self.xy()
			attr[prefix + 'x'] = x
			attr[prefix + 'y'] = y
		elif self.vtype == 'cyl':
			if len(prefix) == 0:
				attr['r'] = self.value[0]
			else:
				attr[prefix + ''] = self.value[0]
			attr[prefix + 'phi'] = self.value[1]
			x, y, z = self.xyz()
			attr[prefix + 'x'] = x
			attr[prefix + 'y'] = y
			attr[prefix + 'z'] = z
		elif self.vtype == 'sph':
			if len(prefix) == 0:
				attr['r'] = self.value[0]
			else:
				attr[prefix + ''] = self.value[0]
			attr[prefix + 'theta'] = self.value[1]
			attr[prefix + 'phi'] = self.value[2]
			x, y, z = self.xyz()
			attr[prefix + 'x'] = x
			attr[prefix + 'y'] = y
			attr[prefix + 'z'] = z
		else:
			raise TypeError
		if self.vtype in ['pol', 'cyl', 'sph']:
			attr['angleunit'] = 'deg' if self.degrees else 'rad'
		return attr

	# legacy function
	def to_tuple(self):
		if self.vtype in ['x', 'z']:
			return self.value[0]
		elif self.vtype in ['xy', 'xyz']:
			return self.value
		elif self.vtype == 'pol':
			return (self.value[0], self.value[1], 'deg' if self.degrees else 'rad')
		elif self.vtype in ['y', 'cyl', 'sph']:
			sys.stderr.write("Warning (Vector.to_tuple): Backconversion not possible for type '%s'.\n" % self.vtype)
			return None
		else:
			raise TypeError

def is_diagonal(m, acc = 1e-9):
	"""Test if a matrix/array is diagonal"""
	return m.ndim == 2 and m.shape[0] == m.shape[1] and m.shape[0] > 0 and (np.amax(np.abs(m - np.diag(np.diagonal(m)))) < acc)

class VectorTransformation(object):
	"""Vector transformation object.
	This defines a linear transformation on cartesian, cylindrical and sperical
	coordinates. For cartesian coordinates, this is just a matrix multiplication
	by a matrix M, i.e., v -> M v. For cylindrical and spherical coordinates,
	the angles may need to be shifted, so that an affine transformation is
	required, i.e., v -> M v + u, where M is a matrix and u is a vector.

	A VectorTransformation instance is used to apply a transformation to either
	a Vector or	a VectorGrid instance.

	Attributes:
	name       String. A label.
	mat_cart   Numpy array of shape (3, 3). Transformation matrix M in cartesian
	           coordinates (vector representation).
	mat_cyl    Numpy array of shape (3, 3). Transformation matrix M in
	           cylindrical coordinates.
	mat_sph    Numpy array of shape (3, 3). Transformation matrix M in spherical
	           coordinates.
	delta_cyl  Numpy array of length 3. Vector shift u for cylindrical
	           transformation.
	delta_sph  Numpy array of length 3. Vector shift u for spherical
	           transformation.
	mat_e      Numpy array of shape (2, 2). Transformation matrix M in the E
	           representation.
	a2g        Float, either 1.0 or -1.0. Transformation in the A2g
	           representation of Oh.
	"""
	def __init__(self, name, mat_cart, mat_cyl, mat_sph, delta_cyl = None, delta_sph = None, mat_e = None, a2g = None):
		self.name = name
		self.mat_cart = np.array(mat_cart)
		self.mat_cart = np.diag(self.mat_cart) if self.mat_cart.ndim == 1 else self.mat_cart
		if mat_cyl is None:
			self.mat_cyl = None
		else:
			self.mat_cyl = np.array(mat_cyl)
			self.mat_cyl = np.diag(self.mat_cyl) if self.mat_cyl.ndim == 1 else self.mat_cyl
		if mat_sph is None:
			self.mat_sph = None
		else:
			self.mat_sph = np.array(mat_sph)
			self.mat_sph = np.diag(self.mat_sph) if self.mat_sph.ndim == 1 else self.mat_sph
		for m in [self.mat_cart, self.mat_cyl, self.mat_sph]:
			if isinstance(m, np.ndarray) and m.shape != (3, 3):
				raise ValueError("Inputs must be 3x3 matrices or length-3 arrays.")
		self.delta_cyl = np.array([0., 0., 0.]) if delta_cyl is None else np.array(delta_cyl)
		self.delta_sph = np.array([0., 0., 0.]) if delta_sph is None else np.array(delta_sph)
		if self.delta_cyl.shape != (3,) or self.delta_sph.shape != (3,):
			raise ValueError("Input arguments 'delta_cyl' and 'delta_sph' must be length-3 arrays or None.")
		if mat_e is None:
			m = self.mat_cart
			s3 = np.sqrt(3)
			self.mat_e = np.array([
				[0.5 * (m[0, 0]**2 - m[1, 0]**2) - 0.5 * (m[0, 1]**2 - m[1, 1]**2), 0.5 * s3 * (m[0, 2]**2 - m[1, 2]**2)],
				[0.5 * s3 * (m[2, 0]**2 - m[2, 1]**2), 1.5 * m[2, 2]**2 - 0.5]
			])  # TODO: Check this!
		else:
			self.mat_e = np.array(mat_e)
			self.mat_e = np.diag(self.mat_e) if self.mat_e.ndim == 1 else self.mat_e
			if self.mat_e.shape != (2, 2):
				raise ValueError("Argument mat_e must be None or an array of shape (2,) or (2, 2).")
		if a2g == -1.0 or a2g == 1.0:
			self.a2g = float(a2g)
		elif a2g is None:
			self.a2g = 1.0
		else:
			raise TypeError("Argument a2g must have the value -1 or 1, or be a 1x1 array with one of these values.")

	def grid_safe(self, vtype, var):
		"""Test whether the transformation is 'grid safe' for a specific vector type.
		Grid safe means that the result of the transformation can again be
		written as a grid of the same type. For example, a rotation about a
		generic angle (not a multiple of 90 degrees) is not 'grid safe' for a
		cartesian grid.

		Arguments:
		vtype   String. Vector type.
		var     String or list of strings. For cartesian grids, which are the
		        variable (non-constant) components of the grid.
		"""
		if isinstance(var, str):
			var = [var]
		if vtype in ['x', 'y', 'z', 'xy', 'xyz']:
			coord = np.array(['x' in var, 'y' in var, 'z' in var])
			m = 1 * self.mat_cart[coord][:, coord]
			m[np.abs(m) < 1e-9] = 0
			for v in m:
				if np.count_nonzero(v) != 1:
					return False
			mh_m = np.dot(np.transpose(np.conjugate(m)), m)
			return is_diagonal(mh_m)
		elif vtype == 'sph':
			if self.mat_sph is None:
				return False
			coord = np.array(['r' in var, 'theta' in var, 'phi' in var])
			return is_diagonal(self.mat_sph[coord][:, coord])
		elif vtype in ['pol', 'cyl']:
			if self.mat_cyl is None:
				return False
			coord = np.array(['r' in var, 'phi' in var, 'z' in var])
			return is_diagonal(self.mat_cyl[coord][:, coord])
		else:
			return ValueError("Invalid vtype")

	def __call__(self, v, fold = True):
		"""Apply transformation to Vector or VectorGrid.

		Arguments:
		v     Vector or VectorGrid instance.
		fold  True or False. Whether to use folding for angular vector types.

		Returns:
		A new Vector or VectorGrid instance.
		"""
		newvtype = v.vtype
		if isinstance(v, Vector):
			if v.vtype in ['x', 'y', 'z', 'xy', 'xyz']:
				vec = v.xyz()
				newvec = np.dot(self.mat_cart, vec)
				if v.vtype != 'xyz':
					newvec = [newvec[0]] if v.vtype == 'x' else [newvec[1]] if v.vtype == 'y' else [newvec[2]] if v.vtype == 'z' else newvec[0:2]
			elif v.vtype == 'pol':
				if self.mat_cyl is None:
					newvec = np.dot(self.mat_cart, np.array(v.xyz()))
					newvtype = 'xyz'
				else:
					vec = np.concatenate((v.value, [0]))
					delta_mult = np.array([1., 1. if v.degrees else pi / 180, 1.])
					newvec = (np.dot(self.mat_cyl, vec) + delta_mult * self.delta_cyl)[0:2]
			elif v.vtype == 'cyl':
				if self.mat_cyl is None:
					newvec = np.dot(self.mat_cart, np.array(v.xyz()))
					newvtype = 'xyz'
				else:
					vec = v.value
					delta_mult = np.array([1., 1. if v.degrees else pi / 180, 1.])
					newvec = np.dot(self.mat_cyl, vec) + delta_mult * self.delta_cyl
			elif v.vtype == 'sph':
				if self.mat_sph is None:
					newvec = np.dot(self.mat_cart, np.array(v.xyz()))
					newvtype = 'xyz'
				else:
					vec = v.value
					delta_mult = np.array([1., 1. if v.degrees else pi / 180, 1. if v.degrees else pi / 180])
					newvec = np.dot(self.mat_sph, vec) + delta_mult * self.delta_sph
			else:
				raise ValueError("Invalid vector type")
			out_v = Vector(*newvec, astype = newvtype, deg = v.degrees)
			if fold:
				out_v.astype(v.vtype, inplace = True, deg = v.degrees, fold = True, force = True)
			elif newvtype != v.vtype:
				out_v.astype(v.vtype, inplace = True, deg = v.degrees, fold = False, force = False)
			return out_v
		elif isinstance(v, VectorGrid):
			if not self.grid_safe(v.vtype, v.var):
				sys.stderr.write("Warning (VectorTransformation): Transformation does not preserve grid.\n")
				return None
			if v.vtype in ['x', 'y', 'z']:
				new_val = [np.dot(self.mat_cart, vec.xyz()) for vec in v]
				return VectorGrid(v.vtype, new_val, astype = v.vtype, prefix = v.prefix)
			elif v.vtype == 'xy':
				new_val = np.array([np.dot(self.mat_cart, vec.xyz()) for vec in v])
				new_val_u = [np.unique(x) for x in new_val.transpose()]
				return VectorGrid('x', new_val_u[0], 'y', new_val_u[1], astype = 'xy', prefix = v.prefix)
			elif v.vtype == 'xyz':
				new_val = np.array([np.dot(self.mat_cart, vec.xyz()) for vec in v])
				new_val_u = [np.unique(x) for x in new_val.transpose()]
				return VectorGrid('x', new_val_u[0], 'y', new_val_u[1], 'z', new_val_u[2], astype = 'xyz', prefix = v.prefix)
			elif v.vtype == 'pol':
				delta_mult = np.array([1., 1. if v.degrees else pi / 180, 1.])
				delta = delta_mult * self.delta_cyl
				new_val = np.array([np.dot(self.mat_cyl, vec.polar(deg = v.degrees, fold = False) + (0,)) for vec in v]) + delta[np.newaxis, :]
				new_val_u = [np.unique(x) for x in new_val.transpose()]
				return VectorGrid('r', new_val_u[0], 'phi', new_val_u[1], astype = 'pol', deg = v.degrees, prefix = v.prefix)
			elif v.vtype == 'cyl':
				delta_mult = np.array([1., 1. if v.degrees else pi / 180, 1.])
				delta = delta_mult * self.delta_cyl
				new_val = np.array([np.dot(self.mat_cyl, vec.cylindrical(deg = v.degrees, fold = False)) for vec in v]) + delta[np.newaxis, :]
				new_val_u = [np.unique(x) for x in new_val.transpose()]
				return VectorGrid('r', new_val_u[0], 'phi', new_val_u[1], 'z', new_val_u[2], astype = 'cyl', deg = v.degrees, prefix = v.prefix)
			elif v.vtype == 'sph':
				delta_mult = np.array([1., 1. if v.degrees else pi / 180, 1. if v.degrees else pi / 180])
				delta = delta_mult * self.delta_sph
				new_val = np.array([np.dot(self.mat_sph, vec.spherical(deg = v.degrees, fold = False)) for vec in v]) + delta[np.newaxis, :]
				new_val_u = [np.unique(x) for x in new_val.transpose()]
				return VectorGrid('r', new_val_u[0], 'theta', new_val_u[1], 'phi', new_val_u[2], astype = 'sph', deg = v.degrees, prefix = v.prefix)
			else:
				raise ValueError("Invalid vector type")
		else:
			raise TypeError("Argument v must be a Vector or VectorGrid instance.")

	def transform(self, rep, values):
		"""Apply representation action.

		Arguments:
		rep      String. The representation label.
		values   Float or numpy array. The value or vector that the
		         representation acts on.

		Returns:
		Float or numpy array, like argument values.
		"""
		if rep.lower() in ['a1', 'a1g', 'triv']:
			return values
		elif rep.lower() in ['a2', 'a1u', 'parity']:
			return self.det() * values
		elif rep.lower() in ['a2g']:
			return self.a2g * values
		elif rep.lower() in ['a2u']:
			return self.a2g * self.det() * values
		elif rep.lower() in ['t1', 't1g', 'axial']:
			return self.det() * np.dot(self.mat_cart, values)
		elif rep.lower() in ['t2', 't1u', 'vector']:
			return np.dot(self.mat_cart, values)
		elif rep.lower() in ['t2g']:
			return self.a2g * self.det() * np.dot(self.mat_cart, values)
		elif rep.lower() in ['t2u']:
			return self.a2g * np.dot(self.mat_cart, values)
		elif rep.lower() in ['e', 'eg']:
			return np.dot(self.mat_e, values)
		elif rep.lower() in ['eu']:
			return self.det() * np.dot(self.mat_e, values)
		else:
			raise ValueError("Invalid representation")

	def __mul__(self, other):
		"""Multiply two VectorTransformation instances"""
		new_name = self.name + '*' + other.name
		new_mat_cart = np.dot(self.mat_cart, other.mat_cart)
		if self.mat_cyl is None or other.mat_cyl is None:
			new_mat_cyl = None
			new_delta_cyl = None
		else:
			new_mat_cyl = np.dot(self.mat_cyl, other.mat_cyl)
			new_delta_cyl = np.dot(self.mat_cyl, other.delta_cyl) + self.delta_cyl
		if self.mat_sph is None or other.mat_sph is None:
			new_mat_sph = None
			new_delta_sph = None
		else:
			new_mat_sph = np.dot(self.mat_sph, other.mat_sph)
			new_delta_sph = np.dot(self.mat_sph, other.delta_sph) + self.delta_sph
		new_mat_e = np.dot(self.mat_e, other.mat_e)
		new_a2g = self.a2g * other.a2g
		return VectorTransformation(new_name, new_mat_cart, new_mat_cyl, new_mat_sph, delta_cyl = new_delta_cyl, delta_sph = new_delta_sph, mat_e = new_mat_e, a2g = new_a2g)

	def inv(self):
		"""Get the inverse transformation"""
		new_name = self.name[:-2] if self.name.endswith('\u207b\xb9') else self.name[:-1] + '\u207a' if self.name.endswith('\u207b') else self.name[:-1] + '\u207b' if self.name.endswith('\u207a') else self.name[:-1] + '+' if self.name.endswith('-') else self.name[:-1] + '-' if self.name.endswith('+') else self.name + '\u207b\xb9'
		new_mat_cart = np.linalg.inv(self.mat_cart)
		if self.mat_cyl is None:
			new_mat_cyl = None
			new_delta_cyl = None
		else:
			new_mat_cyl = np.linalg.inv(self.mat_cyl)
			new_delta_cyl = -np.dot(new_mat_cyl, self.delta_cyl)
		if self.mat_sph is None:
			new_mat_sph = None
			new_delta_sph = None
		else:
			new_mat_sph = np.linalg.inv(self.mat_sph)
			new_delta_sph = -np.dot(new_mat_sph, self.delta_sph)
		new_mat_e = np.linalg.inv(self.mat_e)
		return VectorTransformation(new_name, new_mat_cart, new_mat_cyl, new_mat_sph, delta_cyl = new_delta_cyl, delta_sph = new_delta_sph, mat_e = new_mat_e, a2g = self.a2g)

	def det(self):
		"""Get the determinant"""
		return np.linalg.det(self.mat_cart)

	def __str__(self):
		"""String representations"""
		return ("<Vector transformation %s>" % self.name)


### VECTOR TRANSFORMATION DEFINITIONS ###
_c3 = np.cos(2 * pi / 3)
_s3 = np.sin(2 * pi / 3)
vt_1 = VectorTransformation('1', [1, 1, 1], [1, 1, 1], [1, 1, 1])
vt_i = VectorTransformation('i', [-1, -1, -1], [1, 1, -1], [1, -1, 1], delta_cyl = [0, 180, 0], delta_sph = [0, 180, 180])
vt_2z = VectorTransformation('2(z)', [-1, -1, 1], [1, 1, 1], [1, 1, 1], delta_cyl = [0, 180, 0], delta_sph = [0, 0, 180])
vt_mz = VectorTransformation('m(z)', [1, 1, -1], [1, 1, -1], [1, -1, 1], delta_cyl = [0, 0, 0], delta_sph = [0, 180, 0])
vt_3z = VectorTransformation('3(z)', [[_c3, -_s3, 0], [_s3, _c3, 0], [0, 0, 1]], [1, 1, 1], [1, 1, 1], delta_cyl = [0, 120, 0], delta_sph = [0, 0, 120], mat_e = [[_c3, -_s3], [_s3, _c3]])
vt_3a = VectorTransformation('3(a)', [[0, 0, -1], [-1, 0, 0], [0,  1, 0]], None, None)
vt_3b = VectorTransformation('3(b)', [[0, 0,  1], [-1, 0, 0], [0, -1, 0]], None, None)
vt_3c = VectorTransformation('3(c)', [[0, 0, -1], [ 1, 0, 0], [0, -1, 0]], None, None)
vt_3d = VectorTransformation('3(d)', [[0, 0,  1], [ 1, 0, 0], [0,  1, 0]], None, None)
vt_m3z = VectorTransformation('-3(z)', [[_c3, -_s3, 0], [_s3, _c3, 0], [0, 0, -1]], [1, 1, -1], [1, -1, 1], delta_cyl = [0, 120, 0], delta_sph = [0, 180, 120], mat_e = [[_c3, -_s3], [_s3, _c3]])
vt_4z = VectorTransformation('4(z)', [[0, 1, 0], [-1, 0, 0], [0, 0, 1]], [ 1, 1, 1], [ 1, 1, 1], delta_cyl = [0, 90, 0], delta_sph = [0, 0, 90], a2g = -1)
vt_m4z = VectorTransformation('-4(z)', [[0, 1, 0], [-1, 0, 0], [0, 0, -1]], [ 1, 1, -1], [ 1, -1, 1], delta_cyl = [0, 90, 0], delta_sph = [0, 180, 90], a2g = -1)
vt_mx = VectorTransformation('m(x)', [-1, 1, 1], [1, -1, 1], [1, 1, -1], delta_cyl = [0, 180, 0], delta_sph = [0, 0, 180])
vt_my = VectorTransformation('m(y)', [1, -1, 1], [1, -1, 1], [1, 1, -1], delta_cyl = [0, 0, 0], delta_sph = [0, 0, 0])
vt_mt = VectorTransformation('m(t)', [[-_c3,  _s3, 0], [ _s3,  _c3, 0], [0, 0, 1]], [1, -1, 1], [1, 1, -1], delta_cyl = [0, 60, 0], delta_sph = [0, 0, 60], mat_e = [[-_c3, _s3], [_s3, _c3]])
vt_mu = VectorTransformation('m(u)', [[ _c3, -_s3, 0], [-_s3, -_c3, 0], [0, 0, 1]], [1, -1, 1], [1, 1, -1], delta_cyl = [0, -120, 0], delta_sph = [0, 0, -120], mat_e = [[_c3, -_s3], [-_s3, -_c3]])
vt_mv = VectorTransformation('m(v)', [[-_c3, -_s3, 0], [-_s3,  _c3, 0], [0, 0, 1]], [1, -1, 1], [1, 1, -1], delta_cyl = [0, -60, 0], delta_sph = [0, 0, -60], mat_e = [[-_c3, -_s3], [-_s3, _c3]])
vt_mw = VectorTransformation('m(w)', [[ _c3,  _s3, 0], [ _s3, -_c3, 0], [0, 0, 1]], [1, -1, 1], [1, 1, -1], delta_cyl = [0, 120, 0], delta_sph = [0, 0, 120], mat_e = [[_c3, _s3], [_s3, -_c3]])
vt_mxpy = VectorTransformation('m(x+y)', [[0, 1, 0], [1, 0, 0], [0, 0, 1]], [1, -1, 1], [1, 1, -1], delta_cyl = [0, 90, 0], delta_sph = [0, 0, 90], a2g = -1)
vt_mxmy = VectorTransformation('m(x-y)', [[0, -1, 0], [-1, 0, 0], [0, 0, 1]], [1, -1, 1], [1, 1, -1], delta_cyl = [0, -90, 0], delta_sph = [0, 0, -90], a2g = -1)
vt_2x = VectorTransformation('2(x)', [1, -1, -1], [1, -1, -1], [1, -1, -1], delta_cyl = [0, 0, 0], delta_sph = [0, 180, 0])
vt_2y = VectorTransformation('2(y)', [-1, 1, -1], [1, -1, -1], [1, -1, -1], delta_cyl = [0, 180, 0], delta_sph = [0, 180, 180])
vt_2xpy = VectorTransformation('2(x+y)', [[0, 1, 0], [1, 0, 0], [0, 0, -1]], [1, -1, -1], [1, -1, -1], delta_cyl = [0, 90, 0], delta_sph = [0, 180, 90], a2g = -1)
vt_2xmy = VectorTransformation('2(x-y)', [[0, -1, 0], [-1, 0, 0], [0, 0, -1]], [1, -1, -1], [1, -1, -1], delta_cyl = [0, -90, 0], delta_sph = [0, 180, -90], a2g = -1)
all_vectrans = [vt_1, vt_i, vt_2z, vt_mz, vt_3z, vt_m3z, vt_3a, vt_3b, vt_3c, vt_3d, vt_4z, vt_m4z, vt_mx, vt_my, vt_mt, vt_mu, vt_mv, vt_mw, vt_mxpy, vt_mxmy, vt_2x, vt_2y, vt_2xpy, vt_2xmy]


def get_vectortransformation(name):
	"""Get vector transformation by name/label"""
	if name == 'all':
		return all_vectrans
	for vt in all_vectrans:
		if vt.name == name:
			return vt
	raise IndexError

def vector_from_attr(attr, prefix = '', deg = True):
	"""Get Vector instance from XML attributes

	Arguments:
	attr     A dict instance of the form {attribute: value, ...}.
	prefix   String. Vector prefix common to all of its components.
	deg      True or False. Whether the angular unit of the output vector should
	         be degrees (True) or radians (False).

	Returns:
	A Vector instance.
	"""
	if prefix + '' in attr and prefix + 'phi' in attr and prefix + 'theta' in attr:
		return Vector(float(attr[prefix + '']), float(attr[prefix + 'theta']), float(attr[prefix + 'phi']), astype = 'sph', deg = deg)
	elif prefix + '' in attr and prefix + 'phi' in attr and prefix + 'z' in attr:
		return Vector(float(attr[prefix + '']), float(attr[prefix + 'phi']), float(attr[prefix + 'z']), astype = 'cyl', deg = deg)
	elif prefix + '' in attr and prefix + 'phi' in attr:
		return Vector(float(attr[prefix + '']), float(attr[prefix + 'phi']), astype = 'pol', deg = deg)
	elif prefix + '' in attr and prefix + 'theta' in attr:
		return Vector(float(attr[prefix + '']), float(attr[prefix + 'theta']), 0.0, astype = 'sph', deg = deg)
	elif prefix + 'x' in attr and prefix + 'y' in attr and prefix + 'z' in attr:
		return Vector(float(attr[prefix + 'x']), float(attr[prefix + 'y']), float(attr[prefix + 'z']), astype = 'xyz')
	elif prefix + 'x' in attr and prefix + 'y' in attr:
		return Vector(float(attr[prefix + 'x']), float(attr[prefix + 'y']), astype = 'xy')
	elif prefix + 'x' in attr and prefix + 'z' in attr:
		return Vector(float(attr[prefix + 'x']), 0.0, float(attr[prefix + 'z']), astype = 'xyz')
	elif prefix + 'y' in attr and prefix + 'z' in attr:
		return Vector(0.0, float(attr[prefix + 'y']), float(attr[prefix + 'z']), astype = 'xyz')
	elif prefix + 'x' in attr:
		return Vector(float(attr[prefix + 'x']), astype = 'x')
	elif prefix + 'y' in attr:
		return Vector(float(attr[prefix + 'y']), astype = 'y')
	elif prefix + 'z' in attr:
		return Vector(float(attr[prefix + 'z']), astype = 'z')
	elif prefix + '' in attr:
		return Vector(float(attr[prefix + '']), 0.0, astype = 'pol', deg = deg)
	else:
		raise ValueError("Illegal combination of components")

class VectorGrid:
	"""Container class for vector grids.
	Vector grids are defined in terms of their components, which may be variable
	(multiple components) or constant.

	Example:
	  VectorGrid('x', [0, 1], 'y', 1, 'z', [2, 3, 4])
	contains the vectors (in cartesian notation)
	  (0, 1, 2), (0, 1, 3), (0, 1, 4), (1, 1, 2), (1, 1, 3),  (1, 1, 4).
	Here, 'x' and 'z' are the variable components and 'y' is a constant
	component.

	Attributes:
	var          List of strings. The variable components.
	values       List of arrays. The values for the variable components.
	const        List of strings. The constant components.
	constvalues  List of floats. The values for the constant components.
	vtype        String. The vector type, which defines the parametrization of
	             the vector. Is one of: 'x', 'y', 'z', 'xy', 'xyz', 'pol',
	             'cyl', 'sph'.
	degrees      True, False or None. Whether angular units are degrees (True)
	             or radians (False). None means unknown or undefined.
	shape        Tuple or integers. Shape of the resulting grid.
	ndim         Integer. Number of variable components.
	prefix       String. Common prefix for vector components.
	"""
	def __init__(self, *args, astype = None, deg = None, prefix = None):
		self.vtype = astype
		if self.vtype in ['pol', 'cyl', 'sph']:
			self.degrees = degrees_by_default if deg is None else deg
		elif self.vtype in ['x', 'y', 'z', 'xy', 'xyz']:
			self.degrees = None
		else:
			raise ValueError("Invalid vector type")

		if prefix is None:
			self.prefix = ''
		elif isinstance(prefix, str):
			self.prefix = prefix
		else:
			raise TypeError("Prefix must be a string")

		if len(args) % 2 != 0:
			raise ValueError("Invalid number of inputs")
		self.var = []
		self.values = []
		self.const = []
		self.constvalues = []
		self.shape = []
		self.ndim = 0
		for j in range(0, len(args), 2):
			var = args[j]
			val = args[j+1]
			if not isinstance(var, str):
				raise TypeError("Invalid variable")
			if self.prefix != '' and var.startswith(self.prefix):
				var = "".join(var.split(self.prefix)[1:])
			if var == '':
				var = 'r'
			if isrealnum(val):
				self.const.append(var)
				self.constvalues.append(val)
			elif isinstance(val, list) or (isinstance(val, np.ndarray) and val.ndim == 1):
				if len(val) == 1:
					self.const.append(var)
					self.constvalues.append(val[0])
				else:
					self.var.append(var)
					self.values.append(np.array(val))
					self.ndim += 1
					self.shape.append(len(val))
			else:
				raise TypeError("Invalid value")
		allvar = self.var + self.const
		if self.vtype in ['x', 'y', 'z']:
			if len(allvar) != 1 or allvar[0] != self.vtype:
				raise ValueError("Variable '%s' not valid for vector type '%s'" % (allvar[0], self.vtype))
		elif self.vtype == 'xy':
			for i in allvar:
				if i not in ['x', 'y']:
					raise ValueError("Variable '%s' not valid for vector type '%s'" % (i, self.vtype))
			for i in ['x', 'y']:
				if i not in allvar:
					self.const.append(i)
					self.constvalues.append(0.0)
		elif self.vtype == 'xyz':
			for i in allvar:
				if i not in ['x', 'y', 'z']:
					raise ValueError("Variable '%s' not valid for vector type '%s'" % (i, self.vtype))
			for i in ['x', 'y', 'z']:
				if i not in allvar:
					self.const.append(i)
					self.constvalues.append(0.0)
		elif self.vtype == 'pol':
			for i in allvar:
				if i not in ['', 'r', 'phi']:
					raise ValueError("Variable '%s' not valid for vector type '%s'" % (i, self.vtype))
			if '' not in allvar and 'r' not in allvar:
				raise ValueError("Variable '' or 'r' required for vector type '%s', but missing" % self.vtype)
			if 'phi' not in allvar:
				self.const.append('phi')
				self.constvalues.append(0.0)
		elif self.vtype == 'cyl':
			for i in allvar:
				if i not in ['', 'r', 'phi', 'z']:
					raise ValueError("Variable '%s' not valid for vector type '%s'" % (i, self.vtype))
			if '' not in allvar and 'r' not in allvar:
				raise ValueError("Variable '' or 'r' required for vector type '%s', but missing" % self.vtype)
			for i in ['phi', 'z']:
				if i not in allvar:
					self.const.append(i)
					self.constvalues.append(0.0)
		elif self.vtype == 'sph':
			for i in allvar:
				if i not in ['', 'r', 'theta', 'phi']:
					raise ValueError("Variable '%s' not valid for vector type '%s'" % (i, self.vtype))
			if '' not in allvar and 'r' not in allvar:
				raise ValueError("Variable '' or 'r' required for vector type '%s', but missing" % self.vtype)
			for i in ['theta', 'phi']:
				if i not in allvar:
					self.const.append(i)
					self.constvalues.append(0.0)
		self.shape = tuple(self.shape)

	def __getitem__(self, idx):
		"""Get an instance of the (flat) array (argument is int) OR get the grid for a component (argument is str)"""
		if isinstance(idx, str):
			return self.get_grid(idx)
		elif isinstance(idx, (int, np.integer)):
			# preformance warning: OK for once, avoid calling in sequence
			flatvalues = [gr.flatten() for gr in self.get_grid()]
			flatvec = np.array(flatvalues).transpose()
			return Vector(*(flatvec[idx]), astype = self.vtype, deg = self.degrees)
		else:
			raise IndexError

	def get_array(self, comp = None):
		"""Get array(s), i.e., factorized values

		Argument:
		comp   String or None. If None, then return a tuple of the values
		       (arrays) for all variable components. If 'all', return a tuple of
		       the values of all (including constant) components. If a string
		       matching a component (e.g., 'x') return the values; this works
		       for variable and constant components alike.
		"""
		if comp is None:
			return tuple([np.array(val) for val in self.values])
		elif comp == 'all':
			return tuple([self.get_array(c) for c in self.get_components()])
		elif comp in self.var:
			i = self.var.index(comp)
			return np.array(self.values[i])
		elif comp in self.const:
			i = self.const.index(comp)
			return np.array([self.constvalues[i]])
		else:
			raise KeyError("Component '%s' is not defined" % comp)

	def get_components(self, include_prefix = False):
		"""Get natural components for the vector type

		Argument:
		include_prefix  True or False. Whether to append the prefix to the
		                vector components.

		Returns:
		List of strings.
		"""
		if self.vtype in ['x', 'y', 'z']:
			components = [self.vtype]
		elif self.vtype == 'xy':
			components = ['x', 'y']
		elif self.vtype == 'xyz':
			components = ['x', 'y', 'z']
		elif self.vtype == 'pol':
			components = ['r', 'phi']
		elif self.vtype == 'cyl':
			components = ['r', 'phi', 'z']
		elif self.vtype == 'sph':
			components = ['r', 'theta', 'phi']
		else:
			raise ValueError("Invalid vtype")
		if include_prefix:
			return [self.prefix if c == 'r' else self.prefix + c for c in components]
		else:
			return components

	def get_grid(self, comp = None):
		"""Get grid for one or more components.

		Arguments:
		comp   String or None. If a string, this must be one of the components
		       in which the VectorGrid is defined. If None, use the 'natural'
		       components.
		"""
		if isinstance(comp, str):
			return self.get_array(comp)
		elif isinstance(comp, list):
			axisarrays = (self.get_array(c) for c in comp)
			return np.meshgrid(*axisarrays, indexing = 'ij')
		elif comp is None:
			axisarrays = (self.get_array(c) for c in self.get_components())
			return np.meshgrid(*axisarrays, indexing = 'ij')
		else:
			raise TypeError

	def get_values(self, comp, flat = True):
		"""Get (flat) values for a vector component.
		Unlike get_grid(), this does not necessarily have to be one of the
		components in which the VectorGrid is defined.

		Arguments:
		comp   String. The vector component.
		flat   True or False. If True, return a one-dimensional array over all
		       vectors in the grid. If False, return an array the same shape as
		       the VectorGrid (like self.shape).

		Returns:
		A numpy array of floats.
		"""
		flatcomp = np.array([v.component(comp, prefix = self.prefix) for v in self])
		return flatcomp if flat else flatcomp.reshape(self.shape)

	def __iter__(self):
		"""Iterator over flat array; yields Vector instances"""
		flatvalues = [gr.flatten() for gr in self.get_grid()]
		flatvec = np.array(flatvalues).transpose()
		for v in flatvec:
			yield Vector(*v, astype = self.vtype, deg = self.degrees)

	def __len__(self):
		"""Get total array size"""
		size = 1
		for x in self.shape:
			size *= x
		return size

	def subgrid_shapes(self, dim):
		"""Get total shape of d-dimensional subgrids (d = argument dim)"""
		if dim == 0 or dim > len(self.shape):
			return []
		elif dim == 1:
			return [(s,) for s in self.shape]
		else:
			return list(itertools.combinations(self.shape, dim))

	def __min__(self):
		"""Get a vector of minimal length (if not unique, return one of them)"""
		if len(self) == 0:
			return None
		vmin, lmin = self[0], self[0].len()
		for v in self:
			if v.len() < lmin:
				vmin = v
				lmin = v.len()
		return vmin

	def __max__(self):
		"""Get a vector of maximal length (if not unique, return one of them)"""
		if len(self) == 0:
			return None
		vmax, lmax = self[0], self[0].len()
		for v in self:
			if v.len() > lmax:
				vmax = v
				lmax = v.len()
		return vmax

	def __eq__(self, other):
		"""Test equality with another VectorGrid instance"""
		if isinstance(other, VectorGrid):
			return self.var == other.var and self.const == other.const and \
				self.vtype == other.vtype and \
				np.array_equal(self.values, other.values) and \
				np.array_equal(self.constvalues, other.constvalues)
		else:
			# We raise a TypeError exception rather than returning
			# NotImplemented, because we want to forbid comparisons with numpy
			# types, which would invoke array expansion because VectorGrid is
			# iterable.
			raise TypeError("Comparison must be with another VectorGrid instance")

	def index(self, v, flat = True, acc = None, angle_fold = True, fast_method_only = True):
		"""Return index of a given vector. Acts as a 'find' function.

		This function employs two methods: The 'fast method' compares the
		components of the input vector to that of the arrays (variable and
		constant) values of the vector grid. The 'slow method' finds vectors
		by equality (of Vector instances).

		Arguments:
		v                 Vector instance or float.
		flat              True or False. If True, return index in flat array. If
		                  False, return (multi-dimensional) index in the grid.
		acc               Float or None. If float, the maximum difference for
		                  two vectors or values to be considered equal. If None,
		                  find vectors by minimal distance (uses the slow method
		                  only).
		angle_fold        True or False. Whether to permit folding for angular
		                  vector types.
		fast_method_only  True or False. If True, return None if no match could
		                  be found using the fast method. If False, retry using
		                  the slow method.

		Returns:
		An integer (flat = True) or array/tuple of integers (flat = False).
		"""
		if acc is None:
			diff = np.array([w - v for w in self])
			idx = np.argmin(diff)
			return idx if flat else np.unravel_index(idx, self.shape)
		elif isinstance(v, Vector) and v.vtype == self.vtype:
			components = v.components()
			values = [v.value] if not isinstance(v.value, (list, tuple, np.ndarray)) else v.value
			idx = []
			full_angle = 360 if self.degrees else 2 * np.pi
			for co, val in zip(components, values):
				if co in self.const:
					cval = self.constvalues[self.const.index(co)]
					if abs(cval - val) > acc:
						return None
				elif co in self.var:
					if co.endswith('phi'):
						diff = diff_mod(self.values[self.var.index(co)], val, full_angle)
					else:
						diff = np.abs(self.values[self.var.index(co)] - val)
					idx1 = np.argmin(diff)
					if diff[idx1] < acc:
						idx.append(idx1)
					else:
						break
				else:
					break
			if len(idx) == len(self.var):
				return np.ravel_multi_index(idx, self.shape) if flat else tuple(idx)
			elif angle_fold and v.vtype == 'pol':
				r, phi = v.value
				v1 = Vector(-r, phi + full_angle / 2, astype = 'pol', deg = self.degrees)
				return self.index(v1, flat = flat, acc = acc, angle_fold = False)
			elif angle_fold and v.vtype == 'cyl':
				r, phi, z = v.value
				v1 = Vector(-r, phi + full_angle / 2, z, astype = 'cyl', deg = self.degrees)
				return self.index(v1, flat = flat, acc = acc, angle_fold = False)
			elif angle_fold and v.vtype == 'sph':
				r, theta, phi = v.value
				v1 = Vector(-r, full_angle / 2 - theta, phi + full_angle / 2, astype = 'sph', deg = self.degrees)
				return self.index(v1, flat = flat, acc = acc, angle_fold = False)
			elif fast_method_only:
				return None
			# else: fallthrough to 'slow' method

		diff = np.array([w - v for w in self])
		idx = np.argmin(diff)
		if acc is not None and self[idx] - v > acc:
			return None
		return idx if flat else np.unravel_index(idx, self.shape)

	def get_var_const(self, return_tuples = False, use_prefix = True):
		"""Find variables and constants

		Arguments:
		use_prefix      True or False. If True (default), add the prefix. If
		                False, return the bare variable names.
		return_tuples   True or False. How to handle the return values. If False
		                (default), then reduce 0-tuple to None and 1-tuple to
		                its single element. If True, always return tuples.

		Returns:
		val       Tuple of values (arrays) for variable components.
		var       Tuple of strings. The variable components.
		constval  Tuple of floats or None. The constant values. None is returned
		          when there are no constant values.
		const     Tuple of strings. The constant components. None is returned
		          when there are no constant values.
		"""
		val = tuple(self.values)
		constval = tuple(self.constvalues)
		if use_prefix:
			var = tuple([add_var_prefix(v, self.prefix) for v in self.var])
			const = tuple([add_var_prefix(c, self.prefix) for c in self.const])
		else:
			var = tuple(self.var)
			const = tuple(self.const)
		if return_tuples:
			return val, var, constval, const

		if len(self.const) == 0:
			constval, const = None, None
		elif len(self.const) == 1:
			constval = self.constvalues[0]
			const = add_var_prefix(self.const[0], self.prefix) if use_prefix else self.const[0]
		if len(self.var) == 0:
			val, var = None, None
		elif len(self.var) == 1:
			val = self.values[0]
			var = add_var_prefix(self.var[0], self.prefix) if use_prefix else self.var[0]
		return val, var, constval, const

	def select(self, *arg, flat = True, acc = 1e-10, fold = None, deg = None):
		"""Select certain vectors in the grid.
		The argument specifies the component values that should match. For
		example, grid.select('x', 0.1) returns all vectors with component x
		equal to 0.1.

		Arguments:
		*arg    What to match. If a dict, it must be of the form {component:
		        value, ...}. If a string and a value, interpret as single
		        component and value. If two lists/tuples, interpret as multiple
		        components and respective values.
		flat    True or False. If True, return index in flat array. If False,
		        return (multi-dimensional) index in the grid.
		acc     Float. The maximum difference for two vectors to be considered
		        equal.
		fold    None. Not (yet) implemented.
		deg     True or False. Whether to interpret input values of angular
		        components as values in degrees (True) or radians (False).

		Returns:
		indices  Array of integers (flat = True) or multidimensional array
		         of multi-indices (flat = False)
		vectors  List of Vector instances. Only if flat = True.
		"""

		if len(arg) == 1 and isinstance(arg[0], dict):
			matchval = arg[0]
		elif len(arg) == 2 and isinstance(arg[0], str) and isrealnum(arg[1]):
			matchval = {arg[0]: arg[1]}
		elif len(arg) == 2 and isinstance(arg[0], (list, tuple)) and isinstance(arg[1], (list, tuple)):
			matchval = {}
			for var, val in zip(arg[0], arg[1]):
				if not isinstance(var, str):
					raise TypeError("Input must be a list of strings")
				if not isrealnum(val):
					raise TypeError("Input must be a list of numerical values")
				matchval[var] = val
		else:
			raise TypeError("Invalid combination of arguments")

		l = len(self)
		if fold is not None:
			raise NotImplementedError
		else:
			sel = np.ones(l, dtype = bool)
			for var in matchval:
				if (var.endswith('phi') or var.endswith('theta')) and deg is not None:
					if deg and not self.degrees:
						matchval[var] *= np.pi / 180.
					elif not deg and self.degrees:
						matchval[var] *= 180. / np.pi
				if var in self.const:
					constval = self.constvalues[self.const.index(var)]
					if abs(matchval[var] - constval) > acc:
						sel = np.zeros(l, dtype = bool)
						break
				else:
					values = self.get_values(var, flat = True)
					sel = sel & (np.abs(values - matchval[var]) < acc)
		indices = np.arange(0, l)[sel]
		vectors = [v for v, s in zip(self, sel) if s]
		if flat:
			return indices, vectors
		else:
			return np.unravel_index(indices, self.shape)

	def subdivide(self, comp, subdivisions, quadratic = None):
		"""Subdivide the grid

		Arguments:
		comp          String or None. Which component to subdivide. If the grid
		              is 1-dimensional, the value None means the only variable
		              component.
		subdivisions  Integer. The number of subdivisions, i.e.,
		              step_new = step_old / subdivisions.
		quadratic     True, False, or None. Whether the grid is quadratic (True)
		              or linear (False). If None, determine it automatically.

		Returns:
		A new VectorGrid instance.
		"""
		if comp is None:
			if len(self.var) != 1:
				raise ValueError("Component can only be None for 1D grids")
			comp = self.var[0]
		elif comp not in self.var:
			raise ValueError("Only variable components can be subdivided")
		if not isinstance(subdivisions, (int, np.integer)):
			raise TypeError("Argument subdivisions should be a positive integer")
		if subdivisions <= 0:
			raise ValueError("Argument subdivisions should be strictly positive")
		if subdivisions == 1:
			return self
		j = self.var.index(comp)
		oldvalues = self.values[j]
		n = len(oldvalues)
		if quadratic is None:  # determine quadratic range automatically
			if n < 3:
				quadratic = False
			else:
				quadratic = (abs((oldvalues[2] - oldvalues[0]) / (oldvalues[1] - oldvalues[0]) - 4.0) < 0.01)
		if quadratic:
			oldindex = np.arange(0, n)**2
			newindex = np.linspace(0, n - 1, (n - 1) * subdivisions + 1)**2
		else:
			oldindex = np.arange(0, n)
			newindex = np.linspace(0, n - 1, (n - 1) * subdivisions + 1)
		newvalues = np.interp(newindex, oldindex, oldvalues)

		# Construct new VectorGrid
		newarg = []
		for var, val in zip(self.var, self.values):
			newarg.append(var)
			newarg.append(newvalues if var == comp else val)
		for const, constval in zip(self.const, self.constvalues):
			newarg.append(const)
			newarg.append(constval)
		return VectorGrid(*tuple(newarg), astype = self.vtype, deg = self.degrees, prefix = self.prefix)
		# TODO: Subdivisions over multiple variables

	def subdivide_to(self, comp, n_target, quadratic = None):
		"""Subdivide the grid

		Arguments:
		comp          String or None. Which component to subdivide. If the grid
		              is 1-dimensional, the value None means the only variable
		              component.
		n_target      Integer. The minimum number of grid points in the new
		              grid. The new step size is chosen to be commensurate with
		              the old one.
		quadratic     True, False, or None. Whether the grid is quadratic (True)
		              or linear (False). If None, determine it automatically.

		Returns:
		A new VectorGrid instance.
		"""
		if comp is None:
			if len(self.var) != 1:
				raise ValueError("Component can only be None for 1D grids")
			comp = self.var[0]
		elif comp not in self.var:
			raise ValueError("Only variable components can be subdivided")
		j = self.var.index(comp)
		oldvalues = self.values[j]
		n = len(oldvalues)
		if (n_target - 1) % (n - 1) != 0:
			raise ValueError("Target size is incommensurate with input size")
		subdivisions = (n_target - 1) // (n - 1)
		return self.subdivide(comp, subdivisions, quadratic = quadratic)

	def symmetrize(self, axis = None, deg = None):
		"""Symmetrize the vector grid by applying a transformation.

		Arguments:
		axis   String or VectorTransformation instance, or None. If a string,
		       the axis or axes in which to apply reflection. If a
		       VectorTransformation instance, define new grid points by applying
		       the transformation to the existing grid. None is equivalent to
		       'xyz'.
		deg    True, False, or None. Whether the angular units of the new grid
		       are degrees (True), radians (False), or the same as the present
		       instance (None).

		Returns:
		newgrid    A new VectorGrid instance
		mapping    If axis is a VectorTransformation instance, then a numpy
		           array of integers. Set such that mapping[i] = j means that
		           vector with index i of the present grid maps to vector with
		           index j of the new grid. If axis is a string, then mapping is
		           a dict {component: map, ...}, where map is such a mapping as
		           for axis = VectorTransformation.

		Note:
		These are essentially two versions of the same version: The 'old style'
		using reflections and the 'new style' using VectorTransformation.
		Eventually, we might abandon the 'old style'.
		"""
		if deg is None:
			deg = self.degrees
		# Default axis (None) is equivalent to 'xyz'

		if isinstance(axis, VectorTransformation):
			tfm = axis  # TODO: rename variable
			tgrid = tfm(self)
			newgrid = self.extend(tgrid).sort()[0]
			mapping = -np.ones(np.prod(newgrid.shape), dtype = int)
			for j, v in enumerate(self):
				i = newgrid.index(v, flat = True, acc = 1e-10)
				if mapping[i] == -1:
					mapping[i] = j
			invtfm = tfm.inv()
			for i, v in enumerate(newgrid):
				if mapping[i] == -1:
					j = self.index(invtfm(v), flat = True, acc = 1e-10)
					if j is None:
						sys.stderr.write("ERROR (VectorGrid.symmetrize): Result is not a grid [transformation %s].\n" % (tfm.name))
						return None, None
					mapping[i] = j
			return newgrid, mapping
		elif axis is None:
			axis = 'xyz'
		elif axis not in ['', 'x', 'y', 'z', 'xy', 'xyz']:
			raise ValueError("Invalid axis")
		if self.vtype == 'x':
			newval, xmap = reflect_array(self.get_array('x')) if 'x' in axis else no_reflect_array(self.get_array('x'))
			newgrid = VectorGrid('x', newval, astype = 'x', deg = deg, prefix = self.prefix)
			mapping = {'x': xmap}
		elif self.vtype == 'y':
			newval, ymap = reflect_array(self.get_array('y')) if 'y' in axis else no_reflect_array(self.get_array('y'))
			newgrid = VectorGrid('y', newval, astype = 'y', deg = deg, prefix = self.prefix)
			mapping = {'y': ymap}
		elif self.vtype == 'z':
			newval, zmap = reflect_array(self.get_array('z')) if 'z' in axis else no_reflect_array(self.get_array('z'))
			newgrid = VectorGrid('z', newval, astype = 'z', deg = deg, prefix = self.prefix)
			mapping = {'z': zmap}
		elif self.vtype == 'xy':
			newxval, xmap = reflect_array(self.get_array('x')) if 'x' in axis else no_reflect_array(self.get_array('x'))
			newyval, ymap = reflect_array(self.get_array('y')) if 'y' in axis else no_reflect_array(self.get_array('y'))
			newgrid = VectorGrid('x', newxval, 'y', newyval, astype = 'xy', deg = deg, prefix = self.prefix)
			mapping = {'x': xmap, 'y': ymap}
		elif self.vtype == 'xyz':
			newxval, xmap = reflect_array(self.get_array('x')) if 'x' in axis else no_reflect_array(self.get_array('x'))
			newyval, ymap = reflect_array(self.get_array('y')) if 'y' in axis else no_reflect_array(self.get_array('y'))
			newzval, zmap = reflect_array(self.get_array('z')) if 'z' in axis else no_reflect_array(self.get_array('z'))
			newgrid = VectorGrid('x', newxval, 'y', newyval, 'z', newzval, astype = 'xyz', deg = deg, prefix = self.prefix)
			mapping = {'x': xmap, 'y': ymap, 'z': zmap}
		elif self.vtype == 'pol':
			if len(self.get_array('phi')) == 1 and axis in ['xy', 'xyz']:
				rval, rmap = reflect_array(self.get_array('r'))
				newphival, phimap = no_reflect_array(self.get_array('phi'))
			else:
				rval, rmap = no_reflect_array(self.get_array('r'))
				newphival, phimap = reflect_angular_array(self.get_array('phi'), axis, self.degrees)
			newgrid = VectorGrid('r', rval, 'phi', newphival, astype = 'pol', deg = deg, prefix = self.prefix)
			mapping = {'r': rmap, 'phi': phimap}
		elif self.vtype == 'cyl':
			if len(self.get_array('phi')) == 1 and axis in ['xy', 'xyz']:
				rval, rmap = reflect_array(self.get_array('r'))
				newphival, phimap = no_reflect_array(self.get_array('phi'))
			else:
				rval, rmap = no_reflect_array(self.get_array('r'))
				newphival, phimap = reflect_angular_array(self.get_array('phi'), axis, self.degrees)
			newzval, zmap = reflect_array(self.get_array('z')) if 'z' in axis else self.get_array('z')
			newgrid = VectorGrid('r', rval, 'phi', newphival, 'z', newzval, astype = 'cyl', deg = deg, prefix = self.prefix)
			mapping = {'r': rmap, 'phi': phimap, 'z': zmap}
		elif self.vtype == 'sph':
			if len(self.get_array('phi')) == 1 and len(self.get_array('theta')) == 1 and axis == 'xyz':
				rval, rmap = reflect_array(self.get_array('r'))
				newthetaval, thetamap = no_reflect_array(self.get_array('theta'))
				newphival, phimap = no_reflect_array(self.get_array('phi'))
			else:
				rval, rmap = no_reflect_array(self.get_array('r'))
				newthetaval, thetamap = reflect_array(self.get_array('theta'), offset = 180.0 if self.degrees else np.pi) if 'z' in axis else self.get_array('theta')
				newphival, phimap = reflect_angular_array(self.get_array('phi'), axis, self.degrees)
			newgrid = VectorGrid('r', rval, 'theta', newthetaval, 'phi', newphival, astype = 'sph', deg = deg, prefix = self.prefix)
			mapping = {'r': rmap, 'theta': thetamap, 'phi': phimap}
		return newgrid, mapping

	def integration_element(self, dk = None, dphi = None, full = True, flat = True):
		"""Get integration elements.
		The function applies an appropriate multiplication factor if the input
		is only	a fraction of the Brillouin zone, e.g., in the first quadrant.

		Arguments:
		dk    Float or None. Step size in the radial direction.
		dphi  Float or None. Step size in the angular direction.
		full  True or False. Whether to extend to a full circle or square, if
		      the vector grid spans it only partially.
		flat  True or False. If True, the output array will be one-dimensional.
		      If False, it will have the same shape as the grid.

		Returns:
		A numpy array, which may be multi-dimensional if flat is False and if
		the grid also has this property.

		Note:
		See linear_integration_element() and quadratic_integration_element() for
		more details.
		"""
		if 'x' in self.var and 'y' in self.var:  # Cartesian
			xval = self.get_array('x')
			yval = self.get_array('y')
			dx = linear_integration_element(xval, fullcircle = False)
			dy = linear_integration_element(yval, fullcircle = False)
			mult = 1.0
			if full and abs(min(xval)) < 1e-9:
				mult *= 2.0
			if full and abs(min(yval)) < 1e-9:
				mult *= 2.0
			da = np.outer(dx, dy) * mult
			return da.flatten() if flat else da
		elif 'x' in self.var:  # 1D, along x
			xval = self.get_array('x')
			rmax = np.amax(np.abs(xval))
			return circular_integration_element(xval, dk, rmax, full = full)
		elif 'y' in self.var:  # 1D, along y
			yval = self.get_array('y')
			rmax = np.amax(np.abs(yval))
			return circular_integration_element(yval, dk, rmax, full = full)
		elif 'z' in self.var and len(self.var) == 1:  # 1D, along z
			zval = self.get_array('z')
			mult = 1.0
			# mult = 2.0 if full and abs(min(zval)) < 1e-9 else 1.0
			return linear_integration_element(zval, fullcircle = False) * mult
		elif self.vtype == 'pol' and 'phi' in self.var:
			rval = self.get_array('r')
			phival = self.get_array('phi')
			if self.degrees:
				phival *= np.pi / 180.
			rmax = np.amax(np.abs(rval))
			dr2 = quadratic_integration_element(rval, dk, rmax)
			dphi = linear_integration_element(phival, dphi, phival.min(), phival.max(), full)
			da = np.outer(dr2, dphi)
			return da.flatten() if flat else da
		elif self.vtype == 'pol' and 'phi' not in self.var:
			rval = self.get_array('r')
			rmax = np.amax(np.abs(rval))
			return circular_integration_element(rval, dk, rmax)
		else:
			sys.stderr.write("Warning (VectorGrid.integration_element): Not yet implemented for this type (%s) and/or combination of components %s\n" % (self.vtype, tuple(self.var)))
			return None

	def volume(self, *args, **kwds):
		"""Return the total volume of the grid
		This is simply the sum over all integration elements.
		TODO: Return more accurate values from min and max values of self.var.
		"""
		ie = self.integration_element(*args, **kwds)
		return np.nan if ie is None else np.sum(ie)

	def jacobian(self, component, unit=False):
		"""Return the Jacobian for calculating a derivative.

		This function returns the derivatives dvi/dc, where vi are the natural
		components of the vector grid and c is the input component. This is used
		for a variable substitution. The result is the ingredient for the chain
		rule:
		df/dc = df/dv1 * dv1/dc + df/dv2 * dv2/dc + df/dv3 * dv3/dc.
		If the option unit is set to True, then return the derivatives with
		respect to the unit vectors, thus one obtains the derivatives dui/dc in
		∇f.unitvec(c) = df/dv1 * du1/dc + df/dv2 * du2/dc + df/dv3 * du3/dc;
		note that dui/dc and dvi/dc only differ if c is an angular coordinate,
		φ (phi) or θ (theta).

		Notes:
		The angular coordinates φ (phi) and θ (theta) are converted to radians.
		Arrays will contain NaN values in singular points.

		Arguments:
		component   String. The input component c.
		unit        True or False. If False, return the derivatives dvi/dc as
		            is. If True, scale the values, i.e., return dui/dc; this
		            option affects the φ (phi) and θ (theta) derivatives only.

		Returns:
		dv1_dc   Float or numpy array. Either a numerical value (constant) or a
		         d-dimensional array, where d is the dimensionality of the
		         vector grid.
		dv2_dc   Float or numpy array. Only if d >= 2.
		dv3_dc   Float or numpy array. Only if d == 3.
		"""
		nan = float('nan')
		if component == self.prefix or component == '':
			component = 'r'
		elif component.startswith(self.prefix):
			component = component[len(self.prefix):]
		if component not in ['r', 'x', 'y', 'z', 'phi', 'theta']:
			raise ValueError("Argument component must resolve to 'r', 'x', 'y', 'z', 'phi', or 'theta'.")

		if self.vtype in ['x', 'y', 'z']:
			if component == self.vtype:
				return (1.0,)
			elif component == 'r':
				# dx/dr = sgn(r) where r = |x|
				xyz = self.get_grid(self.vtype)
				return (np.sign(xyz, where = (xyz >= 1e-6)),)
			else:
				return (nan,)
		elif self.vtype == 'xy':
			x, y = [np.squeeze(a) for a in self.get_grid()]
			if component == 'x':
				return 1.0, 0.0
			elif component == 'y':
				return 0.0, 1.0
			elif component == 'r':
				# dx/dr = x / r, dy/dr = y / r
				r = np.sqrt(x**2 + y**2)
				dxdr = np.divide(x, r, where = (r >= 1e-6))
				dydr = np.divide(y, r, where = (r >= 1e-6))
				dxdr[r < 1e-6] = nan
				dydr[r < 1e-6] = nan
				return dxdr, dydr
			elif component == 'phi':
				if unit:
					r = np.sqrt(x**2 + y**2)
					dxdphi = np.divide(-y, r, where = (r >= 1e-6))
					dydphi = np.divide(x, r, where = (r >= 1e-6))
					dxdphi[r < 1e-6] = nan
					dydphi[r < 1e-6] = nan
					return dxdphi, dydphi
				else:
					return -y, x  # dx/dφ = -y, dy/dφ = x
			else:
				return nan, nan
		elif self.vtype == 'pol':
			r, phi = [np.squeeze(a) for a in self.get_grid()]
			if self.degrees:
				phi *= np.pi / 180.0
			if component == 'r':
				return 1.0, 0.0
			elif component == 'phi':
				if unit:
					dphidphi = np.divide(1, r, where = (r >= 1e-6))
					dphidphi[r < 1e-6] = nan
					return 0.0, dphidphi
				else:
					return 0.0, 1.0
			elif component == 'x':
				# dr/dx = cos(φ), dφ/dx = -sin(φ) / r
				drdx = np.cos(phi)
				dphidx = np.divide(-np.sin(phi), r, where = (r >= 1e-6))
				drdx[r < 1e-6] = nan
				dphidx[r < 1e-6] = nan
				return drdx, dphidx
			elif component == 'y':
				# dr/dy = sin(φ), dφ/dy = cos(φ) / r
				drdy = np.sin(phi)
				dphidy = np.divide(np.cos(phi), r, where = (r >= 1e-6))
				drdy[r < 1e-6] = nan
				dphidy[r < 1e-6] = nan
				return drdy, dphidy
			else:
				return nan, nan
		elif self.vtype == 'xyz':
			x, y, z = [np.squeeze(a) for a in self.get_grid()]
			if component == 'x':
				return 1.0, 0.0, 0.0
			elif component == 'y':
				return 0.0, 1.0, 0.0
			elif component == 'z':
				return 0.0, 0.0, 1.0
			elif component == 'r':
				# dx/dr = x / r, dy/dr = y / r, dz / dr = z / r
				r = np.sqrt(x**2 + y**2 + z**2)
				dxdr = np.divide(x, r, where = (r >= 1e-6))
				dydr = np.divide(y, r, where = (r >= 1e-6))
				dzdr = np.divide(z, r, where = (r >= 1e-6))
				dxdr[r < 1e-6] = nan
				dydr[r < 1e-6] = nan
				dzdr[r < 1e-6] = nan
				return dxdr, dydr, dzdr
			elif component == 'theta':
				# dx/dθ = xz / R, dy/dθ = yz / R, dz / dθ = -R with R = sqrt(x^2 + y^2)
				R = np.sqrt(x**2 + y**2)
				if unit:
					# ∇f.unitvec(θ) = (1/r) df/dθ with r = sqrt(x^2 + y^2 + z^2)
					r = np.sqrt(x**2 + y**2 + z**2)
					dxdtheta = np.divide(x * z, R * r, where = (R >= 1e-6))
					dydtheta = np.divide(y * z, R * r, where = (R >= 1e-6))
					dzdtheta = np.divide(-R, r, where = (R >= 1e-6))
				else:
					dxdtheta = np.divide(x * z, R, where = (R >= 1e-6))
					dydtheta = np.divide(y * z, R, where = (R >= 1e-6))
					dzdtheta = -R
				dxdtheta[R < 1e-6] = nan
				dydtheta[R < 1e-6] = nan
				dzdtheta[R < 1e-6] = nan
				return dxdtheta, dydtheta, dzdtheta
			elif component == 'phi':
				if unit:
					r = np.sqrt(x**2 + y**2)
					dxdphi = np.divide(-y, r, where = (r >= 1e-6))
					dydphi = np.divide(x, r, where = (r >= 1e-6))
					dxdphi[r < 1e-6] = nan
					dydphi[r < 1e-6] = nan
					return dxdphi, dydphi, 0.0
				else:
					return -y, x, 0.0  # dx/dφ = -y, dy/dφ = x, dz/dφ = 0
			else:
				return nan, nan, nan
		elif self.vtype == 'cyl':
			r, phi, z = [np.squeeze(a) for a in self.get_grid()]
			if self.degrees:
				phi *= np.pi / 180.0
			if component == 'r':
				return 1.0, 0.0, 0.0
			elif component == 'phi':
				if unit:
					# ∇f.unitvec(φ) = (1/r) df/dφ
					dphidphi = np.divide(1, r, where = (r >= 1e-6))
					dphidphi[r < 1e-6] = nan
					return 0.0, dphidphi, 0.0
				else:
					return 0.0, 1.0, 0.0
			elif component == 'x':
				# dr/dx = cos(φ), dφ/dx = -sin(φ) / r, dz/dx = 0
				drdx = np.cos(phi)
				dphidx = np.divide(-np.sin(phi), r, where = (r >= 1e-6))
				drdx[r < 1e-6] = nan
				dphidx[r < 1e-6] = nan
				return drdx, dphidx, 0.0
			elif component == 'y':
				# dr/dy = sin(φ), dφ/dy = cos(φ) / r, dz/dy = 0
				drdy = np.sin(phi)
				dphidy = np.divide(np.cos(phi), r, where = (r >= 1e-6))
				drdy[r < 1e-6] = nan
				dphidy[r < 1e-6] = nan
				return drdy, dphidy, 0.0
			elif component == 'z':
				return 0.0, 0.0, 1.0
			elif component == 'theta':
				# dr/dθ = z, dφ/dθ = 0, dz/dθ = -r with r = sqrt(x^2 + y^2)
				if unit:
					# ∇f.unitvec(θ) = (1/R) df/dθ
					# with R = sqrt(r^2 + z^2) = sqrt(x^2 + y^2 + z^2)
					rr = np.sqrt(r**2 + z**2)
					drdtheta = np.divide(z, rr, where = (rr >= 1e-6))
					dzdtheta = np.divide(-r, rr, where = (rr >= 1e-6))
					drdtheta[rr < 1e-6] = nan
					dzdtheta[rr < 1e-6] = nan
					return drdtheta, 0.0, dzdtheta
				else:
					return z, 0.0, -r
			else:
				return nan, nan, nan
		elif self.vtype == 'sph':
			r, theta, phi = [np.squeeze(a) for a in self.get_grid()]
			if self.degrees:
				theta *= np.pi / 180.0
				phi *= np.pi / 180.0
			if component == 'r':
				return 1.0, 0.0, 0.0
			elif component == 'theta':
				if unit:
					# ∇f.unitvec(θ) = (1/r) df/dθ
					dthetadtheta = np.divide(1, r, where = (r >= 1e-6))
					dthetadtheta[r < 1e-6] = nan
					return 0.0, dthetadtheta, 0.0
				else:
					return 0.0, 1.0, 0.0
			elif component == 'phi':
				if unit:
					# ∇f.unitvec(φ) = (1/R) df/dφ with R = r sin θ = sqrt(x^2 + y^2)
					R = r * np.sin(theta)
					dphidphi = np.divide(1, R, where = (R >= 1e-6))
					dphidphi[R < 1e-6] = nan
					return 0.0, 0.0, dphidphi
				else:
					return 0.0, 0.0, 1.0
			elif component == 'x':
				# dr/dx = x / r = sin θ cos φ
				# dθ/dx = xz / (r^2 R) = (1/r) cos θ cos φ
				# dφ/dx = -y / R^2 = -sin φ / r sin θ
				R = r * np.sin(theta)  # R = r sin θ
				drdx = np.sin(theta) * np.cos(phi)
				dthetadx = np.divide(np.cos(theta) * np.cos(phi), r, where = (r >= 1e-6))
				dphidx = np.divide(-np.sin(phi), R, where = (R >= 1e-6))
				drdx[r < 1e-6] = nan
				dthetadx[r < 1e-6] = nan
				dphidx[r < 1e-6] = nan
				return drdx, dthetadx, dphidx
			elif component == 'y':
				# dr/dy = y / r = sin θ sin φ
				# dθ/dy = yz / (r^2 R) = (1/r) cos θ sin φ
				# dφ/dy = x / R^2 = cos φ / r sin θ
				R = r * np.sin(theta)  # R = r sin θ
				drdy = np.sin(theta) * np.sin(phi)
				dthetady = np.divide(np.cos(theta) * np.sin(phi), r, where = (r >= 1e-6))
				dphidy = np.divide(np.cos(phi), R, where = (R >= 1e-6))
				drdy[r < 1e-6] = nan
				dthetady[r < 1e-6] = nan
				dphidy[r < 1e-6] = nan
				return drdy, dthetady, dphidy
			elif component == 'z':
				# dr/dz = cos θ, dθ/dz = -sin θ / r, dφ/dz = 0
				drdz = np.cos(theta)
				dthetadz = np.divide(-np.sin(theta), r, where = (r >= 1e-6))
				drdz[r < 1e-6] = nan
				dthetadz[r < 1e-6] = nan
				return drdz, dthetadz, 0.0
			else:
				return nan, nan, nan
		else:
			raise ValueError("Invalid value for self.vtype")

	def gradient_length_coeff(self):
		"""Return the Jacobian factors for calculating the length of the gradient.

		This function returns the coefficients ai, such that
		|∇f|^2 = a1 (df/dv1)^2 + a2 (df/dv2)^2 + a3 (df/dv3)^2
		where vi are the natural components of the vector grid. This result is
		equivalent to squaring the result of the function VectorGrid.jacobian()
		using the natural components of the vector grid and with unit=True.

		Notes:
		The derivatives in angular coordinates φ (phi) and θ (theta) in the
		above expression should be in radians for the result to be correct.
		Arrays will contain NaN values in singular points.

		Returns:
		a1       Float or numpy array. Either a numerical value (constant) or a
		         d-dimensional array, where d is the dimensionality of the
		         vector grid.
		a2       Float or numpy array. Only if d >= 2.
		a3       Float or numpy array. Only if d == 3.
		"""
		nan = float('nan')
		if self.vtype in ['x', 'y', 'z']:
			return (1.0,)
		elif self.vtype == 'xy':
			return 1.0, 1.0
		elif self.vtype == 'pol':
			# |∇f|^2 = (df/dr)^2 + (1/r^2) (df/dφ)^2
			r, _ = [np.squeeze(a) for a in self.get_grid()]
			a2 = np.divide(1.0, r**2, where = (r >= 1e-6))
			a2[r < 1e-6] = nan
			return 1.0, a2
		elif self.vtype == 'xyz':
			return 1.0, 1.0, 1.0
		elif self.vtype == 'cyl':
			# |∇f|^2 = (df/dr)^2 + (1/r^2) (df/dφ)^2 + (df/dz)^2
			r, _, _ = [np.squeeze(a) for a in self.get_grid()]
			a2 = np.divide(1.0, r**2, where = (r >= 1e-6))
			a2[r < 1e-6] = nan
			return 1.0, a2, 1.0
		elif self.vtype == 'sph':
			# |∇f|^2 = (df/dr)^2 + (1/r^2) (df/dθ)^2 + (1/rsinφ)^2 (df/dφ)^2
			r, theta, _ = [np.squeeze(a) for a in self.get_grid()]
			if self.degrees:
				theta *= np.pi / 180.
			R = r * np.sin(theta)
			a2 = np.divide(1.0, r**2, where = (r >= 1e-6))
			a3 = np.divide(1.0, R**2, where = (R >= 1e-6))
			a2[r < 1e-6] = nan
			a3[r < 1e-6] = nan
			return 1.0, a2, a3
		else:
			raise ValueError("Invalid value for self.vtype")

	def get_derivative_components(self):
		if self.vtype in ['xyz', 'cyl', 'sph'] and len(self.var) == 3:
			return ['', 'r', 'x', 'y', 'z', 'theta', 'phi']
		if len(self.var) == 2:
			var = tuple(self.var)
			deriv_components_2d = {
				('x', 'y'):       ['r', 'x', 'y', 'phi'],
				('x', 'z'):       ['r', 'x', 'z', 'theta'],
				('y', 'z'):       ['r', 'y', 'z', 'theta'],
				('r', 'phi'):     ['', 'r', 'x', 'y', 'phi'],
				('r', 'z'):       ['', 'r', 'x', 'y', 'z', 'theta'],
				('phi', 'z'):     ['x', 'y', 'z', 'theta', 'phi'],
				('r', 'theta'):   ['', 'r', 'x', 'y', 'z', 'theta'],
				('theta', 'phi'): ['x', 'y', 'z', 'theta', 'phi']
			}
			if var in deriv_components_2d:
				return deriv_components_2d[var]
			elif (var[1], var[0]) in deriv_components_2d:
				return deriv_components_2d[(var[1], var[0])]
			else:
				raise ValueError("Invalid combination of variables")
		if len(self.var) == 1:
			if self.var[0] == 'r':
				return ['', 'r']
			else:
				return [self.var[0]]
		raise ValueError("Invalid combination of variables")


	# Comparisons
	def identical(self, other, acc = 1e-9):
		"""Test identity of two VectorGrid instances.
		Two VectorGrid instances are identical if they are of the same shape,
		have the same vector type, and contain the same values in the same
		order.

		Arguments:
		other   VectorGrid instance. The second vector grid.
		acc     Float. The maximal difference between two values below which
		        they are considered equal.
		"""
		if not isinstance(other, VectorGrid):
			raise TypeError("Comparison must be with another VectorGrid instance")
		if self.ndim != other.ndim:
			return False
		if self.var != other.var or len(self.values) != len(other.values):
			return False
		if self.const != other.const or len(self.constvalues) != len(other.constvalues):
			return False
		if self.shape != other.shape:
			return False
		if self.vtype != other.vtype:
			return False
		for v1, v2 in zip(self.values, other.values):
			if len(v1) != len(v2):
				return False
			if np.amax(np.abs(v1 - v2)) > acc:
				return False
		for c1, c2 in zip(self.constvalues, other.constvalues):
			if abs(c1 - c2) > acc:
				return False
		return True

	def equal(self, other, acc = 1e-9):
		"""Test equality of two VectorGrid instances.
		Two VectorGrid instances are equal if they are of the same shape and
		have the same values in the same order, but possibly with a different
		vector type.

		Arguments:
		other   VectorGrid instance. The second vector grid.
		acc     Float. The maximal difference between two vectors below which
		        they are considered equal.
		"""
		if not isinstance(other, VectorGrid):
			raise TypeError("Comparison must be with another VectorGrid instance")
		if len(self) != len(other):
			return False
		for v1, v2 in zip(self, other):
			if not v1.equal(v2, acc):
				return False
		return True

	def get_subset(self, indices):
		"""Get subgrid of VectorGrid from (numpy style) array index.

		Arguments:
		indices    Tuple of integers and slice objects. A numpy style array
		           index.

		Returns:
		newgrid    VectorGrid instance. A new instance with the subset grid.
		"""
		if len(indices) > len(self.var):
			raise IndexError(f"Too many indices for VectorGrid of shape {self.shape}")
		newarg = []
		for var, val, idx in zip(self.var, self.values, indices):
			newarg.append(var)
			newarg.append(val[idx])
		for var, val in zip(self.const, self.constvalues):
			newarg.append(var)
			newarg.append(val)
		return VectorGrid(*tuple(newarg), astype = self.vtype, deg = self.degrees, prefix = self.prefix)

	def is_subset_of(self, other, acc = 1e-9):
		"""Test whether the present VectorGrid is a subset of another VectorGrid instance.
		The answer is True if all vectors from the present instance are
		contained also in the other instance. The comparison is preformed by
		identity, i.e., the vector types/components and the dimensionality must
		be identical for the answer to be possibly True.

		Arguments:
		other   VectorGrid instance. The second vector grid.
		acc     Float. The maximal difference between two values below which
		        they are considered equal.
		"""
		if self.ndim != other.ndim:
			return False
		comp1 = self.get_components()
		comp2 = other.get_components()
		if comp1 != comp2:
			return False
		for co in comp1:
			val1 = self.get_array(co)
			val2 = other.get_array(co)
			delta = np.abs(val1[:, np.newaxis] - val2[np.newaxis, :])
			if np.amax(np.amin(delta, axis = 1)) > acc:
				return False
		return True

	def is_compatible_with(self, other, acc = 1e-9):
		"""Test whether the union of two vector grids is a vector grid.
		Two VectorGrid instances are 'compatible' if their union again defines
		a grid. For this to be True, the values must be the same at all axes
		except for mostly one of them. (Think of this problem geometrically:
		When is the union of two rectangles again a rectangle?)

		Arguments:
		other   VectorGrid instance. The second vector grid.
		acc     Float. The maximal difference between two values below which
		        they are considered equal.
		"""
		comp1 = self.get_components()
		comp2 = other.get_components()
		if comp1 != comp2:
			return False

		n_nonequal = 0
		for co in comp1:
			val1 = self.get_array(co)
			val2 = other.get_array(co)
			delta = np.abs(val1[:, np.newaxis] - val2[np.newaxis, :])
			subset = (np.amax(np.amin(delta, axis = 1)) <= acc)
			superset = (np.amax(np.amin(delta, axis = 0)) <= acc)
			if not subset and not superset:
				n_nonequal += 1
		return n_nonequal <= 1  # the number of nonequal axes must be either zero or one

	def is_sorted(self, increasing = False, strict = True):
		"""Test whether the values are sorted.

		Arguments:
		increasing   True or False. If True, accept sorted values in ascending
		             (increasing) order only. If False, also accept reverse
		             (descending/decreasing) order also.
		strict       True or False. If True, the values must be strictly
		             monotonic for the function to return True. If False, also
		             accept equal subsequent values.

		Returns:
		True or False.
		"""
		if increasing:
			if strict:
				result = [np.all(np.diff(val) > 0) for val in self.values]
			else:
				result = [np.all(np.diff(val) >= 0) for val in self.values]
		else:
			if strict:
				result = [np.all(np.diff(val) > 0) or np.all(np.diff(val) < 0) for val in self.values]
			else:
				result = [np.all(np.diff(val) >= 0) or np.all(np.diff(val) <= 0) for val in self.values]
		return all(result)

	def zero(self):
		"""Test whether all vectors in the grid are zero."""
		return all([v.zero() for v in self])

	def is_vertical(self):
		"""Test whether VectorGrid has vertical (z) components only.
		The negation is useful to check for in-plane components of magnetic fields
		"""
		zaxis = Vector(1.0, astype = 'z')
		return all([v.parallel(zaxis) for v in self])

	def is_inplane(self):
		"""Test whether VectorGrid has in-plane (x, y) components only.
		The negation is useful to check for out-of-plane components of magnetic fields
		"""
		zaxis = Vector(1.0, astype = 'z')
		return all([v.perpendicular(zaxis) for v in self])

	def sort(self, in_place = False, flat_indices = False, expand_indices = False):
		"""Sort by value and provide sorting indices (like argsort).

		Arguments:
		in_place        True or False. If True, return the present VectorGrid
		                instance. If False, return a new instance.
		flat_indices    True or False. See comments for return value.
		expand_indices  True or False. See comments for return value.

		Returns:
		grid_new   The present VectorGrid instance or a new one.
		indices    Sort indices, comparable to the result of an 'argsort'. If
		           flat_indices and expand_indices are both False, return the
		           separate sort orders for the variable arrays. If flat_indices
		           is True, return the sort order of the flattened array. If
		           expand_indices is True, return a multi-dimensional array with
		           multi-indices. (The resulting array has dimension ndim + 1.)
		           flat_indices and expand_indices cannot be True
		           simultaneously.
		"""
		order = [np.argsort(val) for val in self.values]
		newval = [np.sort(val) for val in self.values]
		if flat_indices and expand_indices:
			raise ValueError("Arguments flat_indices and expand_indices cannot both be True.")
		elif flat_indices:
			grid_order = np.meshgrid(*order, indexing = 'ij')
			indices = np.ravel_multi_index([go.flatten() for go in grid_order], self.shape)
		elif expand_indices:
			grid_order = np.meshgrid(*order, indexing = 'ij')
			indices = np.stack(grid_order, axis = -1)
		else:
			indices = order
		if in_place:
			self.values = newval
			return self, indices
		else:
			newarg = []
			for var, val in zip(self.var, newval):
				newarg.append(var)
				newarg.append(val)
			for const, constval in zip(self.const, self.constvalues):
				newarg.append(const)
				newarg.append(constval)
			return VectorGrid(*tuple(newarg), astype = self.vtype, deg = self.degrees, prefix = self.prefix), indices

	def extend(self, other, acc = 1e-9):
		"""Extend the present VectorGrid instance with another one

		Arguments:
		other   VectorGrid instance. The second vector grid.
		acc     Float. The maximal difference between two values below which
		        they are considered equal.

		Returns:
		A new VectorGrid instance.
		"""
		if not self.is_compatible_with(other, acc):
			raise ValueError("Two VectorGrid instances are not compatible")

		comp = self.get_components()
		newarg = []
		for co in comp:
			val1 = self.get_array(co)
			val2 = other.get_array(co)
			delta = np.abs(val1[:, np.newaxis] - val2[np.newaxis, :])
			subset = (np.amax(np.amin(delta, axis = 1)) <= acc)
			superset = (np.amax(np.amin(delta, axis = 0)) <= acc)
			if not subset and not superset:
				newval = np.concatenate((val1, val2[np.amin(delta, axis = 0) > acc]))
			elif subset and not superset:
				newval = np.concatenate((val1, val2[np.amin(delta, axis = 0) > acc]))
			elif not subset and superset:
				newval = np.concatenate((val1[np.amin(delta, axis = 1) > acc], val2))
			else:
				newval = val1
			newarg.append(co)
			newarg.append(newval)
		return VectorGrid(*tuple(newarg), astype = self.vtype, deg = self.degrees, prefix = self.prefix)

	def to_dict(self):
		"""Return a dict related to the VectorGrid"""
		grid_dict = {}
		pf = '' if self.prefix is None else self.prefix
		for var, val in zip(self.var, self.values):
			fullvar = pf if (pf and var == 'r') else ('%s_%s' % (pf, var))
			grid_dict[fullvar + '_min'] = np.amin(val)
			grid_dict[fullvar + '_max'] = np.amax(val)
			grid_dict[fullvar + '_n'] = len(val)
		for const, val in zip(self.const, self.constvalues):
			fullconst = pf if (pf and const == 'r') else ('%s_%s' % (pf, const))
			grid_dict[fullconst] = val
		if len(self.shape) == 0:
			grid_dict[pf + '_shape'] = '1'
		else:
			times = '\u00d7'  # multiplication sign
			grid_dict[pf + '_shape'] = times.join(['%i' % x for x in self.shape])
		return grid_dict

def vectorgrid_from_components(val, var, constval, const, **kwds):
	"""Return a VectorGrid instance from VectorGrid.get_var_const() output.
	This 'wrapper' puts the arguments to the VectorGrid initializer in the
	correct order.

	Arguments:
	val       Number, list/array or tuple thereof. The values of the variables
	          in the vector grid.
	var       String or tuple of strings. The labels (vector components) of the
	          variables.
	constval  Number or tuple of numbers. The values for the constants of the
	          vector grid.
	const     String or tuple of strings. The labels (vector components) of the
	          constants.
	**kwds    Keyword arguments passed to VectorGrid initializer.

	Note:
	The pairs {val, var}, and {constval, const} must be tuples of equal length.
	A 1-tuple can be replaced by a single value. A 0-tuple can be replaced by
	None.

	Returns:
	grid      A VectorGrid instance.
	"""
	if val is None:
		val = ()
	elif isinstance(val, tuple):
		pass
	elif isinstance(val, (float, int, np.floating, np.integer, list, np.array)):
		val = (val,)
	else:
		raise TypeError("Argument val must be tuple, numeric, list, or array")
	if var is None:
		var = ()
	elif isinstance(var, str):
		var = (var,)
	elif isinstance(var, tuple) and all([isinstance(v, str) for v in var]):
		pass
	else:
		raise TypeError("Argument var must be str of tuple of str")
	if len(var) != len(val):
		raise ValueError
	vgargs = []
	for var1, val1 in zip(var, val):
		vgargs.append(var1)
		vgargs.append(val1)
	if const is None and constval is None:
		pass
	elif isinstance(const, str) and isinstance(constval, (float, int, np.floating, np.integer)):
		vgargs.append(const)
		vgargs.append(constval)
	elif isinstance(const, tuple) and isinstance(constval, tuple):
		if len(const) != len(constval):
			raise ValueError("Arguments constval and const must be of equal length")
		for c, cval in zip(const, constval):
			vgargs.append(c)
			vgargs.append(cval)
	else:
		raise TypeError("Invalid combination of types for arguments constval and const")
	return VectorGrid(*vgargs, **kwds)


class ZippedKB:
	"""Container class for combination of two VectorGrids, for momentum and magnetic field.

	Attributes:
	k   VectorGrid instance, Vector instance, float, or None. Momentum values.
	b   VectorGrid instance, Vector instance, float, or None. Magnetic field
	    values.

	Note:
	Either k or b may be of length > 1 (VectorGrid or list with more than one
	element), but not both.
	"""
	def __init__(self, k, b):
		lk = 1 if k is None or isinstance(k, (float, np.floating, Vector)) else len(k)
		lb = 1 if b is None or isinstance(b, (float, np.floating, Vector)) else len(b)
		if lk > 1 and lb > 1:
			raise ValueError("At least one component must be a constant")
		self.k = [Vector(0.0, astype = 'x')] if k is None else [k] if isinstance(k, (float, np.floating, Vector)) else k
		self.b = [Vector(0.0, astype = 'z')] if b is None else [b] if isinstance(b, (float, np.floating, Vector)) else b

	def __len__(self):
		"""Get length (number of elements in either k or b)"""
		return max(len(self.k), len(self.b))

	def shape(self):
		"""Get shape of either k or b, whichever is not constant"""
		if len(self.k) > 1:
			return (len(self.k),) if isinstance(self.k, list) else self.k.shape
		elif len(self.b) > 1:
			return (len(self.b),) if isinstance(self.b, list) else self.b.shape
		else:
			return (1,)

	def __iter__(self):
		"""Iterator over flat array.

		Yields:
		Tuple of two Vector instances (or float, if appropriate)
		"""
		if len(self.k) > 1 and len(self.b) == 1:
			for k in self.k:
				yield (k, self.b[0])
		elif len(self.k) == 1 and len(self.b) > 1:
			for b in self.b:
				yield (self.k[0], b)
		elif len(self.k) == 1 and len(self.b) == 1:
			yield (self.k[0], self.b[0])

	def __getitem__(self, idx):
		"""Get element.

		Returns:
		Tuple of two Vector instances (or float, if appropriate)
		"""
		if not isinstance(idx, (int, np.integer)):
			raise TypeError("Index must be an integer")
		if len(self.k) > 1 and len(self.b) == 1:
			return (self.k[idx], self.b[0])
		elif len(self.k) == 1 and len(self.b) > 1:
			return (self.k[0], self.b[idx])
		elif len(self.k) == 1 and len(self.b) == 1 and idx == 0:
			return (self.k[0], self.b[0])
		else:
			raise ValueError("Illegal index value")

	def dependence(self):
		"""Return k or b, whichever is not constant."""
		if len(self.k) > 1:
			return "k"
		elif len(self.b) > 1:
			return "b"
		else:
			return ""

	def get_grid(self):
		"""Get the grid of k or b, whichever is not constant."""
		if len(self.k) > 1 and isinstance(self.k, VectorGrid):
			return self.k
		elif len(self.b) > 1 and isinstance(self.b, VectorGrid):
			return self.b
		else:
			return None

	def to_dict(self):
		"""Return a dict related to the VectorGrid instances or values k and b"""
		grid_dict = {}
		if isinstance(self.k, VectorGrid):
			grid_dict.update(self.k.to_dict())
		elif len(self.k) == 1:
			if isinstance(self.k[0], Vector):
				grid_dict.update(self.k[0].to_dict(prefix = 'k'))
			elif isinstance(self.k[0], (float, np.floating)):
				grid_dict['k'] = self.k[0]
		if isinstance(self.b, VectorGrid):
			grid_dict.update(self.b.to_dict())
		elif len(self.b) == 1:
			if isinstance(self.b[0], Vector):
				grid_dict.update(self.b[0].to_dict(prefix = 'b'))
			elif isinstance(self.b[0], (float, np.floating)):
				grid_dict['b'] = self.b[0]
		return grid_dict


def get_momenta_from_locations(all_kval1, locations, exact_match = None):
	"""Get momenta from location labels.

	Arguments:
	all_kval     ZippedKB instance or VectorGrid. Contains a grid of all
	             momentum values.
	locations    List/array of strings or floats.
	exact_match  True, False or None. If True, momentum values must match the
	             location exactly; if there is not an exact match, 'skip' the
	             location ('old' behaviour). If False, find the nearest match
	             for all locations. If None, extract it from configuration.

	Returns:
	A VectorGrid instance with the momenta that correspond to a valid location
	label or value.
	"""
	if exact_match is None:
		exact_match = get_config_bool('wf_locations_exact_match')
	# TODO: If locations is a VectorGrid instance, we get an error. What is this supposed to do?
	if isinstance(all_kval1, ZippedKB):
		all_kval = all_kval1.b if all_kval1.dependence() == 'b' else all_kval1.k
	else:
		all_kval = all_kval1
	if isinstance(all_kval, (list, np.ndarray)):
		out_kval = []
		l = len(all_kval)
		k_maxstep = 0.0 if l == 1 else np.max(np.abs(np.diff(np.sort(all_kval))))
		for loc in locations:
			if isinstance(loc, (float, np.floating)):
				if not exact_match:
					diffs = np.abs(np.abs(all_kval) - loc)
					idx = np.argmin(diffs)
					this_diff = diffs[idx]
					## Accept non-exact match only if not too far away from
					## values in all_kval. The maximal acceptable distance is
					## the largest difference between two values in all_kval.
					if this_diff < k_maxstep + 1e-6:
						loc = all_kval[idx]
					else:
						sys.stderr.write("ERROR (get_momenta_from_locations): Location '%s' does not match momentum value; (too far) out of range.\n" % loc)
						continue
				for k in all_kval:
					if abs(abs(k) - loc) < 1e-6:
						out_kval.append(k)
			elif loc == 'zero':
				for k in all_kval:
					if abs(k) < 1e-6:
						out_kval.append(k)
			elif loc == 'min':
				out_kval.append(all_kval[0])
			elif loc == 'max':
				out_kval.append(all_kval[-1])
			elif loc == 'all':
				out_kval.extend(all_kval)
			else:
				if loc == 'mid':
					loc = '1/2'
				try:
					frac = [int(i) for i in loc.split('/')]
					if not exact_match or l % frac[1] == 1:
						out_kval.append(all_kval[(l - 1) * frac[0] // frac[1]])
					else:
						sys.stderr.write("ERROR (get_momenta_from_locations): Momentum list not commensurate with point '%s'.\n" % loc)
				except:
					sys.stderr.write("ERROR (get_momenta_from_locations): Invalid location '%s'.\n" % loc)
		return sorted(list(set(out_kval)))
	elif isinstance(all_kval, VectorGrid):
		vg_arg = []
		for co in all_kval.get_components():
			val = all_kval.get_array(co)
			if len(val) == 1:
				compval = val
			else:
				compval = get_momenta_from_locations(val, locations)
			vg_arg.append(co)
			vg_arg.append(compval)
		return VectorGrid(*vg_arg, astype = all_kval.vtype, deg = all_kval.degrees, prefix = all_kval.prefix)
	else:
		raise TypeError("Input must be a list/array or a VectorGrid instance.")

def locations_index(locations, vec, vec_numeric = None):
	"""Find a value in locations list matching vector vec, and return its index.

	Arguments:
	locations     List, array, or VectorGrid. Contains the vectors or values
	              used for matching against. For this argument, the return value
	              of get_momenta_from_locations() can be used.
	vec           Vector or number. The vector which is matched against the
	              vectors or values in argument locations.
	vec_numeric   Number or None. If a number, use this value if using the
	              numerical match fallback.

	Returns:
	match   Integer or None. Index of the matching value in locations if any
	        value in locations matches vec, None if none matches. If both inputs
	        are Vectors of the same type, then check for identity. Otherwise, if
	        locations contains Vectors, check equality. Otherwise, check
	        equality of numerical value.
	"""
	if vec_numeric is None:
		vec_numeric = vec.len() if isinstance(vec, Vector) else vec
	for j, loc in enumerate(locations):
		if isinstance(loc, Vector) and isinstance(vec, Vector) and loc.vtype == vec.vtype:
			if loc.identical(vec):
				return j
		elif isinstance(loc, Vector) and loc.equal(vec):
			return j
		elif isinstance(loc, (int, float, np.integer, np.floating)) and np.abs(loc - vec_numeric) < 1e-9:
			return j
	return None
