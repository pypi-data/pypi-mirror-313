"""
Classifies: CHEBI:25238 methoxybenzoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_methoxybenzoic_acid(smiles: str):
    """
    Determines if a molecule is a methoxybenzoic acid (benzoic acid with one or more methoxy substituents).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a methoxybenzoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of carboxylic acid group (-COOH)
    carboxylic_acid_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Check for presence of methoxy group (-OCH3) connected to benzene ring
    methoxy_benzene_pattern = Chem.MolFromSmarts('c-[OX2][CH3]')
    if not mol.HasSubstructMatch(methoxy_benzene_pattern):
        return False, "No methoxy group attached to benzene ring found"

    # Find all carboxylic acid groups
    carboxylic_matches = mol.GetSubstructMatches(carboxylic_acid_pattern)
    
    # Find all methoxy groups
    methoxy_matches = mol.GetSubstructMatches(methoxy_benzene_pattern)

    # For each carboxylic acid group, check if it's connected to a benzene ring
    # that also has a methoxy substituent
    for acid_match in carboxylic_matches:
        acid_carbon = acid_match[0]  # Get the carbon atom of COOH
        
        # Get the atom connected to COOH
        acid_neighbors = mol.GetAtomWithIdx(acid_carbon).GetNeighbors()
        for neighbor in acid_neighbors:
            if neighbor.GetIsAromatic():  # If COOH is connected to aromatic ring
                ring_atom = neighbor.GetIdx()
                
                # Find the ring this atom belongs to
                ring_info = mol.GetRingInfo()
                for ring in ring_info.AtomRings():
                    if ring_atom in ring and len(ring) == 6:  # Found 6-membered ring containing COOH
                        # Check if any methoxy group is attached to this ring
                        for methoxy_match in methoxy_matches:
                            methoxy_oxygen = methoxy_match[0]
                            methoxy_neighbors = mol.GetAtomWithIdx(methoxy_oxygen).GetNeighbors()
                            for methoxy_neighbor in methoxy_neighbors:
                                if methoxy_neighbor.GetIsAromatic():
                                    if methoxy_neighbor.GetIdx() in ring:
                                        # Count number of methoxy groups on this ring
                                        methoxy_count = sum(1 for m in methoxy_matches 
                                                          if any(mol.GetAtomWithIdx(m[0]).GetNeighbors()[i].GetIdx() in ring 
                                                                for i in range(len(mol.GetAtomWithIdx(m[0]).GetNeighbors()))))
                                        return True, f"Found benzoic acid with {methoxy_count} methoxy substituent{'s' if methoxy_count > 1 else ''}"

    return False, "No methoxy group found on the same ring as carboxylic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25238',
                          'name': 'methoxybenzoic acid',
                          'definition': 'Any benzoic acid carrying one or more '
                                        'methoxy substituents.',
                          'parents': ['CHEBI:22723', 'CHEBI:51683']},
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
    'num_true_positives': 10,
    'num_false_positives': 100,
    'num_true_negatives': 107316,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 0.625,
    'f1': 0.15873015873015875,
    'accuracy': 0.9990133293618289}