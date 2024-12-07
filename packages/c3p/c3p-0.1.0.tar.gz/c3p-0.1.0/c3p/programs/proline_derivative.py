"""
Classifies: CHEBI:26273 proline derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition

def is_proline_derivative(smiles: str):
    """
    Determines if a molecule is a proline derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a proline derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Check for proline core structure (5-membered N-containing ring)
    proline_core = Chem.MolFromSmarts('[NX3;R5]1[CH2][CH2][CH2][CH]1')
    if not mol.HasSubstructMatch(proline_core):
        return False, "No proline core structure found"
        
    # Check for carboxyl group
    carboxyl = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxyl):
        return False, "No carboxyl group found"
        
    # Get proline core atoms
    core_match = mol.GetSubstructMatch(proline_core)
    if not core_match:
        return False, "Could not map proline core atoms"
        
    # Check for modifications
    modifications = []
    
    # Check N-substitution
    n_atom = mol.GetAtomWithIdx(core_match[0])
    for neighbor in n_atom.GetNeighbors():
        if neighbor.GetIdx() not in core_match:
            modifications.append("N-substituted")
            break
            
    # Check for substitutions on carbons
    for i in range(1, len(core_match)):
        c_atom = mol.GetAtomWithIdx(core_match[i])
        for neighbor in c_atom.GetNeighbors():
            if neighbor.GetIdx() not in core_match:
                if neighbor.GetSymbol() != 'H':
                    modifications.append(f"C{i}-substituted")
                    break
                    
    # Check if it's a peptide
    peptide = Chem.MolFromSmarts('[NX3][CX3](=[OX1])[CX4]')
    if mol.HasSubstructMatch(peptide):
        # Count peptide bonds
        matches = mol.GetSubstructMatches(peptide)
        if len(matches) > 1:
            return False, "Appears to be a peptide containing proline"
            
    if modifications:
        return True, f"Proline derivative with modifications: {', '.join(set(modifications))}"
    else:
        return True, "Unmodified proline"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26273',
                          'name': 'proline derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of proline at the amino '
                                        'group or the carboxy group, or from '
                                        'the replacement of any hydrogen of '
                                        'proline by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing proline residues.',
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
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}