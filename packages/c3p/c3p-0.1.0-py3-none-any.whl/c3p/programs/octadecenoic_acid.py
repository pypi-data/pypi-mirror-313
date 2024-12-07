"""
Classifies: CHEBI:25634 octadecenoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_octadecenoic_acid(smiles: str):
    """
    Determines if a molecule is an octadecenoic acid (C18 monounsaturated fatty acid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an octadecenoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Count carbon atoms
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 18:
        return False, f"Carbon count is {carbon_count}, should be 18"

    # Count double bonds using SMARTS pattern
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    matches = mol.GetSubstructMatches(double_bond_pattern)
    double_bond_count = len(matches)

    if double_bond_count != 1:
        return False, f"Number of double bonds is {double_bond_count}, should be 1"

    # Check if the double bond is in the aliphatic chain
    for match in matches:
        atoms = [mol.GetAtomWithIdx(i) for i in match]
        # Check if both carbons in the double bond are aliphatic
        if all(not atom.GetIsAromatic() for atom in atoms):
            # Find position of double bond by counting carbons from acid end
            acid_carbon = mol.GetSubstructMatch(carboxylic_acid_pattern)[0]
            path_to_double_bond = Chem.GetShortestPath(mol, acid_carbon, match[0])
            position = len(path_to_double_bond) - 1
            
            return True, f"C18 monounsaturated fatty acid with double bond at position {position}"

    return False, "Double bond not found in aliphatic chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25634',
                          'name': 'octadecenoic acid',
                          'definition': 'Any member of the group of C18 '
                                        'monounsaturated fatty acids with the '
                                        'double bond located at any position '
                                        'in the chain.',
                          'parents': [   'CHEBI:140948',
                                         'CHEBI:15904',
                                         'CHEBI:25413',
                                         'CHEBI:53339']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 48270,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9979326883320929}