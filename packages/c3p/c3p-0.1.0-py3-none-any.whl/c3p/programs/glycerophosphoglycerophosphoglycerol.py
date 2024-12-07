"""
Classifies: CHEBI:166988 glycerophosphoglycerophosphoglycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_glycerophosphoglycerophosphoglycerol(smiles: str):
    """
    Determines if a molecule is a glycerophosphoglycerophosphoglycerol.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycerophosphoglycerophosphoglycerol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of required elements
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    if not all(element in atoms for element in ['C', 'O', 'P']):
        return False, "Missing required elements (C, O, P)"

    # Count phosphorus atoms - should be exactly 2
    p_count = len([atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'P'])
    if p_count != 2:
        return False, f"Found {p_count} phosphorus atoms, expected 2"

    # Core structure pattern: two phosphate groups connected by a glycerol bridge
    core_pattern = Chem.MolFromSmarts('[P](=O)([O,OH])[O]CC([OH1,O])COP(=O)([O,OH])[O]')
    if not mol.HasSubstructMatch(core_pattern):
        return False, "Missing core glycerophosphoglycerophosphoglycerol structure"

    # Check for glycerol moieties with ester linkages
    glycerol_ester_pattern = Chem.MolFromSmarts('[O]P(=O)([O,OH])[O]CC(OC(=O)[C])CO[C](=O)[C]')
    if len(mol.GetSubstructMatches(glycerol_ester_pattern)) < 2:
        return False, "Missing required glycerol moieties with ester linkages"

    # Check for fatty acid chains (at least 8 carbons)
    fatty_acid_pattern = Chem.MolFromSmarts('[C][C][C][C][C][C][C][C]')
    fatty_acid_count = len(mol.GetSubstructMatches(fatty_acid_pattern))
    if fatty_acid_count < 2:
        return False, "Missing required fatty acid chains"

    # Additional check for the complete structure connectivity
    complete_pattern = Chem.MolFromSmarts('[O]P(=O)([O,OH])[O]CC(OC(=O)[C])CO[C](=O)[C].CC([OH1,O])COP(=O)([O,OH])[O]CC(OC(=O)[C])CO[C](=O)[C]')
    if not mol.HasSubstructMatch(complete_pattern):
        return False, "Incorrect overall structure connectivity"

    return True, "Valid glycerophosphoglycerophosphoglycerol structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:166988',
                          'name': 'glycerophosphoglycerophosphoglycerol',
                          'definition': 'A glycerophospholipid composed of two '
                                        'molecules of glycerol phosphate '
                                        'covalently linked to a molecule of '
                                        'glycerol, and in which each of the '
                                        'glycerol phosphate moieties may be '
                                        'esterified to one or two fatty acids.',
                          'parents': ['CHEBI:37739']},
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
               "[('P(OC[C@H](OC(=O)CCCCCCCCCC)COC(=O)CCCCCCCCC)(OC[C@@H](O)COP(OC[C@H](OC(=O)CCCCCCCCC)COC(=O)CCCCCCCCC)(O)=O)(O)=O', "
               "'Missing required phosphate groups'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(OC[C@H](O)COP(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(O)=O)(O)=O', "
               "'Missing required phosphate groups'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OC[C@@H](O)COP(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O)(O)=O', "
               "'Missing required phosphate groups'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OC[C@H](O)COP(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(O)=O)(O)=O', "
               "'Missing required phosphate groups')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 11,
    'num_true_negatives': 183887,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.26666666666666666,
    'recall': 1.0,
    'f1': 0.4210526315789474,
    'accuracy': 0.9999401855335994}