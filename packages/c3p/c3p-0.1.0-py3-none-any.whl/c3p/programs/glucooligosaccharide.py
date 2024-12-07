"""
Classifies: CHEBI:24268 glucooligosaccharide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_glucooligosaccharide(smiles: str):
    """
    Determines if a molecule is a glucooligosaccharide (oligosaccharide made up of glucose residues).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glucooligosaccharide, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for minimum number of atoms (glucose monomer has 24 atoms)
    if mol.GetNumAtoms() < 24:
        return False, "Too few atoms to be a glucooligosaccharide"
        
    # Check for C:H:O ratio typical of carbohydrates
    num_c = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_o = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    num_h = sum(atom.GetTotalNumHs() for atom in mol.GetAtoms())
    
    if num_c == 0 or num_o == 0:
        return False, "Missing required elements C and O"
        
    # Check for presence of only C, H, O atoms
    other_atoms = [atom.GetSymbol() for atom in mol.GetAtoms() if atom.GetSymbol() not in ['C','O','H']]
    if other_atoms:
        return False, f"Contains non-carbohydrate elements: {','.join(set(other_atoms))}"
        
    # Check for cyclic structures (pyranose rings)
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        return False, "No rings found - glucose requires pyranose ring"
        
    # Count number of 6-membered rings (pyranose)
    pyranose_rings = sum(1 for ring in rings.AtomRings() if len(ring) == 6)
    
    if pyranose_rings == 0:
        return False, "No 6-membered (pyranose) rings found"
        
    # Check for glycosidic linkages between rings
    glycosidic_o = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            if len([n for n in atom.GetNeighbors() if n.GetSymbol() == 'C']) == 2:
                glycosidic_o += 1
                
    if glycosidic_o == 0 and pyranose_rings > 1:
        return False, "Multiple rings but no glycosidic linkages found"
        
    # Rough check of C:H:O ratio for glucose units
    # Each glucose unit is C6H12O6, but loses H2O in oligomer
    expected_glucose_units = pyranose_rings
    
    # Allow some deviation from perfect ratios due to different linkage types
    if abs(num_c/6 - expected_glucose_units) > 0.5:
        return False, "Carbon count inconsistent with glucose oligomer"
        
    if abs(num_o/(6-1) - expected_glucose_units) > 1:
        return False, "Oxygen count inconsistent with glucose oligomer"
        
    return True, f"Glucooligosaccharide with approximately {expected_glucose_units} glucose units"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24268',
                          'name': 'glucooligosaccharide',
                          'definition': 'An oligosaccharide comprised of '
                                        'glucose residues.',
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
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 13453,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 0.8888888888888888,
    'f1': 0.13675213675213674,
    'accuracy': 0.9925527208376346}