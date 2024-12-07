"""
Classifies: CHEBI:183509 branched-chain fatty acyl-CoA(4-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_branched_chain_fatty_acyl_CoA_4__(smiles: str):
    """
    Determines if a molecule is a branched-chain fatty acyl-CoA(4-).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a branched-chain fatty acyl-CoA(4-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for required substructures
    # CoA core structure
    coa_pattern = Chem.MolFromSmarts('[O-]P([O-])(=O)OCC1OC(n2cnc3c(N)ncnc32)C(O)C1OP([O-])([O-])=O')
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "Missing CoA core structure"

    # Check for 4 negative charges from phosphate groups
    negative_charge_pattern = Chem.MolFromSmarts('[O-]')
    negative_charges = len(mol.GetSubstructMatches(negative_charge_pattern))
    if negative_charges != 4:
        return False, f"Incorrect number of negative charges: {negative_charges} (should be 4)"

    # Check for thioester linkage
    thioester_pattern = Chem.MolFromSmarts('SC(=O)')
    if not mol.HasSubstructMatch(thioester_pattern):
        return False, "Missing thioester linkage"

    # Check for branched chain
    # Look for branching carbons in the fatty acid portion
    branched_carbon_pattern = Chem.MolFromSmarts('[CH1,CH0](-[CH3,CH2])(-[CH3,CH2])(-[!O;!N;!S])')
    if not mol.HasSubstructMatch(branched_carbon_pattern):
        return False, "No branched carbon found in fatty acid chain"

    # Additional checks for fatty acid chain
    fatty_chain_pattern = Chem.MolFromSmarts('C(=O)SCCNC(=O)CCNC(=O)')
    if not mol.HasSubstructMatch(fatty_chain_pattern):
        return False, "Missing characteristic fatty acid-CoA linkage"

    return True, "Molecule contains branched fatty acid chain, CoA structure, and 4 negative charges"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:183509',
                          'name': 'branched-chain fatty acyl-CoA(4-)',
                          'definition': 'A fatty acyl-CoA(4-) arising from '
                                        'deprotonation of the phosphate and '
                                        'diphosphate OH groups of any '
                                        'branched-chain fatty acyl-CoA; major '
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:77636']},
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
    'num_true_negatives': 183875,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999673702013803}