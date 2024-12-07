"""
Classifies: CHEBI:24650 hydroxamic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_hydroxamic_acid(smiles: str):
    """
    Determines if a molecule contains a hydroxamic acid group (-C(=O)NHOH).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains hydroxamic acid group, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for hydroxamic acid group
    # [CX3](=O)[NX3H]([OX2H]) matches -C(=O)NHOH
    # Also match variations like -C(=O)N(OH)R where R is not H
    hydroxamic_pattern = Chem.MolFromSmarts('[CX3](=O)[NX3]([OX2H])')
    
    matches = mol.GetSubstructMatches(hydroxamic_pattern)
    
    if not matches:
        return False, "No hydroxamic acid group found"
        
    # Get number of hydroxamic acid groups
    num_groups = len(matches)
    
    # Analyze substituents on the carbon
    substituents = []
    for match in matches:
        carbon_idx = match[0]
        carbon = mol.GetAtomWithIdx(carbon_idx)
        
        for neighbor in carbon.GetNeighbors():
            if neighbor.GetIdx() not in match:
                if neighbor.GetSymbol() == 'C':
                    substituents.append('alkyl/aryl')
                else:
                    substituents.append(neighbor.GetSymbol())
                    
    substituents = list(set(substituents))
    
    if num_groups == 1:
        if substituents:
            return True, f"Contains one hydroxamic acid group with {', '.join(substituents)} substituent(s)"
        else:
            return True, "Contains one unsubstituted hydroxamic acid group"
    else:
        if substituents:
            return True, f"Contains {num_groups} hydroxamic acid groups with {', '.join(substituents)} substituent(s)"
        else:
            return True, f"Contains {num_groups} unsubstituted hydroxamic acid groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24650',
                          'name': 'hydroxamic acid',
                          'definition': 'A compound, RkE(=O)lNHOH, derived '
                                        'from an oxoacid RkE(=O)l(OH) (l =/= '
                                        '0) by replacing -OH with -NHOH, and '
                                        'derivatives thereof. Specific '
                                        'examples of hydroxamic acids are '
                                        'preferably named as N-hydroxy amides.',
                          'parents': ['CHEBI:37622']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 34589,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 0.8888888888888888,
    'f1': 0.13675213675213674,
    'accuracy': 0.9970891694045766}