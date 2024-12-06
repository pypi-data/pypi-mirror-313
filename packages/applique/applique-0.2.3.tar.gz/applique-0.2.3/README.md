# applique


[![Downloads](https://static.pepy.tech/personalized-badge/applique?period=total&units=international_system&left_color=orange&right_color=blue&left_text=Downloads)](https://pepy.tech/project/applique)
[![License: GPL v3](https://img.shields.io/badge/License-GPL_v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C-blue)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![PyPI - Version](https://img.shields.io/pypi/v/applique.svg)](https://pypi.org/project/applique)

`applique` is a simple program that can write .xyz file from .mol files. It really is just a missing puzzle piece in the quantum chemistry world, as some molecular editors went corrupt. Now one can use common Quantum Chemistry software again. It mimics Avogadros behaviour.

Nothing special.

Okay by now it is an understatement. It is infact a molecular model suitable for generating simulations. It can also convert fileformats.

## Installation

Simple as always 

```bash 
pip install applique
```

## Usage 

### Cli

In your venv 
```bash 
applique --i in_file.mol --o out_file.xyz
```
Easy peasy

### Programs 
Within programs for example you load a molfile like this 


```bash
from applique.molecule import Molecule as Mol

mol_file_benzene = "tests/molecules/benzene.mol"
benzene = Mol().from_mol(mol_file_benzene)
```
Then write the `.xyz` like this 

```bash
from applique.writer import write_xyz
from applique.molecule import Molecule as Mol

mol_file_benzene = "tests/molecules/benzene.mol"
benzene = Mol().from_mol(mol_file_benzene)
file_name_benzene = "./tests/molecules/benzene.xyz"
coordinates = benzene.struct3D() #you can omit if you don't want to preoptimize the structure.
write_xyz(self.benzene, file_name_benzene)
```

# Errors

This is wanted (don't want to impose bonds at this stage)
```bash
E       RuntimeError: Pre-condition Violation
E               getNumImplicitHs() called without preceding call to calcImplicitValence()
E               Violation occurred on line 287 in file Code/GraphMol/Atom.cpp
E               Failed Expression: d_implicitValence > -1
E               RDKIT: 2024.03.5
E               BOOST: 1_85
```