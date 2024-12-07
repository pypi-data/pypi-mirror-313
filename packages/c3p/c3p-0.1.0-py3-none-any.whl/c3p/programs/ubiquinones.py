"""
Classifies: CHEBI:16389 ubiquinones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ubiquinones(smiles: str):
    """
    Determines if a molecule is a ubiquinone based on structural features.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if molecule is a ubiquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for benzoquinone core with specific substitution pattern
    # SMARTS pattern for 2,3-dimethoxy/hydroxy-5-methyl-1,4-benzoquinone core
    core_pattern = Chem.MolFromSmarts('[$(C1(=O)C(=[C](C)C(=O)C(O[CH3,H])=C1O[CH3,H]))]')
    
    if core_pattern is None:
        return None, "Invalid SMARTS pattern"

    if not mol.HasSubstructMatch(core_pattern):
        return False, "Missing required benzoquinone core structure"

    # Check for methoxy/hydroxy groups at positions 2,3
    if not (('COC1=C(OC)' in smiles) or ('COC1=C(O)' in smiles)):
        return False, "Missing required methoxy/hydroxy groups at positions 2,3"
        
    # Check for polyprenoid side chain
    isoprenoid_pattern = Chem.MolFromSmarts('CC(=C)CC')
    if isoprenoid_pattern is None:
        return None, "Invalid isoprenoid SMARTS pattern"
        
    matches = mol.GetSubstructMatches(isoprenoid_pattern)
    
    if len(matches) < 1:
        return False, "Missing polyprenoid side chain"

    # Count isoprenoid units
    num_units = len(matches)

    if 'COC1=C(OC)' in smiles:
        return True, f"Ubiquinone with {num_units} isoprenoid units"
    else:
        return True, f"Demethylubiquinone with {num_units} isoprenoid units"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16389',
                          'name': 'ubiquinones',
                          'definition': 'Any benzoquinone derived from '
                                        '2,3-dimethoxy-5-methylbenzoquinone; '
                                        'one of a group of naturally occurring '
                                        'homologues. The redox-active quinoid '
                                        'moiety usually carries a polyprenoid '
                                        'side chain at position 6, the number '
                                        'of isoprenoid units in which is '
                                        'species-specific. Ubiquinones are '
                                        'involved in the control of '
                                        'mitochondrial electron transport, and '
                                        'are also potent anti-oxidants.',
                          'parents': ['CHEBI:132124', 'CHEBI:26255']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 2,
    'num_true_negatives': 183909,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.3333333333333333,
    'recall': 0.5,
    'f1': 0.4,
    'accuracy': 0.9999836879394062}