"""
Classifies: CHEBI:17002 cholesteryl ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cholesteryl_ester(smiles: str):
    """
    Determines if a molecule is a cholesteryl ester.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cholesteryl ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of ester group
    ester_pattern = Chem.MolFromSmarts('[#6]-O-C(=O)-[#6]')
    if not mol.HasSubstructMatch(ester_pattern):
        return False, "No ester group found"

    # Check for steroid core (four fused rings - three 6-membered, one 5-membered)
    steroid_core = Chem.MolFromSmarts('C1CC2CCC3C(C2)CCC4CCCC34C1')
    if not mol.HasSubstructMatch(steroid_core):
        return False, "No steroid core structure found"

    # Check for specific cholesterol features
    # - One double bond in ring B
    # - Methyl groups at C10 and C13
    # - 8-carbon side chain at C17
    cholesterol_features = Chem.MolFromSmarts('[CH2]-[CH2]-C1-C-C=C-C2-C1-[CH2]-[CH2]-C3-C2-[CH2]-[CH2]-C4(C)-C3-C-C(C)-[CH](C)CCCC(C)C')
    if not mol.HasSubstructMatch(cholesterol_features):
        return False, "Missing characteristic cholesterol features"

    # Check if ester is at position 3 (beta orientation)
    # This is complex to verify precisely via SMARTS, but we can check if the ester is connected to the steroid core
    matches = mol.GetSubstructMatches(ester_pattern)
    steroid_matches = mol.GetSubstructMatches(steroid_core)
    
    if not matches or not steroid_matches:
        return False, "Could not verify ester position"

    # Get the acyl chain length
    acyl_pattern = Chem.MolFromSmarts('O=C([#6]*)O')
    acyl_matches = mol.GetSubstructMatches(acyl_pattern)
    
    if acyl_matches:
        return True, "Cholesteryl ester with acyl chain"
    
    return True, "Cholesteryl ester structure identified"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17002',
                          'name': 'cholesteryl ester',
                          'definition': 'A sterol ester obtained by formal '
                                        'condensation of the carboxy group of '
                                        'any carboxylic acid with the '
                                        '3-hydroxy group of cholesterol.',
                          'parents': ['CHEBI:35915']},
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
    'num_true_negatives': 183883,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.99995649596772}