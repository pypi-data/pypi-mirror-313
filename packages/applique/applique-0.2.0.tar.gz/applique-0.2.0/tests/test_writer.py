"""
Unittests to test molecule object
"""

import os
import unittest

from applique.molecule import Molecule as Mol
from applique.writer import write_xyz


class TestWriter(unittest.TestCase):

    mol_file_benzene = "tests/molecules/benzene.mol"
    mol_file_cyclohexane = "tests/molecules/cyclohexane.mol"
    benzene = Mol().from_mol(mol_file_benzene)
    cyclohexane = Mol().from_mol(mol_file_cyclohexane)

    def testXYZWriter(self):

        file_name_benzene = "./tests/molecules/benzene.xyz"
        file_name_cyclohexane = "./tests/molecules/cyclohexane.xyz"

        # case 1
        coordinates = self.benzene.get_3D_coordinates()
        write_xyz(self.benzene, file_name_benzene)

        assert os.path.isfile(file_name_benzene)

        # case 2
        coordinates = self.cyclohexane.get_3D_coordinates()
        write_xyz(self.cyclohexane, file_name_cyclohexane)

        assert os.path.isfile(file_name_cyclohexane)
