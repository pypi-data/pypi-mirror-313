"""
Classifies: CHEBI:24631 hydrazines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydrazines(smiles: str):
    """
    Determines if a molecule is a hydrazine or hydrazine derivative.
    Hydrazines contain an N-N single bond with possible substitutions.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydrazine, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find N-N bonds
    n_n_bonds = []
    for bond in mol.GetBonds():
        atoms = [bond.GetBeginAtom(), bond.GetEndAtom()]
        if all(atom.GetAtomicNum() == 7 for atom in atoms):
            n_n_bonds.append(bond)

    if not n_n_bonds:
        return False, "No N-N bonds found"

    # Check each N-N bond
    for bond in n_n_bonds:
        # Get the nitrogen atoms
        n1, n2 = bond.GetBeginAtom(), bond.GetEndAtom()

        # Check if it's a single bond (hydrazine-like)
        if bond.GetBondType() == Chem.BondType.SINGLE:
            # Get substituents count
            subst_n1 = len([a for a in n1.GetNeighbors() if a.GetAtomicNum() != 7])
            subst_n2 = len([a for a in n2.GetNeighbors() if a.GetAtomicNum() != 7])
            
            total_subst = subst_n1 + subst_n2
            
            if total_subst == 0:
                return True, "Unsubstituted hydrazine"
            else:
                return True, f"Substituted hydrazine with {total_subst} substituent(s)"
                
        # Check for hydrazone-like structures (N-N=C)
        elif bond.GetBondType() == Chem.BondType.SINGLE or bond.GetBondType() == Chem.BondType.DOUBLE:
            for n_atom in [n1, n2]:
                for neighbor in n_atom.GetNeighbors():
                    if neighbor.GetAtomicNum() == 6:  # Carbon
                        bond_to_c = mol.GetBondBetweenAtoms(n_atom.GetIdx(), neighbor.GetIdx())
                        if bond_to_c.GetBondType() == Chem.BondType.DOUBLE:
                            return True, "Hydrazone derivative"

    return False, "Contains N-N bond but does not match hydrazine patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24631',
                          'name': 'hydrazines',
                          'definition': 'Hydrazine (diazane) and its '
                                        'substituted derivatives.',
                          'parents': ['CHEBI:51143']},
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
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 8620,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9885399954159981}