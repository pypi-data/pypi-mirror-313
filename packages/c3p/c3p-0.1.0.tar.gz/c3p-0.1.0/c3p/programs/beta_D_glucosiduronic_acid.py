"""
Classifies: CHEBI:15341 beta-D-glucosiduronic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprint
from rdkit.Chem import rdDecomposition
from rdkit.Chem import rdmolops

def is_beta_D_glucosiduronic_acid(smiles: str):
    """
    Determines if a molecule contains a beta-D-glucosiduronic acid moiety.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains beta-D-glucosiduronic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for beta-D-glucuronic acid core
    # Matches pyranose ring with beta configuration at C1, carboxylic acid at C6,
    # and hydroxyl groups at C2,C3,C4 positions
    glucuronic_pattern = Chem.MolFromSmarts('[C@@H]1O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)C(O)=O')
    
    if mol.HasSubstructMatch(glucuronic_pattern):
        # Find atoms involved in the glucuronic acid substructure
        matches = mol.GetSubstructMatches(glucuronic_pattern)
        
        # For each match, verify it's connected to rest of molecule via glycosidic bond
        for match in matches:
            glucuronic_atoms = set(match)
            
            # Get the anomeric carbon (C1)
            anomeric_carbon = mol.GetAtomWithIdx(match[1])
            
            # Check its neighbors for glycosidic bond
            for neighbor in anomeric_carbon.GetNeighbors():
                if neighbor.GetIdx() not in glucuronic_atoms:
                    if neighbor.GetSymbol() == 'O':  # Found glycosidic oxygen
                        for next_neighbor in neighbor.GetNeighbors():
                            if next_neighbor.GetIdx() not in glucuronic_atoms:
                                return True, "Contains beta-D-glucosiduronic acid moiety with glycosidic bond"
                                
        return False, "Contains glucuronic acid but no glycosidic bond found"
        
    return False, "No beta-D-glucuronic acid pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15341',
                          'name': 'beta-D-glucosiduronic acid',
                          'definition': 'A glucosiduronic acid resulting from '
                                        'the formal condensation of any '
                                        'substance with beta-D-glucuronic acid '
                                        'to form a glycosidic bond.',
                          'parents': ['CHEBI:24302']},
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