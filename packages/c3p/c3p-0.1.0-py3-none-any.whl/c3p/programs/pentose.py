"""
Classifies: CHEBI:25901 pentose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_pentose(smiles: str):
    """
    Determines if a molecule is a pentose (5-carbon monosaccharide).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a pentose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Count carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 5:
        return False, f"Contains {carbon_count} carbons, pentoses must have exactly 5"
        
    # Count oxygens 
    oxygen_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if oxygen_count < 4:
        return False, f"Contains only {oxygen_count} oxygens, pentoses require at least 4"

    # Check for aldehyde (C=O) or ketone (C(=O)C) group
    has_aldehyde = False
    has_ketone = False
    
    # Look for aldehyde pattern
    patt_ald = Chem.MolFromSmarts('[CH]=O')
    if mol.HasSubstructMatch(patt_ald):
        has_aldehyde = True
        
    # Look for ketone pattern 
    patt_ket = Chem.MolFromSmarts('CC(=O)C')
    if mol.HasSubstructMatch(patt_ket):
        has_ketone = True

    # Check for cyclic forms (furanose/pyranose)
    ring_info = mol.GetRingInfo()
    has_ring = ring_info.NumRings() > 0
    
    if has_ring:
        # Check ring sizes
        ring_sizes = [len(ring) for ring in ring_info.AtomRings()]
        if 5 in ring_sizes:
            return True, "Furanose form of pentose"
        elif 6 in ring_sizes:
            return True, "Pyranose form of pentose"
    elif has_aldehyde:
        return True, "Linear aldopentose"
    elif has_ketone:
        return True, "Linear ketopentose"
        
    return False, "Does not match pentose structural patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25901',
                          'name': 'pentose',
                          'definition': 'A five-carbon monosaccharide which in '
                                        'its linear form contains either an '
                                        'aldehyde group at position 1 '
                                        '(aldopentose) or a ketone group at '
                                        'position 2 (ketopentose).',
                          'parents': ['CHEBI:35381']},
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
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 54932,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 0.8888888888888888,
    'f1': 0.13675213675213674,
    'accuracy': 0.9981650042695446}