"""
Classifies: CHEBI:25750 oxime
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_oxime(smiles: str):
    """
    Determines if a molecule contains an oxime group (R2C=NOH).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains an oxime group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for oxime group: C=NOH
    # Note: This will match both aldoximes (RC(H)=NOH) and ketoximes (R2C=NOH)
    oxime_pattern = Chem.MolFromSmarts('[C;!$(C=[!N])]=[N]O[H]')
    
    if oxime_pattern is None:
        return None, "Invalid SMARTS pattern"
        
    matches = mol.GetSubstructMatches(oxime_pattern)
    
    if not matches:
        return False, "No oxime group found"
        
    # Analyze type of oxime
    oxime_types = []
    for match in matches:
        carbon_atom = mol.GetAtomWithIdx(match[0])
        # Count number of carbon neighbors to determine if aldoxime or ketoxime
        carbon_neighbors = sum(1 for neighbor in carbon_atom.GetNeighbors() 
                             if neighbor.GetSymbol() == 'C')
        
        if carbon_neighbors == 1:
            oxime_types.append("aldoxime")
        else:
            oxime_types.append("ketoxime")
    
    if len(matches) == 1:
        return True, f"Contains one {oxime_types[0]} group"
    else:
        type_counts = {}
        for t in oxime_types:
            type_counts[t] = type_counts.get(t, 0) + 1
            
        type_str = ", ".join(f"{count} {t}" for t, count in type_counts.items())
        return True, f"Contains multiple oxime groups ({type_str})"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25750',
                          'name': 'oxime',
                          'definition': 'Compounds of structure R2C=NOH '
                                        'derived from condensation of '
                                        'aldehydes or ketones with '
                                        'hydroxylamine. Oximes from aldehydes '
                                        'may be called aldoximes; those from '
                                        'ketones may be called ketoximes.',
                          'parents': ['CHEBI:50860', 'CHEBI:51143']},
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
    'num_true_negatives': 183819,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999401621062939}