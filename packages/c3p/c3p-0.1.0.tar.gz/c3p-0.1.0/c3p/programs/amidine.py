"""
Classifies: CHEBI:2634 amidine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_amidine(smiles: str):
    """
    Determines if a molecule contains an amidine group (R-C(=NR')-NR''R''').
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains amidine, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for amidine group: [C;!$(C=O)]=N[N,C]
    amidine_pattern = Chem.MolFromSmarts('[C;!$(C=O)]=N[N,C]')
    
    # Find matches
    matches = mol.GetSubstructMatches(amidine_pattern)
    
    if not matches:
        return False, "No amidine group found"
        
    # Validate each match
    valid_matches = []
    for match in matches:
        c_atom = mol.GetAtomWithIdx(match[0])
        n_atom = mol.GetAtomWithIdx(match[1])
        n_neighbor = mol.GetAtomWithIdx(match[2])
        
        # Check carbon has correct valence and is not part of other functional groups
        if c_atom.GetTotalValence() != 3:
            continue
            
        # Check nitrogen has correct valence
        if n_atom.GetTotalValence() != 2:
            continue
            
        # Check second nitrogen/carbon is bonded correctly
        if n_neighbor.GetTotalValence() < 1:
            continue
            
        valid_matches.append(match)
        
    if valid_matches:
        return True, f"Contains {len(valid_matches)} amidine group(s)"
    else:
        return False, "No valid amidine groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:2634',
                          'name': 'amidine',
                          'definition': 'Derivatives of oxoacids RnE(=O)OH in '
                                        'which the hydroxy group is replaced '
                                        'by an amino group and the oxo group '
                                        'is replaced by =NR. In organic '
                                        'chemistry an unspecified amidine is '
                                        'commonly a carboxamidine.',
                          'parents': ['CHEBI:51143']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183883,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999728095362395}