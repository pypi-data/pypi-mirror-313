"""
Classifies: CHEBI:24079 formamides
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_formamides(smiles: str):
    """
    Determines if a molecule contains a formamide group R(1)R(2)NCHO.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains formamide group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # SMARTS pattern for formamide group [NX3]([#1,*])([#1,*])C(=O)[H]
    # This matches:
    # - An N with 3 connections (NX3)
    # - Two substituents that can be H or any atom ([#1,*])
    # - A C=O group
    # - A hydrogen on the carbonyl carbon
    formamide_pattern = Chem.MolFromSmarts('[NX3]([#1,*])([#1,*])C(=O)[H]')
    
    matches = mol.GetSubstructMatches(formamide_pattern)
    
    if not matches:
        return False, "No formamide group found"
        
    # For each match, verify it's a true formamide
    valid_matches = []
    for match in matches:
        n_atom = mol.GetAtomWithIdx(match[0])
        c_atom = mol.GetAtomWithIdx(match[3])
        
        # Verify N has exactly 3 bonds
        if len(n_atom.GetBonds()) != 3:
            continue
            
        # Verify C has exactly 2 bonds (one single to N, one double to O)
        if len(c_atom.GetBonds()) != 2:
            continue
            
        valid_matches.append(match)
    
    if not valid_matches:
        return False, "No valid formamide groups found"
        
    # Get substituents on N for the first formamide group
    n_atom = mol.GetAtomWithIdx(valid_matches[0][0])
    substituents = []
    for neighbor in n_atom.GetNeighbors():
        if neighbor.GetIdx() != valid_matches[0][3]:  # Skip the carbonyl C
            if neighbor.GetSymbol() == 'H':
                substituents.append('H')
            else:
                substituents.append('R')
                
    if len(valid_matches) == 1:
        return True, f"Contains formamide group with N-substituents: {', '.join(substituents)}"
    else:
        return True, f"Contains {len(valid_matches)} formamide groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24079',
                          'name': 'formamides',
                          'definition': 'Amides with the general formula '
                                        'R(1)R(2)NCHO (R(1) and R(2) can be '
                                        'H).',
                          'parents': ['CHEBI:37622']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183886,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999782478655718}