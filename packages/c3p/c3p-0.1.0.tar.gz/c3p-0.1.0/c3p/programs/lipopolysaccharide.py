"""
Classifies: CHEBI:16412 lipopolysaccharide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_lipopolysaccharide(smiles: str):
    """
    Determines if a molecule is a lipopolysaccharide based on structural features.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a lipopolysaccharide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for minimum size/complexity
    num_atoms = mol.GetNumAtoms()
    if num_atoms < 20:
        return False, "Too small to be a lipopolysaccharide"

    # Check for presence of sugar units (cyclic ethers)
    sugar_pattern = Chem.MolFromSmarts('[CR1]1[CR1][CR1][CR1][CR1]O1')
    if not mol.HasSubstructMatch(sugar_pattern):
        return False, "No sugar/saccharide units found"
    
    sugar_matches = len(mol.GetSubstructMatches(sugar_pattern))
    if sugar_matches < 1:
        return False, "Insufficient number of sugar units"

    # Check for hydroxy groups on sugars
    hydroxy_pattern = Chem.MolFromSmarts('[CR1]([CR1])O')
    if not mol.HasSubstructMatch(hydroxy_pattern):
        return False, "No hydroxy groups found on sugar units"

    # Check for fatty acid components
    fatty_acid = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(fatty_acid):
        return False, "No fatty acid components found"
    
    # Check for long alkyl chains
    alkyl_chain = Chem.MolFromSmarts('CCCCC')
    if not mol.HasSubstructMatch(alkyl_chain):
        return False, "No long alkyl chains found"

    # Check for glycosidic linkages
    glycosidic = Chem.MolFromSmarts('[CR1]O[CR1]')
    if not mol.HasSubstructMatch(glycosidic):
        return False, "No glycosidic linkages found"

    # If all criteria are met, classify as lipopolysaccharide
    reason = f"Contains {sugar_matches} sugar units with hydroxy groups, fatty acid components, and glycosidic linkages"
    return True, reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16412',
                          'name': 'lipopolysaccharide',
                          'definition': 'Liposaccharide natural compounds '
                                        'consisting of a trisaccharide '
                                        'repeating unit (two heptose units and '
                                        'octulosonic acid) with '
                                        'oligosaccharide side chains and '
                                        '3-hydroxytetradecanoic acid units '
                                        '(they are a major constituent of the '
                                        'cell walls of Gram-negative '
                                        'bacteria).',
                          'parents': ['CHEBI:35740', 'CHEBI:65212']},
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
    'num_true_negatives': 1630,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.10714285714285714,
    'recall': 1.0,
    'f1': 0.19354838709677416,
    'accuracy': 0.9425947187141217}