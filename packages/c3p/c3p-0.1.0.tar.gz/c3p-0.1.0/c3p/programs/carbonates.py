"""
Classifies: CHEBI:23016 carbonates
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_carbonates(smiles: str):
    """
    Determines if a molecule contains a carbonate group (salt or ester of carbonic acid).
    Carbonate pattern: R-O-C(=O)-O-R or R-O-C(=O)-O-M+ where R is organic group and M is metal

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains carbonate group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # SMARTS patterns for carbonate groups
    # Organic carbonate ester pattern: R-O-C(=O)-O-R
    carbonate_ester_pattern = Chem.MolFromSmarts('[C;!$(C=[!O])]-O-C(=O)-O-[C;!$(C=[!O])]')
    # Mixed carbonate pattern: R-O-C(=O)-O-R where R can be C or H
    mixed_carbonate_pattern = Chem.MolFromSmarts('[#6,#1]-O-C(=O)-O-[#6,#1]')
    # Inorganic carbonate pattern: [O-]C(=O)[O-]
    inorganic_carbonate_pattern = Chem.MolFromSmarts('[O-]C(=O)[O-]')
    
    # Check for organic carbonate esters
    if mol.HasSubstructMatch(carbonate_ester_pattern):
        matches = mol.GetSubstructMatches(carbonate_ester_pattern)
        return True, f"Contains organic carbonate ester group(s) ({len(matches)} found)"
        
    # Check for mixed carbonates
    if mol.HasSubstructMatch(mixed_carbonate_pattern):
        matches = mol.GetSubstructMatches(mixed_carbonate_pattern)
        return True, f"Contains mixed carbonate group(s) ({len(matches)} found)"
        
    # Check for inorganic carbonates
    if mol.HasSubstructMatch(inorganic_carbonate_pattern):
        matches = mol.GetSubstructMatches(inorganic_carbonate_pattern)
        return True, f"Contains inorganic carbonate group(s) ({len(matches)} found)"
    
    # Additional check for carbonate esters with specific patterns
    methyl_carbonate = Chem.MolFromSmarts('COC(=O)O[#6]')
    ethyl_carbonate = Chem.MolFromSmarts('CCO-C(=O)O[#6]')
    
    if mol.HasSubstructMatch(methyl_carbonate):
        return True, "Contains methyl carbonate ester group"
    if mol.HasSubstructMatch(ethyl_carbonate):
        return True, "Contains ethyl carbonate ester group"
        
    return False, "No carbonate groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23016',
                          'name': 'carbonates',
                          'definition': 'Organooxygen compounds that are salts '
                                        'or esters of carbonic acid, H2CO3.',
                          'parents': ['CHEBI:36963']},
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
    'num_true_positives': 3,
    'num_false_positives': 72,
    'num_true_negatives': 183822,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.04,
    'recall': 0.75,
    'f1': 0.07594936708860758,
    'accuracy': 0.9996030408161046}