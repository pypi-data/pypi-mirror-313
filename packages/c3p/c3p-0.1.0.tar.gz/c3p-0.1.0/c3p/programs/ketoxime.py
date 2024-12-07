"""
Classifies: CHEBI:24983 ketoxime
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition

def is_ketoxime(smiles: str):
    """
    Determines if a molecule contains a ketoxime group (R2C=NOH where R =/= H).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains ketoxime, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for ketoxime: [C]([!H])=N[OH]
    # Matches carbon with non-H substituent connected to N-OH
    ketoxime_pattern = Chem.MolFromSmarts('[C]([!H])=N[OH]')
    
    # Find matches
    matches = mol.GetSubstructMatches(ketoxime_pattern)
    
    if not matches:
        return False, "No ketoxime group found"
        
    # For each match, verify it's a ketoxime by checking:
    # 1. The carbon has exactly 2 non-H substituents (ketone requirement)
    # 2. The nitrogen is connected to exactly one OH and one C
    for match in matches:
        c_idx = match[0]  # Carbon atom index
        n_idx = match[1]  # Nitrogen atom index
        o_idx = match[2]  # Oxygen atom index
        
        c_atom = mol.GetAtomWithIdx(c_idx)
        n_atom = mol.GetAtomWithIdx(n_idx)
        o_atom = mol.GetAtomWithIdx(o_idx)
        
        # Check carbon valence (should have 3 bonds total - 2 substituents + 1 to N)
        if c_atom.GetDegree() != 3:
            continue
            
        # Check nitrogen valence (should have 2 bonds - 1 to C and 1 to O)
        if n_atom.GetDegree() != 2:
            continue
            
        # Check oxygen (should have 1 bond to N)
        if o_atom.GetDegree() != 1:
            continue
            
        # At this point we've confirmed a valid ketoxime group
        return True, "Contains ketoxime group (R2C=NOH)"
        
    return False, "No valid ketoxime group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24983',
                          'name': 'ketoxime',
                          'definition': 'Oximes of ketones R2C=NOH (where R '
                                        '=/= H).',
                          'parents': ['CHEBI:25750']},
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
    'success': False,
    'best': True,
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}