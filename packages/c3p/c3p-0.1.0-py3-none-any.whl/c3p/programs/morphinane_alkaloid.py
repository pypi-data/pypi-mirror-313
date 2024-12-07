"""
Classifies: CHEBI:25418 morphinane alkaloid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdMolDescriptors

def is_morphinane_alkaloid(smiles: str):
    """
    Determines if a molecule is a morphinane alkaloid based on the morphinan skeleton.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a morphinane alkaloid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Key structural features of morphinane alkaloids:
    # 1. Must contain nitrogen (N)
    # 2. Must have 4 or 5 rings total
    # 3. Must have specific ring systems characteristic of morphinan skeleton
    
    # Check for nitrogen
    if not any(atom.GetSymbol() == 'N' for atom in mol.GetAtoms()):
        return False, "No nitrogen atom found"

    # Count rings
    ring_count = rdMolDescriptors.CalcNumRings(mol)
    if ring_count < 4 or ring_count > 5:
        return False, f"Incorrect number of rings ({ring_count}). Expected 4-5 rings."

    # Check for characteristic ring systems using SMARTS patterns
    # Morphinan core structure patterns
    morphinan_patterns = [
        # Basic morphinan skeleton with N-containing ring
        "[#6]1[#6][#6][#7][#6][#6]2[#6][#6][#6][#6][#6]3[#6][#6][#6][#6][#6]123",
        # Alternative pattern with oxygen bridge
        "[#6]1[#6][#6][#7][#6][#6]2[#6][#6]3[#6][#6][#6][#6][#8][#6]2[#6]13"
    ]

    matches_core = False
    for pattern in morphinan_patterns:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            matches_core = True
            break
            
    if not matches_core:
        return False, "Does not match morphinan core structure"

    # Additional checks for typical substituents
    common_substituents = []
    
    # Check for hydroxyl groups
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[#8H1]")):
        common_substituents.append("hydroxyl")
        
    # Check for methoxy groups
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[#6][#8][#6]")):
        common_substituents.append("methoxy")
        
    # Check for carbonyl groups
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[#6]=O")):
        common_substituents.append("carbonyl")

    substituents_str = ", ".join(common_substituents) if common_substituents else "no common"
    
    return True, f"Matches morphinan core structure with {substituents_str} substituents"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25418',
                          'name': 'morphinane alkaloid',
                          'definition': 'An  isoquinoline alkaloid based on a '
                                        'morphinan skeleton and its '
                                        'substituted derivatives.',
                          'parents': ['CHEBI:24921']},
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
    'num_true_negatives': 183851,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999564883959992}