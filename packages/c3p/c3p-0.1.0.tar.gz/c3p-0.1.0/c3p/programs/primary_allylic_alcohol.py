"""
Classifies: CHEBI:134394 primary allylic alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_primary_allylic_alcohol(smiles: str):
    """
    Determines if a molecule contains a primary allylic alcohol group.
    A primary allylic alcohol has a carbon atom that:
    1. Is attached to a hydroxy (-OH) group
    2. Is attached to two hydrogens (primary)
    3. Is adjacent to a carbon-carbon double bond (allylic)

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains primary allylic alcohol, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Add explicit hydrogens
    mol = Chem.AddHs(mol)
    
    # Find all OH groups
    pattern = Chem.MolFromSmarts("[CH2][OH]")
    matches = mol.GetSubstructMatches(pattern)
    
    if not matches:
        return False, "No primary alcohol groups found"
        
    # For each OH group, check if carbon is adjacent to C=C
    for match in matches:
        c_atom = mol.GetAtomWithIdx(match[0])
        
        # Check if carbon has exactly 2 hydrogens (primary)
        h_count = sum(1 for n in c_atom.GetNeighbors() if n.GetAtomicNum() == 1)
        if h_count != 2:
            continue
            
        # Check neighbors for double bond
        for neighbor in c_atom.GetNeighbors():
            if neighbor.GetAtomicNum() == 6:  # Carbon
                for bond in neighbor.GetBonds():
                    if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                        other_atom = bond.GetOtherAtom(neighbor)
                        if other_atom.GetAtomicNum() == 6:  # C=C
                            return True, "Contains primary allylic alcohol group"
                            
    return False, "No primary allylic alcohol groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134394',
                          'name': 'primary allylic alcohol',
                          'definition': 'An allylic alcohol in which the '
                                        'carbon atom that links the double '
                                        'bond to the hydroxy group is also '
                                        'attached to two hydrogens.',
                          'parents': ['CHEBI:134361', 'CHEBI:15734']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 11068,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9910498523225634}