"""
Classifies: CHEBI:166904 glycosyldiradylglycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_glycosyldiradylglycerol(smiles: str):
    """
    Determines if a molecule is a glycosyldiradylglycerol based on the following criteria:
    - Contains a glycerol backbone
    - Has a glycosyl group attached
    - Has two additional substituent groups (acyl, alkyl or alk-1-enyl)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycosyldiradylglycerol, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for glycerol backbone pattern
    # Look for C-C-C with O substituents
    glycerol_pattern = Chem.MolFromSmarts("[OX2H0]-[CH2]-[CH]-[CH2]-[OX2]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    # Check for glycosyl group
    # Look for cyclic sugar structure with multiple OH groups
    sugar_pattern = Chem.MolFromSmarts("[CH1,CH2]-[OH1]")
    sugar_matches = mol.GetSubstructMatches(sugar_pattern)
    if len(sugar_matches) < 3:  # Typical sugar has multiple OH groups
        return False, "No glycosyl group found"

    # Check for cyclic sugar structure
    ring_pattern = Chem.MolFromSmarts("[C]1[O][C][C][C][C]1")
    if not mol.HasSubstructMatch(ring_pattern):
        return False, "No sugar ring structure found"

    # Check for two additional substituents
    # Look for ester groups (acyl) or ether groups (alkyl/alkenyl)
    acyl_pattern = Chem.MolFromSmarts("C(=O)-O")
    alkyl_pattern = Chem.MolFromSmarts("C-O")
    
    acyl_count = len(mol.GetSubstructMatches(acyl_pattern))
    alkyl_count = len(mol.GetSubstructMatches(alkyl_pattern))
    
    if acyl_count + alkyl_count < 2:
        return False, "Does not have two additional substituent groups"

    substituent_types = []
    if acyl_count > 0:
        substituent_types.append("acyl")
    if alkyl_count > acyl_count:
        substituent_types.append("alkyl/alkenyl")

    return True, f"Contains glycerol backbone, glycosyl group and {', '.join(substituent_types)} substituents"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:166904',
                          'name': 'glycosyldiradylglycerol',
                          'definition': 'Any glycerolipid that is glycerol '
                                        'bearing a glycosyl group and two '
                                        'further substituent groups - either '
                                        'acyl, alkyl, or alk-1-enyl - at the '
                                        'remaining two positions.',
                          'parents': ['CHEBI:35741']},
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
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 60422,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 1.0,
    'f1': 0.13793103448275862,
    'accuracy': 0.9983479266479431}