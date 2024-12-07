"""
Classifies: CHEBI:15897 N-(long-chain-acyl)ethanolamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_N__long_chain_acyl_ethanolamine(smiles: str):
    """
    Determines if a molecule is an N-(long-chain-acyl)ethanolamine.
    These are N-acylethanolamines with acyl chain length ≥ C12.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-(long-chain-acyl)ethanolamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of required functional groups
    if not all(group in Chem.MolToSmiles(mol) for group in ['C(=O)N', 'CCO']):
        return False, "Missing required N-acylethanolamine structure"

    # Find the amide carbon
    pattern = Chem.MolFromSmarts('C(=O)NCCO')
    if not mol.HasSubstructMatch(pattern):
        return False, "Missing N-acylethanolamine backbone"

    # Get the amide carbon and trace back the chain
    matches = mol.GetSubstructMatches(pattern)
    amide_carbon_idx = matches[0][0]  # First atom in the SMARTS pattern is the amide carbon
    
    # Function to count carbons in the acyl chain
    def count_chain_carbons(mol, start_idx, visited=None):
        if visited is None:
            visited = set()
        
        count = 1  # Count the current carbon
        visited.add(start_idx)
        
        atom = mol.GetAtomWithIdx(start_idx)
        for neighbor in atom.GetNeighbors():
            n_idx = neighbor.GetIdx()
            if n_idx not in visited and neighbor.GetSymbol() == 'C':
                # Don't count carbons in the ethanolamine part
                if not any(n_idx in [m[3], m[4]] for m in matches):
                    count += count_chain_carbons(mol, n_idx, visited)
        
        return count

    chain_length = count_chain_carbons(mol, amide_carbon_idx)

    if chain_length >= 12:
        return True, f"N-acylethanolamine with chain length C{chain_length}"
    else:
        return False, f"N-acylethanolamine with chain length C{chain_length} (less than C12)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15897',
                          'name': 'N-(long-chain-acyl)ethanolamine',
                          'definition': 'Any N-acylethanolamine in which the '
                                        'acyl group has a chain length of C12 '
                                        'or greater.',
                          'parents': ['CHEBI:167098']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: invalid syntax (<string>, line 47)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 63521,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9984282660631209}