"""
Classifies: CHEBI:23899 icosanoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_icosanoid(smiles: str):
    """
    Determines if a molecule is an icosanoid based on its SMILES string.
    Icosanoids are signaling molecules derived from C20 fatty acids.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an icosanoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check carbon count - should be around 20 carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 15 or carbon_count > 25:
        return False, f"Carbon count {carbon_count} outside typical range for icosanoids (15-25)"

    # Define and check SMARTS patterns
    patterns = {
        'carboxyl': '[CX3](=O)[OX2H1]',
        'double_bond': '[CX3]=[CX3]',
        'hydroxy': '[OX2H]',
        'carbonyl': '[CX3](=O)[CX4]',
        'carbon_chain': 'CCCCCC'
    }

    features = []
    matched_patterns = {}

    for name, pattern in patterns.items():
        pat = Chem.MolFromSmarts(pattern)
        if pat is not None and mol.HasSubstructMatch(pat):
            matched_patterns[name] = True
            if name != 'carbon_chain':  # Don't include carbon chain in features list
                features.append(name.replace('_', ' '))

    # Must have carboxylic acid group
    if not matched_patterns.get('carboxyl'):
        return False, "No carboxylic acid group found"

    # Must have carbon chain
    if not matched_patterns.get('carbon_chain'):
        return False, "No long carbon chain found"

    # Should have at least one other typical feature
    if len(features) < 2:  # carboxyl is already one feature
        return False, "Insufficient typical icosanoid structural features"

    feature_description = []
    if matched_patterns.get('double_bond'):
        feature_description.append("unsaturated bonds")
    if matched_patterns.get('hydroxy'):
        feature_description.append("hydroxyl groups")
    if matched_patterns.get('carbonyl'):
        feature_description.append("carbonyl groups")
    if matched_patterns.get('carboxyl'):
        feature_description.append("carboxylic acid")

    return True, f"Icosanoid containing {', '.join(feature_description)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23899',
                          'name': 'icosanoid',
                          'definition': 'Any member of the group of signalling '
                                        'molecules arising from oxidation of '
                                        'the three C20 essential fatty acids '
                                        '(EFAs) icosapentaenoic acid (EPA), '
                                        'arachidonic acid (AA) and '
                                        'dihomo-gamma-linolenic acid (DGLA).',
                          'parents': ['CHEBI:61697']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.HasSubstructMatch(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params=True)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool recursionPossible=True, bool useChirality=False, '
               'bool useQueryQueryMatches=False)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'bool recursionPossible=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 55,
    'num_false_positives': 100,
    'num_true_negatives': 2412,
    'num_false_negatives': 37,
    'num_negatives': None,
    'precision': 0.3548387096774194,
    'recall': 0.5978260869565217,
    'f1': 0.44534412955465585,
    'accuracy': 0.9473886328725039}