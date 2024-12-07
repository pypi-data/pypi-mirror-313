"""
Classifies: CHEBI:24397 glycophospholipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_glycophospholipid(smiles: str):
    """
    Determines if a molecule is a glycophospholipid based on presence of both
    phosphate and carbohydrate structural components.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycophospholipid, False otherwise
        str: Reason for classification
    """
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"
            
        # Check for phosphate group
        has_phosphate = False
        matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[P](=O)([O,OH])[O,OH]'))
        if len(matches) > 0:
            has_phosphate = True
            
        if not has_phosphate:
            return False, "No phosphate group found"
            
        # Check for carbohydrate components
        # Look for pyranose rings with multiple OH groups
        has_carb = False
        
        # Pattern for pyranose ring with multiple OH groups
        pyranose_pattern = Chem.MolFromSmarts('[C]1[C][C]([OH1,OH0])[C]([OH1,OH0])[C]([OH1,OH0])[C]1[OH1,OH0]')
        if mol.HasSubstructMatch(pyranose_pattern):
            has_carb = True
            
        # Alternative pattern for sugar rings
        sugar_pattern = Chem.MolFromSmarts('[C]1[O][C]([CH2][OH1,OH0])[C]([OH1,OH0])[C]([OH1,OH0])[C]1[OH1,OH0]')
        if mol.HasSubstructMatch(sugar_pattern):
            has_carb = True
            
        if not has_carb:
            return False, "No carbohydrate component found"
            
        # Count OH groups
        oh_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[OH1]')))
        
        # Additional checks for lipid characteristics
        carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
        
        if has_phosphate and has_carb and oh_count >= 3 and carbon_count > 10:
            return True, "Contains both phosphate and carbohydrate components with appropriate lipid characteristics"
            
        return False, "Missing required structural components"
        
    except Exception as e:
        return None, f"Error processing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24397',
                          'name': 'glycophospholipid',
                          'definition': 'Any phospholipid that contain both '
                                        'phosphate and carbohydrate as '
                                        'integral structural components.',
                          'parents': ['CHEBI:16247', 'CHEBI:33563']},
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
    'num_true_positives': 12,
    'num_false_positives': 100,
    'num_true_negatives': 16050,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.10714285714285714,
    'recall': 0.5714285714285714,
    'f1': 0.18045112781954886,
    'accuracy': 0.9932595386803538}