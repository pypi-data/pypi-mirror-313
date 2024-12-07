"""
Classifies: CHEBI:133959 4'-methoxyisoflavones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_4__methoxyisoflavones(smiles: str):
    """
    Determines if a molecule is a 4'-methoxyisoflavone.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 4'-methoxyisoflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Match isoflavone core structure with 4'-methoxy group
    # The pattern matches:
    # - isoflavone core (benzopyrone with phenyl at position 3)
    # - methoxy group at para position of the phenyl substituent
    pattern = Chem.MolFromSmarts('[#6]-[#8]-c1ccc(-c2coc3ccccc3c2=O)cc1')
    
    if not mol.HasSubstructMatch(pattern):
        return False, "Not a 4'-methoxyisoflavone"

    # Count number of substituents for additional info
    matches = mol.GetSubstructMatches(pattern)
    num_matches = len(matches)
    
    if num_matches > 0:
        # Get all substituents
        substituents = []
        for atom in mol.GetAtoms():
            if atom.GetSymbol() == 'O' and atom.GetDegree() == 2:
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 1:
                        substituents.append('methoxy')
                        break
        
        return True, f"4'-methoxyisoflavone with {len(substituents)} methoxy groups total"

    return False, "Structure does not match 4'-methoxyisoflavone pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133959',
                          'name': "4'-methoxyisoflavones",
                          'definition': 'Any methoxyisoflavone which has a '
                                        'methoxy group at the 4-position of '
                                        'the phenyl substituent.',
                          'parents': ['CHEBI:38756']},
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
               "[('COC1=CC=C(C=C1)C2=COC3=C(C2=O)C(=CC(=C3OC)OC)OC', 'Not an "
               "isoflavone core structure'), "
               "('COc1ccc(cc1)-c1coc2cc(O)c(OC)c(O)c2c1=O', 'Not an isoflavone "
               "core structure'), "
               "('COc1ccc(cc1)-c1coc2cc(O[C@@H]3O[C@H](COC(=O)CC(O)=O)[C@@H](O)[C@H](O)[C@H]3O)cc(O)c2c1=O', "
               "'Not an isoflavone core structure')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 106659,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.999063337142429}