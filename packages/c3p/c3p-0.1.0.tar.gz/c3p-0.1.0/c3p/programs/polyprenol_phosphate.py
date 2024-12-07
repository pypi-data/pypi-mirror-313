"""
Classifies: CHEBI:16460 polyprenol phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdMolDescriptors

def is_polyprenol_phosphate(smiles: str):
    """
    Determines if a molecule is a polyprenol phosphate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a polyprenol phosphate, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Check for phosphate group
    phosphate_pattern = Chem.MolFromSmarts('[P](=[O])([O,OH])[O,OH]')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group found"
        
    # Check for isoprene units (C5H8)
    isoprene_pattern = Chem.MolFromSmarts('C=C(C)CC')
    matches = mol.GetSubstructMatches(isoprene_pattern)
    if len(matches) < 2:  # Need at least 2 isoprene units
        return False, "Insufficient isoprene units found"
        
    # Check for conjugated double bonds characteristic of polyprenols
    conjugated_pattern = Chem.MolFromSmarts('C=CC=C')
    if mol.HasSubstructMatch(conjugated_pattern):
        return False, "Contains conjugated double bonds"
        
    # Check for phosphate linkage to prenol chain
    phosphate_prenol_pattern = Chem.MolFromSmarts('[P](=[O])([O,OH])[O]C/C=C')
    if not mol.HasSubstructMatch(phosphate_prenol_pattern):
        return False, "No phosphate linkage to prenol chain found"
        
    # Count number of isoprene units
    num_isoprene = len(matches)
    
    # Count number of phosphate groups
    num_phosphate = len(mol.GetSubstructMatches(phosphate_pattern))
    
    return True, f"Polyprenol phosphate with {num_isoprene} isoprene units and {num_phosphate} phosphate groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16460',
                          'name': 'polyprenol phosphate',
                          'definition': 'A prenol phosphate resulting from the '
                                        'formal condensation of the terminal '
                                        'allylic hydroxy group of a polyprenol '
                                        'with 1 mol eq. of phosphoric acid.',
                          'parents': ['CHEBI:26250', 'CHEBI:26875']},
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
    'num_true_positives': 12,
    'num_false_positives': 100,
    'num_true_negatives': 123954,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.10714285714285714,
    'recall': 0.9230769230769231,
    'f1': 0.19199999999999998,
    'accuracy': 0.9991859237347562}