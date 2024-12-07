"""
Classifies: CHEBI:25996 phenylhydrazines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phenylhydrazines(smiles: str):
    """
    Determines if a molecule is a phenylhydrazine (hydrazine with phenyl substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phenylhydrazine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define phenylhydrazine pattern - phenyl ring connected to N-N group
    phenylhydrazine_pattern = Chem.MolFromSmarts('c1ccccc1-[NX3;H2,H1,H0]-[NX3;H2,H1,H0]')
    
    # Find phenylhydrazine groups
    matches = mol.GetSubstructMatches(phenylhydrazine_pattern)
    
    if not matches:
        return False, "No phenylhydrazine group found"
        
    # Count number of phenylhydrazine groups
    num_matches = len(matches)
    
    # Get substituents on hydrazine nitrogens
    substituents = set()
    for match in matches:
        # The N atoms are at indices 6 and 7 in the pattern
        for n_idx in [match[6], match[7]]:
            n_atom = mol.GetAtomWithIdx(n_idx)
            for neighbor in n_atom.GetNeighbors():
                # Skip the N-N bond and phenyl connection
                if neighbor.GetIdx() not in [match[6], match[7]] + list(match[:6]):
                    substituents.add(neighbor.GetSymbol())
                    
    if substituents:
        return True, f"Found {num_matches} phenylhydrazine group(s) with substituents: {', '.join(substituents)}"
    else:
        return True, f"Found {num_matches} unsubstituted phenylhydrazine group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25996',
                          'name': 'phenylhydrazines',
                          'definition': 'Any member of the class of  '
                                        'hydrazines carrying a phenyl '
                                        'substituent.',
                          'parents': ['CHEBI:24631']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: No module named 'rdkit.Chem.rdDecomposition'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 176159,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 0.2,
    'f1': 0.018867924528301886,
    'accuracy': 0.9994099759451731}