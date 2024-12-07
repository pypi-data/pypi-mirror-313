"""
Classifies: CHEBI:25985 phenylalanine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phenylalanine_derivative(smiles: str):
    """
    Determines if a molecule is a phenylalanine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phenylalanine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for phenyl ring
    phenyl_pattern = Chem.MolFromSmarts('c1ccccc1')
    if not mol.HasSubstructMatch(phenyl_pattern):
        return False, "No phenyl ring found"
        
    # Look for amino acid backbone
    amino_acid_pattern = Chem.MolFromSmarts('[NX3,NX4+][CX4H]([*])[CX3](=[OX1])[OX2H,OX1-,N]')
    if not mol.HasSubstructMatch(amino_acid_pattern):
        return False, "No amino acid backbone found"
        
    # Look for phenylalanine substructure - phenyl ring connected to amino acid via CH2
    phe_pattern = Chem.MolFromSmarts('[NX3,NX4+][CX4H](Cc1ccccc1)[CX3](=[OX1])[OX2H,OX1-,N]')
    if not mol.HasSubstructMatch(phe_pattern):
        return False, "Phenyl ring not properly connected to amino acid backbone"

    # Get number of peptide bonds
    peptide_pattern = Chem.MolFromSmarts('[NX3H][CX3](=[OX1])[#6]')
    peptide_matches = len(mol.GetSubstructMatches(peptide_pattern))
    
    # Check if it's a peptide (more than 1 peptide bond)
    if peptide_matches > 1:
        return False, "Appears to be a peptide"

    # Look for modifications
    modifications = []
    
    # Check for N-substitution
    n_sub_pattern = Chem.MolFromSmarts('[NX3,NX4+]([#6,#7,#8,#16])[CX4H](Cc1ccccc1)[CX3](=[OX1])[OX2H,OX1-,N]')
    if mol.HasSubstructMatch(n_sub_pattern):
        modifications.append("N-substituted")
        
    # Check for O-substitution on carboxyl
    o_sub_pattern = Chem.MolFromSmarts('[NX3,NX4+][CX4H](Cc1ccccc1)[CX3](=[OX1])[OX2][#6,#7,#8,#16]')
    if mol.HasSubstructMatch(o_sub_pattern):
        modifications.append("O-substituted")
        
    # Check for ring substitutions
    ring_sub_pattern = Chem.MolFromSmarts('c1c([#6,#7,#8,#9,#17,#35,#53])cccc1CC[CX4H]([NX3,NX4+])[CX3](=[OX1])[OX2H,OX1-,N]')
    if mol.HasSubstructMatch(ring_sub_pattern):
        modifications.append("ring-substituted")

    if len(modifications) > 0:
        return True, f"Phenylalanine derivative with modifications: {', '.join(modifications)}"
    else:
        return True, "Unmodified phenylalanine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25985',
                          'name': 'phenylalanine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of alanine at the amino '
                                        'group or the carboxy group, or from '
                                        'the replacement of any hydrogen of '
                                        'phenylalanine  by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing phenylalanine  residues.',
                          'parents': ['CHEBI:83821']},
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
    'num_true_positives': 28,
    'num_false_positives': 100,
    'num_true_negatives': 23346,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.21875,
    'recall': 0.7567567567567568,
    'f1': 0.33939393939393936,
    'accuracy': 0.9953583443341992}