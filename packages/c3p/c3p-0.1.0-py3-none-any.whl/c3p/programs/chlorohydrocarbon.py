"""
Classifies: CHEBI:23115 chlorohydrocarbon
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_chlorohydrocarbon(smiles: str):
    """
    Determines if a molecule is a chlorohydrocarbon (compound derived from hydrocarbon 
    by replacing at least one hydrogen with chlorine).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a chlorohydrocarbon, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count atoms
    num_carbons = 0
    num_chlorines = 0
    num_other = 0
    other_atoms = set()
    
    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        if symbol == 'C':
            num_carbons += 1
        elif symbol == 'Cl':
            num_chlorines += 1
        else:
            num_other += 1
            other_atoms.add(symbol)

    # Must have at least one carbon and one chlorine
    if num_carbons == 0:
        return False, "No carbon atoms found"
    if num_chlorines == 0:
        return False, "No chlorine atoms found"

    # Create parent hydrocarbon by replacing chlorines with hydrogens
    parent_smiles = smiles.replace('Cl','H')
    parent_mol = Chem.MolFromSmiles(parent_smiles)
    
    if parent_mol is None:
        return False, "Could not generate valid parent hydrocarbon structure"

    # Check if parent molecule is a hydrocarbon
    for atom in parent_mol.GetAtoms():
        if atom.GetSymbol() not in ['C', 'H']:
            return False, f"Contains non-hydrocarbon atoms: {', '.join(other_atoms)}"

    return True, f"Chlorohydrocarbon with {num_carbons} carbons and {num_chlorines} chlorines" + \
           (f" (also contains {', '.join(other_atoms)})" if other_atoms else "")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23115',
                          'name': 'chlorohydrocarbon',
                          'definition': 'A compound derived from a hydrocarbon '
                                        'by replacing at least one hydrogen '
                                        'atom with a chlorine atom.',
                          'parents': ['CHEBI:24472', 'CHEBI:36683']},
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
    'num_true_negatives': 183854,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999564891059599}