"""
Classifies: CHEBI:23628 deoxyhexose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_deoxyhexose(smiles: str):
    """
    Determines if a molecule is a deoxyhexose (C6 deoxy sugar with at least one OH replaced by H).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a deoxyhexose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check if molecule has exactly 6 carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 6:
        return False, f"Not a C6 sugar - has {carbon_count} carbons"

    # Count oxygen atoms
    oxygen_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    
    # Regular hexose would have 6 oxygens (5 OH groups + 1 ring/carbonyl O)
    # Deoxyhexose should have fewer oxygens due to H replacement
    if oxygen_count >= 6:
        return False, "Not deoxy - has all hydroxyl groups"
    
    # Check for presence of at least one OH group
    patt = Chem.MolFromSmarts('[OH]')
    if not mol.HasSubstructMatch(patt):
        return False, "No hydroxyl groups found"
        
    # Check for presence of either a ring oxygen or carbonyl group 
    # (characteristic of sugars)
    ring_o = Chem.MolFromSmarts('[O;R]')  # Ring oxygen
    carbonyl = Chem.MolFromSmarts('[C]=O') # Carbonyl
    
    if not (mol.HasSubstructMatch(ring_o) or mol.HasSubstructMatch(carbonyl)):
        return False, "No ring oxygen or carbonyl group found"

    # Calculate number of deoxy positions (missing OH groups)
    deoxy_count = 6 - oxygen_count
    
    return True, f"Deoxyhexose with {deoxy_count} deoxy position(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23628',
                          'name': 'deoxyhexose',
                          'definition': 'Any C6 deoxy sugar having at least '
                                        'one hydroxy group replaced by '
                                        'hydrogen.',
                          'parents': ['CHEBI:23639', 'CHEBI:33917']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 14249,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9930333008220705}