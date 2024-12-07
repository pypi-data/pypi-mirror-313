"""
Classifies: CHEBI:26400 purine ribonucleotide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
import re

def is_purine_ribonucleotide(smiles: str):
    """
    Determines if a molecule is a purine ribonucleotide.
    A purine ribonucleotide must have:
    1. A purine base (adenine or guanine derivatives)
    2. A ribose sugar
    3. At least one phosphate group
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a purine ribonucleotide, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for phosphate group
    if not 'P' in [atom.GetSymbol() for atom in mol.GetAtoms()]:
        return False, "No phosphate group found"
    
    # Check for purine scaffold
    purine_pattern = Chem.MolFromSmarts('[#7]1[#6]=N[#6]2[#6](=[#7])[#7][#6]=[#7][#6]12')
    if not mol.HasSubstructMatch(purine_pattern):
        return False, "No purine base found"
        
    # Check for ribose sugar connected to purine
    ribose_pattern = Chem.MolFromSmarts('[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O')
    if not mol.HasSubstructMatch(ribose_pattern):
        return False, "No ribose sugar found"
        
    # Check connection between purine and ribose
    purine_ribose_pattern = Chem.MolFromSmarts('[#7]1[#6]=N[#6]2[#6](=[#7])[#7][#6]=[#7][#6]12-[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O')
    if not mol.HasSubstructMatch(purine_ribose_pattern):
        return False, "Purine not properly connected to ribose"

    # Determine purine base type
    if mol.HasSubstructMatch(Chem.MolFromSmarts('Nc1ncnc2[nH]cnc12')):
        base = "adenine"
    elif mol.HasSubstructMatch(Chem.MolFromSmarts('O=c1[nH]c(N)nc2[nH]cnc12')):
        base = "guanine"
    else:
        base = "modified purine"

    # Count phosphate groups
    phosphate_pattern = Chem.MolFromSmarts('OP(=O)(O)O')
    num_phosphates = len(mol.GetSubstructMatches(phosphate_pattern))
    
    return True, f"Purine ribonucleotide with {base} base and {num_phosphates} phosphate group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26400',
                          'name': 'purine ribonucleotide',
                          'definition': 'Any ribonucleotide that has a purine '
                                        'nucleobase.',
                          'parents': ['CHEBI:26395', 'CHEBI:26561']},
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
    'num_true_negatives': 183760,
    'num_false_negatives': 17,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999074965855357}