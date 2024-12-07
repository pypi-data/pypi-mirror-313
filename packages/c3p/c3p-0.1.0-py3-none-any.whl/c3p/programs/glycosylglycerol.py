"""
Classifies: CHEBI:24406 glycosylglycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_glycosylglycerol(smiles: str):
    """
    Determines if a molecule is a glycosylglycerol - a glycoside formed by condensation 
    of glycerol with a glycosyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glycosylglycerol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of glycerol moiety (C-C-C backbone with 3 oxygens)
    glycerol_pattern = Chem.MolFromSmarts("[OX2H1,OX2R]-[CH2]-[CH1](-[OX2H1,OX2R])-[CH2]-[OX2H1,OX2R]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol moiety found"

    # Check for presence of pyranose sugar ring
    sugar_pattern = Chem.MolFromSmarts("O1[CH1][CH1][CH1][CH1][CH1]1")
    if not mol.HasSubstructMatch(sugar_pattern):
        return False, "No pyranose sugar ring found"

    # Check for glycosidic linkage between sugar and glycerol
    glycosidic_pattern = Chem.MolFromSmarts("O1[CH1][CH1][CH1][CH1][CH1]1-[O]-[CH2,CH1]-[CH1,CH2]-[CH2]")
    if not mol.HasSubstructMatch(glycosidic_pattern):
        return False, "No glycosidic linkage between sugar and glycerol found"

    # Count hydroxy groups on sugar ring
    sugar_hydroxy_pattern = Chem.MolFromSmarts("O1[CH1][CH1][CH1][CH1][CH1]1-[OX2H1]")
    sugar_hydroxy_count = len(mol.GetSubstructMatches(sugar_hydroxy_pattern))
    
    if sugar_hydroxy_count < 3:
        return False, "Sugar ring does not have enough hydroxyl groups"

    # All criteria met
    return True, "Molecule contains glycosyl group linked to glycerol backbone via glycosidic bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24406',
                          'name': 'glycosylglycerol',
                          'definition': 'A glycoside resulting from the '
                                        'condensation of one of the hydroxy '
                                        'groups of glycerol with a glycosyl '
                                        'group.',
                          'parents': ['CHEBI:24400', 'CHEBI:36307']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183906,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891249972812}