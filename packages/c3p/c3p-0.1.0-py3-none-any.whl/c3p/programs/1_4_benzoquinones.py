"""
Classifies: CHEBI:132124 1,4-benzoquinones
"""
from rdkit import Chem

def is_1_4_benzoquinones(smiles: str):
    """
    Determines if a molecule is a 1,4-benzoquinone or a C-substituted derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 1,4-benzoquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for 1,4-benzoquinone core
    # Two C=O groups in para positions on a cyclohexadiene ring
    pattern = Chem.MolFromSmarts('[#6]1=C[#6](=O)C=C[#6](=O)1')
    
    if not mol.HasSubstructMatch(pattern):
        return False, "No 1,4-benzoquinone core structure found"

    # Find all matches of the pattern
    matches = mol.GetSubstructMatches(pattern)
    
    for match in matches:
        # Get the atoms in the ring
        ring_atoms = [mol.GetAtomWithIdx(i) for i in match]
        
        # Check that we have a six-membered ring with two carbonyls
        carbonyl_count = sum(1 for atom in ring_atoms if any(n.GetSymbol() == 'O' and n.GetDegree() == 1 
                                                           for n in atom.GetNeighbors()))
        
        if carbonyl_count == 2:
            # Get substituents
            substituents = []
            for atom_idx in match:
                atom = mol.GetAtomWithIdx(atom_idx)
                if atom.GetSymbol() == 'C':
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetIdx() not in match and neighbor.GetSymbol() != 'O':
                            substituents.append(neighbor.GetSymbol())
                            
            if substituents:
                return True, f"1,4-benzoquinone with substituents"
            else:
                return True, "Unsubstituted 1,4-benzoquinone"

    return False, "Not a valid 1,4-benzoquinone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132124',
                          'name': '1,4-benzoquinones',
                          'definition': 'Any member of the class of '
                                        'benzoquinones that is '
                                        '1,4-benzoquinone or its C-substituted '
                                        'derivatives.',
                          'parents': ['CHEBI:22729', 'CHEBI:25830']},
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
               "[('C1=C(C(=O)C=C(C1=O)CCCC=2C=C(C(O)=CC2)OC)OC', 'No valid "
               "1,4-benzoquinone structure found'), "
               "('COC1=C(OC)C(=O)C(CC=C(C)C)=C(C)C1=O', 'No valid "
               "1,4-benzoquinone structure found'), "
               "('O(C=1C(=O)C([C@@H](C2=CC=C(O)C=C2)C=C)=CC(=O)C1OC)C', 'No "
               "valid 1,4-benzoquinone structure found'), "
               "('C1=C(C(C(=C(C1=O)OC)O)=O)C', 'No valid 1,4-benzoquinone "
               "structure found'), ('CC1=C(C([C@H]2[C@@H](C1=O)O2)=O)O', 'No "
               "1,4-benzoquinone core structure found'), "
               "('COC1=C(OC)C(=O)C(C\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CCC=C(C)C)=C(C)C1=O', "
               "'No valid 1,4-benzoquinone structure found'), "
               "('O=C1C(OC)=C(OC)C(=O)C=C1C(C(O)C)C', 'No valid "
               "1,4-benzoquinone structure found'), "
               "('COC1=CC(=O)C(O)=C(CCCCCCC\\\\C=C/C\\\\C=C/CC=C)C1=O', 'No "
               "valid 1,4-benzoquinone structure found'), "
               "('COC1=C(OC)C(=O)C(C\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CCC=C(C)C)=C(C)C1=O', "
               "'No valid 1,4-benzoquinone structure found'), "
               "('C=1(C(C(=CC(C1)=O)OC)=O)CCCCC', 'No valid 1,4-benzoquinone "
               "structure found')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 85689,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 0.7,
    'f1': 0.11965811965811965,
    'accuracy': 0.9987995198079231}