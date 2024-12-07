"""
Classifies: CHEBI:26347 prostanoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
import re

def is_prostanoid(smiles: str):
    """
    Determines if a molecule is a prostanoid (prostaglandin or prostaglandin-like compound).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a prostanoid, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for cyclopentane ring which is common in prostanoids
    ring_info = mol.GetRingInfo()
    has_5_ring = False
    for ring in ring_info.AtomRings():
        if len(ring) == 5:
            has_5_ring = True
            break
            
    if not has_5_ring:
        return False, "No cyclopentane ring found"

    # Count carbons, oxygens
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    
    if num_oxygens < 2:
        return False, "Too few oxygen atoms for a prostanoid"
        
    # Look for carboxylic acid group or ester
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    ester_pattern = Chem.MolFromSmarts('C(=O)O[CH]')
    
    has_acid = mol.HasSubstructMatch(carboxyl_pattern)
    has_ester = mol.HasSubstructMatch(ester_pattern)
    
    if not (has_acid or has_ester):
        return False, "No carboxylic acid or ester group found"

    # Count double bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    
    if double_bonds < 1:
        return False, "No double bonds found"
        
    # Look for typical prostanoid features:
    # - Cyclopentane ring
    # - Carboxylic acid/ester group 
    # - Multiple oxygen-containing groups
    # - Double bonds
    # - Carbon chain length in typical range
    if (has_5_ring and 
        (has_acid or has_ester) and
        num_oxygens >= 2 and
        double_bonds >= 1 and
        15 <= num_carbons <= 40):
        return True, "Contains characteristic prostanoid features"
        
    return False, "Does not match prostanoid structural requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26347',
                          'name': 'prostanoid',
                          'definition': 'The family of natural prostaglandins '
                                        'and prostaglandin-like compounds '
                                        'including prostacyclins and '
                                        'thromboxanes.',
                          'parents': ['CHEBI:23899']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.rdMolDescriptors' has no "
               "attribute 'CalcNumAliphaticDoubleBonds'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 32,
    'num_false_positives': 100,
    'num_true_negatives': 2320,
    'num_false_negatives': 29,
    'num_negatives': None,
    'precision': 0.24242424242424243,
    'recall': 0.5245901639344263,
    'f1': 0.3316062176165803,
    'accuracy': 0.9480048367593712}