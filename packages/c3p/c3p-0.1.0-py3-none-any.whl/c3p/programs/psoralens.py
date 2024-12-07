"""
Classifies: CHEBI:26369 psoralens
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetSubstructMatches

def is_psoralens(smiles: str):
    """
    Determines if a molecule is a psoralen (furanocoumarin with a 7H-furo[3,2-g]chromen-7-one skeleton).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a psoralen, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for the core psoralen scaffold
    # 7H-furo[3,2-g]chromen-7-one skeleton
    psoralen_pattern = Chem.MolFromSmarts('[#6]1:[#6]:[#6]2:[#6]:[#6](:[#6]:1):[#6]3:[#6]:[#6]:[#6](=[O:4]):[O:5]:[#6]:3:[#6]:2')
    
    # SMARTS pattern for the furan ring
    furan_pattern = Chem.MolFromSmarts('[#6]1:[#6]:[#6]:[#6]:[O:1]:1')

    # Check for psoralen core scaffold
    core_matches = mol.GetSubstructMatches(psoralen_pattern)
    if not core_matches:
        return False, "Missing core 7H-furo[3,2-g]chromen-7-one skeleton"

    # Check for furan ring
    furan_matches = mol.GetSubstructMatches(furan_pattern)
    if not furan_matches:
        return False, "Missing furan ring"

    # Count number of oxygen atoms
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if num_oxygens < 3:
        return False, "Insufficient number of oxygen atoms for psoralen structure"

    # Check for presence of lactone group (O=C-O)
    lactone_pattern = Chem.MolFromSmarts('[O:1]=[C:2]-[O:3]')
    if not mol.HasSubstructMatch(lactone_pattern):
        return False, "Missing lactone group"

    # Get number of rings
    rings = mol.GetRingInfo()
    if rings.NumRings() < 3:
        return False, "Insufficient number of rings"

    # Check for substitutions
    num_substituents = 0
    for atom in mol.GetAtoms():
        if atom.GetDegree() > 2 and atom.IsInRing():
            for neighbor in atom.GetNeighbors():
                if not neighbor.IsInRing():
                    num_substituents += 1

    if num_substituents > 0:
        return True, f"Substituted psoralen with {num_substituents} substituent(s)"
    else:
        return True, "Unsubstituted psoralen"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26369',
                          'name': 'psoralens',
                          'definition': 'A furanocoumarin with a '
                                        '7H-furo[3,2-g]chromen-7-one skeleton '
                                        'and its substituted derivatives '
                                        'thereof.',
                          'parents': ['CHEBI:24128']},
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
    'error': "cannot import name 'GetSubstructMatches' from "
             "'rdkit.Chem.AllChem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/AllChem.py)',
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