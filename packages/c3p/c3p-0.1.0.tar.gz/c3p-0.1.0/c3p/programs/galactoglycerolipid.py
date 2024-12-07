"""
Classifies: CHEBI:24145 galactoglycerolipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

def is_galactoglycerolipid(smiles: str):
    """
    Determines if a molecule is a galactoglycerolipid based on structure.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a galactoglycerolipid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for required elements C,H,O
    formula = CalcMolFormula(mol)
    if not all(x in formula for x in ['C', 'H', 'O']):
        return False, "Missing required elements (C,H,O)"

    # Check for glycerol backbone (C-C-C with 3 oxygens attached)
    glycerol_pattern = Chem.MolFromSmarts("[OX2]-[CH2]-[CH]-[CH2]-[OX2]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "Missing glycerol backbone"

    # Check for galactose moiety
    # Pattern for pyranose ring with specific stereochemistry of galactose
    galactose_pattern = Chem.MolFromSmarts("O1[C][C]([O])[C]([O])[C]([O])[C]1[O]")
    if not mol.HasSubstructMatch(galactose_pattern):
        return False, "Missing galactose moiety"

    # Check for at least one ester group (fatty acid)
    ester_pattern = Chem.MolFromSmarts("[#6]-C(=O)-O-[#6]")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    
    if not ester_matches:
        return False, "Missing ester linkage"

    # Count number of ester groups
    num_esters = len(ester_matches)
    
    # Verify galactose is connected to glycerol via glycosidic bond
    glycosidic_pattern = Chem.MolFromSmarts("O1[C][C]([O])[C]([O])[C]([O])[C]1OC")
    if not mol.HasSubstructMatch(glycosidic_pattern):
        return False, "Galactose not properly connected to glycerol"

    return True, f"Galactoglycerolipid with {num_esters} fatty acid chain(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24145',
                          'name': 'galactoglycerolipid',
                          'definition': 'Any glycoglycerolipid having '
                                        'galactosyl as the glyco component.',
                          'parents': ['CHEBI:24385', 'CHEBI:63425']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 151388,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 0.75,
    'f1': 0.10526315789473685,
    'accuracy': 0.999326714896763}