"""
Classifies: CHEBI:25174 mannooligosaccharide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_mannooligosaccharide(smiles: str):
    """
    Determines if a molecule is a mannooligosaccharide (oligosaccharide composed of mannose units).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a mannooligosaccharide, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Basic structure requirements for mannose units:
    # - 6 carbons (pyranose ring)
    # - 5 oxygens (4 hydroxyls + 1 ring oxygen)
    # - Correct stereochemistry at C2,C3,C4,C5 positions
    
    # Count atoms
    num_c = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_o = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    
    # Check for minimum size (at least one mannose unit)
    if num_c < 6 or num_o < 5:
        return False, "Too few atoms for a mannooligosaccharide"
        
    # Check if number of C and O atoms is consistent with mannose units
    # Each mannose unit has 6C and 5O
    if num_c % 6 != 0:
        return False, "Number of carbons not consistent with mannose units"
        
    # Look for pyranose rings
    rings = mol.GetRingInfo()
    six_membered_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if ring has 5C and 1O
            c_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'C')
            o_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'O')
            if c_count == 5 and o_count == 1:
                six_membered_rings.append(ring)
                
    if not six_membered_rings:
        return False, "No pyranose rings found"
        
    # Count number of mannose units based on pyranose rings
    num_mannose = len(six_membered_rings)
    
    if num_mannose < 1:
        return False, "No mannose units found"
        
    # Check for glycosidic linkages between units
    glycosidic_bonds = 0
    for bond in mol.GetBonds():
        if (bond.GetBeginAtom().GetSymbol() == 'O' and 
            bond.GetEndAtom().GetSymbol() == 'C'):
            glycosidic_bonds += 1
            
    if num_mannose > 1 and glycosidic_bonds < num_mannose - 1:
        return False, "Insufficient glycosidic linkages for oligosaccharide"

    return True, f"Mannooligosaccharide with {num_mannose} mannose units"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25174',
                          'name': 'mannooligosaccharide',
                          'definition': 'An oligosaccharide comprised of '
                                        'mannose residues.',
                          'parents': ['CHEBI:50699']},
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
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 2031,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9532054281703323}