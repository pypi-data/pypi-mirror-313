"""
Classifies: CHEBI:13601 3-oxo-5alpha-steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_3_oxo_5alpha_steroid(smiles: str):
    """
    Determines if a molecule is a 3-oxo-5alpha-steroid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 3-oxo-5alpha-steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for steroid core (4 fused rings)
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[#6]~1~2~[#6]~[#6]~[#6]~3~[#6]~[#6]~[#6]~4~[#6]~[#6]~[#6]~[#6]~4~[#6]~3~[#6]~[#6]~2~[#6]~[#6]~1'))
    
    if not matches:
        return False, "No steroid core structure found"

    # Check for ketone at position 3
    ketone_pattern = Chem.MolFromSmarts('C1CC(=O)CC2')
    if not mol.HasSubstructMatch(ketone_pattern):
        return False, "No ketone group at position 3"

    # Check for alpha configuration at position 5
    # In steroid numbering, position 5 is at the junction of rings A and B
    # Alpha configuration means the hydrogen is pointing down (below the plane)
    
    # First find the position 5 carbon
    steroid_core = matches[0]
    pos5_idx = steroid_core[4]  # Position 5 in the steroid core
    
    # Get the atom and check its stereochemistry
    pos5_atom = mol.GetAtomWithIdx(pos5_idx)
    
    # For 5-alpha steroids, need to check if hydrogen is pointing down (alpha)
    # This can be done by checking if the chiral tag indicates the correct configuration
    chiral_tag = pos5_atom.GetChiralTag()
    
    if chiral_tag == Chem.ChiralType.CHI_UNSPECIFIED:
        return False, "Stereochemistry at position 5 is not specified"
        
    # Create 3D conformation to check stereochemistry
    try:
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
        
        # Get coordinates of relevant atoms
        conf = mol.GetConformer()
        pos5_coords = conf.GetAtomPosition(pos5_idx)
        
        # Check neighbors of pos5 atom to find the hydrogen
        for neighbor in pos5_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'H':
                h_coords = conf.GetAtomPosition(neighbor.GetIdx())
                # Check if H is below the plane (alpha configuration)
                if h_coords.z < pos5_coords.z:
                    return True, "Found 3-oxo-5alpha-steroid structure"
                    
        return False, "Position 5 hydrogen is not in alpha configuration"
        
    except:
        # If 3D embedding fails, fall back to checking just the presence of stereochemistry
        if mol.HasSubstructMatch(Chem.MolFromSmarts('[C@H]1CCC2')):
            return True, "Found 3-oxo-5alpha-steroid structure (based on 2D structure)"
        else:
            return False, "Position 5 hydrogen is not in alpha configuration (based on 2D structure)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13601',
                          'name': '3-oxo-5alpha-steroid',
                          'definition': 'A 3-oxo steroid that has alpha '
                                        'configuration at position 5.',
                          'parents': ['CHEBI:47788']},
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
    'num_true_negatives': 183871,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999673694915623}