"""
Classifies: CHEBI:25401 monomethoxyflavone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_monomethoxyflavone(smiles: str):
    """
    Determines if a molecule is a monomethoxyflavone (flavone with exactly one methoxy substituent).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a monomethoxyflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for flavone core structure
    flavone_pattern = Chem.MolFromSmarts('[#6]1=[#6]-c2c([#6](=[O])[#6]1)c(=[#6])c([#6,#8,#1])c([#6,#8,#1])c2')
    if not mol.HasSubstructMatch(flavone_pattern):
        return False, "Not a flavone structure"

    # Count methoxy groups
    methoxy_pattern = Chem.MolFromSmarts('CO')
    methoxy_matches = mol.GetSubstructMatches(methoxy_pattern)
    
    if len(methoxy_matches) == 0:
        return False, "No methoxy groups found"
    elif len(methoxy_matches) > 1:
        return False, f"Contains {len(methoxy_matches)} methoxy groups - more than one"
    
    # Verify the methoxy is attached to the flavone core
    flavone_atoms = set([atom_idx for match in mol.GetSubstructMatches(flavone_pattern) for atom_idx in match])
    methoxy_o = methoxy_matches[0][0]
    methoxy_c = methoxy_matches[0][1]
    
    # Get the atom the methoxy oxygen is bonded to (besides the methyl carbon)
    o_atom = mol.GetAtomWithIdx(methoxy_o)
    connected_atoms = [neighbor.GetIdx() for neighbor in o_atom.GetNeighbors() if neighbor.GetIdx() != methoxy_c]
    
    if not any(atom_idx in flavone_atoms for atom_idx in connected_atoms):
        return False, "Methoxy group not attached to flavone core"

    return True, "Valid monomethoxyflavone structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25401',
                          'name': 'monomethoxyflavone',
                          'definition': 'Any methoxyflavone with a single '
                                        'methoxy substituent.',
                          'parents': ['CHEBI:25241']},
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
    'num_true_negatives': 183849,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.999956487922679}