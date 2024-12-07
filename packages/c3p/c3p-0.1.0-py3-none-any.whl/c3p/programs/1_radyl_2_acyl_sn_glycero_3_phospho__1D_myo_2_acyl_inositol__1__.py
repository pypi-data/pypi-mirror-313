"""
Classifies: CHEBI:143813 1-radyl,2-acyl-sn-glycero-3-phospho-(1D-myo-2-acyl-inositol)(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_radyl_2_acyl_sn_glycero_3_phospho__1D_myo_2_acyl_inositol__1__(smiles: str):
    """
    Determines if a molecule is a 1-radyl,2-acyl-sn-glycero-3-phospho-(1D-myo-2-acyl-inositol)(1-)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule belongs to the class, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for required substructures
    
    # myo-inositol core with phosphate attachment
    inositol_pattern = Chem.MolFromSmarts('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)O)[C@H](O)[C@@H]1O')
    if not mol.HasSubstructMatch(inositol_pattern):
        return False, "Missing myo-inositol core with correct stereochemistry"

    # Check for glycerol backbone with two acyl groups and phosphate connection
    glycerol_backbone = Chem.MolFromSmarts('OC[C@@H](COC(=O)*)OC(=O)*')
    if not mol.HasSubstructMatch(glycerol_backbone):
        return False, "Missing glycerol backbone with correct substitution pattern"

    # Check for phosphate group connecting inositol and glycerol
    phosphate = Chem.MolFromSmarts('OP([O-])(=O)OC')
    if not mol.HasSubstructMatch(phosphate):
        return False, "Missing phosphate group"

    # Check for two carbonyl groups (acyl chains)
    carbonyls = mol.GetSubstructMatches(Chem.MolFromSmarts('C(=O)'))
    if len(carbonyls) != 2:
        return False, "Must have exactly two carbonyl groups"

    # Verify the presence of exactly one negative charge
    charge_count = sum(1 for atom in mol.GetAtoms() if atom.GetFormalCharge() == -1)
    if charge_count != 1:
        return False, "Should have exactly one negative charge"

    return True, "Structure matches 1-radyl,2-acyl-sn-glycero-3-phospho-(1D-myo-2-acyl-inositol)(1-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:143813',
                          'name': '1-radyl,2-acyl-sn-glycero-3-phospho-(1D-myo-2-acyl-inositol)(1-)',
                          'definition': 'A phosphatidylinositol where R1 can '
                                        'be an alkyl or an acyl chain and 2R2 '
                                        'is an acyl chain.',
                          'parents': ['CHEBI:50860']},
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
               "[('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)[C@H](O)[C@@H]1O', "
               "'Missing phosphate group'), "
               "('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)[C@H](O)[C@@H]1O', "
               "'Missing phosphate group'), "
               "('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)[C@H](O)[C@@H]1O', "
               "'Missing phosphate group'), "
               "('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)[C@H](O)[C@@H]1O', "
               "'Missing phosphate group'), "
               "('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)[C@H](O)[C@@H]1O', "
               "'Missing phosphate group'), "
               "('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)[C@H](O)[C@@H]1O', "
               "'Missing phosphate group'), "
               "('O=P([O-])(O[C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O)O)O)O)O)OC[C@@H](COC(CCCCCCC/C=C\\\\CCCCCCCC)=O)OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O', "
               "'Missing phosphate group')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 7,
    'num_false_positives': 11,
    'num_true_negatives': 183888,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.3888888888888889,
    'recall': 1.0,
    'f1': 0.56,
    'accuracy': 0.9999401868345785}