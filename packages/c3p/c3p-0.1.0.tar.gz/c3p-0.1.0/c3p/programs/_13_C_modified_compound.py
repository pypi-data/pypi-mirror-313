"""
Classifies: CHEBI:139357 (13)C-modified compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is__13_C_modified_compound(smiles: str):
    """
    Determines if a molecule is a (13)C-modified compound.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains 13C isotopes, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Count total carbons and 13C isotopes
    total_carbons = 0
    c13_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            total_carbons += 1
            if atom.GetIsotope() == 13:
                c13_atoms.append(atom.GetIdx())
                
    if len(c13_atoms) == 0:
        return False, "No 13C isotopes found"
        
    # If molecule is just a single 13C atom, return False
    if total_carbons == 1 and len(c13_atoms) == 1:
        return False, "Single 13C atom is not considered a modified compound"
        
    # Get positions of 13C atoms
    positions = []
    for idx in c13_atoms:
        atom = mol.GetAtomWithIdx(idx)
        positions.append(str(idx+1))  # Convert to 1-based indexing
        
    return True, f"13C isotopes found at positions: {', '.join(positions)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139357',
                          'name': '(13)C-modified compound',
                          'definition': 'An isotopically modified compound in '
                                        'which the abundance of a (13)C '
                                        'isotope at one or more positions has '
                                        'been increased above that of the '
                                        'naturally occurring level.',
                          'parents': ['CHEBI:139358']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.7499999999999999 is too low.\n'
               'True positives: '
               "[('O1[13C@@](O[13C@H]2O[13C@@H]([13C@@H](O)[13C@H](O)[13C@H]2O)[13CH2]O)([13C@@H](O)[13C@H](O)[13C@H]1[13CH2]O)[13CH2]O', "
               "'13C isotopes found at positions: 2, 4, 6, 7, 9, 11, 13, 15, "
               "17, 19, 20, 22'), ('C=1C=C(O[13CH3])C=CC1NC(C)=O', '13C "
               "isotopes found at positions: 5'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[13C@@H](O)[13C@H]1O)CO', '13C "
               "isotopes found at positions: 7, 9')]\n"
               "False positives: [('[13C]', '13C isotopes found at positions: "
               "1'), "
               "('O=C([C@]1([13C@H](C(=C[C@@H]2[C@@H]1[C@@H](C[C@@H]([13CH2]2)C)C)C)C[C@H](O[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@H]3O)O)CO)[C@@H]([C@H](O)/C(=C/CC)/C)C)C)C[13CH2]O', "
               "'13C isotopes found at positions: 4, 12, 41')]\n"
               'False negatives: []',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 1,
    'num_true_negatives': 183903,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.75,
    'recall': 1.0,
    'f1': 0.8571428571428571,
    'accuracy': 0.999994562469074}