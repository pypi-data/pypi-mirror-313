"""
Classifies: CHEBI:24803 indole-3-acetic acids
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_indole_3_acetic_acids(smiles: str):
    """
    Determines if a molecule is an indole-3-acetic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an indole-3-acetic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Pattern for indole core with acetic acid at position 3
    # Matches indole with -CH2COOH at position 3
    indole_pattern = Chem.MolFromSmarts('c1ccc2c(c1)[nH]cc2CC(=O)O')
    
    if not mol.HasSubstructMatch(indole_pattern):
        # Try alternate pattern with different bond representation
        indole_pattern2 = Chem.MolFromSmarts('[cH]1[cH][cH][c]2[c]1[nH][cH][c]2CC(=O)O')
        if not mol.HasSubstructMatch(indole_pattern2):
            return False, "Not an indole-3-acetic acid structure"

    # Check for carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts('CC(=O)O')
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "Missing acetic acid group"

    # Verify position of acetic acid group
    matches = mol.GetSubstructMatches(indole_pattern)
    if not matches:
        matches = mol.GetSubstructMatches(indole_pattern2)

    # Check for aromaticity
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    aromatic_rings = 0
    for ring in rings:
        if len(ring) in [5,6]:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings += 1
    
    if aromatic_rings < 2:
        return False, "Indole core not properly aromatic"

    # Check for substituents
    match_atoms = set(matches[0])
    substituents = []
    
    for atom in mol.GetAtoms():
        if atom.GetIdx() not in match_atoms and atom.GetSymbol() not in ['H', 'O']:
            substituents.append(atom.GetSymbol())
            
    if substituents:
        return True, f"Substituted indole-3-acetic acid with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted indole-3-acetic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24803',
                          'name': 'indole-3-acetic acids',
                          'definition': 'An  indol-3-yl carboxylic acid in '
                                        'which the carboxylic acid specified '
                                        'is acetic acid.',
                          'parents': ['CHEBI:24810']},
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
               "False negatives: [('O=C(O)CC=1C2=C(C=C(CC=C(C)C)C=C2)NC1', "
               "'Not an indole-3-acetic acid structure'), "
               "('OC(=O)CC=1C=2C(NC1C)=CC=CC2', 'Not an indole-3-acetic acid "
               "structure'), ('O(C1=CC=2C(=C(NC2C=C1)C)CC(O)=O)C', 'Not an "
               "indole-3-acetic acid structure')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 18,
    'num_true_negatives': 183881,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.14285714285714285,
    'recall': 1.0,
    'f1': 0.25,
    'accuracy': 0.9999021217822536}