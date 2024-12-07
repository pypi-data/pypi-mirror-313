"""
Classifies: CHEBI:17984 acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_acyl_CoA(smiles: str):
    """
    Determines if a molecule is an acyl-CoA (thioester formed between coenzyme A and a carboxylic acid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an acyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for thioester group (R-C(=O)-S-R)
    thioester_pattern = Chem.MolFromSmarts('[CX3](=O)[SX2]')
    if not mol.HasSubstructMatch(thioester_pattern):
        return False, "No thioester group found"

    # Check for key parts of CoA structure
    # Adenine base
    adenine_pattern = Chem.MolFromSmarts('c1nc(c2c(n1)n(cn2)[C@H]3O[C@H](COP)C[C@@H]3O)N')
    
    # Pantetheine part with thiol
    pantetheine_pattern = Chem.MolFromSmarts('NCCSC(=O)')
    
    # Phosphate groups
    phosphate_pattern = Chem.MolFromSmarts('OP(O)(O)=O')

    if not (mol.HasSubstructMatch(adenine_pattern) and 
            mol.HasSubstructMatch(pantetheine_pattern) and
            mol.HasSubstructMatch(phosphate_pattern)):
        return False, "Missing key components of Coenzyme A structure"

    # Get the acyl part by finding atoms connected to thioester
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)
    if thioester_matches:
        carbonyl_idx = thioester_matches[0][0]
        carbonyl_atom = mol.GetAtomWithIdx(carbonyl_idx)
        
        # Get neighbors excluding O and S atoms to identify R group
        r_group_atoms = [n for n in carbonyl_atom.GetNeighbors() 
                        if n.GetSymbol() not in ['O','S']]
        
        if r_group_atoms:
            r_group_type = "substituted"
            return True, f"Acyl-CoA with {r_group_type} acyl group"
    
    return True, "Acyl-CoA"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17984',
                          'name': 'acyl-CoA',
                          'definition': 'A thioester that results from the '
                                        'formal condensation of the thiol '
                                        'group of coenzyme A with the carboxy '
                                        'group of any carboxylic acid.',
                          'parents': [   'CHEBI:140325',
                                         'CHEBI:20706',
                                         'CHEBI:231540',
                                         'CHEBI:51277']},
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
    'num_true_positives': 79,
    'num_false_positives': 100,
    'num_true_negatives': 15907,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.441340782122905,
    'recall': 1.0,
    'f1': 0.6124031007751938,
    'accuracy': 0.9937834141489494}