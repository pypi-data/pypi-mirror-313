"""
Classifies: CHEBI:25718 ornithine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_ornithine_derivative(smiles: str):
    """
    Determines if a molecule is an ornithine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an ornithine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for basic ornithine backbone: NH2-CH2-CH2-CH2-CH(NH2)-COOH
    ornithine_pattern = Chem.MolFromSmarts("[NX3,NX4][CH2][CH2][CH2][CH]([NX3,NX4])[CX3](=O)[OX2,OX1-]")
    if not mol.HasSubstructMatch(ornithine_pattern):
        return False, "Does not contain ornithine backbone"

    # Count number of ornithine backbones to exclude peptides
    matches = mol.GetSubstructMatches(ornithine_pattern)
    if len(matches) > 1:
        return False, "Contains multiple ornithine units - likely a peptide"
        
    # Check for modifications at amino groups or carboxyl group
    modifications = []
    
    # Check N-terminal amino group modifications
    n_term_pattern = Chem.MolFromSmarts("[NX3,NX4][CH2][CH2][CH2][CH]([NX3,NX4])[CX3](=O)[OX2,OX1-]")
    if mol.HasSubstructMatch(n_term_pattern):
        n_match = mol.GetSubstructMatch(n_term_pattern)
        n_atom = mol.GetAtomWithIdx(n_match[0])
        if len([x for x in n_atom.GetNeighbors() if x.GetSymbol() != 'H']) > 1:
            modifications.append("N-terminal amino group")
            
    # Check alpha amino group modifications  
    alpha_n_pattern = Chem.MolFromSmarts("[NX3,NX4][CH2][CH2][CH2][CH]([NX3,NX4])[CX3](=O)[OX2,OX1-]")
    if mol.HasSubstructMatch(alpha_n_pattern):
        alpha_match = mol.GetSubstructMatch(alpha_n_pattern)
        alpha_n_atom = mol.GetAtomWithIdx(alpha_match[5])
        if len([x for x in alpha_n_atom.GetNeighbors() if x.GetSymbol() != 'H']) > 2:
            modifications.append("alpha amino group")

    # Check carboxyl group modifications
    carboxyl_pattern = Chem.MolFromSmarts("[NX3,NX4][CH2][CH2][CH2][CH]([NX3,NX4])[CX3](=O)[OX2,OX1-]")
    if mol.HasSubstructMatch(carboxyl_pattern):
        c_match = mol.GetSubstructMatch(carboxyl_pattern)
        c_atom = mol.GetAtomWithIdx(c_match[7])
        if len([x for x in c_atom.GetNeighbors()]) > 1:
            modifications.append("carboxyl group")

    if not modifications:
        return False, "No modifications found on ornithine backbone"
        
    return True, f"Ornithine derivative with modifications at: {', '.join(modifications)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25718',
                          'name': 'ornithine derivative',
                          'definition': 'A non-proteinogenic amino acid '
                                        'derivative resulting from reaction of '
                                        'ornithine at the amino group, the '
                                        'carboxy group, or the side-chain '
                                        'amino group, or from the replacement '
                                        'of any hydrogen of ornithine by a '
                                        'heteroatom. The definition normally '
                                        'excludes peptides containing '
                                        'ornithine residues.',
                          'parents': ['CHEBI:83812']},
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
    'num_false_positives': 100,
    'num_true_negatives': 62228,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9983635488528798}