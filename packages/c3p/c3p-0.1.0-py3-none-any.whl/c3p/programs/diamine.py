"""
Classifies: CHEBI:23666 diamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_diamine(smiles: str):
    """
    Determines if a molecule is a diamine (contains exactly two amino groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a diamine, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find all nitrogen atoms
    n_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'N']
    
    if len(n_atoms) < 2:
        return False, "Contains fewer than 2 nitrogen atoms"
        
    # Count primary and secondary amino groups (-NH2 and -NH-)
    amino_count = 0
    for n_atom in n_atoms:
        # Get number of hydrogens (explicit + implicit)
        h_count = n_atom.GetTotalNumHs()
        
        # Get number of non-H neighbors
        heavy_neighbors = len([x for x in n_atom.GetNeighbors() 
                             if x.GetSymbol() != 'H'])
        
        # Check if nitrogen is sp3 hybridized
        if n_atom.GetHybridization() == Chem.HybridizationType.SP3:
            # Primary amine (-NH2) has 2 H and 1 heavy neighbor
            if h_count == 2 and heavy_neighbors == 1:
                amino_count += 1
            # Secondary amine (-NH-) has 1 H and 2 heavy neighbors    
            elif h_count == 1 and heavy_neighbors == 2:
                amino_count += 1
                
    if amino_count == 2:
        return True, "Contains exactly two amino groups (-NH2 or -NH-)"
    elif amino_count > 2:
        return False, f"Contains {amino_count} amino groups (more than 2)"
    else:
        return False, f"Contains only {amino_count} amino group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23666',
                          'name': 'diamine',
                          'definition': 'Any polyamine that contains two amino '
                                        'groups.',
                          'parents': ['CHEBI:88061']},
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
    'num_true_negatives': 5989,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 0.38461538461538464,
    'f1': 0.0847457627118644,
    'accuracy': 0.9823008849557522}