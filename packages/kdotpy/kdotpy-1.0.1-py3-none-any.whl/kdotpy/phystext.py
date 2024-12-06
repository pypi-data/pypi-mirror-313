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
import re

### HELPER FUNCTIONS ###
superscriptdigits = ['\u2070', '\xB9', '\xB2', '\xB3', '\u2074', '\u2075', '\u2076', '\u2077', '\u2078', '\u2079']
def unicode_power(exponent, quantity = "10"):
	"""Power-of-ten using Unicode superscripts.

	Arguments:
	exponent   Integer. The exponent n in 10^n. This number may be positive,
	           negative, or zero.
	quantity   String. How to express the base ('10').

	Returns:
	String.
	"""
	if exponent == 0:
		return ""
	elif exponent > 0:
		return quantity + "".join(([superscriptdigits[int(c)] for c in ("%i" % exponent)]))
	else:
		return quantity + "\u207B" + "".join(([superscriptdigits[int(c)] for c in ("%i" % -exponent)]))

def format_value(x, style = None, fmt = None):
	"""Format a floating-point numerical value

	Arguments:
	x      Float. The numerical value.
	style  String. One of the formatting styles 'raw', 'plain', 'unicode',
	       'tex'.
	fmt    String. Formatting string such as '{:.3g}' for initial conversion of
	       units to string. Only e, f, g are permitted as formatting types.
	       Format modifiers (e.g., number of digits) are allowed.

	Returns:
	String.
	"""
	if fmt is None:
		fmt = '{:g}'
	if not isinstance(fmt, str):
		raise TypeError("Argument fmt must be a string.")
	m = re.match("^{:[^{}]*[efg]}$", fmt)
	if m is None:
		raise ValueError("Argument fmt must be a format string of types e, f, or g, like '{:.3g}'.")
	s = fmt.format(x)
	if style == 'none' or style == 'false':
		return None
	elif style == 'raw':
		return s
	elif style == 'plain':
		if 'e' in s:
			s1, s2 = s.split('e')
			return "{} x 10^{}".format(s1, int(s2))
		return s
	elif style == 'unicode':
		if 'e' in s:
			s1, s2 = s.split('e')
			return s1 + " \u00d7 " + unicode_power(int(s2))
		return s.replace('inf', '\u221e')
	elif style == 'tex':
		if 'e' in s:
			s1, s2 = s.split('e')
			return "${} \\times 10^{{{}}}$".format(s1, int(s2))
		return s.replace('inf', r'\infty')
	else:
		return None


### UNIT FORMATTING ###
def format_unit(*args, style = None, negexp = True):
	"""Format a unit.

	Arguments:
	*args   One of the following: If None, Return empty string. If a single
	        string, parse it as a raw_unit_str to a sequence of units and powers
	        together with a power of ten. For more arguments, an int is treated
	        as a power of ten, a string as a simple unit (e.g., 'meV', 'nm'),
	        or a tuple (str, int) where the str is a simple unit and int its
	        power, so that e.g. ('nm', -2) means 'nm^-2'.
	style   String. One of the formatting styles 'raw', 'plain', 'unicode',
	        'tex'.
	negexp  True or False. If True, style quotients using negative exponents
	        (e.g., 'm s^-1'). If False, use a slash notation (e.g., 'm/s').

	Returns:
	String.
	"""
	if len(args) == 1 and args[0] is None:
		return ""
	if style == 'none' or style == 'false':
		return None
	if len(args) == 1 and isinstance(args[0], str):
		raw_unit_str = args[0]
		if style is None or style == 'raw':
			return raw_unit_str
		# Parse unit string:
		# value
		m = re.match(r"(1(\.0*)?[eE]([+-]?[0-9]+)|10(\^|\*\*)([+-]?[0-9]+))", raw_unit_str)
		if m is not None:
			unit10p = int(m.group(5)) if m.group(2) is None else int(m.group(2))
			unit_str = raw_unit_str[m.end(0):]
		else:
			unit10p = 0
			unit_str = raw_unit_str
		# unit labels
		matches = re.findall(r"\s*([/\*]?)\s*([a-zA-Z_µ]+)(\s*(\^|\*\*)\s*([+-]?[0-9]+))?", unit_str)
		unitdata = []
		for m in matches:
			unit = m[1]
			power = 1 if m[4] is None or len(m[4]) == 0 else int(m[4])
			if m[0] == '/':
				power *= -1
			unitdata.append((unit, power))
	elif len(args) >= 1:
		raw_unit_str = None
		unitdata = []
		unit10p = 0
		for arg in args:
			if isinstance(arg, int):
				unit10p += arg
			elif isinstance(arg, str):
				unitdata.append((arg, 1))
			elif isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[1], int):
				if arg[0] == 10 or arg[0] == '10':
					unit10p += arg[1]
				elif isinstance(arg[0], str):
					unitdata.append(arg)
				else:
					raise ValueError("Invalid tuple input")
			else:
				raise ValueError("Invalid tuple input")
	else:
		raise ValueError("Invalid input argument")

	# Build formatted unit string
	if style == 'tex':
		valstr = "10^{%i}" % unit10p if unit10p != 0 else ""
		ustr = ""
		for unit, power in unitdata:
			if power == 1:
				ustr += r"\,\mathrm{%s}" % unit
			elif power > 1 or (power < 0 and negexp):
				ustr += r"\,\mathrm{%s}^{%i}" % (unit, power)
			elif power == -1:
				ustr += r"/\mathrm{%s}" % unit
			elif power < -1:
				ustr += r"/\mathrm{%s}^{%i}" % (unit, -power)
		if valstr == "" and ustr.startswith("/"):
			valstr = "1"
		elif valstr == "" and ustr.startswith(r'\,'):
			ustr = ustr[2:]
		return '$' + valstr + ustr + '$'
	elif style == 'plain' or (style == 'raw' and raw_unit_str is None):
		valstr = "10^%i" % unit10p if unit10p != 0 else ""
		ustr = ""
		for unit, power in unitdata:
			if power == 1:
				ustr += " %s" % unit
			elif power > 1 or (power < 0 and negexp):
				ustr += " %s^%i" % (unit, power)
			elif power == -1:
				ustr += "/%s" % unit
			elif power < -1:
				ustr += "/%s^%i" % (unit, -power)
		if valstr == "" and ustr.startswith("/"):
			valstr = "1"
		return (valstr + ustr).lstrip(' ')
	elif style == "unicode":
		valstr = unicode_power(unit10p, "10")
		ustr = ""
		for unit, power in unitdata:
			if power == 1:
				ustr += " %s" % unit
			elif power > 1 or (power < 0 and negexp):
				ustr += " " + unicode_power(power, unit)
			elif power == -1:
				ustr += "/%s" % unit
			elif power < -1:
				ustr += "/" + unicode_power(-power, unit)
		if valstr == "" and ustr.startswith("/"):
			valstr = "1"
		return (valstr + ustr).lstrip(' ')
	elif style == 'raw':
		return raw_unit_str
	else:
		return None

