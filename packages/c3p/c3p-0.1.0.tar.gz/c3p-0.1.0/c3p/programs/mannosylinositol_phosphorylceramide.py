"""
Classifies: CHEBI:25168 mannosylinositol phosphorylceramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_mannosylinositol_phosphorylceramide(smiles: str):
    """
    Determines if a molecule is a mannosylinositol phosphorylceramide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a mannosylinositol phosphorylceramide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for required elements
    elements = set([atom.GetSymbol() for atom in mol.GetAtoms()])
    required_elements = {'C', 'H', 'O', 'N', 'P'}
    if not required_elements.issubset(elements):
        return False, "Missing required elements (C, H, O, N, P)"
    
    # Check for phosphate group
    phos_pattern = Chem.MolFromSmarts('[P](=O)([O-,OH])([O-,OH])[O]')
    if not mol.HasSubstructMatch(phos_pattern):
        return False, "Missing phosphate group"
        
    # Check for ceramide core
    ceramide_pattern = Chem.MolFromSmarts('[CH2][CH]([OH])[CH]([NH][C](=O))[CH2]')
    if not mol.HasSubstructMatch(ceramide_pattern):
        return False, "Missing ceramide core structure"
        
    # Check for mannose
    mannose_pattern = Chem.MolFromSmarts('O[CH]1[CH](O)[CH](O)[CH](O)[CH](O)[CH]1O')
    if not mol.HasSubstructMatch(mannose_pattern):
        return False, "Missing mannose sugar"
        
    # Check for inositol
    inositol_pattern = Chem.MolFromSmarts('O[CH]1[CH](O)[CH](O)[CH](O)[CH](O)[CH]1O')
    if len(mol.GetSubstructMatches(inositol_pattern)) < 2: # Need at least 2 matches for both mannose and inositol
        return False, "Missing inositol group"
        
    # Check for long alkyl chains (ceramide tails)
    alkyl_pattern = Chem.MolFromSmarts('CCCCCCCC') # At least 8 carbons
    if len(mol.GetSubstructMatches(alkyl_pattern)) < 2:
        return False, "Missing required long alkyl chains"
        
    return True, "Contains mannosylinositol phosphorylceramide core structure with required functional groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25168',
                          'name': 'mannosylinositol phosphorylceramide',
                          'definition': 'A class of complex '
                                        'phosphoglycosphingolipids with a '
                                        'mannose-inositol-P head group. As '
                                        'with other ceramide derivatives, '
                                        'substituents R(1) and R(2) vary with '
                                        'different sphingoid bases and fatty '
                                        'acyl moieties.',
                          'parents': ['CHEBI:26057', 'CHEBI:60245']},
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
    'num_true_negatives': 183908,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999891251155456}