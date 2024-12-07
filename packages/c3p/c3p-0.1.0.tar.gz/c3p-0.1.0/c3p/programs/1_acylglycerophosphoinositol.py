"""
Classifies: CHEBI:16617 1-acylglycerophosphoinositol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_1_acylglycerophosphoinositol(smiles: str):
    """
    Determines if a molecule is a 1-acylglycerophosphoinositol.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 1-acylglycerophosphoinositol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for phosphate group
    phos_pattern = Chem.MolFromSmarts('[P](=O)(O)(O)O')
    if not mol.HasSubstructMatch(phos_pattern):
        return False, "No phosphate group found"

    # Check for glycerol backbone with ester at position 1
    glycerol_ester_pattern = Chem.MolFromSmarts('OCC(O)COP(=O)(O)O')
    if not mol.HasSubstructMatch(glycerol_ester_pattern):
        return False, "No glycerol backbone with phosphate found"

    # Check for inositol ring (cyclohexane with OH groups)
    inositol_pattern = Chem.MolFromSmarts('C1C(O)C(O)C(O)C(O)C1O')
    if not mol.HasSubstructMatch(inositol_pattern):
        return False, "No inositol ring found"

    # Check for acyl group at position 1
    acyl_pattern = Chem.MolFromSmarts('C(=O)OCC(O)COP(=O)(O)O')
    if not mol.HasSubstructMatch(acyl_pattern):
        return False, "No acyl group at position 1 found"

    # Check for complete structure
    complete_pattern = Chem.MolFromSmarts('C(=O)OCC(O)COP(=O)(O)OC1C(O)C(O)C(O)C(O)C1O')
    if not mol.HasSubstructMatch(complete_pattern):
        return False, "Structure components not properly connected"

    return True, "Valid 1-acylglycerophosphoinositol structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16617',
                          'name': '1-acylglycerophosphoinositol',
                          'definition': 'A glycerophosphoinositol acylated at '
                                        'O(1) of the glycerol moiety.',
                          'parents': ['CHEBI:36315']},
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
               "[('C(C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CC(=O)OC[C@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)O', "
               "'No phosphate group found'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCCCCCC/C=C\\\\CCCCC)(O)=O', "
               "'No phosphate group found'), "
               "('P(O[C@H]1[C@H](O[C@H]2OC([C@@H](O)C(O)[C@H]2O)CO)C(O)[C@H](O)C(O)C1O)(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCC)(O)=O', "
               "'No phosphate group found'), "
               "('P(O[C@H]1[C@H](O[C@H]2OC([C@@H](O)C(O)[C@H]2O)CO)C(O)[C@H](O)C(O)C1O)(OC[C@H](O)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)=O', "
               "'No phosphate group found')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 28921,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9965546942291128}