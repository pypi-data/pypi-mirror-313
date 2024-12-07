"""
Classifies: CHEBI:17522 alditol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import Compute2DCoords
import re

def is_alditol(smiles: str):
    """
    Determines if a molecule is an alditol - an acyclic polyol with formula HOCH2[CH(OH)]nCH2OH
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an alditol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for required elements
    allowed_atoms = {'C', 'H', 'O'} 
    atom_symbols = {atom.GetSymbol() for atom in mol.GetAtoms()}
    if not atom_symbols.issubset(allowed_atoms):
        return False, f"Contains non-CHO atoms: {atom_symbols - allowed_atoms}"
        
    # Find linear carbon chain with hydroxyl groups
    pattern = Chem.MolFromSmarts("[CH2][CH]([OH])[CH]([OH])[CH2][OH]")
    if not mol.HasSubstructMatch(pattern):
        return False, "Does not match basic alditol pattern HOCH2[CH(OH)]nCH2OH"
        
    # Check that each carbon has exactly one hydroxyl group
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            oh_count = len([n for n in atom.GetNeighbors() if n.GetSymbol() == 'O' and len([nn for nn in n.GetNeighbors()]) == 1])
            if oh_count != 1:
                return False, f"Carbon at position {atom.GetIdx()} has {oh_count} hydroxyl groups instead of 1"
                
    # Check for cyclic structures
    ri = mol.GetRingInfo()
    if ri.NumRings() > 0:
        return False, "Contains cyclic structures"
        
    # Check for terminal CH2OH groups
    terminal_pattern = Chem.MolFromSmarts("[CH2][OH]")
    matches = mol.GetSubstructMatches(terminal_pattern)
    if len(matches) < 2:
        return False, "Missing terminal CH2OH groups"
        
    return True, "Matches alditol pattern HOCH2[CH(OH)]nCH2OH"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17522',
                          'name': 'alditol',
                          'definition': 'A carbohydrate that is an acyclic '
                                        'polyol having the general formula '
                                        'HOCH2[CH(OH)]nCH2OH (formally '
                                        'derivable from an aldose by reduction '
                                        'of the carbonyl group).',
                          'parents': ['CHEBI:16646', 'CHEBI:26191']},
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
    'num_true_positives': 2,
    'num_false_positives': 0,
    'num_true_negatives': 183841,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.2222222222222222,
    'f1': 0.3636363636363636,
    'accuracy': 0.9999619254827304}