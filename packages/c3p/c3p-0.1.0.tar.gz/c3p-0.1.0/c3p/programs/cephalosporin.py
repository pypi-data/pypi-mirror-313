"""
Classifies: CHEBI:23066 cephalosporin
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cephalosporin(smiles: str):
    """
    Determines if a molecule is a cephalosporin based on its core structure.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cephalosporin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define cephalosporin core SMARTS pattern
    # Core structure is a beta-lactam (4-membered ring) fused to a 6-membered thiazine ring
    ceph_core = Chem.MolFromSmarts('[#6]1[#6][#16][#6][#6]2[#7]1[#6](=O)[#6]2')
    
    if mol.HasSubstructMatch(ceph_core):
        # Check for required carboxylic acid group
        carboxyl = Chem.MolFromSmarts('C(=O)[OH]')
        if not mol.HasSubstructMatch(carboxyl):
            return False, "Missing carboxylic acid group characteristic of cephalosporins"
            
        # Check for characteristic beta-lactam carbonyl
        beta_lactam = Chem.MolFromSmarts('N1C(=O)C2')
        if not mol.HasSubstructMatch(beta_lactam):
            return False, "Missing beta-lactam carbonyl group"
            
        # Additional validation - check for 6-membered thiazine ring
        thiazine = Chem.MolFromSmarts('[#6]1[#6][#16][#6][#6][#7]1')
        if not mol.HasSubstructMatch(thiazine):
            return False, "Missing characteristic 6-membered thiazine ring"
            
        return True, "Contains cephalosporin core structure with required functional groups"
        
    return False, "Does not contain cephalosporin core structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23066',
                          'name': 'cephalosporin',
                          'definition': 'A class of beta-lactam antibiotics '
                                        'differing from the penicillins in '
                                        'having a 6-membered, rather than a '
                                        '5-membered, side ring.  Although '
                                        'cephalosporins are among the most '
                                        'commonly used antibiotics in the '
                                        'treatment of routine infections, and '
                                        'their use is increasing over time, '
                                        'they can cause a range of '
                                        'hypersensitivity reactions, from '
                                        'mild, delayed-onset cutaneous '
                                        'reactions to life-threatening '
                                        'anaphylaxis in patients with '
                                        'immunoglobulin E (IgE)-mediated '
                                        'allergy.',
                          'parents': ['CHEBI:38311']},
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
    'num_true_negatives': 183825,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999401640592702}