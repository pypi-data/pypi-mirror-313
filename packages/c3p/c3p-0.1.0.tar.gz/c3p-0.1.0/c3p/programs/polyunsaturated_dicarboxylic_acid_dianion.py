"""
Classifies: CHEBI:133492 polyunsaturated dicarboxylic acid dianion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_polyunsaturated_dicarboxylic_acid_dianion(smiles: str):
    """
    Determines if a molecule is a polyunsaturated dicarboxylic acid dianion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a polyunsaturated dicarboxylic acid dianion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of exactly 2 carboxylate groups (-COO-)
    carboxylate_pattern = Chem.MolFromSmarts('[C](=[O])[O-]')
    matches = mol.GetSubstructMatches(carboxylate_pattern)
    
    if len(matches) != 2:
        return False, f"Found {len(matches)} carboxylate groups, need exactly 2"

    # Count double bonds excluding those in carboxylate groups
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bond_matches = len(mol.GetSubstructMatches(double_bond_pattern))
    
    # Get total formal charge
    total_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    
    if total_charge != -2:
        return False, f"Total charge is {total_charge}, should be -2"
        
    # For polyunsaturated, need at least 2 units of unsaturation 
    # (double bonds or rings) excluding the carboxylate groups
    if double_bond_matches < 2:
        return False, f"Found only {double_bond_matches} C=C double bonds, need at least 2 for polyunsaturation"
        
    # If we get here, molecule meets all criteria
    return True, f"Contains 2 carboxylate groups, {double_bond_matches} C=C double bonds, and -2 total charge"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133492',
                          'name': 'polyunsaturated dicarboxylic acid dianion',
                          'definition': 'A dicarboxylic acid dianion having 2 '
                                        'or more units of unsaturation.',
                          'parents': ['CHEBI:28965']},
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
    'num_true_positives': 2,
    'num_false_positives': 88,
    'num_true_negatives': 183821,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.022222222222222223,
    'recall': 1.0,
    'f1': 0.04347826086956522,
    'accuracy': 0.9995215076857829}