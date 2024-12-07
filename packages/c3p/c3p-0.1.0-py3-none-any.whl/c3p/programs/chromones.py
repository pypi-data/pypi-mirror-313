"""
Classifies: CHEBI:23238 chromones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition

def is_chromones(smiles: str):
    """
    Determines if a molecule is a chromone (1,4-benzopyrone) or derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a chromone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for basic chromone scaffold
    chromone_pattern = Chem.MolFromSmarts('[#6]1=CC(=O)c2ccccc2O1')
    if not mol.HasSubstructMatch(chromone_pattern):
        return False, "Does not contain chromone (1,4-benzopyrone) core structure"
        
    # Get matches of chromone pattern
    matches = mol.GetSubstructMatches(chromone_pattern)
    
    # Check that we have at least one match
    if len(matches) == 0:
        return False, "No chromone substructure found"
        
    # Get atoms in first match
    match_atoms = set(matches[0])
    
    # Check for substituents
    substituents = []
    for match in matches:
        for atom_idx in match:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in match_atoms:
                    substituents.append(neighbor.GetSymbol())
                    
    if len(substituents) > 0:
        return True, f"Substituted chromone with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted chromone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23238',
                          'name': 'chromones',
                          'definition': 'A chromenone that consists of a '
                                        '1,4-benzopyrone skeleton and its '
                                        'substituted derivatives thereof.',
                          'parents': ['CHEBI:38445']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
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