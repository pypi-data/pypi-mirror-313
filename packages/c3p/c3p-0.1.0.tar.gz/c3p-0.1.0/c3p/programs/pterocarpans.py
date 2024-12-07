"""
Classifies: CHEBI:26377 pterocarpans
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetSymmSSSR

def is_pterocarpans(smiles: str):
    """
    Determines if a molecule is a pterocarpan based on its SMILES string.
    
    Pterocarpans have a 6a,11a-dihydro-6H-[1]benzofuro[3,2-c]chromene core structure.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a pterocarpan, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define pterocarpan core SMARTS pattern
    # Matches the 6a,11a-dihydro-6H-[1]benzofuro[3,2-c]chromene skeleton
    pterocarpan_pattern = '[#6]1~[#6]~[#6]~[#6]2~[#6]~[#6]~[#6](~[#6]~1)~[#8]~[#6]1~[#6]~[#6]~[#6]~[#6]~[#6]2~[#8]~[#6]~1'
    
    # Create pattern molecule
    pattern = Chem.MolFromSmarts(pterocarpan_pattern)
    if pattern is None:
        return None, "Invalid SMARTS pattern"

    # Check if molecule contains the pterocarpan core
    if not mol.HasSubstructMatch(pattern):
        return False, "Does not contain pterocarpan core structure"

    # Check ring system
    rings = GetSymmSSSR(mol)
    if len(rings) < 3:
        return False, "Does not have required ring system"

    # Count oxygen atoms in core structure
    matches = mol.GetSubstructMatches(pattern)
    if not matches:
        return False, "Core structure not properly identified"
        
    # Verify the presence of two oxygen atoms in the core
    core_atoms = set(matches[0])
    oxygen_count = 0
    for atom_idx in core_atoms:
        if mol.GetAtomWithIdx(atom_idx).GetSymbol() == 'O':
            oxygen_count += 1
            
    if oxygen_count != 2:
        return False, "Does not have required two oxygen atoms in core"

    # Check for sp3 carbons at 6a and 11a positions
    match_atoms = matches[0]
    sp3_count = 0
    for atom_idx in match_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'C' and atom.GetHybridization() == Chem.HybridizationType.SP3:
            sp3_count += 1
            
    if sp3_count < 2:
        return False, "Missing required sp3 carbons at 6a,11a positions"

    return True, "Contains pterocarpan core structure with required features"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26377',
                          'name': 'pterocarpans',
                          'definition': 'Members of the class of '
                                        'benzofurochromene with a '
                                        '6a,11a-dihydro-6H-[1]benzofuro[3,2-c]chromene '
                                        'skeleton and its substituted '
                                        'derivatives. They generally bear '
                                        'structural resemblance to '
                                        'isoflavanoids that possess antibiotic '
                                        'activity and are produced by plant '
                                        'tissues in response to infection. '
                                        'They are the 3,4-dihydroderivatives '
                                        'of coumestans.',
                          'parents': ['CHEBI:38834', 'CHEBI:72544']},
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
    'num_true_negatives': 183829,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999456045779187}