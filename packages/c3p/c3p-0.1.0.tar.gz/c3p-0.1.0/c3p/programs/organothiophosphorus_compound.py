"""
Classifies: CHEBI:25716 organothiophosphorus compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organothiophosphorus_compound(smiles: str):
    """
    Determines if a molecule is an organothiophosphorus compound (contains P-S bond).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organothiophosphorus compound, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check if molecule contains phosphorus
    has_p = False
    p_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'P':
            has_p = True
            p_atoms.append(atom)
    
    if not has_p:
        return False, "No phosphorus atoms found"

    # Check for P-S bonds
    p_s_bonds = []
    for p_atom in p_atoms:
        for neighbor in p_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'S':
                bond = mol.GetBondBetweenAtoms(p_atom.GetIdx(), neighbor.GetIdx())
                if bond is not None:
                    p_s_bonds.append(bond)

    if not p_s_bonds:
        return False, "No phosphorus-sulfur bonds found"

    # Check for carbon atoms (to confirm it's an organo compound)
    has_carbon = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            has_carbon = True
            break
            
    if not has_carbon:
        return False, "No carbon atoms found - not an organo compound"

    # Count number of P-S bonds
    num_ps_bonds = len(p_s_bonds)
    
    return True, f"Found {num_ps_bonds} phosphorus-sulfur bond(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25716',
                          'name': 'organothiophosphorus compound',
                          'definition': 'An organothiophosphorus compound is '
                                        'an organophosphorus compound which '
                                        'contains a phosphorus-sulfur bond.',
                          'parents': ['CHEBI:25710', 'CHEBI:26835']},
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
    'num_true_positives': 9,
    'num_false_positives': 66,
    'num_true_negatives': 183733,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.12,
    'recall': 0.6923076923076923,
    'f1': 0.20454545454545456,
    'accuracy': 0.999619176114726}