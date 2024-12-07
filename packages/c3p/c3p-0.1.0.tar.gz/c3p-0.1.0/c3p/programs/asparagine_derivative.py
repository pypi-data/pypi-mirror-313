"""
Classifies: CHEBI:22654 asparagine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Fragments import fr_Asn

def is_asparagine_derivative(smiles: str):
    """
    Determines if a molecule is an asparagine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an asparagine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for asparagine substructure
    asn_pattern = Chem.MolFromSmarts('NC(=O)CC(N)C(=O)O')
    if not mol.HasSubstructMatch(asn_pattern):
        return False, "No asparagine core structure found"
    
    # Get match atoms for asparagine pattern
    matches = mol.GetSubstructMatches(asn_pattern)
    
    for match in matches:
        # Get the relevant atoms from the match
        amide_n = mol.GetAtomWithIdx(match[0])  # Terminal amide N
        alpha_n = mol.GetAtomWithIdx(match[3])  # Alpha amino N
        carboxyl_c = mol.GetAtomWithIdx(match[5])  # Carboxyl C
        
        # Check for modifications at amino group
        if len(list(alpha_n.GetNeighbors())) > 2:
            return True, "Modified at alpha amino group"
            
        # Check for modifications at carboxyl group
        if len(list(carboxyl_c.GetNeighbors())) > 2:
            return True, "Modified at carboxyl group"
            
        # Check for modifications at carboxamide
        if len(list(amide_n.GetNeighbors())) > 2:
            return True, "Modified at carboxamide group"
            
    # Additional check for heteroatom substitutions
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in ['C', 'H', 'O', 'N']:
            return True, f"Contains heteroatom substitution ({atom.GetSymbol()})"
            
    # Check if it's just unmodified asparagine
    if fr_Asn(mol) == 1 and mol.GetNumAtoms() == 13:  # Asparagine has 13 atoms
        return False, "Unmodified asparagine"
        
    return True, "Asparagine derivative detected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22654',
                          'name': 'asparagine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of asparagine at the '
                                        'amino group, the carboxy group, or '
                                        'the carboxamide, or from the '
                                        'replacement of any hydrogen of '
                                        'asparagine by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing asparagine residues.',
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
    'success': False,
    'best': True,
    'error': "cannot import name 'fr_Asn' from 'rdkit.Chem.Fragments' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/Fragments.py)',
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