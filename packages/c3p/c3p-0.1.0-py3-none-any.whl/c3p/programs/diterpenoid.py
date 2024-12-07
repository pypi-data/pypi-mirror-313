"""
Classifies: CHEBI:23849 diterpenoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_diterpenoid(smiles: str):
    """
    Determines if a molecule is a diterpenoid based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a diterpenoid, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check carbon count - diterpenoids have C20 skeleton base
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 18 or carbon_count > 22: # Allow some variation from C20
        return False, f"Carbon count {carbon_count} outside typical diterpenoid range (18-22)"

    # Check for cyclic structure
    ring_info = mol.GetRingInfo()
    if not ring_info.NumRings():
        return False, "No ring structures found"

    # Check for methyl groups
    methyl_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('C[CH3]')))
    if methyl_count < 2:
        return False, "Too few methyl groups"

    # Calculate number of sp2 carbons (for unsaturation)
    sp2_carbons = len([atom for atom in mol.GetAtoms() if 
                      atom.GetSymbol() == 'C' and 
                      atom.GetHybridization() == Chem.HybridizationType.SP2])
    
    # Calculate number of oxygen atoms (for oxidation)
    oxygen_count = len([atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'O'])

    # Typical diterpenoid characteristics found
    reasons = []
    if sp2_carbons > 0:
        reasons.append(f"Contains {sp2_carbons} unsaturated carbons")
    if oxygen_count > 0:
        reasons.append(f"Contains {oxygen_count} oxygen atoms")
    reasons.append(f"Contains {methyl_count} methyl groups")
    reasons.append(f"Contains {ring_info.NumRings()} rings")
    reasons.append(f"Contains {carbon_count} carbons")

    return True, "; ".join(reasons)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23849',
                          'name': 'diterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'diterpene. The term includes '
                                        'compounds in which the C20 skeleton '
                                        'of the parent diterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups).',
                          'parents': ['CHEBI:26873']},
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
    'num_true_positives': 57,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.3630573248407643,
    'f1': 0.5327102803738317,
    'accuracy': 0.3630573248407643}