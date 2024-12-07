"""
Classifies: CHEBI:17615 1,2-diacyl-3-beta-D-galactosyl-sn-glycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_1_2_diacyl_3_beta_D_galactosyl_sn_glycerol(smiles: str):
    """
    Determines if a molecule is a 1,2-diacyl-3-beta-D-galactosyl-sn-glycerol.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule belongs to the class, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of galactose moiety
    galactose_pattern = Chem.MolFromSmarts("[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@@H]1O")
    if not mol.HasSubstructMatch(galactose_pattern):
        return False, "Missing beta-D-galactosyl moiety"

    # Check for glycerol backbone with correct stereochemistry
    glycerol_pattern = Chem.MolFromSmarts("[C@@H](COC(=O)*)([C@H](O*)CO*)O*")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "Missing or incorrect sn-glycerol backbone"

    # Check for two acyl groups
    acyl_pattern = Chem.MolFromSmarts("C(=O)-[#6]")
    acyl_matches = mol.GetSubstructMatches(acyl_pattern)
    if len(acyl_matches) < 2:
        return False, "Missing required acyl groups"

    # Check connection between galactose and glycerol
    gal_gly_link = Chem.MolFromSmarts("[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@@H]1OC[C@H]")
    if not mol.HasSubstructMatch(gal_gly_link):
        return False, "Incorrect linkage between galactose and glycerol"

    return True, "Structure contains beta-D-galactosyl moiety at position 3 of 1,2-diacyl-sn-glycerol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17615',
                          'name': '1,2-diacyl-3-beta-D-galactosyl-sn-glycerol',
                          'definition': 'A class of galactoglycerolipids that '
                                        'consists of any '
                                        '1,2-diacyl-sn-glycerol having a '
                                        'beta-D-galactosyl residue attached at '
                                        'position 3.',
                          'parents': ['CHEBI:61799', 'CHEBI:90549']},
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
    'num_false_positives': 47,
    'num_true_negatives': 183871,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9997227085394895}