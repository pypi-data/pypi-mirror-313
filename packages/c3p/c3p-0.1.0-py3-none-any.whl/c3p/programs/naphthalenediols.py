"""
Classifies: CHEBI:23783 naphthalenediols
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_naphthalenediols(smiles: str):
    """
    Determines if a molecule is a naphthalenediol (hydroxynaphthalene derivative with two hydroxy groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a naphthalenediol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for naphthalene core
    naphthalene_pattern = Chem.MolFromSmarts('c1ccc2ccccc2c1')
    dihydronaphthalene_pattern = Chem.MolFromSmarts('C1=Cc2ccccc2C1')
    
    is_naphthalene = mol.HasSubstructMatch(naphthalene_pattern)
    is_dihydronaphthalene = mol.HasSubstructMatch(dihydronaphthalene_pattern)
    
    if not (is_naphthalene or is_dihydronaphthalene):
        return False, "No naphthalene or dihydronaphthalene core found"

    # Count hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts('[OH]')
    hydroxyl_matches = mol.GetSubstructMatches(hydroxyl_pattern)
    
    num_hydroxyls = len(hydroxyl_matches)
    
    if num_hydroxyls != 2:
        return False, f"Found {num_hydroxyls} hydroxyl groups, need exactly 2"

    # Get positions of hydroxyls
    hydroxyl_positions = []
    for match in hydroxyl_matches:
        oh_atom = mol.GetAtomWithIdx(match[0])
        for neighbor in oh_atom.GetNeighbors():
            hydroxyl_positions.append(neighbor.GetIdx())
    
    if is_dihydronaphthalene:
        return True, "Dihydronaphthalene-diol"
    else:
        return True, "Naphthalene-diol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23783',
                          'name': 'naphthalenediols',
                          'definition': 'Any hydroxynaphthalene derivative '
                                        'that has two hydroxy substituents.',
                          'parents': ['CHEBI:24727']},
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
    'num_true_negatives': 35241,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9971139971139971}