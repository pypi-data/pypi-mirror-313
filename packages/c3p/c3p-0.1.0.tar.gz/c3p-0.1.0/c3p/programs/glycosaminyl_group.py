"""
Classifies: CHEBI:24399 glycosaminyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_glycosaminyl_group(smiles: str):
    """
    Determines if a molecule is a glycosaminyl group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycosaminyl group, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for key structural features:
    # 1. Must have at least one N-acetyl group (-NC(=O)C)
    # 2. Must have multiple sugar rings
    # 3. Must have a * indicating attachment point
    # 4. Must have multiple OH groups
    
    # Check for * attachment point
    if '*' not in smiles:
        return False, "No attachment point (*) found"
        
    # Count N-acetyl groups
    nacetyl_pattern = Chem.MolFromSmarts('[NH][C](=O)[CH3]')
    if not mol.HasSubstructMatch(nacetyl_pattern):
        return False, "No N-acetyl group found"
        
    # Count rings
    ring_count = rdMolDescriptors.CalcNumRings(mol)
    if ring_count < 1:
        return False, "No sugar rings found"
        
    # Count OH groups
    oh_pattern = Chem.MolFromSmarts('[OH]')
    oh_count = len(mol.GetSubstructMatches(oh_pattern))
    if oh_count < 3:
        return False, "Too few hydroxyl groups"
        
    # Check for pyranose rings (6-membered sugar rings)
    pyranose_pattern = Chem.MolFromSmarts('[C]1[O][C]([C,H])[C][C][C]1')
    if not mol.HasSubstructMatch(pyranose_pattern):
        return False, "No pyranose rings found"

    # If all checks pass, this is likely a glycosaminyl group
    return True, f"Contains {ring_count} sugar rings, N-acetyl group(s), and {oh_count} OH groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24399',
                          'name': 'glycosaminyl group',
                          'definition': 'A glycosyl group obtained by removing '
                                        'the hydroxy group from the hemiacetal '
                                        'function of a glycosamine and, by '
                                        'extension, of a lower oligosaccharide '
                                        'having a glycosamine at the reducing '
                                        'end.',
                          'parents': ['CHEBI:24403']},
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
    'num_true_positives': 10,
    'num_false_positives': 100,
    'num_true_negatives': 12336,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 0.9090909090909091,
    'f1': 0.1652892561983471,
    'accuracy': 0.9918855949224713}