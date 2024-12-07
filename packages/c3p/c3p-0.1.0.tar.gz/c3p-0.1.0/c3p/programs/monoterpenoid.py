"""
Classifies: CHEBI:25409 monoterpenoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_monoterpenoid(smiles: str):
    """
    Determines if a molecule is a monoterpenoid based on having a C10 skeleton derived from monoterpenes,
    potentially modified by removal of methyl groups or other rearrangements.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a monoterpenoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count carbons
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    
    # Basic check for carbon count - monoterpenoids typically have 10 carbons 
    # but can have fewer due to loss of methyl groups
    if num_carbons > 12 or num_carbons < 7:
        return False, f"Carbon count ({num_carbons}) outside typical range for monoterpenoids (7-12)"

    # Check for common monoterpenoid structural features
    
    # Look for cyclic structures (many monoterpenoids are cyclic)
    rings = mol.GetRingInfo()
    has_rings = rings.NumRings() > 0
    
    # Calculate number of unsaturations
    num_unsaturations = rdMolDescriptors.CalcNumRotatableBonds(mol) + rings.NumRings()
    
    # Check for presence of oxygen (common in monoterpenoids)
    has_oxygen = any(atom.GetSymbol() == 'O' for atom in mol.GetAtoms())
    
    # Look for branching (characteristic of terpene structure)
    num_branches = len([atom for atom in mol.GetAtoms() if atom.GetDegree() > 2])
    
    # Combine evidence
    evidence = []
    if has_rings:
        evidence.append("contains rings")
    if num_unsaturations > 0:
        evidence.append(f"contains {num_unsaturations} unsaturations")
    if has_oxygen:
        evidence.append("contains oxygen")
    if num_branches > 0:
        evidence.append(f"contains {num_branches} branches")
        
    # Decision logic
    if num_carbons >= 7 and num_carbons <= 12 and (has_rings or num_unsaturations > 0):
        return True, f"Likely monoterpenoid: {', '.join(evidence)}"
    
    return False, "Does not match monoterpenoid structural patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25409',
                          'name': 'monoterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'monoterpene. The term includes '
                                        'compounds in which the C10 skeleton '
                                        'of the parent monoterpene has been '
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
    'num_false_positives': 100,
    'num_true_negatives': 617,
    'num_false_negatives': 61,
    'num_negatives': None,
    'precision': 0.3630573248407643,
    'recall': 0.4830508474576271,
    'f1': 0.41454545454545455,
    'accuracy': 0.807185628742515}