"""
Classifies: CHEBI:23798 dimethoxyflavone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_dimethoxyflavone(smiles: str):
    """
    Determines if a molecule is a dimethoxyflavone (flavone with exactly 2 methoxy substituents).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a dimethoxyflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for flavone core structure (C15H10O2)
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('O=C1CC(=O)c2ccccc2O1'))
    if not matches:
        return False, "No flavone core structure found"
        
    # Count methoxy groups (-OCH3)
    methoxy_pattern = Chem.MolFromSmarts('OC')
    methoxy_matches = mol.GetSubstructMatches(methoxy_pattern)
    
    # Verify each methoxy match is actually -OCH3 (not part of larger group)
    true_methoxy_count = 0
    methoxy_positions = []
    
    for match in methoxy_matches:
        o_atom = mol.GetAtomWithIdx(match[0])
        c_atom = mol.GetAtomWithIdx(match[1])
        
        # Check if carbon has exactly 3 hydrogens
        if c_atom.GetTotalNumHs() == 3:
            # Get position number on flavone core
            for neighbor in o_atom.GetNeighbors():
                if neighbor.GetIdx() != match[1]:  # not the methyl carbon
                    methoxy_positions.append(neighbor.GetIdx())
                    true_methoxy_count += 1
                    
    if true_methoxy_count != 2:
        return False, f"Found {true_methoxy_count} methoxy groups, need exactly 2"
        
    return True, f"Dimethoxyflavone with methoxy groups at positions {methoxy_positions}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23798',
                          'name': 'dimethoxyflavone',
                          'definition': 'Any methoxyflavone with two methoxy '
                                        'substituents.',
                          'parents': ['CHEBI:25241']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183891,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999782484569999}