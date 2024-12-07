"""
Classifies: CHEBI:131863 docosanoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_docosanoid(smiles: str):
    """
    Determines if a molecule is a docosanoid (oxygenated derivative of C22 polyunsaturated fatty acids).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a docosanoid, False otherwise 
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check carbon count - should be 22
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 22:
        return False, f"Carbon count is {carbon_count}, should be 22"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"

    # Count double bonds
    double_bond_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('C=C')))
    if double_bond_count < 4:
        return False, f"Only {double_bond_count} double bonds found, should be at least 4"

    # Check for oxygenated derivatives (hydroxyl, hydroperoxy, oxo groups)
    hydroxyl_pattern = Chem.MolFromSmarts('[OH1]')
    hydroperoxy_pattern = Chem.MolFromSmarts('OO')
    oxo_pattern = Chem.MolFromSmarts('C(=O)C')
    
    hydroxyl_matches = len(mol.GetSubstructMatches(hydroxyl_pattern))
    hydroperoxy_matches = len(mol.GetSubstructMatches(hydroperoxy_pattern))
    oxo_matches = len(mol.GetSubstructMatches(oxo_pattern))
    
    total_oxy_groups = hydroxyl_matches + hydroperoxy_matches + oxo_matches
    
    if total_oxy_groups == 0:
        return False, "No oxygenated derivatives found"

    modifications = []
    if hydroxyl_matches > 0:
        modifications.append(f"{hydroxyl_matches} hydroxyl groups")
    if hydroperoxy_matches > 0:
        modifications.append(f"{hydroperoxy_matches} hydroperoxy groups")
    if oxo_matches > 0:
        modifications.append(f"{oxo_matches} oxo groups")

    return True, f"C22 polyunsaturated fatty acid with {double_bond_count} double bonds and {', '.join(modifications)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131863',
                          'name': 'docosanoid',
                          'definition': 'Any oxygenated derivative of C22 '
                                        'polyunsaturated fatty acids, such as '
                                        'docosapentaenoic acid (DPA) and '
                                        'docosahexaenoic acid (DHA).',
                          'parents': ['CHEBI:15904', 'CHEBI:26208']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.rdMolDescriptors' has no "
               "attribute 'CalcNumAliphaticDoubleBonds'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 9,
    'num_false_positives': 100,
    'num_true_negatives': 68582,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.08256880733944955,
    'recall': 0.9,
    'f1': 0.15126050420168066,
    'accuracy': 0.9985296686659291}