"""
Classifies: CHEBI:22300 aldonic acid phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aldonic_acid_phosphate(smiles: str):
    """
    Determines if a molecule is an aldonic acid phosphate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aldonic acid phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"

    # Check for phosphate group
    phosphate_pattern = Chem.MolFromSmarts('P(=O)(O)(O)O')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group found"

    # Check for hydroxy groups
    hydroxy_pattern = Chem.MolFromSmarts('OH')
    if not mol.HasSubstructMatch(hydroxy_pattern):
        return False, "No hydroxy groups found"

    # Check carbon chain between COOH and phosphate
    # First get the indices of the C in COOH and P atom
    cooh_matches = mol.GetSubstructMatches(carboxylic_pattern)
    phos_matches = mol.GetSubstructMatches(phosphate_pattern)
    
    if not cooh_matches or not phos_matches:
        return False, "Could not find required groups"

    cooh_c = cooh_matches[0][0]  # Carbon of COOH
    phos = phos_matches[0][0]    # Phosphorus atom

    # Check if there is a carbon chain path between COOH and phosphate
    path_exists = False
    for path in AllChem.FindAllPathsOfLengthN(mol, 10, useBonds=False):
        if cooh_c in path and phos in path:
            # Check if path contains carbons with OH groups
            for atom_idx in path:
                atom = mol.GetAtomWithIdx(atom_idx)
                if atom.GetSymbol() == 'C':
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                            path_exists = True
                            break
    
    if not path_exists:
        return False, "No suitable carbon chain path found between carboxylic acid and phosphate groups"

    return True, "Molecule contains carboxylic acid group, phosphate group, and hydroxy groups in appropriate arrangement"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22300',
                          'name': 'aldonic acid phosphate',
                          'definition': 'An aldonic acid in which at least one '
                                        'of the hydroxy groups has been '
                                        'phosphorylated.',
                          'parents': ['CHEBI:26816']},
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