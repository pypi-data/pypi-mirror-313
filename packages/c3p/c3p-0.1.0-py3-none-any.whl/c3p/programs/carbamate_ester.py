"""
Classifies: CHEBI:23003 carbamate ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_carbamate_ester(smiles: str):
    """
    Determines if a molecule contains a carbamate ester group (R-O-C(=O)-N).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains carbamate ester, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for carbamate ester: R-O-C(=O)-N
    carbamate_pattern = Chem.MolFromSmarts('[#6,#1]-[O;X2]-[C;X3](=[O;X1])-[N;X3]')
    
    matches = mol.GetSubstructMatches(carbamate_pattern)
    
    if not matches:
        return False, "No carbamate ester group found"
        
    # Get details about the carbamate group(s)
    carbamate_details = []
    for match in matches:
        # Get the nitrogen atom
        n_atom = mol.GetAtomWithIdx(match[3])
        
        # Check substituents on nitrogen
        n_substituents = []
        for neighbor in n_atom.GetNeighbors():
            if neighbor.GetIdx() != match[2]:  # Skip the carbonyl carbon
                if neighbor.GetSymbol() == 'H':
                    n_substituents.append('H')
                else:
                    n_substituents.append('R')
                    
        if len(n_substituents) == 0:
            n_desc = "unsubstituted"
        elif len(n_substituents) == 1:
            n_desc = "mono-substituted"
        else:
            n_desc = "di-substituted"
            
        carbamate_details.append(f"{n_desc} nitrogen")
    
    details_str = ", ".join(set(carbamate_details))
    return True, f"Contains carbamate ester group(s) with {details_str}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23003',
                          'name': 'carbamate ester',
                          'definition': 'Any ester of carbamic acid or its '
                                        'N-substituted derivatives.',
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
    'num_true_positives': 28,
    'num_false_positives': 100,
    'num_true_negatives': 15614,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.21875,
    'recall': 0.9655172413793104,
    'f1': 0.35668789808917195,
    'accuracy': 0.993584450231849}