"""
Classifies: CHEBI:137419 secondary ammonium ion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_secondary_ammonium_ion(smiles: str):
    """
    Determines if a molecule is a secondary ammonium ion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a secondary ammonium ion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for protonated nitrogen patterns
    patterns = [
        '[NH2+]', # Explicit secondary ammonium
        '[NH3+]'  # Primary ammonium (could be secondary with implicit H)
    ]

    secondary_ammonium_count = 0
    for pattern in patterns:
        matches = mol.GetSubstructMatches(Chem.MolFromSmarts(pattern))
        
        for match in matches:
            n_idx = match[0]
            n_atom = mol.GetAtomWithIdx(n_idx)
            
            # Count non-hydrogen neighbors
            non_h_neighbors = [neighbor for neighbor in n_atom.GetNeighbors() 
                             if neighbor.GetSymbol() != 'H']
            
            # For secondary ammonium:
            # - Should have exactly 2 non-H neighbors
            # - Not part of aromatic system
            # - Not part of imine/guanidinium (C=N)
            # - Total valence should be 4 (3 neighbors + positive charge)
            if (len(non_h_neighbors) == 2 and
                not n_atom.GetIsAromatic() and
                not any(bond.GetBondType() == Chem.BondType.DOUBLE for bond in n_atom.GetBonds())):
                secondary_ammonium_count += 1

    if secondary_ammonium_count > 0:
        return True, f"Found {secondary_ammonium_count} secondary ammonium ion(s)"
    return False, "No secondary ammonium ions found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:137419',
                          'name': 'secondary ammonium ion',
                          'definition': 'An organic cation obtained by '
                                        'protonation of any secondary amino '
                                        'compound; major species at pH 7.3.',
                          'parents': ['CHEBI:25697', 'CHEBI:35274']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               "False negatives: [('C(C[NH3+])CCC[NH2+]CC([C@@H](CO)O)=O', 'No "
               "secondary ammonium ions found'), "
               "('[H]\\\\C(C)=C1/C[NH2+][C@@]2([H])CC3=C(NC4=CC=CC=C34)C(=O)C[C@]1([H])[C@]2([H])C(=O)OC', "
               "'No secondary ammonium ions found'), "
               "('[H][C@]12CN(C)[C@]([H])(C[NH2+]1)CC1=C[C@@]([H])(C(=O)CC1)[C@@]1([H])C=C(CCC1=O)C2', "
               "'No secondary ammonium ions found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 29782,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9966538397189225}