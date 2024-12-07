"""
Classifies: CHEBI:25940 peroxides
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_peroxides(smiles: str):
    """
    Determines if a molecule contains a peroxide group (ROOR').
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains peroxide group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find all oxygen atoms
    oxygen_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'O']
    
    # Check for O-O bonds
    for o1 in oxygen_atoms:
        for neighbor in o1.GetNeighbors():
            if neighbor.GetSymbol() == 'O':
                o2 = neighbor
                
                # Check that both oxygens have other neighbors (R groups)
                o1_neighbors = [n for n in o1.GetNeighbors() if n.GetIdx() != o2.GetIdx()]
                o2_neighbors = [n for n in o2.GetNeighbors() if n.GetIdx() != o1.GetIdx()]
                
                if len(o1_neighbors) > 0 and len(o2_neighbors) > 0:
                    # Get R group details
                    r1 = o1_neighbors[0].GetSymbol()
                    r2 = o2_neighbors[0].GetSymbol()
                    return True, f"Contains peroxide group with R groups: {r1} and {r2}"
                    
    return False, "No peroxide group (ROOR') found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25940',
                          'name': 'peroxides',
                          'definition': "Compounds of structure ROOR'.",
                          'parents': ['CHEBI:25741']},
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
    'num_true_negatives': 89177,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9988799534060617}