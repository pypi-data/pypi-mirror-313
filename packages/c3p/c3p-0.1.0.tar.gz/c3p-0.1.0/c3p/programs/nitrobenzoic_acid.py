"""
Classifies: CHEBI:25553 nitrobenzoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_nitrobenzoic_acid(smiles: str):
    """
    Determines if a molecule is a nitrobenzoic acid (benzoic acid with at least one nitro substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a nitrobenzoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for benzoic acid substructure
    benzoic_acid_pattern = Chem.MolFromSmarts('c1ccccc1C(=O)O')
    if not mol.HasSubstructMatch(benzoic_acid_pattern):
        return False, "No benzoic acid substructure found"

    # Check for nitro group substructure
    nitro_pattern = Chem.MolFromSmarts('[N+](=O)[O-]')
    if not mol.HasSubstructMatch(nitro_pattern):
        return False, "No nitro group found"

    # Get all benzoic acid matches
    benzoic_matches = mol.GetSubstructMatches(benzoic_acid_pattern)
    
    # Get all nitro group matches
    nitro_matches = mol.GetSubstructMatches(nitro_pattern)

    # For each benzoic acid match, check if there's a nitro group attached to the ring
    for benzoic_match in benzoic_matches:
        ring_atoms = set(benzoic_match[:6])  # First 6 atoms are the benzene ring
        
        for nitro_match in nitro_matches:
            nitro_n = nitro_match[0]  # nitrogen atom of nitro group
            
            # Get the atom the nitro group is attached to
            nitro_neighbors = [x.GetIdx() for x in mol.GetAtomWithIdx(nitro_n).GetNeighbors() 
                             if x.GetIdx() not in nitro_match]
            
            # If any of the nitro group's neighbors are in the benzene ring
            if any(neighbor in ring_atoms for neighbor in nitro_neighbors):
                # Count number of nitro groups attached to this ring
                nitro_count = sum(1 for nitro_m in nitro_matches 
                                if any(n in ring_atoms for n in [x.GetIdx() for x in mol.GetAtomWithIdx(nitro_m[0]).GetNeighbors() 
                                                               if x.GetIdx() not in nitro_m]))
                
                return True, f"Found benzoic acid with {nitro_count} nitro group(s) attached to the ring"

    return False, "No nitro group attached to benzoic acid ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25553',
                          'name': 'nitrobenzoic acid',
                          'definition': 'Any member of the class of benzoic '
                                        'acids with at least one nitro '
                                        'substituent attached to the benzene '
                                        'ring.',
                          'parents': ['CHEBI:22723', 'CHEBI:35716']},
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
    'num_false_positives': 38,
    'num_true_negatives': 183859,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07317073170731707,
    'recall': 1.0,
    'f1': 0.13636363636363635,
    'accuracy': 0.9997933659597608}