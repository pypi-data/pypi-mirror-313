"""
Classifies: CHEBI:17476 1-(alk-1-enyl)-2-acyl-sn-glycero-3-phosphoethanolamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_1__alk_1_enyl__2_acyl_sn_glycero_3_phosphoethanolamine(smiles: str):
    """
    Determines if a molecule is a 1-(alk-1-enyl)-2-acyl-sn-glycero-3-phosphoethanolamine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule matches the class, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for phosphoethanolamine group
    ptn1 = Chem.MolFromSmarts('[P](=O)([O-,OH])[O][CH2][CH2][NH2]')
    if not mol.HasSubstructMatch(ptn1):
        return False, "Missing phosphoethanolamine group"

    # Check for glycerol backbone with specific stereochemistry
    ptn2 = Chem.MolFromSmarts('[CH2][C@H]([CH2])')  
    if not mol.HasSubstructMatch(ptn2):
        return False, "Missing glycerol backbone or incorrect stereochemistry"

    # Check for alk-1-enyl group at position 1
    ptn3 = Chem.MolFromSmarts('[CH2]O[CH2][C@H]([CH2]OC=C)')
    if not mol.HasSubstructMatch(ptn3):
        return False, "Missing alk-1-enyl group at position 1"

    # Check for acyl group at position 2
    ptn4 = Chem.MolFromSmarts('[CH2]O[CH2][C@H](OC(=O))[CH2]')
    if not mol.HasSubstructMatch(ptn4):
        return False, "Missing acyl group at position 2"

    # If all patterns match, classify as positive
    return True, "Contains 1-(alk-1-enyl)-2-acyl-sn-glycero-3-phosphoethanolamine structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17476',
                          'name': '1-(alk-1-enyl)-2-acyl-sn-glycero-3-phosphoethanolamine',
                          'definition': 'A glycerophosphoethanolamine compound '
                                        'having an alk-1-enyl substituent at '
                                        'the 1-position and an acyl '
                                        'substituent at the 2-position.',
                          'parents': ['CHEBI:36314', 'CHEBI:76170']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183909,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999728133801669}