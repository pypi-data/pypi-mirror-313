"""
Classifies: CHEBI:17387 O-acylcarnitine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_O_acylcarnitine(smiles: str):
    """
    Determines if a molecule is an O-acylcarnitine based on its SMILES string.
    O-acylcarnitines are carboxylic esters obtained by O-acylation of carnitine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an O-acylcarnitine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define SMARTS patterns for key structural features
    # Pattern for carnitine core with ester linkage and carboxylate
    carnitine_pattern = '[CH2,CH]([CH2][N+](C)(C)C)([CH2]C([O-,O])=O)OC(=O)[*]'
    
    # Convert SMARTS to mol object
    carnitine_mol = Chem.MolFromSmarts(carnitine_pattern)
    
    # Check if the molecule contains the carnitine core pattern
    if mol.HasSubstructMatch(carnitine_mol):
        # Get all matches
        matches = mol.GetSubstructMatches(carnitine_mol)
        
        # Count the number of [O-] groups
        o_minus_pattern = Chem.MolFromSmarts('[O-]')
        o_minus_count = len(mol.GetSubstructMatches(o_minus_pattern))
        
        # Check if there's exactly one [O-] group
        if o_minus_count == 1:
            return True, "Valid O-acylcarnitine structure found"
        else:
            return False, "Incorrect number of carboxylate groups"
    
    return False, "Missing required O-acylcarnitine structural features"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17387',
                          'name': 'O-acylcarnitine',
                          'definition': 'Any carboxylic ester obtained by the '
                                        'O-acylation of carnitine.',
                          'parents': ['CHEBI:33308', 'CHEBI:35284']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.6746987951807228 is too low.\n'
               'True positives: '
               "[('CCCC\\\\C=C/CCCCCCCC(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('C([C@@H](CC([O-])=O)OC(CC(CC)O)=O)[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('C[N+](C)(C)CC(CC([O-])=O)OC(=O)\\\\C=C\\\\CCC(O)=O', 'Valid "
               "O-acylcarnitine structure found'), "
               "('O([C@@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCCCCCCCCCCC(O)=O', "
               "'Valid O-acylcarnitine structure found'), "
               "('C[N+](C)(C)CC(CC([O-])=O)OC([*])=O', 'Valid O-acylcarnitine "
               "structure found'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CC(O)CC(=O)OC(CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('CC(C)CCCC(C)C(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('CCCCCCCCCCCC=CC(=O)OC(CC([O-])=O)C[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)C(O)CCCCCCCCCCCC', 'Valid "
               "O-acylcarnitine structure found'), "
               "('C[N+](C)(C)CC(CC([O-])=O)OC([*])=O', 'Valid O-acylcarnitine "
               "structure found'), "
               "('O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CC(O)CCCCCCCCCC', 'Valid "
               "O-acylcarnitine structure found'), "
               "('C[N+](C)(C)C[C@@H](CC([O-])=O)OC([*])=O', 'Valid "
               "O-acylcarnitine structure found'), "
               "('O(C(CCCCCCCCC/C=C/CCCCCC)=O)[C@H](C[N+](C)(C)C)CC([O-])=O', "
               "'Valid O-acylcarnitine structure found'), "
               "('CC(C)C(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('CC(=O)O[C@@H](CC([O-])=O)C[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)C/C=C/C=C/C=C/C(O)=O', "
               "'Valid O-acylcarnitine structure found'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('C(C(CC([O-])=O)OC(C(C(=O)O)C)=O)[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('O([C@@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCCCCCCCCCCCCCCCCCC(O)=O', "
               "'Valid O-acylcarnitine structure found'), "
               "('[C@H](OC(CCCCC)=O)(C[N+](C([2H])([2H])[2H])(C)C)CC(=O)[O-]', "
               "'Valid O-acylcarnitine structure found'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('O([C@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCCC', 'Valid "
               "O-acylcarnitine structure found'), "
               "('C(C(CC([O-])=O)OC(=O)*)[N+](C)(C)C', 'Valid O-acylcarnitine "
               "structure found'), ('C[N+](C)(C)CC(CC([O-])=O)OC(=O)CC(O)=O', "
               "'Valid O-acylcarnitine structure found'), "
               "('O([C@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCO', 'Valid "
               "O-acylcarnitine structure found'), "
               "('O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CC/C=C\\\\CC/C=C\\\\CC/C=C\\\\C/C=C\\\\CC', "
               "'Valid O-acylcarnitine structure found'), "
               "('CCCCCCCCCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('C(C(CC([O-])=O)OC(=O)*)[N+](C)(C)C', 'Valid O-acylcarnitine "
               "structure found')]\n"
               'False positives: '
               "[('CCCCC\\\\C=C/C=C/C(=O)O[C@@H](CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('O([C@@H](C[N+](C)(C)C)CC([O-])=O)C(=O)C1=CC=CC=C1', 'Valid "
               "O-acylcarnitine structure found'), "
               "('CC(C)CCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('CC(C)CCCCCCCCCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('OC1C(C(C(O)C1)CCCCCCC(OC(C[N+](C)(C)C)CC([O-])=O)=O)CCC(O)CCCCC', "
               "'Valid O-acylcarnitine structure found'), "
               "('CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CCC\\\\C=C\\\\CC1C(=CCC1=O)/C=C/C(O)CCCCC', "
               "'Valid O-acylcarnitine structure found'), "
               "('CC(C)CCCCCCCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('O([C@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCCCCCC/C=C/C/C=C/C\\\\C=C\\\\C\\\\C=C\\\\CCCCC', "
               "'Valid O-acylcarnitine structure found'), "
               "('C([C@@H](CC([O-])=O)OC(=O)*C([O-])=O)[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('C(C(CC([O-])=O)OC(C(C(=O)[O-])C)=O)[N+](C)(C)C', 'Valid "
               "O-acylcarnitine structure found'), "
               "('C[N+](C)(C)CC(CC([O-])=O)OC(=O)CCCCC([O-])=O', 'Valid "
               "O-acylcarnitine structure found'), "
               "('C[N+](C)(C)CC(CC([O-])=O)OC(=O)CCCCCCC([O-])=O', 'Valid "
               "O-acylcarnitine structure found'), "
               "('O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CCCCCCCCC(O)CCCCC', 'Valid "
               "O-acylcarnitine structure found'), "
               "('CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('CCCCCCC1C[C@H]1CCCCCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('CCCCCC[C@H]1C[C@H]1CCCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', "
               "'Valid O-acylcarnitine structure found'), "
               "('O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CCC\\\\C=C\\\\CC1/C(/C(=O)C=C1)=C/C=C/CCCCC', "
               "'Valid O-acylcarnitine structure found'), "
               "('OC1C(C(C(=O)C1)C/C=C/CCC(OC(C[N+](C)(C)C)CC([O-])=O)=O)/C=C/C(O)C/C=C\\\\C/C=C/CC', "
               "'Valid O-acylcarnitine structure found')]\n"
               'False negatives: '
               "[('O[C@@](C([N+](CC(=O)CCC)(C)C)([2H])[2H])(CC([O-])=O)[2H]', "
               "'Missing required O-acylcarnitine structural features'), "
               "('O(C(C[N+](C)(C)C)CC(O)=O)C(=O)CCCC/C=C/C/C=C/C/C=C/C/C=C\\\\C/C=C\\\\C/C=C/CC', "
               "'Missing required O-acylcarnitine structural features'), "
               "('O(C(C[N+](C)(C)C)CC(O)=O)C(=O)CCCCCCCCCCCC', 'Missing "
               "required O-acylcarnitine structural features'), "
               "('O(C(C[N+](C)(C)C)CC(O)=O)C(=O)CCCCCCC/C=C/CCCC', 'Missing "
               "required O-acylcarnitine structural features'), "
               "('O(C(C[N+](C)(C)C)CC(O)=O)C(=O)CC/C=C/C/C=C\\\\CCCCCCCC', "
               "'Missing required O-acylcarnitine structural features'), "
               "('C[N+](C)(C)C(CCC([O-])=O)OC(=O)CCCCCC(O)=O', 'Missing "
               "required O-acylcarnitine structural features')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 28,
    'num_false_positives': 17,
    'num_true_negatives': 183646,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.6222222222222222,
    'recall': 0.8235294117647058,
    'f1': 0.7088607594936709,
    'accuracy': 0.9998747938180809}