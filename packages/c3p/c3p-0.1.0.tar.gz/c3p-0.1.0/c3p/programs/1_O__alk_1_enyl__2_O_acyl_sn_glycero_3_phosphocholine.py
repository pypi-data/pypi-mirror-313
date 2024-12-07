"""
Classifies: CHEBI:17810 1-O-(alk-1-enyl)-2-O-acyl-sn-glycero-3-phosphocholine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_1_O__alk_1_enyl__2_O_acyl_sn_glycero_3_phosphocholine(smiles: str):
    """
    Determines if a molecule is a 1-O-(alk-1-enyl)-2-O-acyl-sn-glycero-3-phosphocholine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule matches the class, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for phosphocholine group
    phos_pattern = Chem.MolFromSmarts('[O][P](=O)([O-])OCC[N+](C)(C)C')
    if not mol.HasSubstructMatch(phos_pattern):
        return False, "Missing phosphocholine group"

    # Check for glycerol backbone with correct stereochemistry
    glycerol_pattern = Chem.MolFromSmarts('[C@@H](COP([O-])(=O)*)(*)*')
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "Missing glycerol backbone with correct stereochemistry"

    # Check for alk-1-enyl group at position 1
    alkenyl_pattern = Chem.MolFromSmarts('O/C=C/*')
    if not mol.HasSubstructMatch(alkenyl_pattern):
        return False, "Missing alk-1-enyl group at position 1"

    # Check for acyl group at position 2
    acyl_pattern = Chem.MolFromSmarts('C(=O)O[C@H]')
    if not mol.HasSubstructMatch(acyl_pattern):
        return False, "Missing acyl group at position 2"

    # If all patterns match, this is a valid 1-O-(alk-1-enyl)-2-O-acyl-sn-glycero-3-phosphocholine
    return True, "Contains required 1-O-(alk-1-enyl)-2-O-acyl-sn-glycero-3-phosphocholine structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17810',
                          'name': '1-O-(alk-1-enyl)-2-O-acyl-sn-glycero-3-phosphocholine',
                          'definition': 'A glycero-3-phosphocholine compound '
                                        'having an alk-1-enyl substituent at '
                                        'the 1-position and an acyl '
                                        'substituent at the 2-position.',
                          'parents': [   'CHEBI:167497',
                                         'CHEBI:68489',
                                         'CHEBI:76170',
                                         'CHEBI:78188']},
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
    'num_true_positives': 6,
    'num_false_positives': 82,
    'num_true_negatives': 183826,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06818181818181818,
    'recall': 1.0,
    'f1': 0.1276595744680851,
    'accuracy': 0.9995541394347358}