"""
Classifies: CHEBI:23007 carbohydrate-containing antibiotic
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_carbohydrate_containing_antibiotic(smiles: str):
    """
    Determines if a molecule is a carbohydrate-containing antibiotic.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a carbohydrate-containing antibiotic, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carbohydrate substructure patterns
    sugar_patterns = [
        # Pyranose ring with OH groups
        "[C]1[C@H]([OH])[C@H]([OH])[C@H]([OH])[C@H]([OH])O1",
        # Furanose ring with OH groups 
        "[C]1[C@H]([OH])[C@H]([OH])[C@H]([OH])O1",
        # Common aminosugar pattern
        "[C]1[C@H](N)[C@H]([OH])[C@H]([OH])[C@H]([OH])O1"
    ]

    has_sugar = False
    for pattern in sugar_patterns:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            has_sugar = True
            break

    if not has_sugar:
        return False, "No carbohydrate moiety detected"

    # Check for antibiotic structural features
    antibiotic_features = [
        # Aminoglycoside pattern
        "NC1CC(N)C(OC2OC(CO)C(O)C(O)C2O)C(O)C1",
        # Macrolide pattern
        "CC1OC(=O)CC(O)CC(O)CC(O)CC(O)C1",
        # Anthracycline pattern
        "O=C1c2c(O)c3C(=O)c4cccc(O)c4C(=O)c3c(O)c2CC1",
        # Common aminosugar-antibiotic linkage
        "OC1CC(N)C(O)C(O)C1OC"
    ]

    has_antibiotic_features = False
    for pattern in antibiotic_features:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            has_antibiotic_features = True
            break
            
    if not has_antibiotic_features:
        return False, "No characteristic antibiotic structural features detected"

    # Additional checks
    num_rings = rdMolDescriptors.CalcNumRings(mol)
    if num_rings < 2:
        return False, "Too few rings for a carbohydrate-containing antibiotic"

    molecular_weight = Descriptors.ExactMolWt(mol)
    if molecular_weight < 300:
        return False, "Molecular weight too low for a carbohydrate-containing antibiotic"

    # Check for minimum number of O and N atoms
    num_o = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    num_n = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    
    if num_o < 5 or num_n < 1:
        return False, "Insufficient O/N atoms for a carbohydrate-containing antibiotic"

    return True, "Contains both carbohydrate moiety and antibiotic structural features"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23007',
                          'name': 'carbohydrate-containing antibiotic',
                          'definition': 'Any carbohydrate derivative that '
                                        'exhibits antibiotic activity.',
                          'parents': ['CHEBI:63299']},
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
    'num_true_negatives': 183855,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999564893426084}