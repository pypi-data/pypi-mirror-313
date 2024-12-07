"""
Classifies: CHEBI:26069 phosphonic acids
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phosphonic_acids(smiles: str):
    """
    Determines if a molecule is a phosphonic acid or P-substituted derivative.
    Phosphonic acids have the general structure HP(=O)(OH)2 or RP(=O)(OH)2.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphonic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find phosphorus atoms
    phosphorus_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'P']
    
    if not phosphorus_atoms:
        return False, "No phosphorus atoms found"

    for p_atom in phosphorus_atoms:
        # Get neighbors of phosphorus
        neighbors = list(p_atom.GetNeighbors())
        
        # Check oxidation state/double bond
        if not any(bond.GetBondType() == Chem.BondType.DOUBLE for bond in p_atom.GetBonds()):
            continue
            
        # Count OH groups and O- groups (deprotonated form)
        oh_count = 0
        o_minus_count = 0
        for neighbor in neighbors:
            if neighbor.GetSymbol() == 'O':
                if neighbor.GetFormalCharge() == -1:
                    o_minus_count += 1
                elif sum(1 for n in neighbor.GetNeighbors() if n.GetSymbol() == 'H') == 1:
                    oh_count += 1
                    
        # Check for required pattern: 2 OH groups (or combination with O-)
        if (oh_count + o_minus_count) >= 2:
            # Get the R group (non-OH, non=O substituent)
            r_groups = []
            for neighbor in neighbors:
                if neighbor.GetSymbol() != 'O':
                    r_groups.append(neighbor.GetSymbol())
                    
            if r_groups:
                return True, f"P-substituted phosphonic acid with substituent(s) bonded to P"
            else:
                return True, "Unsubstituted phosphonic acid"
            
    return False, "No phosphonic acid group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26069',
                          'name': 'phosphonic acids',
                          'definition': 'HP(=O)(OH)2  (phosphonic acid) and '
                                        'its P-substituted derivatives.',
                          'parents': ['CHEBI:36360']},
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
    'num_false_positives': 100,
    'num_true_negatives': 8400,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9874221229575644}