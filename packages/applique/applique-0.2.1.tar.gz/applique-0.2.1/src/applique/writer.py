from amarium import write_file
import rdkit

from applique.molecule import Molecule


def write_xyz(molecule: type(Molecule), file_name: str) -> None:

    mol = molecule.rdmol
    xyz = rdkit.Chem.rdmolfiles.MolToXYZBlock(mol)
    xyz = xyz[: len(xyz) - 1]
    write_file(xyz, file_name)
