"""
Classifies: CHEBI:13759 alkylamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alkylamine(smiles: str):
    """
    Determines if a molecule is an alkylamine (primary amine with alkyl substituent).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an alkylamine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find nitrogen atoms
    n_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7]
    if not n_atoms:
        return False, "No nitrogen atoms found"
        
    # Check each nitrogen for primary amine pattern
    for n_atom in n_atoms:
        # Check if nitrogen has 3 bonds total (including hydrogens)
        if n_atom.GetTotalNumHs() + n_atom.GetDegree() != 3:
            continue
            
        # Check if nitrogen has exactly 2 hydrogens (primary amine)
        if n_atom.GetTotalNumHs() != 2:
            continue
            
        # Get the carbon neighbor
        c_neighbors = [neighbor for neighbor in n_atom.GetNeighbors() 
                      if neighbor.GetAtomicNum() == 6]
        
        if not c_neighbors:
            continue
            
        c_neighbor = c_neighbors[0]
        
        # Check if carbon is sp3 hybridized (alkyl)
        if c_neighbor.GetHybridization() != Chem.HybridizationType.SP3:
            continue
            
        # Check if carbon is part of any aromatic ring
        if c_neighbor.GetIsAromatic():
            continue
            
        # Check if carbon is part of any double/triple bonds
        has_multiple_bonds = False
        for bond in c_neighbor.GetBonds():
            if bond.GetBondType() != Chem.BondType.SINGLE:
                has_multiple_bonds = True
                break
                
        if has_multiple_bonds:
            continue
            
        # If we get here, we found an alkylamine group
        return True, "Contains primary amine with alkyl substituent"
        
    return False, "No primary amine with alkyl substituent found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13759',
                          'name': 'alkylamine',
                          'definition': 'Any primary amine in which the '
                                        'substituent attached to nitrogen is '
                                        'an alkyl group.',
                          'parents': ['CHEBI:32877']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 967,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9064546304957904}