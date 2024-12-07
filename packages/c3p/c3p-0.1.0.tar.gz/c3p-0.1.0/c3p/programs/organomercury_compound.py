"""
Classifies: CHEBI:25706 organomercury compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organomercury_compound(smiles: str):
    """
    Determines if a molecule is an organomercury compound (contains at least one C-Hg bond)

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organomercury compound, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check if molecule contains mercury
    if not any(atom.GetSymbol() == 'Hg' for atom in mol.GetAtoms()):
        return False, "No mercury atoms found"

    # Find all mercury atoms
    hg_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'Hg']

    # Check for C-Hg bonds
    c_hg_bonds = []
    for hg_atom in hg_atoms:
        for neighbor in hg_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                bond = mol.GetBondBetweenAtoms(hg_atom.GetIdx(), neighbor.GetIdx())
                c_hg_bonds.append(bond)

    if not c_hg_bonds:
        return False, "No carbon-mercury bonds found"

    # Count number of C-Hg bonds
    num_c_hg_bonds = len(c_hg_bonds)
    
    # Get bond types
    bond_types = [str(bond.GetBondType()) for bond in c_hg_bonds]
    bond_desc = ", ".join(bond_types)

    return True, f"Found {num_c_hg_bonds} carbon-mercury bond(s) of type(s): {bond_desc}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25706',
                          'name': 'organomercury compound',
                          'definition': 'A compound containing at least one '
                                        'carbon-mercury bond.',
                          'parents': ['CHEBI:25196', 'CHEBI:25707']},
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
    'num_false_positives': 11,
    'num_true_negatives': 183897,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.15384615384615385,
    'recall': 1.0,
    'f1': 0.2666666666666667,
    'accuracy': 0.999940188135501}