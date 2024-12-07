"""
Classifies: CHEBI:22512 aminoimidazole
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aminoimidazole(smiles: str):
    """
    Determines if a molecule is an aminoimidazole (imidazole with at least one amino substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aminoimidazole, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for imidazole ring
    imidazole_pattern = Chem.MolFromSmarts('[nH]1cncc1')  # Basic imidazole pattern
    if not mol.HasSubstructMatch(imidazole_pattern):
        return False, "No imidazole ring found"

    # Check for amino substituent (-NH2)
    amino_pattern = Chem.MolFromSmarts('N[H2]')
    if not mol.HasSubstructMatch(amino_pattern):
        return False, "No amino substituent found"

    # Find imidazole rings
    imidazole_matches = mol.GetSubstructMatches(imidazole_pattern)
    
    # Find amino groups
    amino_matches = mol.GetSubstructMatches(amino_pattern)
    
    # Check if any amino group is attached to imidazole ring
    for imidazole_match in imidazole_matches:
        imidazole_atoms = set(imidazole_match)
        
        for amino_match in amino_matches:
            amino_n = amino_match[0]
            # Get neighbors of amino nitrogen
            amino_neighbors = [x.GetIdx() for x in mol.GetAtomWithIdx(amino_n).GetNeighbors()]
            
            # Check if amino group is connected to imidazole ring
            for neighbor in amino_neighbors:
                if neighbor in imidazole_atoms:
                    position = get_amino_position(mol, neighbor, imidazole_match)
                    return True, f"Aminoimidazole found with amino group at position {position}"
                
    return False, "Amino group not attached to imidazole ring"

def get_amino_position(mol, attachment_point, imidazole_atoms):
    """Helper function to determine position of amino substituent on imidazole ring"""
    # Convert tuple to list for easier indexing
    imidazole_list = list(imidazole_atoms)
    
    # Find the nitrogen atoms in the imidazole ring
    n_atoms = [i for i, idx in enumerate(imidazole_list) if mol.GetAtomWithIdx(idx).GetSymbol() == 'N']
    
    # The first nitrogen (NH) is considered position 1
    # Renumber atoms starting from NH
    nh_pos = n_atoms[0]  # Position of NH in the list
    reordered = imidazole_list[nh_pos:] + imidazole_list[:nh_pos]
    
    # Find position of attachment point in reordered list
    try:
        position = reordered.index(attachment_point) + 1
        return position
    except ValueError:
        return "unknown"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22512',
                          'name': 'aminoimidazole',
                          'definition': 'Any member of the class of  '
                                        'imidazoles carrying at least one '
                                        'amino substituent.',
                          'parents': ['CHEBI:24780']},
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
    'num_false_positives': 6,
    'num_true_negatives': 183908,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999565018812936}