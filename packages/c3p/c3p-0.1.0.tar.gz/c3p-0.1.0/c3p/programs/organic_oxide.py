"""
Classifies: CHEBI:25701 organic oxide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organic_oxide(smiles: str):
    """
    Determines if a molecule is an organic oxide (oxygen bonded to carbon).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organic oxide, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule from SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find all oxygen atoms
    oxygen_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8]
    if not oxygen_atoms:
        return False, "No oxygen atoms found"

    # Check each oxygen atom for carbon neighbors
    organic_oxide_oxygens = []
    for oxygen in oxygen_atoms:
        neighbors = [neighbor for neighbor in oxygen.GetNeighbors()]
        carbon_neighbors = [n for n in neighbors if n.GetAtomicNum() == 6]
        
        if carbon_neighbors:
            # Get bonding pattern
            bond_types = []
            for neighbor in neighbors:
                bond = mol.GetBondBetweenAtoms(oxygen.GetIdx(), neighbor.GetIdx())
                bond_types.append(bond.GetBondType())
            
            neighbor_elements = [n.GetSymbol() for n in neighbors]
            organic_oxide_oxygens.append((neighbor_elements, bond_types))

    if organic_oxide_oxygens:
        # Create detailed description of bonding patterns
        patterns = []
        for neighbors, bonds in organic_oxide_oxygens:
            pattern = f"O bonded to {' and '.join(neighbors)}"
            patterns.append(pattern)
        
        return True, f"Organic oxide found with patterns: {'; '.join(patterns)}"
    
    return False, "No oxygen atoms bonded to carbon found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25701',
                          'name': 'organic oxide',
                          'definition': 'An oxide in which the oxygen atom is '
                                        'bonded to a carbon atom.',
                          'parents': ['CHEBI:25741', 'CHEBI:72695']},
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
    'num_true_negatives': 5,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.09090909090909091}