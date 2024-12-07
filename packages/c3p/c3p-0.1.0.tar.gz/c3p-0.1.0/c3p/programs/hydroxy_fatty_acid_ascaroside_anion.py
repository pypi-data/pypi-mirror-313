"""
Classifies: CHEBI:140307 hydroxy fatty acid ascaroside anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxy_fatty_acid_ascaroside_anion(smiles: str):
    """
    Determines if a molecule is a hydroxy fatty acid ascaroside anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxy fatty acid ascaroside anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylate anion
    carboxylate_pattern = Chem.MolFromSmarts('C(=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion group found"
        
    # Check for ascarylose sugar core
    # Pattern for ascarylose ring with methyl group and hydroxyls
    ascarylose_pattern = Chem.MolFromSmarts('[CH3][CH]1O[CH](O)[CH](O)C[CH]1O')
    if not mol.HasSubstructMatch(ascarylose_pattern):
        return False, "No ascarylose sugar core found"
        
    # Check for linking oxygen between sugar and fatty acid chain
    linker_pattern = Chem.MolFromSmarts('O[CH2]C')
    if not mol.HasSubstructMatch(linker_pattern):
        return False, "No ether linkage found between sugar and fatty acid chain"
        
    # Count carbons in fatty acid chain
    # Get the carboxylate carbon index
    matches = mol.GetSubstructMatches(carboxylate_pattern)
    if len(matches) > 0:
        carboxylate_carbon = matches[0][0]
        
        # Traverse chain from carboxylate to sugar
        visited = set()
        current = carboxylate_carbon
        chain_length = 0
        
        while current is not None:
            visited.add(current)
            next_atom = None
            atom = mol.GetAtomWithIdx(current)
            
            for neighbor in atom.GetNeighbors():
                n_idx = neighbor.GetIdx()
                if n_idx not in visited and neighbor.GetSymbol() == 'C':
                    next_atom = n_idx
                    chain_length += 1
                    break
                    
            current = next_atom
            
        if chain_length < 3:
            return False, "Fatty acid chain too short"
            
    return True, "Contains carboxylate anion, ascarylose core, and appropriate fatty acid chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140307',
                          'name': 'hydroxy fatty acid ascaroside anion',
                          'definition': 'A monocarboxylic acid anion obtained '
                                        'by deprotonation of the carboxy group '
                                        'of any hydroxy fatty acid ascaroside; '
                                        'major species at pH 7.3.',
                          'parents': ['CHEBI:35757']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 98128,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9989819914283679}