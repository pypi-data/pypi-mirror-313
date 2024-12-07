"""
Classifies: CHEBI:22475 amino acid amide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_amino_acid_amide(smiles: str):
    """
    Determines if a molecule is an amino acid amide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an amino acid amide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Look for carboxamide group (C(=O)N)
    carboxamide_pattern = Chem.MolFromSmarts('[C;!$(C=O)][C](=O)[N;!$(NC=O)]')
    if not mol.HasSubstructMatch(carboxamide_pattern):
        return False, "No carboxamide group found"
        
    # Look for amine group not part of amide
    amine_pattern = Chem.MolFromSmarts('[N;!$(NC=O);!$(N=*)]')
    if not mol.HasSubstructMatch(amine_pattern):
        return False, "No free amine group found"
        
    # Look for carbon alpha to both amine and carboxamide
    alpha_carbon_pattern = Chem.MolFromSmarts('[C;!$(C=O)][C]([N;!$(NC=O)])[C](=O)[N;!$(NC=O)]')
    if not mol.HasSubstructMatch(alpha_carbon_pattern):
        return False, "No alpha carbon found between amine and carboxamide"
        
    # If all patterns found, classify as amino acid amide
    return True, "Contains amine group, carboxamide group, and alpha carbon characteristic of amino acid amides"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22475',
                          'name': 'amino acid amide',
                          'definition': 'An amide of an amino acid formed '
                                        'formally by conversion of the carboxy '
                                        'group to a carboxamido group.',
                          'parents': ['CHEBI:37622', 'CHEBI:83821']},
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
    'num_true_negatives': 183130,
    'num_false_negatives': 80,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9995633426123028}