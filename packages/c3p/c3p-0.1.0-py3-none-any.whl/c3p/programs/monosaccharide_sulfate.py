"""
Classifies: CHEBI:24589 monosaccharide sulfate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

def is_monosaccharide_sulfate(smiles: str):
    """
    Determines if a molecule is a monosaccharide sulfate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a monosaccharide sulfate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of sulfate group (SO4)
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('OS(=O)(=O)[O-,OH]'))
    if not matches:
        return False, "No sulfate group found"

    # Basic monosaccharide pattern - carbon chain with multiple OH groups
    # Look for carbon chain with 5-6 carbons and multiple OH groups
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    oxygen_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    
    if carbon_count < 5 or carbon_count > 6:
        return False, "Carbon count not consistent with monosaccharide (should be 5-6)"
    
    if oxygen_count < 5:
        return False, "Not enough oxygen atoms for monosaccharide"

    # Check for cyclic structure (pyranose or furanose form)
    ring_info = mol.GetRingInfo()
    if not ring_info.NumRings():
        # Check for open chain form
        aldehyde = mol.HasSubstructMatch(Chem.MolFromSmarts('[CH]=O'))
        ketone = mol.HasSubstructMatch(Chem.MolFromSmarts('C(=O)C'))
        if not (aldehyde or ketone):
            return False, "No ring structure and no aldehyde/ketone group found"
    
    # Check for multiple OH groups
    oh_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('O[H]')))
    if oh_count < 2:
        return False, "Not enough hydroxyl groups for monosaccharide"

    # If we've made it here, we likely have a monosaccharide sulfate
    sulfate_count = len(matches)
    return True, f"Monosaccharide with {sulfate_count} sulfate group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24589',
                          'name': 'monosaccharide sulfate',
                          'definition': 'Any carbohydrate sulfate that is a '
                                        'monosaccharide carrying at least one '
                                        'O-sulfo substituent.',
                          'parents': ['CHEBI:35724', 'CHEBI:63367']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183911,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891252929374}