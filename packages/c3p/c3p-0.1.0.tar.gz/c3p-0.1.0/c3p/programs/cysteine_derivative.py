"""
Classifies: CHEBI:23509 cysteine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cysteine_derivative(smiles: str):
    """
    Determines if a molecule is a cysteine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cysteine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of cysteine core structure (more flexible pattern)
    cysteine_core = Chem.MolFromSmarts("[NX3,NX4+][CX4H]([CH2][SX2,SX2H,SX3,SX4])C(=O)[OX1H,OX2H0,NX3]")
    if cysteine_core is None:
        return None, "Could not process cysteine core pattern"
        
    # Get cysteine matches
    matches = mol.GetSubstructMatches(cysteine_core)
    if not matches:
        return False, "No cysteine core structure found"
        
    # Check modifications at key positions
    modifications = []
    
    for match in matches:
        # Get atoms in match
        n_atom = mol.GetAtomWithIdx(match[0])  # N atom
        c_alpha = mol.GetAtomWithIdx(match[1])  # alpha C
        s_atom = mol.GetAtomWithIdx(match[3])   # S atom
        c_acid = mol.GetAtomWithIdx(match[4])   # acid C
        
        # Check N modifications
        n_neighbors = n_atom.GetNeighbors()
        non_h_n_neighbors = [n for n in n_neighbors if n.GetSymbol() != 'H']
        if len(non_h_n_neighbors) > 1:
            modifications.append("N-modified")
            
        # Check S modifications
        s_neighbors = s_atom.GetNeighbors()
        non_h_s_neighbors = [n for n in s_neighbors if n.GetSymbol() != 'H']
        if len(non_h_s_neighbors) > 1:
            modifications.append("S-modified")
            
        # Check COOH/amide modifications
        if c_acid.GetDegree() != 3:  # Should have 3 neighbors for -COOH or -CONH2
            modifications.append("C(O)-modified")
            
    if not modifications:
        return False, "Unmodified cysteine found"
        
    # Check if it's a peptide (more than one amino acid linkage)
    peptide_pattern = Chem.MolFromSmarts("[NX3][CX4H]([CH2,CH3])C(=O)[NX3]")
    if peptide_pattern:
        peptide_matches = len(mol.GetSubstructMatches(peptide_pattern))
        if peptide_matches > 1:
            return False, "Appears to be a peptide containing cysteine"
        
    modification_str = ", ".join(set(modifications))
    return True, f"Cysteine derivative with modifications: {modification_str}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23509',
                          'name': 'cysteine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of cysteine at the '
                                        'amino group, carboxy group, or thiol '
                                        'group, or from the replacement of any '
                                        'hydrogen of cysteine by a heteroatom. '
                                        'The definition normally excludes '
                                        'peptides containing cysteine '
                                        'residues.',
                          'parents': ['CHEBI:83821']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 34708,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 0.15384615384615385,
    'f1': 0.034782608695652174,
    'accuracy': 0.9968122684586888}