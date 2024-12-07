"""
Classifies: CHEBI:24396 glycopeptide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_glycopeptide(smiles: str):
    """
    Determines if a molecule is a glycopeptide (peptide with glycan moieties attached).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycopeptide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for peptide backbone
    peptide_pattern = Chem.MolFromSmarts('[NX3][CX4H1][CX3](=[OX1])[NX3]')
    if not mol.HasSubstructMatch(peptide_pattern):
        return False, "No peptide backbone found"
        
    # Check for glycan moieties
    # Look for pyranose rings with multiple OH groups
    glycan_pattern = Chem.MolFromSmarts('[CR1]1[CR1][CR1][CR1][CR1][OR1]1')
    if not mol.HasSubstructMatch(glycan_pattern):
        return False, "No glycan moieties found"
        
    # Check for glycosidic linkages
    glycosidic_pattern = Chem.MolFromSmarts('[OR1][CR1]1O[CR1][CR1][CR1][CR1][CR1]1')
    if not mol.HasSubstructMatch(glycosidic_pattern):
        return False, "No glycosidic linkages found"

    # Count number of amino acids (peptide bonds)
    peptide_matches = len(mol.GetSubstructMatches(peptide_pattern))
    
    # Count number of glycan rings
    glycan_matches = len(mol.GetSubstructMatches(glycan_pattern))
    
    # Count glycosidic linkages 
    glycosidic_matches = len(mol.GetSubstructMatches(glycosidic_pattern))

    return True, f"Found {peptide_matches} peptide bonds, {glycan_matches} glycan rings, and {glycosidic_matches} glycosidic linkages"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24396',
                          'name': 'glycopeptide',
                          'definition': 'Any carbohydrate derivative that '
                                        'consists of glycan moieties '
                                        'covalently attached to the side '
                                        'chains of the amino acid residues '
                                        'that constitute the peptide.',
                          'parents': ['CHEBI:16670', 'CHEBI:63299']},
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
    'num_true_negatives': 183843,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999510475817506}