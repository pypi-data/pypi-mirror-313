"""
Classifies: CHEBI:20156 3-oxo-Delta(1) steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_3_oxo_Delta_1__steroid(smiles: str):
    """
    Determines if a molecule is a 3-oxo-Delta(1) steroid.
    These are steroids with a ketone at position 3 and a double bond between positions 1 and 2.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 3-oxo-Delta(1) steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for steroid core (4 fused rings)
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[#6]~1~2~[#6]~[#6]~[#6]~3~[#6]~[#6]~[#6]~4~[#6]~[#6]~[#6]~[#6]~4~[#6]~[#6]~3~[#6]~[#6]~2~[#6]~[#6]~[#6]~1'))
    
    if not matches:
        return False, "No steroid core found"

    # Check for ketone at position 3 and double bond between positions 1-2
    pattern = Chem.MolFromSmarts('[#6]1=[#6]-[#6](=O)-[#6]2-[#6]-[#6]')
    matches = mol.GetSubstructMatches(pattern)
    
    if not matches:
        return False, "No 3-oxo-Delta(1) pattern found"

    # Verify the matched pattern is part of steroid core
    for match in matches:
        # Get neighboring atoms to verify it's part of steroid core
        neighbors = []
        for atom_idx in match:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                neighbors.append(neighbor.GetIdx())
                
        # Check if pattern is connected to rest of steroid core
        if any(n for n in neighbors if mol.GetAtomWithIdx(n).IsInRing()):
            return True, "Found 3-oxo-Delta(1) steroid pattern in steroid core"
            
    return False, "3-oxo-Delta(1) pattern found but not part of steroid core"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20156',
                          'name': '3-oxo-Delta(1) steroid',
                          'definition': 'Any 3-oxo steroid that contains a '
                                        'double bond between positions 1 and '
                                        '2.',
                          'parents': ['CHEBI:47788', 'CHEBI:51689']},
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
    'num_true_negatives': 183844,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999951047848009}