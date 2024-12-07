"""
Classifies: CHEBI:23245 cinnamaldehydes
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cinnamaldehydes(smiles: str):
    """
    Determines if a molecule is a cinnamaldehyde (enal with cinnamaldehyde skeleton).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cinnamaldehyde, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of aldehyde group (-CHO)
    aldehyde_pattern = Chem.MolFromSmarts('[CH1](=O)')
    if not mol.HasSubstructMatch(aldehyde_pattern):
        return False, "No aldehyde group found"

    # Check for conjugated double bond system
    conjugated_pattern = Chem.MolFromSmarts('[#6]=[#6]-[#6]=O')
    if not mol.HasSubstructMatch(conjugated_pattern):
        return False, "No conjugated double bond system found"

    # Check for benzene ring
    benzene_pattern = Chem.MolFromSmarts('c1ccccc1')
    if not mol.HasSubstructMatch(benzene_pattern):
        return False, "No benzene ring found"

    # Check for complete cinnamaldehyde skeleton (benzene-CH=CH-CHO)
    cinnamaldehyde_pattern = Chem.MolFromSmarts('c1ccccc1-[#6]=[#6]-[CH1]=O')
    if not mol.HasSubstructMatch(cinnamaldehyde_pattern):
        return False, "Does not match cinnamaldehyde skeleton"

    # Get substituents on benzene ring
    substituents = []
    matches = mol.GetSubstructMatches(benzene_pattern)
    if matches:
        ring_atoms = set(matches[0])
        for atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms and neighbor.GetSymbol() != 'C':
                    substituents.append(neighbor.GetSymbol())

    if substituents:
        return True, f"Cinnamaldehyde derivative with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted cinnamaldehyde"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23245',
                          'name': 'cinnamaldehydes',
                          'definition': 'An  enal based on a cinnamaldehyde '
                                        'skeleton and its substituted '
                                        'derivatives.',
                          'parents': ['CHEBI:51688']},
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
    'num_true_positives': 3,
    'num_false_positives': 25,
    'num_true_negatives': 183876,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.10714285714285714,
    'recall': 1.0,
    'f1': 0.19354838709677416,
    'accuracy': 0.9998640595093092}