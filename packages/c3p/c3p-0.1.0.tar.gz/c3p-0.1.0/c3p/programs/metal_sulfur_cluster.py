"""
Classifies: CHEBI:25214 metal-sulfur cluster
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_metal_sulfur_cluster(smiles: str):
    """
    Determines if a molecule is a metal-sulfur cluster, defined as a unit with two or more 
    metal atoms and bridging sulfur ligand(s).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a metal-sulfur cluster, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get all atoms
    atoms = mol.GetAtoms()
    
    # Find metal atoms
    metal_atoms = []
    metal_symbols = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',
                     'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd',
                     'La','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg',
                     'Ac','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn']
    
    for atom in atoms:
        if atom.GetSymbol() in metal_symbols:
            metal_atoms.append(atom)

    if len(metal_atoms) < 2:
        return False, "Less than two metal atoms found"

    # Find sulfur atoms
    sulfur_atoms = []
    for atom in atoms:
        if atom.GetSymbol() == 'S':
            sulfur_atoms.append(atom)

    if len(sulfur_atoms) == 0:
        return False, "No sulfur atoms found"

    # Check if sulfur atoms are bridging between metals
    bridging_s = False
    for s_atom in sulfur_atoms:
        metal_neighbors = 0
        for neighbor in s_atom.GetNeighbors():
            if neighbor.GetSymbol() in metal_symbols:
                metal_neighbors += 1
        if metal_neighbors >= 2:
            bridging_s = True
            break

    if not bridging_s:
        return False, "No bridging sulfur atoms found between metals"

    # Count number of metals and sulfurs in cluster
    num_metals = len(metal_atoms)
    num_bridging_s = len([s for s in sulfur_atoms if len([n for n in s.GetNeighbors() if n.GetSymbol() in metal_symbols]) >= 2])

    return True, f"Metal-sulfur cluster with {num_metals} metal atoms and {num_bridging_s} bridging sulfur atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25214',
                          'name': 'metal-sulfur cluster',
                          'definition': 'A metal-sulfur cluster is a unit '
                                        'comprising two or more metal atoms '
                                        'and bridging sulfur ligand(s).',
                          'parents': ['CHEBI:33733']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 2,
    'num_true_negatives': 183908,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.5,
    'recall': 1.0,
    'f1': 0.6666666666666666,
    'accuracy': 0.9999891252338075}