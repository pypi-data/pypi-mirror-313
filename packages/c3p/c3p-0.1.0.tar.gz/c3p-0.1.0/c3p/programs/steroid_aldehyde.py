"""
Classifies: CHEBI:131565 steroid aldehyde
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_steroid_aldehyde(smiles: str):
    """
    Determines if a molecule is a steroid aldehyde (steroid with formyl group).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a steroid aldehyde, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for steroid core structure (cyclopentanoperhydrophenanthrene)
    # This SMARTS pattern matches the 4-ring steroid core structure more flexibly
    steroid_pattern = Chem.MolFromSmarts("C1C[C@H]2[C@H]3C[C@H](C4=CC=CC=C4)C[C@H]3CC[C@]2(C)C1")
    
    # Alternative steroid patterns to catch different configurations
    steroid_pattern2 = Chem.MolFromSmarts("C1CC2C3CCC4CCCCC4C3CCC2C1")
    steroid_pattern3 = Chem.MolFromSmarts("C1CC2C3CC=C4CCCCC4C3CCC2C1")
    steroid_pattern4 = Chem.MolFromSmarts("C1CC2C3CCC4CC(=O)CCC4C3CCC2C1")

    has_steroid = any(mol.HasSubstructMatch(pattern) for pattern in 
                     [steroid_pattern, steroid_pattern2, steroid_pattern3, steroid_pattern4])

    if not has_steroid:
        # Additional check for steroid-like structure by counting fused rings
        ring_info = mol.GetRingInfo()
        if not (len(ring_info.AtomRings()) >= 4):
            return False, "No steroid core structure found"

    # Check for aldehyde group (formyl group)
    aldehyde_pattern = Chem.MolFromSmarts("[CH]=O")
    if not mol.HasSubstructMatch(aldehyde_pattern):
        return False, "No aldehyde group found"

    # Count number of aldehyde groups
    aldehyde_matches = len(mol.GetSubstructMatches(aldehyde_pattern))
    
    return True, f"Steroid with {aldehyde_matches} aldehyde group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131565',
                          'name': 'steroid aldehyde',
                          'definition': 'Any steroid substituted by a formyl '
                                        'group.',
                          'parents': ['CHEBI:17478', 'CHEBI:35341']},
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
               "[('C[C@]12CC(=O)[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2C(=O)C=O', "
               "'No steroid core structure found'), "
               "('CC(=O)O[C@H]1CC[C@@]2(C)[C@@H](CC[C@H]3[C@@H]4CC(C=O)=C[C@@]4(C)CC[C@H]23)C1', "
               "'No steroid core structure found'), "
               "('[H][C@@]1(O[C@H]2CC[C@]3(C=O)[C@@]4([H])[C@H](O)C[C@]5(C)[C@H](CC[C@]5(O)[C@]4([H])CC[C@]3(O)C2)C2=CC(=O)OC2)O[C@H](C)[C@@H](O[C@]2([H])O[C@H](CO)[C@@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H]1O', "
               "'No steroid core structure found'), "
               "('C[C@]12CC[C@@H](O)C[C@H]1CC[C@H]1[C@@H]3CC[C@H](C(=O)CO)[C@]3(C[C@H](O)[C@H]21)C=O', "
               "'No steroid core structure found'), "
               "('C[C@@]12[C@@]3([C@]([C@]4([C@@](C[C@H]3O)(C)[C@@](CC4)(C)O)[H])(CCC1=CC(C(=C2)C=O)=O)[H])[H]', "
               "'No steroid core structure found'), "
               "('C[C@]12CCC3C([C@]1(CCC2C4=CC(=O)OC4)O)CC[C@]5([C@@]3(CC[C@@H](C5)O)C=O)O', "
               "'No steroid core structure found'), "
               "('[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CC[C@H](O)C(C)C=O', "
               "'No steroid core structure found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 20550,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.9951590259960305}