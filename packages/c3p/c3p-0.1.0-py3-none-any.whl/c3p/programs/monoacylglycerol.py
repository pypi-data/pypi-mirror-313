"""
Classifies: CHEBI:17408 monoacylglycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_monoacylglycerol(smiles: str):
    """
    Determines if a molecule is a monoacylglycerol (MAG).
    A MAG has one acyl group and two hydroxyl groups attached to a glycerol backbone.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monoacylglycerol, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define SMARTS patterns
    glycerol_backbone = Chem.MolFromSmarts("[CH2][CH]([OH,OR])[CH2][OH,OR]")
    ester_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[OX2][C]")
    oh_pattern = Chem.MolFromSmarts("[OH]")
    
    # Check for glycerol backbone
    if not mol.HasSubstructMatch(glycerol_backbone):
        return False, "No glycerol backbone found"

    # Count ester groups
    ester_matches = len(mol.GetSubstructMatches(ester_pattern))
    if ester_matches != 1:
        return False, f"Found {ester_matches} ester groups, expected 1"

    # Count hydroxyl groups
    oh_matches = len(mol.GetSubstructMatches(oh_pattern))
    if oh_matches != 2:
        return False, f"Found {oh_matches} hydroxyl groups, expected 2"

    # Check for proper connectivity
    # Find glycerol carbons and ester attachment
    glycerol_matches = mol.GetSubstructMatches(glycerol_backbone)
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    
    if not glycerol_matches or not ester_matches:
        return False, "Required structural elements not found"
        
    glycerol_atoms = set(glycerol_matches[0])
    ester_atoms = set(ester_matches[0])
    
    # Check if ester is connected to glycerol backbone
    ester_oxygen = ester_atoms.intersection(glycerol_atoms)
    if not ester_oxygen:
        return False, "Ester not properly connected to glycerol backbone"

    return True, "Valid monoacylglycerol structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17408',
                          'name': 'monoacylglycerol',
                          'definition': 'A glyceride in which any one of the R '
                                        'groups (position not specified) is an '
                                        'acyl group while the remaining two R '
                                        'groups can be either H or alkyl '
                                        'groups.',
                          'parents': ['CHEBI:47778']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               'False negatives: '
               "[('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)OC(CO)CO', 'No glycerol "
               "backbone found'), "
               "('O(C(=O)CCCCCCCCCCCCCCCCCCCCC)C[C@@H](O)CO', 'Ester group not "
               "properly connected to glycerol backbone'), "
               "('C(O)C(OC(*)=O)CO', 'No glycerol backbone found'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC(CO)CO', 'No glycerol backbone "
               "found'), ('CC(C)CCCCC=CCCCCCCCC(=O)OCC(CO)O', 'Ester group not "
               "properly connected to glycerol backbone'), "
               "('C(CCCCCCCCCCCC(OCC(CO)O)=O)CCCCCCC', 'Ester group not "
               "properly connected to glycerol backbone'), "
               "('CCCCC\\\\C=C\\\\C=C1/[C@@H](C\\\\C=C/CCCC(=O)OC(CO)CO)C=CC1=O', "
               "'No glycerol backbone found'), ('C(O)C(O)COC(=O)*', 'Ester "
               "group not properly connected to glycerol backbone'), "
               "('CCCCCCCCCCCC(=O)OC[C@@H](O)CO', 'Ester group not properly "
               "connected to glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCCCCC)CC(O)CO', 'Ester group not properly "
               "connected to glycerol backbone'), "
               "('O(C[C@@H](O)CO)C(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'Ester group not properly connected to glycerol backbone'), "
               "('O(C(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCC)C(CO)CO', "
               "'No glycerol backbone found'), "
               "('O=C1OC(/C(=C/C(=O)OC[C@H](O)CO)/C)=CC(=C1)OC', 'Ester group "
               "not properly connected to glycerol backbone'), "
               "('O=C(OCC(O)CO)CCCCCCCCCCCCCCC(CC)C', 'Ester group not "
               "properly connected to glycerol backbone'), "
               "('OC(CO)COC(=O)CCCCCCC/C=C/CCCCCCCC', 'Ester group not "
               "properly connected to glycerol backbone'), "
               "('CCCCCCCCCCCCCC(=O)OC[C@H](O)CO', 'Ester group not properly "
               "connected to glycerol backbone'), "
               "('C(CCCCCCCCCCCC)CCCCCCCCC(OCC(O)CO)=O', 'Ester group not "
               "properly connected to glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCC/C=C\\\\CCCCCCCC)C(CO)CO', 'No glycerol "
               "backbone found')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 12,
    'num_false_positives': 12,
    'num_true_negatives': 183768,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.5,
    'recall': 0.6666666666666666,
    'f1': 0.5714285714285715,
    'accuracy': 0.9999020663989815}