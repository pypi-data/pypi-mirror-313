"""
Classifies: CHEBI:22307 aldoxime
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aldoxime(smiles: str):
    """
    Determines if a molecule is an aldoxime (RCH=NOH).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aldoxime, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Look for C=N-O pattern
    pattern = Chem.MolFromSmarts('[CH]=N[OH]')
    if not mol.HasSubstructMatch(pattern):
        return False, "Does not contain aldoxime group (CH=NOH)"
        
    # Find all aldoxime groups
    matches = mol.GetSubstructMatches(pattern)
    
    # Check each match
    aldoxime_carbons = []
    for match in matches:
        carbon = mol.GetAtomWithIdx(match[0])
        nitrogen = mol.GetAtomWithIdx(match[1])
        oxygen = mol.GetAtomWithIdx(match[2])
        
        # Verify carbon has one H and one other substituent
        if carbon.GetTotalNumHs() != 1:
            continue
            
        # Verify nitrogen has double bond to carbon
        if not any(b.GetBondType() == Chem.BondType.DOUBLE for b in carbon.GetBonds()):
            continue
            
        # Verify oxygen has one H
        if oxygen.GetTotalNumHs() != 1:
            continue
            
        aldoxime_carbons.append(carbon)
        
    if len(aldoxime_carbons) == 0:
        return False, "Does not contain valid aldoxime group"
        
    # Get substituents on aldoxime carbons
    substituents = []
    for carbon in aldoxime_carbons:
        for neighbor in carbon.GetNeighbors():
            if neighbor.GetSymbol() != 'N':  # Skip the nitrogen of C=N
                substituents.append(neighbor.GetSymbol())
                
    return True, f"Contains aldoxime group(s) with substituents: {', '.join(set(substituents))}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22307',
                          'name': 'aldoxime',
                          'definition': 'Oximes of aldehydes RCH=NOH.',
                          'parents': ['CHEBI:25750']},
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
    'num_true_positives': 6,
    'num_false_positives': 37,
    'num_true_negatives': 183834,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.13953488372093023,
    'recall': 1.0,
    'f1': 0.24489795918367346,
    'accuracy': 0.9997987785313008}