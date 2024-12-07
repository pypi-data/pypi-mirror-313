"""
Classifies: CHEBI:197506 medium-chain fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_medium_chain_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is a medium-chain fatty alcohol (C6-C12 chain with one OH group)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a medium-chain fatty alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Count carbon atoms
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 6 or carbon_count > 12:
        return False, f"Carbon chain length ({carbon_count}) outside C6-C12 range"

    # Count OH groups
    oh_pattern = Chem.MolFromSmarts('[OH]')
    oh_matches = mol.GetSubstructMatches(oh_pattern)
    if len(oh_matches) != 1:
        return False, f"Contains {len(oh_matches)} OH groups, must contain exactly 1"

    # Check if molecule contains only C, H, O atoms
    allowed_atoms = {'C', 'H', 'O'}
    actual_atoms = {atom.GetSymbol() for atom in mol.GetAtoms()}
    if not actual_atoms.issubset(allowed_atoms):
        return False, f"Contains disallowed atoms: {actual_atoms - allowed_atoms}"

    # Check if the carbon chain is continuous
    # First, remove the OH group
    mol_no_oh = Chem.RWMol(mol)
    oh_atom = mol.GetAtomWithIdx(oh_matches[0][0])
    c_attached_to_oh = oh_atom.GetNeighbors()[0].GetIdx()
    mol_no_oh.RemoveAtom(oh_matches[0][0])
    
    # Now check if remaining carbons form a continuous chain
    remaining_atoms = [atom for atom in mol_no_oh.GetAtoms() if atom.GetSymbol() == 'C']
    if len(remaining_atoms) < 1:
        return False, "No carbon chain found"

    # Check for presence of only single bonds (except possibly one double bond)
    double_bond_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('C=C')))
    if double_bond_count > 1:
        return False, "Contains more than one double bond"
        
    return True, f"Medium-chain fatty alcohol with {carbon_count} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197506',
                          'name': 'medium-chain fatty alcohol',
                          'definition': 'Any fatty alcohol with a chain length '
                                        'between C6 and C12.',
                          'parents': ['CHEBI:24026']},
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
    'num_true_negatives': 7154,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9862220997519978}