"""
Classifies: CHEBI:25479 naphthalenone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_naphthalenone(smiles: str):
    """
    Determines if a molecule is a naphthalenone (naphthalene with at least one oxo substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a naphthalenone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find naphthalene core
    naphthalene_pattern = Chem.MolFromSmarts('c1ccc2ccccc2c1')
    if not mol.HasSubstructMatch(naphthalene_pattern):
        return False, "No naphthalene core found"
    
    # Find ketone/oxo groups
    ketone_pattern = Chem.MolFromSmarts('C(=O)')
    ketone_matches = mol.GetSubstructMatches(ketone_pattern)
    
    if not ketone_matches:
        return False, "No oxo substituents found"

    # Check if any ketone is connected to naphthalene core
    naphthalene_atoms = set()
    for match in mol.GetSubstructMatches(naphthalene_pattern):
        naphthalene_atoms.update(match)

    ketone_connected = False
    for match in ketone_matches:
        carbon_idx = match[0]
        # Get neighbors of the ketone carbon
        neighbors = [n.GetIdx() for n in mol.GetAtomWithIdx(carbon_idx).GetNeighbors()]
        # Check if any neighbor is part of naphthalene core
        if any(n in naphthalene_atoms for n in neighbors):
            ketone_connected = True
            break

    if not ketone_connected:
        return False, "Oxo groups not connected to naphthalene core"

    num_oxo = len(ketone_matches)
    return True, f"Naphthalene with {num_oxo} oxo substituent(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25479',
                          'name': 'naphthalenone',
                          'definition': 'Any naphthalene that is carrying at '
                                        'least one oxo substituent.',
                          'parents': ['CHEBI:25477', 'CHEBI:3992']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 100,
    'num_true_negatives': 17523,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9942127659574468}