"""
Classifies: CHEBI:20060 3-hydroxy fatty acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_3_hydroxy_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a 3-hydroxy fatty acyl-CoA.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 3-hydroxy fatty acyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for CoA core structure
    # Adenine base
    adenine = Chem.MolFromSmarts('n1cnc2c(N)ncnc12')
    # Ribose sugar with phosphate
    ribose = Chem.MolFromSmarts('OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)')
    # Pantetheine arm with thiol
    pantetheine = Chem.MolFromSmarts('SCCNC(=O)CCNC(=O)')
    # Diphosphate bridge
    diphosphate = Chem.MolFromSmarts('P(O)(=O)OP(O)(=O)')

    if not all(mol.HasSubstructMatch(p) for p in [adenine, ribose, pantetheine, diphosphate]):
        return False, "Missing essential CoA structural elements"

    # Check for 3-hydroxy fatty acyl group
    # Pattern looks for R-CH(OH)-CH2-C(=O)-S- where R is alkyl chain
    hydroxy_acyl = Chem.MolFromSmarts('[CX4]-[CH1X4](-[OX2H1])-[CH2X4]-C(=O)-[SX2]')
    if not mol.HasSubstructMatch(hydroxy_acyl):
        return False, "Missing 3-hydroxy fatty acyl group"

    # Check for fatty acid chain (at least 2 carbons)
    fatty_chain = Chem.MolFromSmarts('CCC')
    if not mol.HasSubstructMatch(fatty_chain):
        return False, "Missing fatty acid chain"

    # Count double bonds by looking for C=C patterns
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    
    # Get stereochemistry of 3-hydroxy group
    stereo = ""
    matches = mol.GetSubstructMatches(hydroxy_acyl)
    if matches:
        for match in matches:
            hydroxy_carbon = mol.GetAtomWithIdx(match[1])
            if hydroxy_carbon.GetChiralTag() == Chem.ChiralType.CHI_TETRAHEDRAL_CW:
                stereo = "R"
            elif hydroxy_carbon.GetChiralTag() == Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
                stereo = "S"

    classification = "3-hydroxy fatty acyl-CoA"
    if stereo:
        classification += f" ({stereo}-isomer)"
    if double_bonds > 0:
        classification += f" with {double_bonds} double bonds"

    return True, classification


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20060',
                          'name': '3-hydroxy fatty acyl-CoA',
                          'definition': 'A hydroxy fatty acyl-CoA that results '
                                        'from the formal condensation of the '
                                        'thiol group of coenzyme A with the '
                                        'carboxy group of any 3-hydroxy fatty '
                                        'acid.',
                          'parents': ['CHEBI:61902']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.rdMolDescriptors' has no "
               "attribute 'CalcNumAliphaticDoubleBonds'",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 90511,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 0.8888888888888888,
    'f1': 0.13675213675213674,
    'accuracy': 0.9988854557492827}