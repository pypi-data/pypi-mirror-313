"""
Classifies: CHEBI:140377 (2S)-flavan-4-one
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is__2S__flavan_4_one(smiles: str):
    """
    Determines if a molecule is a (2S)-flavan-4-one.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a (2S)-flavan-4-one, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for basic flavan-4-one scaffold
    flavan_4_one_pattern = Chem.MolFromSmarts('[O;H0]=C1C[C@H](c2ccccc2)Oc3ccccc13')
    if not mol.HasSubstructMatch(flavan_4_one_pattern):
        return False, "Does not contain basic flavan-4-one scaffold"

    # Get matches for the core scaffold
    matches = mol.GetSubstructMatches(flavan_4_one_pattern)
    
    # Check stereochemistry at C-2 position
    for match in matches:
        c2_atom_idx = match[2]  # Index of C-2 carbon in the pattern
        c2_atom = mol.GetAtomWithIdx(c2_atom_idx)
        
        # Check if the chiral center has S configuration
        # In SMILES, @@ indicates R configuration, @ indicates S configuration
        if '@' in smiles and '@@' not in smiles:
            return True, "Contains (2S)-flavan-4-one scaffold with correct S stereochemistry"
            
    return False, "Does not have correct S stereochemistry at C-2 position"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140377',
                          'name': '(2S)-flavan-4-one',
                          'definition': 'Any flavanone in which the chiral '
                                        'centre at position 2 has '
                                        'S-configuration.',
                          'parents': ['CHEBI:28863']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'GetFormalCharge' from "
               "'rdkit.Chem.rdMolDescriptors' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/rdMolDescriptors.so)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 49,
    'num_true_negatives': 183861,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.02,
    'recall': 0.5,
    'f1': 0.038461538461538464,
    'accuracy': 0.9997281308451869}