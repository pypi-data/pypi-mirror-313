"""
Unittests to test molecule object
"""

import unittest
from rdkit import Chem
from rdkit.Chem import (
    rdDepictor,
)  # otherwise it gives import errors during the tests. Strange

import applique as ap
from applique.molecule import Molecule as Mol


class TestMolecule(unittest.TestCase):

    benzene_smiles = "c1ccccc1"
    mol_file_benzene = "tests/molecules/benzene.mol"
    mol_file_cyclohexane = "tests/molecules/cyclohexane.mol"
    benzene = Mol()
    benzene = benzene.from_mol(mol_file_benzene)
    cyclohexane = Mol().from_mol(mol_file_cyclohexane)

    # non-variable benzene
    ref_benzene = Mol().from_xyz_file("tests/molecules/benzene_ref.xyz")

    
    def test_from_smiles(self): 

        mol = Mol().from_smiles(self.benzene_smiles)
        assert type(mol.rdmol) == type(
            Chem.rdmolfiles.MolFromMolFile(self.mol_file_benzene)
        )
        ## test case 2 
        smiles = "OCC3OC(OCC2OC(OC(C#N)c1ccccc1)C(O)C(O)C2O)C(O)C(O)C3O"
        mol = Mol().from_smiles(smiles=smiles)
        assert type(mol.rdmol) == type(
            Chem.rdmolfiles.MolFromMolFile(self.mol_file_benzene)
        )

    
    def test_from_mol(self):

        assert type(self.benzene.rdmol) == type(
            Chem.rdmolfiles.MolFromMolFile(self.mol_file_benzene)
        )

    def test_get_2D_coordinates(self):

        ref_benzene = [
            [1.5000000000000004, 7.401486830834377e-17, 0.0],
            [0.7499999999999993, -1.2990381056766587, 0.0],
            [-0.7500000000000006, -1.2990381056766578, 0.0],
            [-1.5, 2.5771188818044677e-16, 0.0],
            [-0.7499999999999996, 1.2990381056766582, 0.0],
            [0.7500000000000006, 1.299038105676658, 0.0],
            [3.0, 2.9605947323337506e-16, 0.0],
            [1.4999999999999996, -2.598076211353318, 0.0],
            [-1.5000000000000007, -2.598076211353315, 0.0],
            [-3.0, 2.9605947323337506e-16, 0.0],
            [-1.4999999999999998, 2.598076211353316, 0.0],
            [1.5000000000000007, 2.598076211353316, 0.0],
        ]

        # case 1
        coordinates = self.benzene.get_2D_coordinates(self.benzene.rdmol)
        assert coordinates == ref_benzene

        # case 2
        coordinates = self.benzene.get_2D_coordinates()

        assert coordinates == ref_benzene

    def test_get_3D_coordinates(self):

        benzene = Mol().from_mol(self.mol_file_benzene)
        cyclohexane = Mol().from_mol(self.mol_file_cyclohexane)

        # case 1
        coordinates = benzene.get_3D_coordinates(benzene.rdmol)
        assert len(coordinates) == 12

        # case 2
        coordinates_benzene2 = benzene.get_3D_coordinates()
        assert len(coordinates) == 12

        # case 3
        coordinates = cyclohexane.get_3D_coordinates()
        assert coordinates != coordinates_benzene2

        #case 4 difficulties with conformer
        smiles = "OCC3OC(OCC2OC(OC(C#N)c1ccccc1)C(O)C(O)C2O)C(O)C(O)C3O"
        mol = Mol().from_smiles(smiles=smiles)
        coordinates = mol.get_3D_coordinates()
        assert len(coordinates) == 59

    def test_sdfile(self):

        # Test 1 Benzene with embedding H 
        sdfile = "tests/molecules/benzene.sdf"
        benzene = Mol().from_sdf(sdfile)

        coordinates = benzene.get_3D_coordinates(embed=True)
        assert len(coordinates) == 12

        # Test molecule from ALCHEMY Dataset
        sdfile = "tests/molecules/9993322.sdf"
        alchemy_mol = Mol().from_sdf(sdfile)

        coordinates = alchemy_mol.get_3D_coordinates(embed=False)
        assert len(coordinates) == 21

    def test_atomic_number_list(self):
        benzene = Mol()
        benzene = benzene.from_mol(self.mol_file_benzene)
        atom_numbers = benzene.get_atom_numbers()
        assert atom_numbers == [6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1]

    def test_atomic_symbols_list(self):
        
        atom_symbols = self.benzene.get_atom_symbols()
        assert atom_symbols == "CCCCCCHHHHHH"
        benzene = Mol()
        benzene.atom_symbols = "CCCCCCHHHHHH"
        atom_symbols = self.benzene.get_atom_symbols()
        assert atom_symbols == "CCCCCCHHHHHH"

    def test_from_xyz_file(self): 
        
        benzene = Mol()
        benzene = benzene.from_mol(self.mol_file_benzene)
        atom_symbols = benzene.get_atom_symbols()
        assert atom_symbols == "CCCCCCHHHHHH"

    def test_from_xyz_file(self):

        mol = self.ref_benzene
        coords = mol.get_3D_coordinates(embed=False)  # because bonds not relevant
        assert coords == [
            [1.23928, -0.63962, 0.024709],
            [1.173557, 0.753641, 0.018112],
            [-0.065723, 1.393261, -0.006596],
            [-1.23928, 0.63962, -0.024708],
            [-1.173557, -0.753641, -0.018113],
            [0.065723, -1.393261, 0.006596],
            [2.204821, -1.137958, 0.043965],
            [2.087894, 1.340813, 0.032226],
            [-0.11693, 2.478772, -0.01174],
            [-2.204821, 1.137959, -0.043964],
            [-2.087892, -1.340815, -0.032226],
            [0.116928, -2.478772, 0.01174],
        ]

    def test_from_xyz_block(self):

        xyz_block = """3

O      0.000000    0.000000    0.117790
H      0.000000    0.755450   -0.471160
H      0.000000   -0.755450   -0.471160
"""
        mol = Mol().from_xyz_block(xyz_block)
        coords = mol.get_3D_coordinates(embed=False)
        assert coords == [
            [0.0, 0.0, 0.11779],
            [0.0, 0.75545, -0.47116],
            [0.0, -0.75545, -0.47116],
        ]

    def test_get_xyz_block(self):

        xyz_block = self.ref_benzene.get_xyz_block()
        assert (
            xyz_block
            == "12\n\nC      1.23928    -0.63962    0.024709\nC      1.173557    0.753641    0.018112\nC      -0.065723    1.393261    -0.006596\nC      -1.23928    0.63962    -0.024708\nC      -1.173557    -0.753641    -0.018113\nC      0.065723    -1.393261    0.006596\nH      2.204821    -1.137958    0.043965\nH      2.087894    1.340813    0.032226\nH      -0.11693    2.478772    -0.01174\nH      -2.204821    1.137959    -0.043964\nH      -2.087892    -1.340815    -0.032226\nH      0.116928    -2.478772    0.01174"
        )

    def test_center_of_mass(self):

        com = self.ref_benzene.calculate_center_of_mass()
        assert com == [
            1.2081223524505325e-17,
            -1.2903777784112161e-08,
            1.2903777783023964e-08,
        ]

    def test_get_electron_count(self):
        benzene = Mol()
        benzene = benzene.from_mol(self.mol_file_benzene)
        electron_count = benzene.get_total_electron_count()
        assert electron_count == 42

    def test_get_total_atom_count(self): 

        total_atom_count = self.benzene.get_total_atom_count()
        assert total_atom_count == 12