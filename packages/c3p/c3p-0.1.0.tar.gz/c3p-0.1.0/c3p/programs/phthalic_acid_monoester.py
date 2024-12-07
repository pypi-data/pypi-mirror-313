"""
Classifies: CHEBI:132610 phthalic acid monoester
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phthalic_acid_monoester(smiles: str):
    """
    Determines if a molecule is a phthalic acid monoester.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phthalic acid monoester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for aromatic benzene ring
    patt_benzene = Chem.MolFromSmarts('c1ccccc1')
    if not mol.HasSubstructMatch(patt_benzene):
        return False, "No benzene ring found"
    
    # Find carboxylic acid and ester groups
    patt_acid = Chem.MolFromSmarts('C(=O)[OH]')
    patt_ester = Chem.MolFromSmarts('C(=O)O[!O;!N]')  # Exclude cyclic esters and amides
    
    acid_matches = mol.GetSubstructMatches(patt_acid)
    ester_matches = mol.GetSubstructMatches(patt_ester)
    
    if len(acid_matches) != 1 or len(ester_matches) != 1:
        return False, "Must have exactly one carboxylic acid and one ester group"

    # Check for cyclic esters (lactones)
    ring_info = mol.GetRingInfo()
    for ester_match in ester_matches:
        ester_atoms = set(ester_match)
        for ring in ring_info.AtomRings():
            if len(ester_atoms.intersection(set(ring))) >= 2:
                return False, "Contains cyclic ester (lactone)"

    # Get the benzene ring atoms
    benzene_matches = mol.GetSubstructMatches(patt_benzene)
    if not benzene_matches:
        return False, "No benzene ring found"
    ring_atoms = set(benzene_matches[0])

    # Check if both groups are attached to the benzene ring
    acid_carbon = acid_matches[0][0]
    ester_carbon = ester_matches[0][0]
    
    acid_attached = False
    ester_attached = False
    acid_attachment = None
    ester_attachment = None
    
    for ring_atom in ring_atoms:
        atom = mol.GetAtomWithIdx(ring_atom)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() == acid_carbon:
                acid_attached = True
                acid_attachment = ring_atom
            if neighbor.GetIdx() == ester_carbon:
                ester_attached = True
                ester_attachment = ring_atom

    if not (acid_attached and ester_attached):
        return False, "Both carboxylic acid and ester groups must be directly attached to the benzene ring"

    # Check if acid and ester groups are ortho to each other
    path_length = len(Chem.GetShortestPath(mol, acid_attachment, ester_attachment))
    if path_length != 2:  # ortho positions are separated by one atom
        return False, "Carboxylic acid and ester groups must be ortho to each other"

    # Check that the benzene ring doesn't have too many substituents
    num_substituents = 0
    for ring_atom in ring_atoms:
        atom = mol.GetAtomWithIdx(ring_atom)
        if len([n for n in atom.GetNeighbors() if n.GetIdx() not in ring_atoms]) > 0:
            num_substituents += 1
    
    if num_substituents > 2:
        return False, "Too many substituents on benzene ring"

    return True, "Valid phthalic acid monoester"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132610',
                          'name': 'phthalic acid monoester',
                          'definition': 'A dicarboxylic acid monoester '
                                        'resulting from the formal '
                                        'condensation of an alcoholic or '
                                        'aromatic hydroxy group with just one '
                                        'of the two carboxy groups of phthalic '
                                        'acid.',
                          'parents': [   'CHEBI:22723',
                                         'CHEBI:35484',
                                         'CHEBI:36244']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.6666666666666666 is too low.\n'
               "True positives: [('C1(=CC=CC=C1C(=O)OCCCCCCC(C)C)C(=O)O', "
               "'Valid phthalic acid monoester'), "
               "('C=1C=CC(=C(C1)C(=O)OCC)C(=O)O', 'Valid phthalic acid "
               "monoester')]\n"
               "False positives: [('O=C(OC)C1=C(OC)C=C(OC)C=C1C(=O)O', 'Valid "
               "phthalic acid monoester'), "
               "('O=C(OC)C1=C(OC)C(=C(OCC=C(C)C)C=C1C(=O)O)C', 'Valid phthalic "
               "acid monoester')]\n"
               'False negatives: []',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 0,
    'num_true_negatives': 183913,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 1.0,
    'f1': 1.0,
    'accuracy': 1.0}