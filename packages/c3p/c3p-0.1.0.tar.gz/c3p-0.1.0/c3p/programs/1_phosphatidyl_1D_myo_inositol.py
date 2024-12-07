"""
Classifies: CHEBI:16749 1-phosphatidyl-1D-myo-inositol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_phosphatidyl_1D_myo_inositol(smiles: str):
    """
    Determines if a molecule is a 1-phosphatidyl-1D-myo-inositol.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 1-phosphatidyl-1D-myo-inositol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for inositol ring
    inositol_pattern = Chem.MolFromSmarts("[C@@H]1[C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)O)O")
    if not mol.HasSubstructMatch(inositol_pattern):
        return False, "Does not contain 1D-myo-inositol ring with correct stereochemistry"

    # Check for phosphate group at position 1
    phosphate_pattern = Chem.MolFromSmarts("OP(O)(=O)O")
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "Does not contain phosphate group"

    # Check for glycerol backbone with fatty acid esters
    glycerol_pattern = Chem.MolFromSmarts("OC[C@@H](COC(=O)*)OC(=O)*")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "Does not contain glycerol backbone with fatty acid esters"

    # Check if phosphate connects inositol and glycerol
    phosphatidyl_pattern = Chem.MolFromSmarts("[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)O)OP(OC[C@@H](COC(=O)*)OC(=O)*)(=O)O)O")
    if not mol.HasSubstructMatch(phosphatidyl_pattern):
        return False, "Phosphate group does not correctly connect inositol and glycerol moieties"

    return True, "Contains 1D-myo-inositol ring with phosphatidyl group at position 1"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16749',
                          'name': '1-phosphatidyl-1D-myo-inositol',
                          'definition': 'A phosphatidylinositol in which the '
                                        'inositol moiety is the 1D-myo isomer '
                                        'and the phosphatidyl group is located '
                                        'at its position 1.',
                          'parents': ['CHEBI:28874']},
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
    'num_true_negatives': 31194,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 1.0,
    'f1': 0.13793103448275862,
    'accuracy': 0.9968053159542521}