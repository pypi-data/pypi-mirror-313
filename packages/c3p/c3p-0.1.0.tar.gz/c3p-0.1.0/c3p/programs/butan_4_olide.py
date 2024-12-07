"""
Classifies: CHEBI:22950 butan-4-olide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_butan_4_olide(smiles: str):
    """
    Determines if a molecule contains a butan-4-olide (gamma-lactone) moiety.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains butan-4-olide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # SMARTS pattern for gamma-lactone (butan-4-olide) core
    # [#6]1[#6][#6][#8][#6](=O)1
    gamma_lactone_pattern = Chem.MolFromSmarts('[#6]1[#6][#6][#8][#6](=O)1')
    
    # Find matches
    matches = mol.GetSubstructMatches(gamma_lactone_pattern)
    
    if not matches:
        return False, "No butan-4-olide (gamma-lactone) moiety found"
        
    # For each match, verify it's a proper gamma-lactone
    for match in matches:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in match]
        
        # Check that we have a 5-membered ring
        if len(match) != 5:
            continue
            
        # Verify oxygen is sp3 and carbon is sp2 with double bond to oxygen
        oxygen_idx = match[3]  # The ring oxygen
        carbonyl_idx = match[4]  # The carbonyl carbon
        
        oxygen = mol.GetAtomWithIdx(oxygen_idx)
        carbonyl = mol.GetAtomWithIdx(carbonyl_idx)
        
        if oxygen.GetHybridization() != Chem.HybridizationType.SP3:
            continue
            
        if carbonyl.GetHybridization() != Chem.HybridizationType.SP2:
            continue
            
        # Check for carbonyl oxygen
        carbonyl_neighbors = [n for n in carbonyl.GetNeighbors() if n.GetSymbol() == 'O' and n.GetIdx() not in match]
        if not any(n.GetHybridization() == Chem.HybridizationType.SP2 for n in carbonyl_neighbors):
            continue
            
        return True, "Contains butan-4-olide (gamma-lactone) moiety"
        
    return False, "No valid butan-4-olide structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22950',
                          'name': 'butan-4-olide',
                          'definition': 'Any gamma-lactone having the lactone '
                                        'moiety derived from 4-hydroxybutanoic '
                                        'acid.',
                          'parents': ['CHEBI:37581', 'CHEBI:47016']},
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
    'num_true_negatives': 183838,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999510462504148}