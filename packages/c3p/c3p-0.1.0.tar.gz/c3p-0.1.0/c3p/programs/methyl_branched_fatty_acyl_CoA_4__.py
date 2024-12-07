"""
Classifies: CHEBI:183508 methyl-branched fatty acyl-CoA(4-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprint
from rdkit.Chem import Descriptors

def is_methyl_branched_fatty_acyl_CoA_4__(smiles: str):
    """
    Determines if a molecule is a methyl-branched fatty acyl-CoA(4-).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a methyl-branched fatty acyl-CoA(4-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for required substructures
    coenzyme_a = Chem.MolFromSmarts('[O-]P([O-])(=O)OCC1OC(n2cnc3c(N)ncnc32)C(O)C1OP([O-])([O-])=O')
    phosphate = Chem.MolFromSmarts('OP([O-])([O-])=O')
    thioester = Chem.MolFromSmarts('SC(=O)')
    
    if not mol.HasSubstructMatch(coenzyme_a):
        return False, "Missing coenzyme A structure"
    
    if len(mol.GetSubstructMatches(phosphate)) < 3:
        return False, "Missing required phosphate groups"
        
    if not mol.HasSubstructMatch(thioester):
        return False, "Missing thioester linkage"

    # Check for methyl branching
    methyl_branch = Chem.MolFromSmarts('CC(C)')
    if not mol.HasSubstructMatch(methyl_branch):
        return False, "No methyl branching found"

    # Check for fatty acyl chain
    carbon_chain = Chem.MolFromSmarts('CCCCC')
    if not mol.HasSubstructMatch(carbon_chain):
        return False, "Missing fatty acyl chain"

    # Count formal charges to verify 4- charge state
    total_charge = sum([atom.GetFormalCharge() for atom in mol.GetAtoms()])
    if total_charge != -4:
        return False, f"Total charge is {total_charge}, not -4"

    return True, "Methyl-branched fatty acyl-CoA(4-) structure confirmed"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:183508',
                          'name': 'methyl-branched fatty acyl-CoA(4-)',
                          'definition': 'A branched-chain fatty acyl-CoA(4-) '
                                        'arising from deprotonation of the '
                                        'phosphate and diphosphate OH groups '
                                        'of any methyl-branched-chain fatty '
                                        'acyl-CoA; major species at pH 7.3.',
                          'parents': ['CHEBI:183509']},
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