def is_known_vector(q):
	for x in ['k', 'b', 'a']:
		if q.startswith(x):
			prefix = x
			break
	else:
		return False
	if q == prefix:
		return True
	q2 = q[len(prefix):]
	return q2 in ['r', 'x', 'y', 'z', 'phi', 'theta']

def format_vector_unit(q, style = None, negexp = True, degrees = True):
	"""Format unit for vector k, b, and their (cartesian/angular) components"""
	if not is_known_vector(q):
		sys.stderr.write("Warning (vector_unit): Unknown vector quantity '%s'\n" % q)
		return None
	if q.endswith('phi') or q.endswith('theta'):
		if degrees:
			return {'none': None, 'false': None, 'raw': 'deg', 'plain': 'deg', 'unicode': '\xb0', 'tex': '$^{\\circ}$'}[style]
		else:
			return {'none': None, 'false': None, 'raw': 'rad', 'plain': 'deg', 'unicode': 'rad', 'tex': '$\\mathrm{rad}$'}[style]
	if q.startswith('k'):
		return format_unit(('nm', -1), style = style, negexp = negexp)
	if q.startswith('b'):
		return format_unit('T', style = style, negexp = negexp)
	if q.startswith('a'):
		return format_unit('1', style = style, negexp = negexp)
	sys.stderr.write("Warning (vector_unit): Unknown vector quantity '%s'\n" % q)
	return None

### PHYSICAL QUANTITY FORMATTING ###
def format_vector_q(q, style = None):
	if not is_known_vector(q):
		sys.stderr.write("Warning (vector_q): Unknown vector quantity '%s'\n" % q)
		return None
	prefix = ''
	for x in ['k', 'b', 'a']:
		if q.startswith(x):
			prefix = x
			break
	if style == 'none' or style == 'false':
		return None
	elif style == 'raw':
		return q
	comp = '' if q == prefix else q[len(prefix):]
	if style == 'plain':
		return 'B' + comp if prefix == 'b' else q
	elif style == 'unicode':
		if comp == 'theta':
			return '\u03b8' if prefix == 'k' else '\u03b8B' if prefix == 'b' else '\u03b8' + prefix
		elif comp == 'phi':
			return '\u03d5' if prefix == 'k' else '\u03d5B' if prefix == 'b' else '\u03b8' + prefix
		else:
			return q
	elif style == 'tex':
		prefix = 'B' if prefix == 'b' else prefix
		if comp == '':
			return '$%s$' % prefix
		elif comp == 'theta':
			return r'$\theta$' if prefix == 'k' else r'$\theta_B$' if prefix == 'b' else ('$\\theta_{%s}$' % prefix)
		elif comp == 'phi':
			return r'$\phi$' if prefix == 'k' else r'$\phi_B$' if prefix == 'b' else ('$\\phi_{%s}$' % prefix)
		else:
			return '$%s_{%s}$' % (prefix, comp)
	else:
		return None

### MISCELLANEOUS ###
def orbital_labels(style = None, norb = 8):
	"""Return list of formatted orbital labels"""
	if norb not in [6, 8]:
		raise ValueError("Argument norb must be 6 or 8")
	raw_labels = ['G6,+1/2', 'G6,-1/2', 'G8,+3/2', 'G8,+1/2', 'G8,-1/2', 'G8,-3/2', 'G7,+1/2', 'G7,-1/2']
	if style == 'none' or style == 'false':
		return None
	elif style == 'raw':
		return raw_labels[:norb]
	elif style == 'plain':
		return [x.replace('G', 'Gamma') for x in raw_labels[:norb]]
	elif style == 'unicode':
		return [x.replace('G', '\u0393') for x in raw_labels[:norb]]
	elif style == 'tex':
		return [
			'$\\Gamma_6,+\\frac{1}{2}$', '$\\Gamma_6,-\\frac{1}{2}$',
			'$\\Gamma_8,+\\frac{3}{2}$', '$\\Gamma_8,+\\frac{1}{2}$',
			'$\\Gamma_8,-\\frac{1}{2}$', '$\\Gamma_8,-\\frac{3}{2}$',
			'$\\Gamma_7,+\\frac{1}{2}$', '$\\Gamma_7,-\\frac{1}{2}$'
		][:norb]
	else:
		return None

