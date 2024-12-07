"""
Classifies: CHEBI:20702 2-aminopurines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_aminopurines(smiles: str):
    """
    Determines if a molecule is a 2-aminopurine.
    A 2-aminopurine has an amino group (-NH2) at position 2 of the purine ring system.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 2-aminopurine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Generate purine SMARTS pattern - look for fused 5,6 ring system
    # with correct nitrogen positions and NH2 at position 2
    purine_pattern = Chem.MolFromSmarts('[nH]1cnc2c1ncnc2')
    amino_purine_pattern = Chem.MolFromSmarts('[nH]1cnc2c1nc(N)nc2')

    # Check if molecule contains purine core
    if not mol.HasSubstructMatch(purine_pattern):
        return False, "No purine core structure found"

    # Check if molecule contains amino group at position 2
    if not mol.HasSubstructMatch(amino_purine_pattern):
        return False, "No amino group at position 2 of purine"

    # Get matches
    matches = mol.GetSubstructMatches(amino_purine_pattern)
    
    # Check each match
    for match in matches:
        # Get the amino nitrogen atom
        amino_n_idx = match[7]  # Index of N in amino group based on SMARTS pattern
        amino_n = mol.GetAtomWithIdx(amino_n_idx)
        
        # Verify it's NH2 (has 2 hydrogens)
        if amino_n.GetTotalNumHs() == 2:
            substituents = []
            for atom_idx in match[:-1]:  # Exclude amino N from core atoms
                atom = mol.GetAtomWithIdx(atom_idx)
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetIdx() not in match:
                        substituents.append(neighbor.GetSymbol())
            
            if substituents:
                return True, f"2-aminopurine with substituents: {', '.join(set(substituents))}"
            else:
                return True, "Unsubstituted 2-aminopurine"

    return False, "No valid 2-aminopurine structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20702',
                          'name': '2-aminopurines',
                          'definition': 'Any aminopurine having the amino '
                                        'substituent at the 2-position.',
                          'parents': ['CHEBI:22527']},
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
    'num_false_positives': 6,
    'num_true_negatives': 183905,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999565011717497}