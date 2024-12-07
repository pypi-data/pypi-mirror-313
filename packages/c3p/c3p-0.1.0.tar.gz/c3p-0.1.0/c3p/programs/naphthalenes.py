"""
Classifies: CHEBI:25477 naphthalenes
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_naphthalenes(smiles: str):
    """
    Determines if a molecule contains a naphthalene core structure (two ortho-fused benzene rings).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains naphthalene core, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Create naphthalene pattern
    naphthalene_pattern = Chem.MolFromSmarts('c1ccc2ccccc2c1')
    if naphthalene_pattern is None:
        return None, "Could not create naphthalene pattern"

    # Find naphthalene substructures
    matches = mol.GetSubstructMatches(naphthalene_pattern)
    if not matches:
        return False, "No naphthalene core structure found"

    # For the first match, identify substituents
    match = matches[0]
    naphthalene_atoms = set(match)
    substituents = []
    
    for atom_idx in match:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in naphthalene_atoms:
                substituents.append(neighbor.GetSymbol())

    if len(substituents) > 0:
        unique_substituents = set(substituents)
        return True, f"Substituted naphthalene with substituents: {', '.join(unique_substituents)}"
    else:
        return True, "Unsubstituted naphthalene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25477',
                          'name': 'naphthalenes',
                          'definition': 'Any benzenoid aromatic compound '
                                        'having a skeleton composed of two '
                                        'ortho-fused benzene rings.',
                          'parents': ['CHEBI:33836', 'CHEBI:36785']},
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
    'num_true_positives': 121,
    'num_false_positives': 100,
    'num_true_negatives': 8610,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.5475113122171946,
    'recall': 0.9453125,
    'f1': 0.6934097421203439,
    'accuracy': 0.9878931885041865}