"""
Classifies: CHEBI:25712 organoselenium compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organoselenium_compound(smiles: str):
    """
    Determines if a molecule is an organoselenium compound (contains at least one C-Se bond)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an organoselenium compound, False otherwise
        str: Reason for classification
    """
    # Create RDKit mol object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check if molecule contains selenium
    if not any(atom.GetSymbol() == 'Se' for atom in mol.GetAtoms()):
        return False, "No selenium atoms found"
        
    # Find all selenium atoms
    se_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'Se']
    
    # Check for C-Se bonds
    c_se_bonds = []
    for se_atom in se_atoms:
        for neighbor in se_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                c_se_bonds.append((se_atom.GetIdx(), neighbor.GetIdx()))
                
    if not c_se_bonds:
        return False, "No carbon-selenium bonds found"
        
    # Count number of C-Se bonds
    num_c_se_bonds = len(c_se_bonds)
    
    return True, f"Found {num_c_se_bonds} carbon-selenium bond{'s' if num_c_se_bonds > 1 else ''}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25712',
                          'name': 'organoselenium compound',
                          'definition': 'An organoselenium compound is a '
                                        'compound containing at least one '
                                        'carbon-selenium bond.',
                          'parents': ['CHEBI:26628', 'CHEBI:36962']},
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
    'num_true_positives': 3,
    'num_false_positives': 77,
    'num_true_negatives': 183826,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0375,
    'recall': 1.0,
    'f1': 0.07228915662650602,
    'accuracy': 0.9995813078420498}