"""
Classifies: CHEBI:26399 purine ribonucleoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdDecomposition

def is_purine_ribonucleoside(smiles: str):
    """
    Determines if a molecule is a purine ribonucleoside.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a purine ribonucleoside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for ribose sugar
    ribose_pattern = Chem.MolFromSmarts("[C]1[C@H]([OH1,O])[C@@H]([OH1,O])[C@H](O[C])[C@@H]1[CH2][OH1,O]")
    if not mol.HasSubstructMatch(ribose_pattern):
        return False, "No ribose sugar moiety found"

    # Check for purine core
    purine_pattern = Chem.MolFromSmarts("c1ncnc2[nH,n]cnc12")
    if not mol.HasSubstructMatch(purine_pattern):
        return False, "No purine core structure found"

    # Check if purine is connected to ribose
    matches = mol.GetSubstructMatches(purine_pattern)
    ribose_matches = mol.GetSubstructMatches(ribose_pattern)
    
    if not matches or not ribose_matches:
        return False, "Could not find required substructures"

    purine_atoms = set(matches[0])
    ribose_atoms = set(ribose_matches[0])
    
    # Check connectivity between purine and ribose
    connected = False
    for p_atom in purine_atoms:
        for r_atom in ribose_atoms:
            bond = mol.GetBondBetweenAtoms(p_atom, r_atom)
            if bond is not None:
                connected = True
                break
        if connected:
            break
            
    if not connected:
        return False, "Purine not connected to ribose"

    # Additional check for nucleobase connection to ribose at correct position
    glycosidic_n = None
    for atom_idx in purine_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'N':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() in ribose_atoms:
                    glycosidic_n = atom_idx
                    break
            if glycosidic_n is not None:
                break
                
    if glycosidic_n is None:
        return False, "No glycosidic bond found between purine and ribose"

    return True, "Contains connected purine and ribose moieties"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26399',
                          'name': 'purine ribonucleoside',
                          'definition': 'A ribonucleoside that has a purine '
                                        'moiety as the nucleobase (the R group '
                                        'in the illustration).',
                          'parents': ['CHEBI:18254', 'CHEBI:26394']},
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
    'success': False,
    'best': True,
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}