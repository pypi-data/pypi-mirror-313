"""
Classifies: CHEBI:26588 1,3,5-triazines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_3_5_triazines(smiles: str):
    """
    Determines if a molecule contains a 1,3,5-triazine core structure.
    A 1,3,5-triazine has nitrogen atoms at positions 1, 3 and 5 of a 6-membered aromatic ring.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains 1,3,5-triazine core, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for 1,3,5-triazine core
    # n1cnc(nc1) represents a 6-membered ring with alternating N atoms
    triazine_pattern = Chem.MolFromSmarts('n1cnc(nc1)')
    
    if mol.HasSubstructMatch(triazine_pattern):
        # Get matches
        matches = mol.GetSubstructMatches(triazine_pattern)
        
        for match in matches:
            # Get the atoms in the matched ring
            ring_atoms = [mol.GetAtomWithIdx(i) for i in match]
            
            # Count nitrogen atoms in the ring
            n_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'N')
            
            # Verify there are exactly 3 nitrogens
            if n_count == 3:
                # Check if the nitrogens are at positions 1,3,5
                n_positions = [i for i, atom in enumerate(ring_atoms) if atom.GetSymbol() == 'N']
                if set(n_positions) == {0, 2, 4}:  # positions 1,3,5 in 0-based indexing
                    # Get substituents
                    substituents = []
                    for atom_idx in match:
                        atom = mol.GetAtomWithIdx(atom_idx)
                        for neighbor in atom.GetNeighbors():
                            if neighbor.GetIdx() not in match:
                                substituents.append(neighbor.GetSymbol())
                    
                    if substituents:
                        return True, f"1,3,5-triazine with substituents: {', '.join(set(substituents))}"
                    else:
                        return True, "Unsubstituted 1,3,5-triazine"
                    
    return False, "No 1,3,5-triazine core structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26588',
                          'name': '1,3,5-triazines',
                          'definition': 'Any compound with a 1,3,5-triazine '
                                        'skeleton, in which nitrogen atoms '
                                        'replace carbon at positions 1, 3 and '
                                        '5 of the core benzene ring structure.',
                          'parents': ['CHEBI:38102']},
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
    'num_true_positives': 12,
    'num_false_positives': 100,
    'num_true_negatives': 150874,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.10714285714285714,
    'recall': 0.9230769230769231,
    'f1': 0.19199999999999998,
    'accuracy': 0.9993310682376628}