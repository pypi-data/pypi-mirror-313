"""
Classifies: CHEBI:23128 chloroalkane
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_chloroalkane(smiles: str):
    """
    Determines if a molecule is a chloroalkane (alkane with at least one chlorine substituent).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a chloroalkane, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check if molecule contains chlorine
    has_chlorine = False
    chlorine_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'Cl':
            has_chlorine = True
            chlorine_count += 1
    
    if not has_chlorine:
        return False, "No chlorine atoms found"

    # Check if molecule is an alkane (only sp3 carbons)
    is_alkane = True
    carbon_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            carbon_count += 1
            # Check hybridization - must be sp3 for alkanes
            if atom.GetHybridization() != Chem.HybridizationType.SP3:
                is_alkane = False
                break
        # Check for atoms other than C, H, Cl
        elif atom.GetSymbol() not in ['C', 'H', 'Cl']:
            is_alkane = False
            break

    if not is_alkane:
        return False, "Not an alkane (contains unsaturation or non C/H/Cl atoms)"
    
    if carbon_count == 0:
        return False, "No carbon atoms found"

    return True, f"Chloroalkane with {chlorine_count} chlorine atom(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23128',
                          'name': 'chloroalkane',
                          'definition': 'Any haloalkane that consists of an '
                                        'alkane substituted by at least one '
                                        'chloro group.',
                          'parents': ['CHEBI:24469', 'CHEBI:36683']},
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
    'num_true_positives': 2,
    'num_false_positives': 14,
    'num_true_negatives': 183898,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.125,
    'recall': 1.0,
    'f1': 0.2222222222222222,
    'accuracy': 0.9999238774644671}