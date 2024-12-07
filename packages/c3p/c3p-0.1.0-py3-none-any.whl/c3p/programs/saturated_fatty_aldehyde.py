"""
Classifies: CHEBI:133249 saturated fatty aldehyde
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_saturated_fatty_aldehyde(smiles: str):
    """
    Determines if a molecule is a saturated fatty aldehyde.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a saturated fatty aldehyde, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for presence of aldehyde group (C=O)
    pattern_aldehyde = Chem.MolFromSmarts('[CH1](=O)')
    if not mol.HasSubstructMatch(pattern_aldehyde):
        return False, "No aldehyde group found"
    
    # Count number of aldehyde groups
    matches = mol.GetSubstructMatches(pattern_aldehyde)
    if len(matches) > 1:
        return False, "Multiple aldehyde groups found"
    
    # Check for carbon chain length (at least 2 carbons)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 2:
        return False, "Carbon chain too short"
    
    # Check for absence of carbon-carbon double or triple bonds
    pattern_unsaturation = Chem.MolFromSmarts('[#6]=[#6,#7,#8]')
    matches = mol.GetSubstructMatches(pattern_unsaturation)
    
    # We expect exactly one match for the aldehyde C=O
    if len(matches) > 1:
        return False, "Contains carbon-carbon unsaturation"
    elif len(matches) == 1:
        # Verify that the only unsaturation is the aldehyde group
        match = matches[0]
        aldehyde_carbon = mol.GetAtomWithIdx(match[0])
        if not any(n.GetSymbol() == 'O' for n in aldehyde_carbon.GetNeighbors()):
            return False, "Contains carbon-carbon unsaturation"
    
    # Check for triple bonds
    pattern_triple_bond = Chem.MolFromSmarts('[#6]#[#6,#7,#8]')
    if mol.HasSubstructMatch(pattern_triple_bond):
        return False, "Contains triple bonds"
    
    return True, "Saturated fatty aldehyde confirmed"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133249',
                          'name': 'saturated fatty aldehyde',
                          'definition': 'A fatty aldehyde in which there is no '
                                        'carbon-carbon unsaturation.',
                          'parents': ['CHEBI:35746']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 22512,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9955779605554081}