"""
Classifies: CHEBI:23643 depsipeptide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors


def is_depsipeptide(smiles: str):
    """
    Determines if a molecule is a depsipeptide based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a depsipeptide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for ester bonds (-O-C(=O)-)
    ester_pattern = Chem.MolFromSmarts('[#6]-O-C(=O)-[#6]')
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    
    # Look for amide bonds (-N-C(=O)-)
    amide_pattern = Chem.MolFromSmarts('[#7]-C(=O)-[#6]')
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    
    if not ester_matches:
        return False, "No ester bonds found"
    
    if not amide_matches:
        return False, "No amide bonds found"
    
    # Look for cyclic structure
    ring_info = mol.GetRingInfo()
    if not ring_info.NumRings():
        return False, "No cyclic structure found"
        
    # Count number of ester and amide bonds
    num_esters = len(ester_matches)
    num_amides = len(amide_matches)
    
    # Check for amino acid residues
    amino_acid_pattern = Chem.MolFromSmarts('[NX3,NX4+][CH]([CH2,CH3,CH,C])[C](=[O])[O,N]')
    amino_acid_matches = mol.GetSubstructMatches(amino_acid_pattern)
    
    # Check for hydroxy acid residues
    hydroxy_acid_pattern = Chem.MolFromSmarts('[OH][CH2,CH]([CH2,CH3,CH,C])[C](=[O])[O,N]')
    hydroxy_acid_matches = mol.GetSubstructMatches(hydroxy_acid_pattern)
    
    if not amino_acid_matches and not hydroxy_acid_matches:
        return False, "No amino acid or hydroxy acid residues found"
    
    if num_esters > 0 and num_amides > 0 and (amino_acid_matches or hydroxy_acid_matches):
        return True, f"Contains {num_esters} ester bonds, {num_amides} amide bonds, and amino/hydroxy acid residues in a cyclic structure"
    
    return False, "Does not meet all criteria for depsipeptide classification"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23643',
                          'name': 'depsipeptide',
                          'definition': 'A natural or synthetic compound '
                                        'having a sequence of amino and '
                                        'hydroxy carboxylic acid residues '
                                        '(usually alpha-amino and '
                                        'alpha-hydroxy acids), commonly but '
                                        'not necessarily regularly '
                                        'alternating.',
                          'parents': ['CHEBI:16670']},
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
    'num_true_positives': 156,
    'num_false_positives': 100,
    'num_true_negatives': 12852,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.609375,
    'recall': 0.9811320754716981,
    'f1': 0.7518072289156627,
    'accuracy': 0.9921440012203493}