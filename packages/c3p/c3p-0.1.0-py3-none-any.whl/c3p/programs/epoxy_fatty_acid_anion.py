"""
Classifies: CHEBI:190711 epoxy fatty acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_epoxy_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is an epoxy fatty acid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an epoxy fatty acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylate anion group
    carboxylate_pattern = Chem.MolFromSmarts('C(=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion group found"

    # Check for epoxide ring
    epoxide_pattern = Chem.MolFromSmarts('C1OC1')
    if not mol.HasSubstructMatch(epoxide_pattern):
        return False, "No epoxide ring found"

    # Count carbons in main chain
    carbon_count = len([atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'C'])
    if carbon_count < 12:  # Minimum length for fatty acids
        return False, "Carbon chain too short for fatty acid"

    # Check for aliphatic nature (allowing unsaturation)
    aromatic_atoms = [atom for atom in mol.GetAtoms() if atom.GetIsAromatic()]
    if aromatic_atoms:
        return False, "Contains aromatic rings"

    # Additional checks for typical fatty acid features
    # Count unsaturations (double bonds)
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bond_count = len(mol.GetSubstructMatches(double_bond_pattern))
    
    # Count additional oxygen-containing groups (like hydroxy, hydroperoxy)
    oxygen_pattern = Chem.MolFromSmarts('[O]')
    oxygen_count = len(mol.GetSubstructMatches(oxygen_pattern))
    
    return True, f"Epoxy fatty acid anion with {double_bond_count} double bonds and {oxygen_count} oxygen-containing groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:190711',
                          'name': 'epoxy fatty acid anion',
                          'definition': 'An epoxy monocarboxylic acid anion '
                                        'resulting from the deprotonation of '
                                        'the carboxy group of any epoxy fatty '
                                        'acid.',
                          'parents': ['CHEBI:190712']},
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
    'num_true_positives': 3,
    'num_false_positives': 80,
    'num_true_negatives': 183818,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.03614457831325301,
    'recall': 1.0,
    'f1': 0.06976744186046512,
    'accuracy': 0.9995649833334239}