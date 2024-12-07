"""
Classifies: CHEBI:25248 methyl ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_methyl_ester(smiles: str):
    """
    Determines if a molecule contains a methyl ester group (-C(=O)OCH3).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains methyl ester, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # SMARTS pattern for methyl ester: -C(=O)OCH3
    methyl_ester_pattern = Chem.MolFromSmarts('C(=O)OC')
    
    if mol.HasSubstructMatch(methyl_ester_pattern):
        # Find all matches
        matches = mol.GetSubstructMatches(methyl_ester_pattern)
        
        # For each match, verify the carbon is only bonded to hydrogens
        for match in matches:
            o_atom = mol.GetAtomWithIdx(match[2]) # Get O atom
            c_atom = None
            # Find the carbon atom bonded to oxygen that's not the carbonyl carbon
            for neighbor in o_atom.GetNeighbors():
                if neighbor.GetIdx() != match[0]: # If not carbonyl carbon
                    c_atom = neighbor
                    break
                    
            if c_atom is not None:
                # Check if carbon is methyl (CH3)
                if c_atom.GetDegree() == 1 and c_atom.GetTotalNumHs() == 3:
                    return True, "Contains methyl ester group (-C(=O)OCH3)"
                    
    return False, "No methyl ester group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25248',
                          'name': 'methyl ester',
                          'definition': 'Any carboxylic ester resulting from '
                                        'the formal condensation of a carboxy '
                                        'group with methanol.',
                          'parents': ['CHEBI:33308']},
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
    'num_true_positives': 76,
    'num_false_positives': 100,
    'num_true_negatives': 3934,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.4318181818181818,
    'recall': 1.0,
    'f1': 0.6031746031746031,
    'accuracy': 0.975669099756691}