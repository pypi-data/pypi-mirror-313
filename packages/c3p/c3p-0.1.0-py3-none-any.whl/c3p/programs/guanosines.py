"""
Classifies: CHEBI:24458 guanosines
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_guanosines(smiles: str):
    """
    Determines if a molecule is a guanosine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a guanosine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for guanine base structure
    guanine_pattern = Chem.MolFromSmarts('[#7]1[#6][#7][#6]2[#7][#6][#7][#6][#6]2[#7]1')
    if not mol.HasSubstructMatch(guanine_pattern):
        return False, "Missing guanine base structure"

    # Check for ribose sugar
    ribose_pattern = Chem.MolFromSmarts('C1[C@@H](O)[C@@H](O)[C@H](O)C(CO)O1')
    if not mol.HasSubstructMatch(ribose_pattern):
        return False, "Missing ribose sugar structure"

    # Check connection between guanine and ribose
    guanosine_pattern = Chem.MolFromSmarts('[#7]1[#6][#7][#6]2[#7][#6][#7][#6][#6]2[#7]1-[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O')
    if not mol.HasSubstructMatch(guanosine_pattern):
        return False, "Incorrect connection between guanine and ribose"

    # Count modifications/substitutions
    modifications = []
    
    # Check N1 methylation
    n1_methyl = Chem.MolFromSmarts('Cn1c(N)nc2n(cnc2c1=O)')
    if mol.HasSubstructMatch(n1_methyl):
        modifications.append("N1-methylation")
        
    # Check N2 substitution
    n2_subst = Chem.MolFromSmarts('[#6,#7,#8]Nc1nc2n(cnc2c(=O)[nH]1)')
    if mol.HasSubstructMatch(n2_subst):
        modifications.append("N2-substitution")

    # Check other positions for modifications
    base_guanosine = Chem.MolFromSmiles('O=c1[nH]c(N)nc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O')
    if rdMolDescriptors.CalcMolFormula(mol) != rdMolDescriptors.CalcMolFormula(base_guanosine):
        modifications.append("additional modifications")

    if modifications:
        return True, f"Guanosine derivative with {', '.join(modifications)}"
    else:
        return True, "Unmodified guanosine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24458',
                          'name': 'guanosines',
                          'definition': 'Any purine ribonucleoside that is a '
                                        'derivative of guanosine.',
                          'parents': ['CHEBI:26399']},
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
    'num_true_negatives': 183913,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891254111953}