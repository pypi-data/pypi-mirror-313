"""
Classifies: CHEBI:24628 imidazolidine-2,4-dione
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_imidazolidine_2_4_dione(smiles: str):
    """
    Determines if a molecule contains an imidazolidine-2,4-dione core structure
    (a 5-membered ring with N-C-N and C=O groups at positions 2 and 4)

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains imidazolidine-2,4-dione, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for imidazolidine-2,4-dione core
    # 5-membered ring with:
    # - Two nitrogens connected by a carbon (N-C-N)
    # - Two carbonyls (C=O) at positions 2 and 4
    pattern = Chem.MolFromSmarts('[NX3]1[CX3](=[OX1])[NX3][CX3](=[OX1])[CX3]1')
    
    if not mol.HasSubstructMatch(pattern):
        return False, "No imidazolidine-2,4-dione core found"

    # Get matches
    matches = mol.GetSubstructMatches(pattern)
    
    # For each match, verify the carbonyl groups and ring structure
    for match in matches:
        # Get atoms in the match
        atoms = [mol.GetAtomWithIdx(idx) for idx in match]
        
        # Verify nitrogens
        n1, n2 = atoms[0], atoms[2]
        if not (n1.GetAtomicNum() == 7 and n2.GetAtomicNum() == 7):
            continue
            
        # Verify carbonyls
        c2, c4 = atoms[1], atoms[3]
        if not (c2.GetAtomicNum() == 6 and c4.GetAtomicNum() == 6):
            continue
            
        # Verify oxygens
        o2_neighbors = [n for n in c2.GetNeighbors() if n.GetAtomicNum() == 8]
        o4_neighbors = [n for n in c4.GetNeighbors() if n.GetAtomicNum() == 8]
        
        if not (len(o2_neighbors) == 1 and len(o4_neighbors) == 1):
            continue
            
        # If we get here, we've found a valid match
        return True, "Contains imidazolidine-2,4-dione core structure"

    return False, "Structure does not match imidazolidine-2,4-dione requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24628',
                          'name': 'imidazolidine-2,4-dione',
                          'definition': 'An imidazolidinone with oxo groups at '
                                        'position 2 and 4.',
                          'parents': ['CHEBI:55370']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183836,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999510457178602}