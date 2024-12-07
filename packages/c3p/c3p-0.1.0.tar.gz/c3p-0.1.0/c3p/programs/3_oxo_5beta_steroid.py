"""
Classifies: CHEBI:1624 3-oxo-5beta-steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_3_oxo_5beta_steroid(smiles: str):
    """
    Determines if a molecule is a 3-oxo-5beta-steroid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 3-oxo-5beta-steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for steroid core (4 fused rings)
    rings = mol.GetRingInfo()
    if len(rings.AtomRings()) < 4:
        return False, "Does not contain steroid core (4 fused rings)"
        
    # Convert to 3D and generate conformer
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, randomSeed=42)
    AllChem.MMFFOptimizeMolecule(mol)
    
    # Find ketone at position 3
    pattern = Chem.MolFromSmarts('[#6]-C(=O)-[#6]')
    if not mol.HasSubstructMatch(pattern):
        return False, "No ketone group found"
        
    matches = mol.GetSubstructMatches(pattern)
    ketone_found = False
    for match in matches:
        # Check if ketone is at position 3
        if match[1] == 2: # 0-based indexing
            ketone_found = True
            break
            
    if not ketone_found:
        return False, "Ketone not at position 3"
        
    # Check beta configuration at position 5
    # Get coordinates of relevant atoms
    conf = mol.GetConformer()
    c5_idx = 4  # 0-based index for position 5
    c5_neighbors = [x.GetIdx() for x in mol.GetAtomWithIdx(c5_idx).GetNeighbors()]
    
    # Get 3D coordinates
    c5_pos = conf.GetAtomPosition(c5_idx)
    neighbor_positions = [conf.GetAtomPosition(n) for n in c5_neighbors]
    
    # Calculate improper dihedral angle to determine stereochemistry
    # Beta configuration should have a positive dihedral angle
    dihedral = AllChem.ComputeDihedralAngle(conf, c5_neighbors[0], c5_idx, c5_neighbors[1], c5_neighbors[2])
    
    if dihedral > 0:
        return True, "3-oxo steroid with beta configuration at position 5"
    else:
        return False, "Configuration at position 5 is not beta"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:1624',
                          'name': '3-oxo-5beta-steroid',
                          'definition': 'Any 3-oxo steroid that has beta- '
                                        'configuration at position 5.',
                          'parents': ['CHEBI:136889', 'CHEBI:47788']},
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
    'success': False,
    'best': True,
    'error': 'Bad Conformer Id',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}