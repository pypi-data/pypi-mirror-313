"""
Classifies: CHEBI:16219 cucurbitacin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cucurbitacin(smiles: str):
    """
    Determines if a molecule is a cucurbitacin based on structural features.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cucurbitacin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check molecular formula is in reasonable range for cucurbitacins
    num_c = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_o = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    
    if num_c < 25 or num_c > 40:
        return False, "Carbon count outside typical range for cucurbitacins (25-40)"
        
    if num_o < 4:
        return False, "Too few oxygen atoms for cucurbitacin structure"

    # Check for tetracyclic core structure
    rings = mol.GetRingInfo()
    if len(rings.AtomRings()) < 4:
        return False, "Missing tetracyclic core structure"

    # Count 6-membered rings
    six_mem_rings = sum(1 for ring in rings.AtomRings() if len(ring) == 6)
    if six_mem_rings < 3:
        return False, "Insufficient number of 6-membered rings"

    # Look for characteristic ketone/hydroxyl groups
    patt_ketone = Chem.MolFromSmarts('C(=O)C')
    patt_hydroxyl = Chem.MolFromSmarts('CO')
    
    ketone_matches = len(mol.GetSubstructMatches(patt_ketone))
    hydroxyl_matches = len(mol.GetSubstructMatches(patt_hydroxyl))
    
    if ketone_matches == 0 and hydroxyl_matches == 0:
        return False, "Missing characteristic oxygen-containing functional groups"

    # Look for characteristic side chain
    patt_side_chain = Chem.MolFromSmarts('CC(C)(C)C=CC')
    if not mol.HasSubstructMatch(patt_side_chain):
        patt_alt = Chem.MolFromSmarts('CC(C)(C)OC')  # Alternative oxidized form
        if not mol.HasSubstructMatch(patt_alt):
            return False, "Missing characteristic side chain structure"

    return True, "Matches cucurbitacin structural features: tetracyclic core, oxygenated functional groups, and characteristic side chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16219',
                          'name': 'cucurbitacin',
                          'definition': 'Any one of a class of tetracyclic '
                                        'triterpenoids, formally derived from '
                                        'the triterpene hydrocarbon '
                                        'cucurbitane, developed by some plants '
                                        '(especially those of the family '
                                        'Cucurbitaceaeas) as a defence '
                                        'mechanism against herbivores.',
                          'parents': ['CHEBI:26893']},
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
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 5900,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 0.875,
    'f1': 0.12173913043478259,
    'accuracy': 0.9831890812250332}