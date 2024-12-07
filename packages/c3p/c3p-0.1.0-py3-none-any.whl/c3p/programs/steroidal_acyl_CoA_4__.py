"""
Classifies: CHEBI:131622 steroidal acyl-CoA(4-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_steroidal_acyl_CoA_4__(smiles: str):
    """
    Determines if a molecule is a steroidal acyl-CoA(4-).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a steroidal acyl-CoA(4-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of CoA core structure
    coa_substructure = "[O-]P([O-])(=O)OP([O-])(=O)OCC(C)(C)[C@H](O)C(=O)NCCC(=O)NCCSC(=O)"
    if not mol.HasSubstructMatch(Chem.MolFromSmarts(coa_substructure)):
        return False, "Missing CoA core structure"

    # Check for 4 negative charges from phosphate groups
    charge = sum([atom.GetFormalCharge() for atom in mol.GetAtoms()])
    if charge != -4:
        return False, f"Total charge is {charge}, not -4"

    # Check for steroid core (four fused rings - three 6-membered and one 5-membered)
    steroid_core = "C1CC2CCC3C4CCCC3C4CCC2C1"
    if not mol.HasSubstructMatch(Chem.MolFromSmarts(steroid_core)):
        return False, "Missing steroid core structure"

    # Check if steroid is connected to CoA via acyl group
    acyl_connection = "C(=O)SCCNC"
    if not mol.HasSubstructMatch(Chem.MolFromSmarts(acyl_connection)):
        return False, "Steroid not connected to CoA via acyl group"

    # Count number of rings
    ring_info = mol.GetRingInfo()
    if len(ring_info.AtomRings()) < 5:  # 4 steroid rings + adenine ring
        return False, "Insufficient number of rings"

    # Additional checks could be added for specific steroid modifications
    
    return True, "Contains steroidal core, CoA group with -4 charge, and correct connectivity"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131622',
                          'name': 'steroidal acyl-CoA(4-)',
                          'definition': 'An acyl-CoA(4-) arising from '
                                        'deprotonation of the phosphate and '
                                        'diphosphate OH groups of any '
                                        'steroidal acyl-CoA; major species at '
                                        'pH 7.3.',
                          'parents': ['CHEBI:58342']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183883,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999728095362395}