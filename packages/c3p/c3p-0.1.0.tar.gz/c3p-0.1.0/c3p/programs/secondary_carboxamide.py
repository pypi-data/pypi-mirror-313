"""
Classifies: CHEBI:140325 secondary carboxamide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_secondary_carboxamide(smiles: str):
    """
    Determines if a molecule contains a secondary carboxamide group (RC(=O)NHR(1)).
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if molecule contains secondary carboxamide, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # SMARTS pattern for secondary carboxamide: RC(=O)NHR
    # [CX3](=O)[NX3H1][#6] means:
    # [CX3] - carbon with 3 bonds
    # (=O) - double bonded to oxygen
    # [NX3H1] - nitrogen with 3 bonds and 1 hydrogen
    # [#6] - connected to any carbon
    pattern = Chem.MolFromSmarts('[CX3](=O)[NX3H1][#6]')
    
    # Find all matches
    matches = mol.GetSubstructMatches(pattern)
    
    if not matches:
        return False, "No secondary carboxamide group found"
        
    # Get atoms involved in the match
    matched_atoms = []
    for match in matches:
        c = mol.GetAtomWithIdx(match[0])
        o = mol.GetAtomWithIdx(match[1]) 
        n = mol.GetAtomWithIdx(match[2])
        r = mol.GetAtomWithIdx(match[3])
        matched_atoms.extend([c,o,n,r])
    
    return True, f"Contains secondary carboxamide group with {len(matches)} instances"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140325',
                          'name': 'secondary carboxamide',
                          'definition': 'A carboxamide resulting from the '
                                        'formal condensation of a carboxylic '
                                        'acid with a primary amine; formula '
                                        'RC(=O)NHR(1).',
                          'parents': ['CHEBI:37622']},
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
    'num_true_positives': 182,
    'num_false_positives': 100,
    'num_true_negatives': 181,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.6453900709219859,
    'recall': 0.994535519125683,
    'f1': 0.7827956989247313,
    'accuracy': 0.7823275862068966}