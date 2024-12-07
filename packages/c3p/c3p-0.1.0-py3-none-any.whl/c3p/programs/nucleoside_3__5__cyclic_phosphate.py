"""
Classifies: CHEBI:18375 nucleoside 3',5'-cyclic phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_nucleoside_3__5__cyclic_phosphate(smiles: str):
    """
    Determines if a molecule is a nucleoside 3',5'-cyclic phosphate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a nucleoside 3',5'-cyclic phosphate, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for phosphate group
    patt_phosphate = Chem.MolFromSmarts("[P](=O)([O,OH])([O,OH])[O,OH]")
    if not mol.HasSubstructMatch(patt_phosphate):
        return False, "No phosphate group found"

    # Check for ribose/deoxyribose ring with cyclic phosphate
    # Match pattern: ribose/deoxyribose with phosphate connecting C3' and C5'
    patt_cyclic_phosphate = Chem.MolFromSmarts("[C]1[C][C]([C]([C]1[#6,#1])O[P](=O)(O)OC1)O")
    if not mol.HasSubstructMatch(patt_cyclic_phosphate):
        return False, "No ribose/deoxyribose with cyclic phosphate found"

    # Check for purine or pyrimidine base
    patt_purine = Chem.MolFromSmarts("c1ncnc2[nX3]cnc12")  # Purine core
    patt_pyrimidine = Chem.MolFromSmarts("c1cn[cX3]nc1")   # Pyrimidine core
    
    has_purine = mol.HasSubstructMatch(patt_purine)
    has_pyrimidine = mol.HasSubstructMatch(patt_pyrimidine)
    
    if not (has_purine or has_pyrimidine):
        return False, "No purine or pyrimidine base found"

    # Check if base is connected to sugar
    patt_n_glycosidic = Chem.MolFromSmarts("[n]1[c][n][c]2[c][c][n][c]2[c]1[C]1O[C][C]([C]1)O")  # N-glycosidic bond pattern
    if not mol.HasSubstructMatch(patt_n_glycosidic):
        return False, "Base not properly connected to sugar via N-glycosidic bond"

    # Determine base type for more specific classification
    if has_purine:
        base_type = "purine"
    else:
        base_type = "pyrimidine"

    # Check stereochemistry of sugar ring
    chiral_centers = Chem.FindMolChiralCenters(mol)
    if len(chiral_centers) < 3:
        return True, f"Nucleoside 3',5'-cyclic phosphate with {base_type} base (warning: incomplete stereochemistry)"

    return True, f"Nucleoside 3',5'-cyclic phosphate with {base_type} base"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18375',
                          'name': "nucleoside 3',5'-cyclic phosphate",
                          'definition': 'A ribosyl or deoxyribosyl derivative '
                                        'of a pyrimidine or purine base in '
                                        'which C-3 and C-5 of the ribose ring '
                                        'are engaged in formation of a cyclic '
                                        'mono-, di-, tri- or tetra-phosphate.',
                          'parents': ['CHEBI:23447']},
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
    'success': False,
    'best': True,
    'error': 'Python argument types in\n'
             '    Mol.HasSubstructMatch(Mol, NoneType)\n'
             'did not match C++ signature:\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle query, '
             'RDKit::SubstructMatchParameters params=True)\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
             'RDKit::SubstructMatchParameters params)\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle query, '
             'bool recursionPossible=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False)\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
             'bool recursionPossible=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False)',
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