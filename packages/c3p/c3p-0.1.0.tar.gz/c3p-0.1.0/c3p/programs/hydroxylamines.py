"""
Classifies: CHEBI:24709 hydroxylamines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxylamines(smiles: str):
    """
    Determines if a molecule is a hydroxylamine (H2N-OH) or its hydrocarbyl derivatives.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxylamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for N-O single bonds
    n_o_bonds = []
    for bond in mol.GetBonds():
        if (bond.GetBeginAtom().GetSymbol() == 'N' and bond.GetEndAtom().GetSymbol() == 'O') or \
           (bond.GetBeginAtom().GetSymbol() == 'O' and bond.GetEndAtom().GetSymbol() == 'N'):
            if bond.GetBondType() == Chem.BondType.SINGLE:
                n_o_bonds.append(bond)

    if not n_o_bonds:
        return False, "No N-O single bonds found"

    # Check each N-O bond to confirm hydroxylamine pattern
    for bond in n_o_bonds:
        n_atom = bond.GetBeginAtom() if bond.GetBeginAtom().GetSymbol() == 'N' else bond.GetEndAtom()
        o_atom = bond.GetEndAtom() if bond.GetEndAtom().GetSymbol() == 'O' else bond.GetBeginAtom()
        
        # Check oxygen atom
        if len(o_atom.GetBonds()) != 1:  # O should only have one bond
            continue
            
        # Check nitrogen atom
        n_bonds = len(n_atom.GetBonds())
        if n_bonds < 2 or n_bonds > 3:  # N should have 2 or 3 bonds
            continue
            
        # Check if N is part of an amide (N-C(=O))
        is_amide = False
        for neighbor in n_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                for c_neighbor in neighbor.GetNeighbors():
                    if c_neighbor.GetSymbol() == 'O' and \
                       mol.GetBondBetweenAtoms(neighbor.GetIdx(), c_neighbor.GetIdx()).GetBondType() == Chem.BondType.DOUBLE:
                        is_amide = True
                        break
                        
        if is_amide:
            continue

        # If we get here, we've found a valid hydroxylamine group
        if n_bonds == 2:
            return True, "Primary hydroxylamine (H2N-OH) derivative found"
        else:
            return True, "Secondary hydroxylamine (RHN-OH) or tertiary hydroxylamine (R2N-OH) derivative found"

    return False, "No hydroxylamine groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24709',
                          'name': 'hydroxylamines',
                          'definition': 'Hydroxylamine, H2N-OH, and its '
                                        'hydrocarbyl derivatives.',
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
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 7293,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.9864864864864865}