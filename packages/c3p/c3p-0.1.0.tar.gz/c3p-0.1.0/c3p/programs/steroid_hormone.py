"""
Classifies: CHEBI:26764 steroid hormone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_steroid_hormone(smiles: str):
    """
    Determines if a molecule is a steroid hormone based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a steroid hormone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Check for steroid core structure (four fused rings)
    ring_info = mol.GetRingInfo()
    if not ring_info.NumRings() >= 4:
        return False, "Does not contain minimum 4 rings required for steroid core"

    # Look for characteristic steroid ring pattern
    sssr = rdMolDescriptors.GetSymmSSSR(mol)
    six_membered_rings = 0
    five_membered_rings = 0
    
    for ring in sssr:
        if len(ring) == 6:
            six_membered_rings += 1
        elif len(ring) == 5:
            five_membered_rings += 1
            
    if not (six_membered_rings >= 3 and five_membered_rings >= 1):
        return False, "Does not match steroid ring pattern of 3 six-membered rings and 1 five-membered ring"

    # Check for key functional groups characteristic of steroid hormones
    # Look for ketone, hydroxyl, or other oxygen-containing groups
    pattern_matches = []
    
    patterns = [
        "[#6]=O", # Ketone
        "[OX2H]", # Hydroxyl
        "[#6]-O-[#6]", # Ether
        "[#6](=O)O[#6]", # Ester
    ]
    
    for pattern in patterns:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            pattern_matches.append(pattern)
            
    if not pattern_matches:
        return False, "Missing characteristic functional groups of steroid hormones"

    # If all checks pass, classify as steroid hormone
    functional_groups = {
        "[#6]=O": "ketone",
        "[OX2H]": "hydroxyl",
        "[#6]-O-[#6]": "ether",
        "[#6](=O)O[#6]": "ester"
    }
    
    found_groups = [functional_groups[p] for p in pattern_matches]
    return True, f"Steroid core structure with {', '.join(found_groups)} groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26764',
                          'name': 'steroid hormone',
                          'definition': 'Any steroid that acts as hormone.',
                          'parents': ['CHEBI:35341']},
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
    'error': "module 'rdkit.Chem.rdMolDescriptors' has no attribute "
             "'GetSymmSSSR'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}