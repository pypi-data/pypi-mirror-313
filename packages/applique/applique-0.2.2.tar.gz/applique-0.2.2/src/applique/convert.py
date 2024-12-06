from applique.molecule import Molecule as Mol
from applique.writer import write_xyz


def convert(mol_file_name: str, save_name: str) -> None:

    mol = Mol().from_mol(mol_file_name)
    coordinates = mol.struct3D()
    write_xyz(molecule=mol, file_name=save_name)
