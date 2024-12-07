"""
Classifies: CHEBI:26292 propanones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_propanones(smiles: str):
    """
    Determines if a molecule is a propanone (propane with at least one oxo/ketone group).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a propanone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find all ketone groups (C(=O)C)
    ketone_pattern = Chem.MolFromSmarts('[C]-C(=O)-[C]')
    matches = mol.GetSubstructMatches(ketone_pattern)
    
    if not matches:
        return False, "No ketone group found"

    # For each ketone match, check if it's part of a propane backbone
    for match in matches:
        central_carbon = match[1]  # The carbon of C(=O)
        
        # Get the two carbons connected to the ketone carbon
        connected_carbons = []
        for atom_idx in [match[0], match[2]]:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'C':
                connected_carbons.append(atom_idx)
        
        if len(connected_carbons) == 2:
            # Found a propanone backbone (C-C(=O)-C)
            substituents = []
            for atom_idx in connected_carbons:
                atom = mol.GetAtomWithIdx(atom_idx)
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetIdx() not in [central_carbon] + connected_carbons:
                        substituents.append(neighbor.GetSymbol())
            
            return True, f"Propanone found with substituents: {', '.join(set(substituents))}"
            
    return False, "No propanone backbone found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26292',
                          'name': 'propanones',
                          'definition': 'A ketone that is propane carrying at '
                                        'least one oxo substituent.',
                          'parents': ['CHEBI:17087']},
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
    'num_true_negatives': 183905,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999836874959219}