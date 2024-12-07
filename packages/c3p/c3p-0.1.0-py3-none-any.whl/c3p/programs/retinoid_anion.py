"""
Classifies: CHEBI:139589 retinoid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_retinoid_anion(smiles: str):
    """
    Determines if a molecule is a retinoid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if molecule is a retinoid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylate anion
    carboxylate_pattern = Chem.MolFromSmarts('C(=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion group found"

    # Pattern for retinoid core with flexible chain length and terminal carboxylate
    # This pattern allows for variations in the cyclohexene ring substitution
    retinoid_pattern = Chem.MolFromSmarts('[#6]1~[#6]~[#6]~[#6]~[#6]~[#6]1~[#6]=[#6]~[#6]=[#6]~[#6]=[#6]~[#6]=C-C(=O)[O-]')
    
    # Pattern for retinoid glucuronate derivatives
    retinoid_glucuronate = Chem.MolFromSmarts('[#6]1~[#6]~[#6]~[#6]~[#6]~[#6]1~[#6]=[#6]~[#6]=[#6]~[#6]=[#6]~[#6]-C(=O)O[C]1[C][C]([C]([C]([C]1)C(=O)[O-])O)O')

    if mol.HasSubstructMatch(retinoid_pattern):
        # Additional check for conjugated system
        conjugated_system = Chem.MolFromSmarts('C=CC=CC=CC=C')
        if mol.HasSubstructMatch(conjugated_system):
            return True, "Retinoid anion with conjugated system and carboxylate group"
    
    if mol.HasSubstructMatch(retinoid_glucuronate):
        return True, "Retinoid glucuronate derivative with carboxylate group"

    # Check for specific pattern with methyl substitutions
    specific_pattern = Chem.MolFromSmarts('[CH3]-[#6]1-[#6](-[CH3])-[#6]-[#6]-[#6](-[CH3])-[#6]1-[#6]=[#6]-[#6](-[CH3])=[#6]-[#6]=[#6]-[#6](-[CH3])=[#6]-C(=O)[O-]')
    if mol.HasSubstructMatch(specific_pattern):
        return True, "Methylated retinoid anion"

    return False, "Not a retinoid anion structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139589',
                          'name': 'retinoid anion',
                          'definition': 'A carboxylic acid anion obtained by '
                                        'deprotonation of any retinoid carboxy '
                                        'group.',
                          'parents': ['CHEBI:29067']},
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
               "[('C1(C)(CO)CCC(C(=C1\\\\C=C\\\\C(=C\\\\C=C\\\\C(=C\\\\C(=O)[O-])\\\\C)\\\\C)C)O', "
               "'No retinoid core structure found'), "
               "('C1C(C(=C(CC1)C)/C=C/C(/C)=C/C=C/C(/C)=C/C(O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C(=O)[O-])O)O)O)=O)(C)C', "
               "'No retinoid core structure found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 6,
    'num_true_negatives': 183908,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.14285714285714285,
    'recall': 0.5,
    'f1': 0.22222222222222224,
    'accuracy': 0.999961939146132}