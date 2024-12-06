from typing import List
import rdkit
from rdkit.Chem import AllChem
import molmass as mm
import numpy as np


class Molecule:
    """
    Simple molecule class that extends RDKit molecules
    """

    def __init__(self, rdmol=None, coordinates3D=None, atom_symbols:str=None):

        self.coordinates3D = coordinates3D
        self.rdmol = rdmol
        self.atom_symbols = atom_symbols

    def from_smiles(self, smiles:str, add_H=True)->None: 

        self.rdmol = rdkit.Chem.MolFromSmiles(smiles)
        if add_H == True: 
            self.rdmole = rdkit.Chem.rdmolops.AddHs(self.rdmol)
        return self

    def from_canonical_smiles(self, can_smiles: str) -> None:
        raise NotImplementedError

    def from_mol(self, file_path: str) -> None:
        self.rdmol = rdkit.Chem.rdmolfiles.MolFromMolFile(file_path)
        self.rdmol = rdkit.Chem.rdmolops.AddHs(self.rdmol)
        return self

    def from_xyz_file(self, xyz_file: str) -> None:
        self.rdmol = rdkit.Chem.rdmolfiles.MolFromXYZFile(xyz_file)
        return self

    def from_xyz_block(self, xyz_block: str) -> None:
        self.rdmol = rdkit.Chem.rdmolfiles.MolFromXYZBlock(xyz_block)
        return self



    def from_sdf(self, file_path: str) -> None:
        """
        It is a bit hacky to admit. Becasuse SDF files usually store more molecules,
        only the first molecule of the whole collection is selected.

        """
        supplier = rdkit.Chem.rdmolfiles.SDMolSupplier(file_path)
        mol = supplier[0]
        self.rdmol = mol
        return self

    def get_atom_numbers(self, rdmol=None):
        """
        Useful for generating graphs and xyz_files
        """

        if rdmol == None:
            mol = self.rdmol
        else:
            mol = rdmol

        atomic_numbers = []
        for atom in mol.GetAtoms():
            atomic_numbers.append(atom.GetAtomicNum())
        return atomic_numbers

    def get_atom_symbols(self, rdmol=None):
        """
        Is useful for creating your own xyz files
        """
        if self.atom_symbols != None and rdmol==None: 
            return self.atoms
        if rdmol == None:
            mol = self.rdmol
        else:
            mol = rdmol

        atomic_symbols = []

        for atom in mol.GetAtoms():
            atomic_symbols.append(atom.GetSymbol())
        atomic_symbols= "".join(atomic_symbols)
        return atomic_symbols

    def get_total_electron_count(self) -> int:

        atomic_numbers = self.get_atom_numbers()
        electron_count = sum(atomic_numbers)
        return electron_count
    
    def get_total_atom_count(self) -> int: 
        
        atomic_numbers = self.get_atom_numbers()
        total_atom_count = len(atomic_numbers)
        return total_atom_count

    def embed(self, rdmol=None):
        """make emebedding in RDKit0:00 • 58.8 MB/s


        Args:
            rdmol (_type_, optional): rdmol object. Defaults to None.

        Returns:
            _type_: Mol Object
        """
        mol = self._check_mol(rdmol=rdmol)
        mol = rdkit.Chem.rdmolops.AddHs(mol)
        assert type(mol) != None
        AllChem.EmbedMolecule(mol)
        AllChem.MMFFOptimizeMolecule(mol)
        self.rdmol = mol
        return mol

    def get_xyz_block(self):
        """generate an xyz block out of 3D coordinates and
        the corresponding atomic symbols
        """
        if self.atom_symbols == None: 
            atom_symbols = self.get_atom_symbols()
        else: 
            atom_symbols = self.atom_symbols

        if self.coordinates3D == None:
            self.get_3D_coordinates(embed=False)
        xyz_block = ""

        for i in range(len(atom_symbols)):
            if i == 0:
                xyz_block += str(len(atom_symbols)) + "\n\n"
            line = atom_symbols[i] + 6 * " "
            tmp_coords = self.coordinates3D[i]  # 3D coords from one atom
            for j in range(len(tmp_coords)):
                if j == 0:
                    line += str(tmp_coords[j])
                else:
                    line += 4 * " " + str(tmp_coords[j])
            if i != len(atom_symbols) - 1:
                line += "\n"
            xyz_block += line

        return xyz_block

    def get_2D_coordinates(self, rdmol=None, embed=True) -> List[float]:
        """Gets 2D coordinates

        Args:
            rdmol (_type_, optional): RDMol object

        Returns:
            List[float]: Coordinates 3D but only in 2D
        """
        if embed == True:
            mol = self.embed(rdmol=rdmol)
        else:
            if rdmol is None:
                rdmol = self.rdmol
            mol = rdmol

        rdkit.Chem.rdDepictor.Compute2DCoords(mol)
        coordinates = []

        for i in range(len(mol.GetAtoms())):
            pos = mol.GetConformer().GetAtomPosition(i)
            coordinates.append(list(pos))
        self.coordinates2D = coordinates

        return coordinates

    def get_masses(self) -> List[float]:

        masses = []
        for atom in self.get_atom_symbols():
            formula = mm.Formula(atom)
            masses.append(formula.mass)
        return masses

    def get_3D_coordinates(self, rdmol=None, embed=False) -> List[List[float]]:
        """Gets 3D coordinates

        Args:
            rdmol (_type_, optional): RDMol object

        Returns:
            List[float]: Coordinates 3D but only in 2D
        """

        if embed == True:
            mol = self.embed(rdmol=rdmol)
        else:
            if rdmol is None:
                rdmol = self.rdmol
            mol = rdmol

        coordinates = []

        for i in range(len(mol.GetAtoms())):
            pos = mol.GetConformer().GetAtomPosition(i)
            coordinates.append(list(pos))
        self.coordinates3D = coordinates

        return coordinates

    def calculate_center_of_mass(self):
        """Calculates the center of mass for a given set of particles"""

        masses = self.get_masses()
        coordinates = self.get_3D_coordinates(embed=False)
        nominator = [0, 0, 0]

        for i in range(len(masses)):
            tmp = np.multiply(masses[i], coordinates[i])
            nominator += tmp

        center_of_mass = nominator / np.sum(masses)
        return center_of_mass.tolist()


    def get_graph_representation(self): 
        pass
    
    def _check_mol(self, rdmol):
        """
        Reused snipptet to either use the stored rdmol or a new one
        """

        if rdmol is None:
            mol = self.rdmol
        else:
            mol = rdmol
        return mol


class MoleculeCollection:
    """
    Defines a collection of molecules, for example for solvent or gas phase mixtures
    """

    def __init__(self, molecules, Box):

        self.molecules = molecules
        self.Box = Box

    def add_molecules(self, molecules) -> None:

        assert type(molecules) == type([])
        self.molecules.append(molecules)

    def remove_molecules(self, indices: List) -> None:

        assert type(indices) == type([])

    def get_atoms_from_molecule(self, Molecule) -> List[List[str | float]]:

        atom_numbers = Molecule.get_atom_numbers()
        atom_symbols = Molecule.get_atom_symbols
        return [atom_numbers, atom_symbols]


class MoleculeCollectionIndistinct:
    """
    Defines a molecular collection with indistinct molecules. That means only atom positions are relevant

    """

    def __init__(self):
        pass

    def add_molecules(self):
        # need to unpack the atom coordinates
        raise NotImplementedError
