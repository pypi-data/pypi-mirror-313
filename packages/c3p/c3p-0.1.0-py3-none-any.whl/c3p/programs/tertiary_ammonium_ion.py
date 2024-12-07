"""
Classifies: CHEBI:137982 tertiary ammonium ion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tertiary_ammonium_ion(smiles: str):
    """
    Determines if a molecule is a tertiary ammonium ion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a tertiary ammonium ion, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find all nitrogen atoms
    n_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7]
    
    if not n_atoms:
        return False, "No nitrogen atoms found"
        
    # Check each nitrogen for tertiary ammonium characteristics
    for n_atom in n_atoms:
        # Check formal charge
        if n_atom.GetFormalCharge() != 1:
            continue
            
        # Count number of non-H neighbors
        n_neighbors = len([x for x in n_atom.GetNeighbors()])
        
        # Count number of H neighbors (explicit and implicit)
        n_hydrogens = n_atom.GetTotalNumHs()
        
        total_bonds = n_neighbors + n_hydrogens
        
        # Tertiary ammonium should have 4 total bonds (3 non-H + 1 H or 4 non-H)
        if total_bonds == 4:
            # Check if it's tertiary (3 non-H neighbors)
            if n_neighbors == 3 and n_hydrogens == 1:
                return True, "Found tertiary ammonium ion (3 non-H neighbors + 1 H)"
            elif n_neighbors == 4 and n_hydrogens == 0:
                return True, "Found quaternary ammonium ion (4 non-H neighbors)"
                
    return False, "No tertiary ammonium ions found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:137982',
                          'name': 'tertiary ammonium ion',
                          'definition': 'An organic cation obtained by '
                                        'protonation of the amino group of any '
                                        'tertiary amino compound.',
                          'parents': ['CHEBI:25697']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 6496,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9848461888164873}