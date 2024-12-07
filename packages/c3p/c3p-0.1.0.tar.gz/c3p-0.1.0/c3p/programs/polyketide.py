"""
Classifies: CHEBI:26188 polyketide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_polyketide(smiles: str):
    """
    Determines if a molecule is a polyketide based on structural patterns.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a polyketide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for alternating carbonyl and methylene groups
    carbonyl_pattern = Chem.MolFromSmarts('[#6](=[O])[#6][#6](=[O])')
    if carbonyl_pattern is not None and mol.HasSubstructMatch(carbonyl_pattern):
        has_alternating = True
    else:
        has_alternating = False
        
    # Check for presence of oxygen atoms (common in polyketides)
    num_oxygen = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if num_oxygen == 0:
        return False, "No oxygen atoms present"
        
    # Check for macrocyclic structure (common in polyketides)
    rings = mol.GetRingInfo()
    has_large_ring = False
    for ring in rings.AtomRings():
        if len(ring) >= 12:  # Typical macrocycle size
            has_large_ring = True
            break
            
    # Check for ketone groups
    ketone_pattern = Chem.MolFromSmarts('[#6](=[O])[#6]')
    if ketone_pattern is not None:
        num_ketones = len(mol.GetSubstructMatches(ketone_pattern))
    else:
        num_ketones = 0
    
    # Check for ester groups
    ester_pattern = Chem.MolFromSmarts('[#6](=[O])[O][#6]')
    if ester_pattern is not None:
        num_esters = len(mol.GetSubstructMatches(ester_pattern))
    else:
        num_esters = 0
    
    # Check for hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts('[O][H]')
    if hydroxyl_pattern is not None:
        num_hydroxyls = len(mol.GetSubstructMatches(hydroxyl_pattern))
    else:
        num_hydroxyls = 0
    
    # Combine evidence
    features = []
    if has_large_ring:
        features.append("macrocyclic structure")
    if has_alternating:
        features.append("alternating carbonyl-methylene groups")
    if num_ketones > 0:
        features.append(f"{num_ketones} ketone groups")
    if num_esters > 0:
        features.append(f"{num_esters} ester groups") 
    if num_hydroxyls > 0:
        features.append(f"{num_hydroxyls} hydroxyl groups")
    
    # Decision criteria
    if (has_alternating or (num_ketones >= 2 and num_hydroxyls >= 1)) and len(features) >= 2:
        return True, f"Polyketide structure containing {', '.join(features)}"
    
    return False, "Does not match polyketide structural patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26188',
                          'name': 'polyketide',
                          'definition': 'Natural and synthetic compounds '
                                        'containing alternating carbonyl and '
                                        'methylene groups '
                                        "('beta-polyketones'), biogenetically "
                                        'derived from repeated condensation of '
                                        'acetyl coenzyme A (via malonyl '
                                        'coenzyme A), and usually the '
                                        'compounds derived from them by '
                                        'further condensations, etc. '
                                        'Considered by many to be synonymous '
                                        'with the less frequently used terms '
                                        'acetogenins and ketides.',
                          'parents': ['CHEBI:36963']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.GetSubstructMatches(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool uniquify=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False, unsigned int maxMatches=1000)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
               'bool uniquify=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False, unsigned int maxMatches=1000)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 14,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.12280701754385964,
    'f1': 0.21875,
    'accuracy': 0.12280701754385964}