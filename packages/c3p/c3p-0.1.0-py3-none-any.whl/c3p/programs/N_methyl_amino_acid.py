"""
Classifies: CHEBI:21760 N-methyl-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_N_methyl_amino_acid(smiles: str):
    """
    Determines if a molecule is an N-methyl amino acid derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-methyl amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for amino group
    amino_pattern = Chem.MolFromSmarts('[NX3;H2,H1;!$(NC=O)]')
    if not mol.HasSubstructMatch(amino_pattern):
        return False, "No primary/secondary amino group found"
        
    # Check for N-methyl group
    n_methyl_pattern = Chem.MolFromSmarts('[NX3;H1,H0]C')
    if not mol.HasSubstructMatch(n_methyl_pattern):
        return False, "No N-methyl group found"
        
    # Check that carbon alpha to carboxylic acid is also bonded to amino group
    alpha_amino_acid_pattern = Chem.MolFromSmarts('[NX3][CX4][CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(alpha_amino_acid_pattern):
        return False, "Not an alpha amino acid structure"
        
    # Find all N-methyl groups
    n_methyl_matches = mol.GetSubstructMatches(n_methyl_pattern)
    n_methyl_count = len(n_methyl_matches)
    
    # Find positions of N-methylation
    positions = []
    for match in n_methyl_matches:
        n_atom = mol.GetAtomWithIdx(match[0])
        # Count number of carbons bonded to nitrogen
        c_neighbors = sum(1 for neighbor in n_atom.GetNeighbors() if neighbor.GetSymbol() == 'C')
        if c_neighbors == 1:  # Only count if single methyl group
            positions.append(str(match[0]))
            
    if positions:
        return True, f"N-methyl amino acid with methylation at position(s): {','.join(positions)}"
    else:
        return False, "No valid N-methyl groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21760',
                          'name': 'N-methyl-amino acid',
                          'definition': 'An amino acid derivative in which at '
                                        'least one of the hydrogens of the '
                                        'amino group has been replaced by a '
                                        'methyl group.',
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
    'num_true_positives': 0,
    'num_false_positives': 100,
    'num_true_negatives': 78976,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9987101342977819}