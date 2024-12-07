"""
Classifies: CHEBI:26649 serine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_serine_derivative(smiles: str):
    """
    Determines if a molecule is a serine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a serine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Look for serine core structure:
    # NH2-CH(CH2OH)-COOH or NH2-CH(CH2O-)-COO-
    serine_pattern = Chem.MolFromSmarts('[NH2,NH3+][CH]([CH2][OH,O-,OX2])[CX3](=[OX1])[OH,O-,OX2]')
    if not mol.HasSubstructMatch(serine_pattern):
        return False, "Does not contain serine core structure"
        
    # Count number of serine cores
    matches = mol.GetSubstructMatches(serine_pattern)
    if len(matches) > 1:
        return False, "Contains multiple serine residues - likely a peptide"
        
    # Look for modifications at amino group, carboxy group or hydroxy group
    # Get the serine core atoms
    core_atoms = list(matches[0])
    
    # Check for modifications
    modifications = []
    
    # Check amino group modifications
    n_atom = mol.GetAtomWithIdx(core_atoms[0])
    if len(n_atom.GetNeighbors()) > 2:
        modifications.append("N-modified")
        
    # Check carboxy group modifications  
    c_atom = mol.GetAtomWithIdx(core_atoms[3])
    if len(c_atom.GetNeighbors()) > 2:
        modifications.append("C-modified")
        
    # Check hydroxy group modifications
    o_atom = mol.GetAtomWithIdx(core_atoms[2])
    if len(o_atom.GetNeighbors()) > 1:
        modifications.append("O-modified")
        
    if len(modifications) == 0:
        return False, "No modifications found on serine core"
        
    return True, f"Serine derivative with {', '.join(modifications)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26649',
                          'name': 'serine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of serine at the amino '
                                        'group or the carboxy group, or from '
                                        'the replacement of any hydrogen of '
                                        'serine by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing serine residues.',
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
    'num_true_positives': 65,
    'num_false_positives': 100,
    'num_true_negatives': 158304,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.3939393939393939,
    'recall': 0.9558823529411765,
    'f1': 0.5579399141630902,
    'accuracy': 0.9993500429097885}