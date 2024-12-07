"""
Classifies: CHEBI:26401 purines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_purines(smiles: str):
    """
    Determines if a molecule is a purine or purine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a purine, False otherwise
        str: Reason for classification
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"
            
        # SMARTS patterns for purine and related structures
        patterns = [
            ('purine_core', 'c1ncnc2[nH]cnc12'),
            ('purine_N9', 'c1ncnc2n(*)cnc12'),  # N9-substituted
            ('purine_N7', 'c1ncnc2ncn(*)c12'),  # N7-substituted
            ('imidazopyrimidine', 'c1ncnc2n1ccn2'),
            ('oxidized_purine', 'c1nc(=O)c2[nH]cnc2n1'),  # For xanthine-like structures
            ('aminopurine', 'c1nc(N)nc2[nH]cnc12')  # For adenine-like structures
        ]
        
        for name, smarts in patterns:
            pattern = Chem.MolFromSmarts(smarts)
            if pattern and mol.HasSubstructMatch(pattern):
                # Get the atoms in the matched core
                matches = mol.GetSubstructMatches(pattern)
                if matches:
                    core_atoms = set(matches[0])
                    
                    # Find substituents
                    substituents = set()
                    for atom_idx in core_atoms:
                        atom = mol.GetAtomWithIdx(atom_idx)
                        for neighbor in atom.GetNeighbors():
                            if neighbor.GetIdx() not in core_atoms:
                                # Add substituent type
                                if neighbor.GetSymbol() != 'H':  # Ignore hydrogens
                                    substituent = neighbor.GetSymbol()
                                    if neighbor.GetDegree() > 1:  # If it's part of a larger group
                                        substituent += "-substituted"
                                    substituents.add(substituent)
                    
                    if substituents:
                        return True, f"Substituted purine ({name}) with substituents: {', '.join(substituents)}"
                    else:
                        return True, f"Unsubstituted purine ({name})"
        
        return False, "Does not contain purine or imidazopyrimidine core"
        
    except Exception as e:
        return False, f"Error analyzing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26401',
                          'name': 'purines',
                          'definition': 'A class of imidazopyrimidines that '
                                        'consists of purine and its '
                                        'substituted derivatives.',
                          'parents': ['CHEBI:35875']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 157,
    'num_false_positives': 100,
    'num_true_negatives': 7466,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.6108949416342413,
    'recall': 0.9457831325301205,
    'f1': 0.7423167848699764,
    'accuracy': 0.9859027418520434}