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
import shutil
from .materials import MaterialsList

configpath = os.path.join(os.path.expanduser('~'), '.kdotpy')
materialspath = os.path.join(configpath, 'materials')
materialsfile = 'default'
scriptpath = os.path.dirname(os.path.realpath(__file__))
debug_fname = "kdotpy-materials.log"

allMaterials = MaterialsList({})

def initialize_materials():
	"""Initialize materials file

	Read the 'default' materials file from the directory '~/.kdotpy/materials'.
	If it does not exist yet, copy the 'default' materials file there. Then read
	all other files in '~/.kdotpy/materials'.
	"""
	# Default materials file
	source_mat_file = os.path.join(scriptpath, materialsfile)
	default_mat_file = os.path.join(materialspath, materialsfile)
	if not os.path.isfile(source_mat_file):
		raise OSError("Built-in default materials file does not exist")
	if not os.path.isdir(materialspath):
		os.mkdir(materialspath)
	if not os.path.isfile(default_mat_file):
		shutil.copy(source_mat_file, default_mat_file)
		sys.stderr.write(f"Info (initialize_materials): New materials file '{materialsfile}' created in {materialspath}.\n")
	allMaterials.load_from_file(source_mat_file)
	allMaterials.load_from_file(default_mat_file, redef_warning=False)

	# All other files in ~/.kdotpy/materials
	all_mat_files = sorted([f.name for f in os.scandir(materialspath) if f.is_file()])
	if 'verbose' in sys.argv:
		print("Material files:", ", ".join(['<built-in>', materialsfile] + [f for f in all_mat_files if f != materialsfile]))

	for filename in all_mat_files:
		if filename == materialsfile:  # skip default materials file
			continue

		filename_full = os.path.join(materialspath, filename)
		allMaterials.load_from_file(filename_full)

	if 'verbose' in sys.argv:
		print(f"Material parameters dumped to {debug_fname} for debugging")
		with open(debug_fname, 'w') as f:
			allMaterials.dump(stream=f)

