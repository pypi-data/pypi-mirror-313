"""
Classifies: CHEBI:25713 organosilicon compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organosilicon_compound(smiles: str):
    """
    Determines if a molecule is an organosilicon compound (contains at least one C-Si bond).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an organosilicon compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Find all silicon atoms
    si_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'Si']
    
    if not si_atoms:
        return False, "No silicon atoms found"
        
    # Check for C-Si bonds
    c_si_bonds = []
    for si_atom in si_atoms:
        si_idx = si_atom.GetIdx()
        for neighbor in si_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                c_si_bonds.append((si_idx, neighbor.GetIdx()))
                
    if not c_si_bonds:
        return False, "No carbon-silicon bonds found"
        
    num_si = len(si_atoms)
    num_c_si = len(c_si_bonds)
    
    return True, f"Found {num_si} silicon atoms and {num_c_si} carbon-silicon bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25713',
                          'name': 'organosilicon compound',
                          'definition': 'An organosilicon compound is a '
                                        'compound containing at least one '
                                        'carbon-silicon bond.',
                          'parents': ['CHEBI:26677', 'CHEBI:50860']},
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
    'num_true_positives': 7,
    'num_false_positives': 68,
    'num_true_negatives': 183788,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.09333333333333334,
    'recall': 1.0,
    'f1': 0.17073170731707318,
    'accuracy': 0.999630159412171}