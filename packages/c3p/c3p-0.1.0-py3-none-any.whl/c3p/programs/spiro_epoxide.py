"""
Classifies: CHEBI:133131 spiro-epoxide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_spiro_epoxide(smiles: str):
    """
    Determines if a molecule contains a spiro-epoxide motif - where a carbon atom
    of an epoxide ring is the only common member of two rings.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains spiro-epoxide, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get ring information
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        return False, "No rings found"

    # Find epoxide rings (3-membered rings containing oxygen)
    epoxide_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 3:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            atom_symbols = [atom.GetSymbol() for atom in atoms]
            if 'O' in atom_symbols:
                epoxide_rings.append(ring)

    if not epoxide_rings:
        return False, "No epoxide rings found"

    # Check each epoxide ring for spiro fusion
    for epoxide_ring in epoxide_rings:
        # Get carbon atoms in epoxide ring
        epoxide_carbons = [i for i in epoxide_ring if mol.GetAtomWithIdx(i).GetSymbol() == 'C']
        
        for carbon_idx in epoxide_carbons:
            # Find all rings containing this carbon
            rings_with_carbon = []
            for ring in rings.AtomRings():
                if carbon_idx in ring:
                    rings_with_carbon.append(set(ring))
            
            # Check if this carbon is a spiro center
            if len(rings_with_carbon) == 2:
                # Check if this carbon is the only common atom between the rings
                intersection = rings_with_carbon[0].intersection(rings_with_carbon[1])
                if len(intersection) == 1 and carbon_idx in intersection:
                    return True, f"Spiro-epoxide found with spiro carbon at index {carbon_idx}"

    return False, "No spiro-epoxide pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133131',
                          'name': 'spiro-epoxide',
                          'definition': 'An oxaspiro compound in which a '
                                        'carbon atom of an epoxide ring is the '
                                        'only common member of two rings.',
                          'parents': ['CHEBI:32955', 'CHEBI:37948']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 89404,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9988827939089924}