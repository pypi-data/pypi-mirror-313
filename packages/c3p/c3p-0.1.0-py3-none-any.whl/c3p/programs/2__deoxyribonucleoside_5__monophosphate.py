"""
Classifies: CHEBI:18241 2'-deoxyribonucleoside 5'-monophosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition

def is_2__deoxyribonucleoside_5__monophosphate(smiles: str):
    """
    Determines if a molecule is a 2'-deoxyribonucleoside 5'-monophosphate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 2'-deoxyribonucleoside 5'-monophosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of phosphate group
    phosphate_pattern = Chem.MolFromSmarts("[PX4](=O)([OH])([OH])[O,S]")
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group found"

    # Check for deoxyribose sugar
    deoxyribose_pattern = Chem.MolFromSmarts("[CH2]-1-[CH2]-[CH]([OH])-[CH](-[CH2]-O-P)-O-1")
    if not mol.HasSubstructMatch(deoxyribose_pattern):
        return False, "No 2'-deoxyribose sugar found"

    # Check for nucleobase attachment
    nucleobase_patterns = [
        Chem.MolFromSmarts("n1cnc2c(N)ncnc12"), # Adenine
        Chem.MolFromSmarts("n1c(N)nc(=O)cc1"),  # Cytosine 
        Chem.MolFromSmarts("n1c(=O)[nH]c(=O)cc1"), # Uracil
        Chem.MolFromSmarts("n1c(=O)[nH]c(=O)c(C)c1"), # Thymine
        Chem.MolFromSmarts("n1cnc2c(=O)[nH]cnc12"), # Guanine
        Chem.MolFromSmarts("n1cccnc1=O") # Zebularine
    ]
    
    has_nucleobase = False
    nucleobase_type = None
    nucleobase_names = ["adenine", "cytosine", "uracil", "thymine", "guanine", "zebularine"]
    
    for i, pattern in enumerate(nucleobase_patterns):
        if pattern is not None and mol.HasSubstructMatch(pattern):
            has_nucleobase = True
            nucleobase_type = nucleobase_names[i]
            break
            
    if not has_nucleobase:
        return False, "No nucleobase found"

    # Check connectivity between components
    # Get atoms in phosphate group
    phosphate_matches = mol.GetSubstructMatches(phosphate_pattern)
    if not phosphate_matches:
        return False, "Cannot analyze phosphate connectivity"
        
    phosphate_atoms = set(phosphate_matches[0])
    
    # Get atoms in deoxyribose
    deoxyribose_matches = mol.GetSubstructMatches(deoxyribose_pattern)
    if not deoxyribose_matches:
        return False, "Cannot analyze deoxyribose connectivity"
        
    deoxyribose_atoms = set(deoxyribose_matches[0])
    
    # Check if phosphate is connected to 5' position
    phosphate_O = mol.GetAtomWithIdx(phosphate_atoms.pop())
    connected_to_5_prime = False
    
    for neighbor in phosphate_O.GetNeighbors():
        if neighbor.GetIdx() in deoxyribose_atoms:
            connected_to_5_prime = True
            break
            
    if not connected_to_5_prime:
        return False, "Phosphate not connected to 5' position"

    return True, f"Valid 2'-deoxyribonucleoside 5'-monophosphate containing {nucleobase_type}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18241',
                          'name': "2'-deoxyribonucleoside 5'-monophosphate",
                          'definition': "A 2'-deoxyribonucleoside "
                                        'monophosphate compound with the '
                                        "phosphate group in the 5'-position.",
                          'parents': ['CHEBI:19257', 'CHEBI:37016']},
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