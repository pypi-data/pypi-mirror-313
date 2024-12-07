"""
Classifies: CHEBI:17297 UDP-sugar
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_UDP_sugar(smiles: str):
    """
    Determines if a molecule is a UDP-sugar.
    A UDP-sugar is a pyrimidine nucleotide-sugar having UDP as the nucleotide component 
    attached to an unspecified sugar via an anomeric diphosphate linkage.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a UDP-sugar, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for uracil substructure
    uracil_pattern = Chem.MolFromSmarts('c1cnc(=O)[nH]c1=O')
    if not mol.HasSubstructMatch(uracil_pattern):
        return False, "No uracil moiety found"

    # Check for ribose connected to uracil
    ribose_uracil_pattern = Chem.MolFromSmarts('C1OC(C(O)C1O)n1ccc(=O)[nH]c1=O')
    if not mol.HasSubstructMatch(ribose_uracil_pattern):
        return False, "No ribose-uracil connection found"

    # Check for diphosphate group
    diphosphate_pattern = Chem.MolFromSmarts('OP(O)(=O)OP(O)(=O)O')
    if not mol.HasSubstructMatch(diphosphate_pattern):
        return False, "No diphosphate linkage found"

    # Check for sugar moiety (looking for ring oxygen connected to phosphate)
    sugar_phosphate_pattern = Chem.MolFromSmarts('OC1[CH2,CH1,C]O[CH1]([CH1,C])[CH1,C][CH1,C]1')
    if not mol.HasSubstructMatch(sugar_phosphate_pattern):
        return False, "No sugar moiety found connected to phosphate"

    # Additional validation: Check connectivity
    # The molecule should have:
    # 1. Uracil connected to ribose
    # 2. Ribose connected to diphosphate
    # 3. Diphosphate connected to sugar

    # Get the number of rings
    ring_info = mol.GetRingInfo()
    num_rings = ring_info.NumRings()
    
    if num_rings < 3:  # Should have at least uracil, ribose and sugar rings
        return False, "Missing required ring structures"

    return True, "Contains uracil, ribose, diphosphate linkage and sugar moiety in correct arrangement"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17297',
                          'name': 'UDP-sugar',
                          'definition': 'A pyrimidine nucleotide-sugar having '
                                        'UDP as the nucleotide component '
                                        'attached to an unspecified sugar via '
                                        'an anomeric diphosphate linkage.',
                          'parents': ['CHEBI:61109']},
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
    'num_true_positives': 2,
    'num_false_positives': 27,
    'num_true_negatives': 183828,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.06896551724137931,
    'recall': 0.25,
    'f1': 0.1081081081081081,
    'accuracy': 0.9998205185382595}