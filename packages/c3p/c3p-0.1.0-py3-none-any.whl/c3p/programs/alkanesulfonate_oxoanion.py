"""
Classifies: CHEBI:134249 alkanesulfonate oxoanion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alkanesulfonate_oxoanion(smiles: str):
    """
    Determines if a molecule is an alkanesulfonate oxoanion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an alkanesulfonate oxoanion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Look for sulfur atom
    sulfur_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'S']
    if not sulfur_atoms:
        return False, "No sulfur atom found"
    
    for sulfur in sulfur_atoms:
        # Check sulfur oxidation state/environment
        neighbors = sulfur.GetNeighbors()
        
        # Count oxygen neighbors and their types
        oxygen_count = 0
        oxo_count = 0
        oxoanion_count = 0
        carbon_neighbors = []
        
        for neighbor in neighbors:
            if neighbor.GetSymbol() == 'O':
                oxygen_count += 1
                if neighbor.GetFormalCharge() == -1:
                    oxoanion_count += 1
                elif len(neighbor.GetBonds()) == 1:  # Double bonded oxygen
                    oxo_count += 1
            elif neighbor.GetSymbol() == 'C':
                carbon_neighbors.append(neighbor)
                
        # Check if we have the SO3- group (one O-, two O=)
        if oxoanion_count == 1 and oxo_count == 2 and oxygen_count == 3:
            # Check if we have exactly one carbon neighbor
            if len(carbon_neighbors) == 1:
                carbon = carbon_neighbors[0]
                # The carbon can have any other substituents
                return True, "Valid alkanesulfonate oxoanion found"
                
    return False, "No valid alkanesulfonate oxoanion group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134249',
                          'name': 'alkanesulfonate oxoanion',
                          'definition': 'An alkanesulfonate in which the '
                                        'carbon at position 1 is attached to '
                                        'R, which can represent hydrogens, a '
                                        'carbon chain, or other groups.',
                          'parents': ['CHEBI:33554']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 43884,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.99772665272347}