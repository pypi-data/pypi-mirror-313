"""
Classifies: CHEBI:139173 heparin oligosaccharide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition

def is_heparin_oligosaccharide(smiles: str):
    """
    Determines if a molecule is a heparin oligosaccharide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a heparin oligosaccharide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of sulfate groups
    sulfate_pattern = Chem.MolFromSmarts('OS(=O)(=O)O')
    if not mol.HasSubstructMatch(sulfate_pattern):
        return False, "No sulfate groups found"
        
    # Check for presence of carboxyl groups
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "No carboxyl groups found"
        
    # Check for presence of glycosidic linkages
    glycosidic_pattern = Chem.MolFromSmarts('OC1OC(C)CCC1')
    if not mol.HasSubstructMatch(glycosidic_pattern):
        return False, "No glycosidic linkages found"
        
    # Count number of monosaccharide units
    sugar_rings = rdDecomposition.identify_glycans(mol)
    n_sugars = len(sugar_rings)
    
    if n_sugars < 2:
        return False, "Less than 2 monosaccharide units found"
        
    # Check for N-acetyl or N-sulfo groups
    n_acetyl = Chem.MolFromSmarts('NC(=O)C')
    n_sulfo = Chem.MolFromSmarts('NS(=O)(=O)O')
    
    if not (mol.HasSubstructMatch(n_acetyl) or mol.HasSubstructMatch(n_sulfo)):
        return False, "No N-acetyl or N-sulfo groups found"
        
    # Count functional groups
    n_sulfates = len(mol.GetSubstructMatches(sulfate_pattern))
    n_carboxyls = len(mol.GetSubstructMatches(carboxyl_pattern))
    n_n_acetyl = len(mol.GetSubstructMatches(n_acetyl))
    n_n_sulfo = len(mol.GetSubstructMatches(n_sulfo))
    
    return True, f"Heparin oligosaccharide with {n_sugars} monosaccharide units, {n_sulfates} sulfate groups, {n_carboxyls} carboxyl groups, {n_n_acetyl} N-acetyl groups and {n_n_sulfo} N-sulfo groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139173',
                          'name': 'heparin oligosaccharide',
                          'definition': 'Any oligosaccharide derivative '
                                        'resulting from  either chemical or '
                                        'enzymatic cleavage of the polymeric '
                                        'glycosaminoglycan heparin.',
                          'parents': ['CHEBI:63563']},
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
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}