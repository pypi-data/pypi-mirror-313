"""
Classifies: CHEBI:17088 monoacyl-sn-glycerol 3-phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_monoacyl_sn_glycerol_3_phosphate(smiles: str):
    """
    Determines if a molecule is a monoacyl-sn-glycerol 3-phosphate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a monoacyl-sn-glycerol 3-phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for phosphate group
    patt_phosphate = Chem.MolFromSmarts('[PX4](=O)([OH])[OH]')
    if not mol.HasSubstructMatch(patt_phosphate):
        return False, "No phosphate group found"
        
    # Check for glycerol backbone with one acyl group
    # Match pattern: -O-CH2-CH(OH)-CH2-O-P where one of the non-phosphate oxygens has an acyl group
    patt_glycerol = Chem.MolFromSmarts('[OX2][CH2][CH]([OH])[CH2][OX2]P(=O)([OH])[OH]')
    if not mol.HasSubstructMatch(patt_glycerol):
        return False, "No glycerol backbone with phosphate found"
        
    # Check for exactly one acyl group (-C(=O)-)
    patt_acyl = Chem.MolFromSmarts('[CX3](=O)')
    acyl_matches = mol.GetSubstructMatches(patt_acyl)
    
    if len(acyl_matches) == 0:
        return False, "No acyl group found"
    elif len(acyl_matches) > 1:
        return False, "More than one acyl group found"
        
    # Check if acyl group is attached to glycerol backbone
    patt_full = Chem.MolFromSmarts('[CX3](=O)-[OX2]-[CH2]-[CH]([OH])-[CH2]-[OX2]-P(=O)([OH])[OH]')
    patt_full2 = Chem.MolFromSmarts('[CX3](=O)-[OX2]-[CH2]-[CH](-[OX2]-[CH2]-P(=O)([OH])[OH])[OH]')
    
    if not (mol.HasSubstructMatch(patt_full) or mol.HasSubstructMatch(patt_full2)):
        return False, "Acyl group not properly connected to glycerol backbone"

    return True, "Molecule is a monoacyl-sn-glycerol 3-phosphate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17088',
                          'name': 'monoacyl-sn-glycerol 3-phosphate',
                          'definition': 'An sn-glycero-3-phosphate compound '
                                        'having a single unspecified acyl '
                                        'group at either position 1 or '
                                        'position 2.',
                          'parents': ['CHEBI:16961', 'CHEBI:26706']},
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
    'num_true_positives': 4,
    'num_false_positives': 5,
    'num_true_negatives': 183864,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.4444444444444444,
    'recall': 0.6666666666666666,
    'f1': 0.5333333333333333,
    'accuracy': 0.9999619306594154}