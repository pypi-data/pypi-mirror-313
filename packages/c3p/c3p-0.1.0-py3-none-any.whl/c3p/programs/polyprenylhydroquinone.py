"""
Classifies: CHEBI:26253 polyprenylhydroquinone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_polyprenylhydroquinone(smiles: str):
    """
    Determines if a molecule is a polyprenylhydroquinone (hydroquinone with polyprenyl substituent).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a polyprenylhydroquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for hydroquinone core
    hydroquinone_pattern = Chem.MolFromSmarts('c1c(O)c([*])c([*])c(O)c1') # Basic hydroquinone pattern
    hydroquinone_pattern2 = Chem.MolFromSmarts('c1c(O)c([*])cc(O)c1') # Alternative pattern
    
    if not mol.HasSubstructMatch(hydroquinone_pattern) and not mol.HasSubstructMatch(hydroquinone_pattern2):
        return False, "No hydroquinone core found"

    # Pattern for prenyl/isoprenyl unit (C=C(C)C)
    prenyl_pattern = Chem.MolFromSmarts('C=C(C)C')
    
    # Pattern for connected prenyl units
    polyprenyl_pattern = Chem.MolFromSmarts('CC(C)=CCC') 
    
    prenyl_matches = mol.GetSubstructMatches(prenyl_pattern)
    polyprenyl_matches = mol.GetSubstructMatches(polyprenyl_pattern)
    
    if not prenyl_matches and not polyprenyl_matches:
        return False, "No prenyl/polyprenyl substituent found"

    # Count number of prenyl units
    num_prenyl_units = len(polyprenyl_matches)
    
    if num_prenyl_units == 0:
        return False, "No connected prenyl units found"
        
    # Additional check for connected prenyl chain
    # Look for alternating single-double bond pattern with methyl branches
    chain_pattern = Chem.MolFromSmarts('CC(C)=CCC(C)=C')
    if not mol.HasSubstructMatch(chain_pattern):
        return False, "No proper polyprenyl chain structure found"

    return True, f"Polyprenylhydroquinone with approximately {num_prenyl_units} prenyl units"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26253',
                          'name': 'polyprenylhydroquinone',
                          'definition': 'A hydroquinone compound having a '
                                        'polyprenyl substituent in an '
                                        'unspecified position.',
                          'parents': ['CHEBI:24646']},
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
    'num_true_positives': 0,
    'num_false_positives': 12,
    'num_true_negatives': 183877,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999129928817302}