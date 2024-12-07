"""
Classifies: CHEBI:21731 N-glycosyl compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
import re

def is_N_glycosyl_compound(smiles: str):
    """
    Determines if a molecule is an N-glycosyl compound.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-glycosyl compound, False otherwise
        str: Reason for classification
    """
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None, None
            
        # Look for sugar ring patterns
        sugar_pattern = Chem.MolFromSmarts('[CR1]1[CR1][CR1][CR1][CR1]O1') # pyranose
        furanose_pattern = Chem.MolFromSmarts('[CR1]1[CR1][CR1][CR1]O1') # furanose
        
        sugar_matches = mol.GetSubstructMatches(sugar_pattern)
        furanose_matches = mol.GetSubstructMatches(furanose_pattern)
        
        if not (sugar_matches or furanose_matches):
            return False, "No sugar ring found"
            
        # Get all sugar ring atoms
        sugar_atoms = set()
        for match in sugar_matches:
            sugar_atoms.update(match)
        for match in furanose_matches:
            sugar_atoms.update(match)
            
        # Look for N-glycosidic bonds
        for atom_idx in sugar_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'O': # anomeric oxygen
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetIdx() not in sugar_atoms:
                        # Check if this non-sugar atom is connected to N
                        for n2 in neighbor.GetNeighbors():
                            if n2.GetSymbol() == 'N':
                                return True, "N-glycosidic bond found"
                                
        return False, "No N-glycosidic bond found"
        
    except Exception as e:
        return None, f"Error: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21731',
                          'name': 'N-glycosyl compound',
                          'definition': 'A glycosyl compound arising formally '
                                        'from the elimination of water from a '
                                        'glycosidic hydroxy group and an H '
                                        'atom bound to a nitrogen atom, thus '
                                        'creating a C-N bond.',
                          'parents': [   'CHEBI:35352',
                                         'CHEBI:63161',
                                         'CHEBI:63299']},
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
    'num_true_negatives': 183221,
    'num_false_negatives': 71,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9996126399406412}