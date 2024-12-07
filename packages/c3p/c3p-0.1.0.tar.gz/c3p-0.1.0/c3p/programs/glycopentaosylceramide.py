"""
Classifies: CHEBI:23073 glycopentaosylceramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_glycopentaosylceramide(smiles: str):
    """
    Determines if a molecule is a glycopentaosylceramide - an oligoglycosylceramide with 5 sugar units
    attached to ceramide.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glycopentaosylceramide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for ceramide core
    ceramide_pattern = Chem.MolFromSmarts("[CH2]-[CH]-[CH]-N-C(=O)-*") 
    if not mol.HasSubstructMatch(ceramide_pattern):
        return False, "No ceramide core found"

    # Count sugar units (pyranose rings)
    sugar_pattern = Chem.MolFromSmarts("[C]1[C][C][C][C]([C]1)O")
    sugar_matches = mol.GetSubstructMatches(sugar_pattern)
    
    if len(sugar_matches) != 5:
        return False, f"Found {len(sugar_matches)} sugar units instead of required 5"

    # Check for glycosidic linkages between sugars
    glycosidic_pattern = Chem.MolFromSmarts("[C]-O-[C]")
    glycosidic_matches = mol.GetSubstructMatches(glycosidic_pattern)
    
    if len(glycosidic_matches) < 5:
        return False, "Insufficient glycosidic linkages between sugar units"

    # Check for hydroxyl groups characteristic of sugars
    hydroxyl_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts("O[CH]")))
    if hydroxyl_count < 15: # Each sugar typically has 3-4 OH groups
        return False, "Insufficient hydroxyl groups for pentasaccharide structure"

    # If all checks pass, this is likely a glycopentaosylceramide
    return True, "Contains ceramide core with 5 sugar units connected by glycosidic bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23073',
                          'name': 'glycopentaosylceramide',
                          'definition': 'An oligoglycosylceramide consisting '
                                        'of a glycopentaosyl moiety attached '
                                        'to the ceramide oxygen with an '
                                        'unspecified N-acyl substituent '
                                        'attached to the ceramide nitrogen.',
                          'parents': ['CHEBI:36520']},
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
    'num_true_negatives': 183838,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999510462504148}