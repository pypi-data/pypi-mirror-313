"""
Classifies: CHEBI:17962 CDP-diacylglycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprint
from rdkit.Chem import rdMolDescriptors

def is_CDP_diacylglycerol(smiles: str):
    """
    Determines if a molecule is a CDP-diacylglycerol.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a CDP-diacylglycerol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for required substructures
    cytidine_pattern = Chem.MolFromSmarts("O1[C@H](CO)[C@@H](O)[C@H](O)[C@H]1N1C=CC(=NC1=O)N")
    diphosphate_pattern = Chem.MolFromSmarts("OP(=O)(O)OP(=O)(O)O")
    ester_pattern = Chem.MolFromSmarts("CC(=O)O")
    
    if not mol.HasSubstructMatch(cytidine_pattern):
        return False, "Missing cytidine moiety"
        
    if not mol.HasSubstructMatch(diphosphate_pattern):
        return False, "Missing diphosphate bridge"
    
    # Count number of ester groups
    ester_matches = len(mol.GetSubstructMatches(ester_pattern))
    if ester_matches < 2:
        return False, "Missing required acyl groups"
    elif ester_matches > 2:
        return False, "Too many ester groups"

    # Check for glycerol backbone
    glycerol_pattern = Chem.MolFromSmarts("OCC(CO)O")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "Missing glycerol backbone"

    # Check for long chain fatty acids (at least 8 carbons)
    carbon_chain = Chem.MolFromSmarts("CCCCCCCC")
    if len(mol.GetSubstructMatches(carbon_chain)) < 2:
        return False, "Acyl groups too short (need at least 8 carbons)"

    return True, "Contains cytidine diphosphate, glycerol backbone, and two fatty acyl groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17962',
                          'name': 'CDP-diacylglycerol',
                          'definition': 'A CDP-glycerol having unspecified '
                                        'acyl groups (most commonly fatty acyl '
                                        'groups) at the 1- and 2-positions.',
                          'parents': ['CHEBI:35774']},
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
    'num_true_negatives': 183885,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999728098319648}