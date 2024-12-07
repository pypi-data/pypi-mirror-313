"""
Classifies: CHEBI:22661 aspartic acid derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_aspartic_acid_derivative(smiles: str):
    """
    Determines if a molecule is an aspartic acid derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aspartic acid derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for basic carbon skeleton of aspartic acid
    # Looking for C-C-C with appropriate substitutions
    aspartic_pattern = Chem.MolFromSmarts('[#6]-[#6](-[#7,#15])-[#6]')
    if not mol.HasSubstructMatch(aspartic_pattern):
        return False, "Does not have basic aspartic acid carbon skeleton"
        
    # Check for two carboxylic acid groups (or derivatives)
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH,NH2,O-,N]')
    matches = mol.GetSubstructMatches(carboxyl_pattern)
    if len(matches) < 2:
        return False, "Does not have two carboxylic acid groups or derivatives"
        
    # Check for amino group or amino derivative
    amino_pattern = Chem.MolFromSmarts('[NH2,NH][#6,#15]')
    n_acyl_pattern = Chem.MolFromSmarts('[NH]C(=O)')
    
    if not (mol.HasSubstructMatch(amino_pattern) or mol.HasSubstructMatch(n_acyl_pattern)):
        return False, "Does not have amino group or derivative"
        
    # Check if it's a simple peptide (exclude these)
    peptide_pattern = Chem.MolFromSmarts('[NH]C(=O)[CH]([NH2,NH])C(=O)[NH]')
    if mol.HasSubstructMatch(peptide_pattern):
        return False, "Appears to be a peptide containing aspartic acid"
        
    # Additional checks for specific types of derivatives
    if mol.HasSubstructMatch(Chem.MolFromSmarts('[NH]C(=O)c1ccccc1')):
        return True, "N-acyl aspartic acid derivative"
    elif mol.HasSubstructMatch(Chem.MolFromSmarts('[CH]([NH2])[CH](O)')):
        return True, "Hydroxy-aspartic acid derivative"
    elif mol.HasSubstructMatch(Chem.MolFromSmarts('C(=O)[NH2]')):
        return True, "Aspartic acid amide derivative"
    elif mol.HasSubstructMatch(Chem.MolFromSmarts('[NH]C([*])=O')):
        return True, "N-substituted aspartic acid derivative"
    elif any(atom.GetIsotope() > 0 for atom in mol.GetAtoms()):
        return True, "Isotopically labeled aspartic acid derivative"
        
    return True, "Aspartic acid derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22661',
                          'name': 'aspartic acid derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of aspartic acid at the '
                                        'amino group or either of the carboxy '
                                        'groups, or from the replacement of '
                                        'any hydrogen of aspartic acid by a '
                                        'heteroatom. The definition normally '
                                        'excludes peptides containing aspartic '
                                        'acid residues.',
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
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 319,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.7652582159624414}