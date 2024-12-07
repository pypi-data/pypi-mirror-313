"""
Classifies: CHEBI:19573 2-enoyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_enoyl_CoA(smiles: str):
    """
    Determines if a molecule is a 2-enoyl-CoA (unsaturated fatty acyl-CoA with double bond between positions 2-3).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 2-enoyl-CoA, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for CoA substructure pattern
    coA_pattern = Chem.MolFromSmarts('[#16]CCNC(=O)CCNC(=O)[CH]([OH])C(C)(C)COP([OH])(=O)OP([OH])(=O)OC[CH]1O[CH]([CH]([OH])[CH]1OP([OH])([OH])=O)n1cnc2c(N)ncnc12')
    
    # Look for thioester with alpha,beta unsaturation pattern
    thioester_pattern = Chem.MolFromSmarts('[#16]C(=O)C=C')

    if not mol.HasSubstructMatch(coA_pattern):
        return False, "Missing CoA structure"

    if not mol.HasSubstructMatch(thioester_pattern):
        return False, "Missing thioester with alpha,beta unsaturation"

    # Get the matches
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)
    
    # For each thioester match, verify it's connected to the CoA part
    coA_matches = mol.GetSubstructMatches(coA_pattern)
    if coA_matches and thioester_matches:
        coA_sulfur = coA_matches[0][0]  # First atom (sulfur) in CoA pattern
        for match in thioester_matches:
            thioester_sulfur = match[0]  # First atom (sulfur) in thioester pattern
            if coA_sulfur == thioester_sulfur:
                return True, "Contains 2-enoyl-CoA structure with double bond between positions 2-3"

    return False, "Thioester and CoA parts not properly connected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:19573',
                          'name': '2-enoyl-CoA',
                          'definition': 'An unsaturated fatty acyl-CoA in '
                                        'which the S-acyl group contains a '
                                        'double bond between positions 2 and '
                                        '3.',
                          'parents': ['CHEBI:51006']},
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
               "[('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C=C', "
               "'Missing 2-enoyl-CoA structure'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CC(O)=O', "
               "'Missing 2-enoyl-CoA structure'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\C=C/[*]', "
               "'Missing 2-enoyl-CoA structure'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Missing 2-enoyl-CoA structure'), "
               "('C\\\\C(CC(O)=O)=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N', "
               "'Missing 2-enoyl-CoA structure'), "
               "('S(CCNC(=O)CCNC(=O)[C@H](O)C(COP(OP(OC[C@H]1O[C@@H](N2C3=NC=NC(N)=C3N=C2)C(O)[C@H]1OP(O)(O)=O)(O)=O)(O)=O)(C)C)C(=O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'Missing 2-enoyl-CoA structure')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 138982,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9992810307143679}