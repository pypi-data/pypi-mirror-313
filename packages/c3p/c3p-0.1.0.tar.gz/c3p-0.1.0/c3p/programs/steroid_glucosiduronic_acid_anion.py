"""
Classifies: CHEBI:136637 steroid glucosiduronic acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdMolDescriptors

def is_steroid_glucosiduronic_acid_anion(smiles: str):
    """
    Determines if a molecule is a steroid glucosiduronic acid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a steroid glucosiduronic acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of glucuronic acid anion moiety
    glucuronic_acid_pattern = Chem.MolFromSmarts("[OX2H1][CH]1[CH]([CH]([CH]([CH](O1)C(=O)[O-])[OH1])[OH1])[OH1]")
    if not mol.HasSubstructMatch(glucuronic_acid_pattern):
        return False, "No glucuronic acid anion moiety found"

    # Check for steroid core (four fused rings - three 6-membered, one 5-membered)
    steroid_core = Chem.MolFromSmarts("C1CC2CCC3C(C2)CCC4C3(CCC4)C1")
    if not mol.HasSubstructMatch(steroid_core):
        return False, "No steroid core structure found"

    # Count rings
    ring_info = mol.GetRingInfo()
    if len(ring_info.AtomRings()) < 5:  # At least 5 rings (4 for steroid core + 1 for glucuronic acid)
        return False, "Insufficient number of rings"

    # Check for negative charge
    total_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    if total_charge >= 0:
        return False, "No negative charge found"

    # Additional check for O-linkage between steroid and glucuronic acid
    o_linkage = Chem.MolFromSmarts("*-O-[CH]1O[CH][CH][CH][CH]1C(=O)[O-]")
    if not mol.HasSubstructMatch(o_linkage):
        return False, "No O-linkage between steroid and glucuronic acid found"

    # If all checks pass
    return True, "Molecule contains steroid core conjugated to glucuronic acid via O-linkage with negative charge"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:136637',
                          'name': 'steroid glucosiduronic acid anion',
                          'definition': 'A steroid conjugate anion formed by '
                                        'deprotonation of the carboxy group of '
                                        'any steroid glucosiduronic acid.',
                          'parents': ['CHEBI:50160', 'CHEBI:63551']},
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
    'num_true_negatives': 183873,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999673698464752}