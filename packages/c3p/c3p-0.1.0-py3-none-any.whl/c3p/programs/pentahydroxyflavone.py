"""
Classifies: CHEBI:25883 pentahydroxyflavone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_pentahydroxyflavone(smiles: str):
    """
    Determines if a molecule is a pentahydroxyflavone (flavone with 5 hydroxy groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a pentahydroxyflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for flavone core structure
    flavone_pattern = Chem.MolFromSmarts('[#6]1=[#6]-c2c([#6](=[O])[#6]1)c(=O)c1ccccc1o2')
    if not mol.HasSubstructMatch(flavone_pattern):
        return False, "No flavone core structure found"
    
    # Count number of hydroxy groups directly attached to the flavone core
    # First get the atoms in the flavone core
    flavone_match = mol.GetSubstructMatch(flavone_pattern)
    flavone_atoms = set(flavone_match)
    
    # Pattern for hydroxy groups
    oh_pattern = Chem.MolFromSmarts('O[H]')
    
    # Count hydroxy groups attached to flavone core
    hydroxy_count = 0
    matches = mol.GetSubstructMatches(oh_pattern)
    
    for match in matches:
        oh_oxygen = match[0]
        # Get the atom the OH is attached to
        for bond in mol.GetAtomWithIdx(oh_oxygen).GetBonds():
            neighbor = bond.GetOtherAtom(mol.GetAtomWithIdx(oh_oxygen))
            # Check if this neighbor is part of the flavone core or directly attached to it
            if neighbor.GetIdx() in flavone_atoms or any(n.GetIdx() in flavone_atoms for n in neighbor.GetNeighbors()):
                hydroxy_count += 1
                
    if hydroxy_count == 5:
        return True, "Found flavone with exactly 5 hydroxy groups"
    else:
        return False, f"Found flavone but with {hydroxy_count} hydroxy groups instead of 5"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25883',
                          'name': 'pentahydroxyflavone',
                          'definition': 'A hydroxyflavone substituted by five '
                                        'hydroxy groups.',
                          'parents': ['CHEBI:24698']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183901,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999836871411171}