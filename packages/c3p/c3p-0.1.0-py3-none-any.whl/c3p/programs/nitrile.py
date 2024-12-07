"""
Classifies: CHEBI:18379 nitrile
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_nitrile(smiles: str):
    """
    Determines if a molecule contains a nitrile group (R-C#N).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains nitrile group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # SMARTS pattern for nitrile group (R-C#N)
    nitrile_pattern = Chem.MolFromSmarts('C#N')
    
    # Find matches
    matches = mol.GetSubstructMatches(nitrile_pattern)
    
    if not matches:
        return False, "No nitrile group found"
        
    # For each match, verify it's a true nitrile:
    valid_nitriles = []
    for match in matches:
        c_atom = mol.GetAtomWithIdx(match[0])  # Carbon atom
        n_atom = mol.GetAtomWithIdx(match[1])  # Nitrogen atom
        
        # Check carbon has triple bond
        if not any(bond.GetBondType() == Chem.BondType.TRIPLE for bond in c_atom.GetBonds()):
            continue
            
        # Check nitrogen has only one bond (to carbon)
        if len(n_atom.GetBonds()) != 1:
            continue
            
        # Check carbon has exactly one other single bond (to R group)
        single_bonds = sum(1 for bond in c_atom.GetBonds() if bond.GetBondType() == Chem.BondType.SINGLE)
        if single_bonds != 1:
            continue
            
        valid_nitriles.append(match)

    if valid_nitriles:
        if len(valid_nitriles) == 1:
            return True, "Contains 1 nitrile group"
        else:
            return True, f"Contains {len(valid_nitriles)} nitrile groups"
    
    return False, "No valid nitrile groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18379',
                          'name': 'nitrile',
                          'definition': 'A compound having the structure RC#N; '
                                        'thus a C-substituted derivative of '
                                        'hydrocyanic acid, HC#N. In systematic '
                                        'nomenclature, the suffix nitrile '
                                        'denotes the triply bound #N atom, not '
                                        'the carbon atom attached to it.',
                          'parents': ['CHEBI:23424']},
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
    'num_true_positives': 65,
    'num_false_positives': 100,
    'num_true_negatives': 7970,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.3939393939393939,
    'recall': 1.0,
    'f1': 0.5652173913043478,
    'accuracy': 0.9877074370006146}