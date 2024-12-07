"""
Classifies: CHEBI:25051 lipid As
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_lipid_As(smiles: str):
    """
    Determines if a molecule is a Lipid A based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a Lipid A, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of glucosamine core
    glucosamine_pattern = Chem.MolFromSmarts('[CH2]-[CH](-[OH])-[CH](-[NH2])-[CH](-[OH])-[CH](-[OH])-[CH2]-[OH]')
    if not mol.HasSubstructMatch(glucosamine_pattern):
        return False, "Missing glucosamine core structure"

    # Check for phosphate groups
    phosphate_pattern = Chem.MolFromSmarts('P(=O)([OH])([OH])')
    if len(mol.GetSubstructMatches(phosphate_pattern)) < 1:
        return False, "Missing phosphate groups"

    # Check for acyl chains
    acyl_pattern = Chem.MolFromSmarts('C(=O)-O')
    acyl_matches = len(mol.GetSubstructMatches(acyl_pattern))
    if acyl_matches < 4:
        return False, "Insufficient acyl chains (minimum 4 required)"

    # Check for beta-hydroxy acyl chains
    beta_hydroxy_pattern = Chem.MolFromSmarts('O=C-C-C(-[OH])')
    beta_hydroxy_matches = len(mol.GetSubstructMatches(beta_hydroxy_pattern))
    if beta_hydroxy_matches < 2:
        return False, "Insufficient beta-hydroxy acyl chains"

    # Check for long carbon chains (10-16 carbons)
    long_chain_pattern = Chem.MolFromSmarts('CCCCCCCCCC')
    if len(mol.GetSubstructMatches(long_chain_pattern)) < 4:
        return False, "Missing long carbon chains"

    # Calculate molecular weight to ensure it's in reasonable range for Lipid A
    mol_weight = Descriptors.ExactMolWt(mol)
    if mol_weight < 1000 or mol_weight > 5000:
        return False, f"Molecular weight {mol_weight:.1f} outside typical range for Lipid A"

    return True, "Molecule contains characteristic Lipid A structural features: glucosamine core, phosphate groups, " \
                 f"multiple acyl chains ({acyl_matches} found), beta-hydroxy acyl chains ({beta_hydroxy_matches} found), " \
                 "and long carbon chains"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25051',
                          'name': 'lipid As',
                          'definition': 'Glycophospholipids that are the '
                                        'components of endotoxins held '
                                        'responsible for the toxicity of '
                                        'Gram-negative bacteria. Lipid A is '
                                        'the innermost of the three regions of '
                                        'the lipopolysaccharide (LPS) '
                                        'molecule, and its hydrophobic nature '
                                        'allows it to anchor the LPS to the '
                                        'outer membrane.  Four acyl chains '
                                        'attached directly to two '
                                        '(1->6)-linked glucosamine sugars are '
                                        'beta-hydroxy acyl chains usually '
                                        'between 10 and 16 carbons in length. '
                                        'Two additional acyl chains are often '
                                        'attached to the beta-hydroxy group.',
                          'parents': [   'CHEBI:166828',
                                         'CHEBI:24397',
                                         'CHEBI:35371']},
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
    'num_true_negatives': 183881,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999728092405077}