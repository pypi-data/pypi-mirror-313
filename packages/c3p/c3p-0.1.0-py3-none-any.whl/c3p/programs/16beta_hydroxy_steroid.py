"""
Classifies: CHEBI:17354 16beta-hydroxy steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import Compute2DCoords

def is_16beta_hydroxy_steroid(smiles: str):
    """
    Determines if a molecule is a 16beta-hydroxy steroid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 16beta-hydroxy steroid, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for steroid core
    steroid_pattern = Chem.MolFromSmarts("[#6]~1~[#6]~[#6]~[#6]~2~[#6]~[#6]~[#6]~3~[#6]~[#6]~[#6]~4~[#6]~[#6]~[#6]~[#6]~[#6]~4~[#6]~[#6]~3~[#6]~[#6]~2~[#6]~1")
    if not mol.HasSubstructMatch(steroid_pattern):
        return False, "No steroid core found"
        
    # Check for OH group at position 16
    oh_pattern = Chem.MolFromSmarts("[C;H1]16-[OH]")
    if not mol.HasSubstructMatch(oh_pattern):
        return False, "No hydroxyl group at position 16"
        
    # Generate 3D coordinates if not present
    if mol.GetNumConformers() == 0:
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
        
    # Get the atoms involved in the 16-OH bond
    matches = mol.GetSubstructMatches(oh_pattern)
    if not matches:
        return False, "Could not find 16-OH bond"
        
    c16_idx = matches[0][0]
    oh_idx = matches[0][1]
    
    # Get neighboring atoms to check configuration
    neighbors = [n.GetIdx() for n in mol.GetAtomWithIdx(c16_idx).GetNeighbors()]
    neighbors.remove(oh_idx)
    
    # Check beta configuration by examining dihedral angles
    conf = mol.GetConformer()
    dihedral = Chem.rdMolTransforms.GetDihedralDeg(conf, neighbors[0], c16_idx, oh_idx, neighbors[1])
    
    # Beta configuration should have dihedral angle around -60 degrees
    if -120 < dihedral < 0:
        return True, "16beta-hydroxy steroid found"
    else:
        return False, "Hydroxyl group at position 16 is not in beta configuration"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17354',
                          'name': '16beta-hydroxy steroid',
                          'definition': 'A 16-hydroxy steroid in which the '
                                        'hydroxy group at position 16 has a '
                                        'beta-configuration.',
                          'parents': ['CHEBI:36840']},
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
    'num_true_negatives': 183905,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999836874959219}