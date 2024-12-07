"""
Classifies: CHEBI:24261 glucocorticoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdMolDescriptors

def is_glucocorticoid(smiles: str):
    """
    Determines if a molecule is a glucocorticoid based on structural features.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glucocorticoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of steroid core (4 fused rings)
    rings = mol.GetRingInfo()
    if len(rings.AtomRings()) < 4:
        return False, "Missing steroid core (4 fused rings)"
    
    # Check for 6-6-6-5 ring pattern characteristic of steroids
    ring_sizes = [len(ring) for ring in rings.AtomRings()]
    if not (ring_sizes.count(6) >= 3 and 5 in ring_sizes):
        return False, "Missing characteristic 6-6-6-5 steroid ring pattern"

    # Check for key functional groups common in glucocorticoids
    # Look for ketone at C3 position (typically in A ring)
    patt_ketone = Chem.MolFromSmarts('C1CCC(=O)CC1')
    if not mol.HasSubstructMatch(patt_ketone):
        return False, "Missing ketone group in ring A"

    # Look for hydroxyl groups (common in glucocorticoids)
    patt_oh = Chem.MolFromSmarts('OH')
    if not mol.HasSubstructMatch(patt_oh):
        return False, "Missing hydroxyl groups"

    # Look for C17 side chain with hydroxyl/ketone
    patt_c17_chain = Chem.MolFromSmarts('[CH2]C(=O)CO')
    patt_c17_chain_alt = Chem.MolFromSmarts('[CH2]C(O)CO')
    
    if not (mol.HasSubstructMatch(patt_c17_chain) or mol.HasSubstructMatch(patt_c17_chain_alt)):
        return False, "Missing characteristic C17 side chain"

    # If all checks pass, likely a glucocorticoid
    # Identify some common modifications
    modifications = []
    
    # Check for halogen substitutions
    if mol.HasSubstructMatch(Chem.MolFromSmarts('[F,Cl,Br,I]')):
        modifications.append("halogenated")
        
    # Check for acetate groups
    if mol.HasSubstructMatch(Chem.MolFromSmarts('CC(=O)O')):
        modifications.append("acetylated")
        
    # Check for methyl groups beyond the core structure
    if len(mol.GetSubstructMatches(Chem.MolFromSmarts('C[CH3]'))) > 2:
        modifications.append("additional methyl groups")

    if modifications:
        return True, f"Glucocorticoid with modifications: {', '.join(modifications)}"
    else:
        return True, "Basic glucocorticoid structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24261',
                          'name': 'glucocorticoid',
                          'definition': 'Glucocorticoids are a class of '
                                        'steroid hormones that regulate a '
                                        'variety of physiological processes, '
                                        'in particular control of the '
                                        'concentration of glucose in blood.',
                          'parents': ['CHEBI:36699']},
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