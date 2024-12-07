"""
Classifies: CHEBI:17389 2-monoglyceride
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_monoglyceride(smiles: str):
    """
    Determines if a molecule is a 2-monoglyceride.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 2-monoglyceride, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Pattern matches glycerol backbone with:
    # - Primary alcohol at C1 and C3
    # - Ester at C2
    pattern = Chem.MolFromSmarts('[OX2H1]C[CH]([OX2]C(=O)[#6])C[OX2H1]')
    
    if not mol.HasSubstructMatch(pattern):
        return False, "No 2-monoglyceride pattern found"
        
    matches = mol.GetSubstructMatches(pattern)
    
    if len(matches) >= 1:
        # Verify we found exactly one glycerol backbone with correct substitution pattern
        match = matches[0]
        
        # Get the central carbon (C2) 
        c2_idx = match[2]
        c2_atom = mol.GetAtomWithIdx(c2_idx)
        
        # Check that C2 has exactly one ester group
        ester_count = 0
        for neighbor in c2_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'O':
                for nn in neighbor.GetNeighbors():
                    if nn.GetSymbol() == 'C' and any(b.GetBondType() == Chem.BondType.DOUBLE 
                                                   for b in nn.GetBonds()):
                        ester_count += 1
        
        if ester_count == 1:
            return True, "2-monoglyceride structure found with ester at C2 position and terminal OH groups"
            
    return False, "No valid 2-monoglyceride pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17389',
                          'name': '2-monoglyceride',
                          'definition': 'A monoglyceride in which the acyl '
                                        'substituent is located at position 2.',
                          'parents': ['CHEBI:17408', 'CHEBI:76575']},
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
               "[('O(C(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)C(CO)CO', "
               "'No 2-monoglyceride pattern found'), "
               "('C([C@@](CO)(OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'No 2-monoglyceride pattern found'), "
               "('O(C(=O)CCCCCCCC=CCCCCCCCCC)C(CO)CO', 'No 2-monoglyceride "
               "pattern found'), "
               "('[C@H]1(O)[C@@H](CO)O[C@H]([C@@H]([C@H]1O)O)OC[C@@H](CO)OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'No 2-monoglyceride pattern found'), "
               "('CCCCCCCCCCCC(=O)OC(CO)CO', 'No 2-monoglyceride pattern "
               "found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 48123,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 0.8,
    'f1': 0.07339449541284404,
    'accuracy': 0.997905780874181}