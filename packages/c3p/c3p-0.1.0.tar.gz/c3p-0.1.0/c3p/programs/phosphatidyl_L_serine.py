"""
Classifies: CHEBI:18303 phosphatidyl-L-serine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phosphatidyl_L_serine(smiles: str):
    """
    Determines if a molecule is a phosphatidyl-L-serine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phosphatidyl-L-serine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for key functional groups
    
    # Must have phosphate group
    phosphate_pattern = Chem.MolFromSmarts('[P](=O)([O-,OH])[O-,OH]')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "Missing phosphate group"
        
    # Must have serine moiety (NH2-CH-COOH)
    serine_pattern = Chem.MolFromSmarts('[NH2,NH3+][CH]C(=O)[O-,OH]')
    if not mol.HasSubstructMatch(serine_pattern):
        return False, "Missing serine moiety"
        
    # Must have glycerol backbone with two ester groups
    glycerol_pattern = Chem.MolFromSmarts('[CH2][CH][CH2]')
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "Missing glycerol backbone"
        
    ester_pattern = Chem.MolFromSmarts('C(=O)O')
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) < 2:
        return False, "Missing required ester groups"
        
    # Check connectivity - phosphate must be connected to both serine and glycerol
    phosphate_matches = mol.GetSubstructMatches(phosphate_pattern)
    serine_matches = mol.GetSubstructMatches(serine_pattern)
    glycerol_matches = mol.GetSubstructMatches(glycerol_pattern)
    
    if len(phosphate_matches) > 0 and len(serine_matches) > 0 and len(glycerol_matches) > 0:
        phosphate_atoms = set(phosphate_matches[0])
        serine_atoms = set(serine_matches[0]) 
        glycerol_atoms = set(glycerol_matches[0])
        
        # Check if phosphate is connected to both serine and glycerol
        for p_atom in phosphate_atoms:
            atom = mol.GetAtomWithIdx(p_atom)
            neighbors = [n.GetIdx() for n in atom.GetNeighbors()]
            if any(n in serine_atoms for n in neighbors) and any(n in glycerol_atoms for n in neighbors):
                return True, "Contains phosphatidyl-L-serine structure"
                
    return False, "Required connectivity between phosphate, serine and glycerol not found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18303',
                          'name': 'phosphatidyl-L-serine',
                          'definition': 'A class of aminophospholipids in '
                                        'which a phosphatidyl group is '
                                        'esterified to the hydroxy group of '
                                        'serine.',
                          'parents': [   'CHEBI:52565',
                                         'CHEBI:60971',
                                         'CHEBI:84135']},
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
    'num_true_negatives': 183546,
    'num_false_negatives': 44,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9997603355302577}