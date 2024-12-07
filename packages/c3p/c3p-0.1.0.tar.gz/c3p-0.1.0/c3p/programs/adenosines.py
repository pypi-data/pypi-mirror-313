"""
Classifies: CHEBI:22260 adenosines
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_adenosines(smiles: str):
    """
    Determines if a molecule is an adenosine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an adenosine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for ribose sugar
    ribose_pattern = Chem.MolFromSmarts('[CH2]1[CH]([OH])[CH]([OH])[CH]([OH])[O]1')
    if not mol.HasSubstructMatch(ribose_pattern):
        return False, "Missing ribose sugar moiety"
        
    # Check for adenine base 
    adenine_pattern = Chem.MolFromSmarts('c1nc(N)nc2c1ncn2')
    if not mol.HasSubstructMatch(adenine_pattern):
        return False, "Missing adenine base"
        
    # Check connection between ribose and adenine
    # N9 position of adenine should be connected to C1' of ribose
    connection_pattern = Chem.MolFromSmarts('O1[CH][CH]([OH])[CH]([OH])[CH]([CH2][OH])N2c3ncnc(N)c3ncn12')
    if not mol.HasSubstructMatch(connection_pattern):
        return False, "Incorrect connection between ribose and adenine"
    
    # Count number of modifications/substituents compared to adenosine
    adenosine = Chem.MolFromSmiles('Nc1ncnc2c1ncn2[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O')
    if mol.HasSubstructMatch(adenosine) and mol.GetNumAtoms() == adenosine.GetNumAtoms():
        return True, "Unmodified adenosine"
    
    # Analyze modifications
    modifications = []
    
    # Check for substitutions on adenine
    if mol.HasSubstructMatch(Chem.MolFromSmarts('Nc1nc([*])nc2c1ncn2')):
        modifications.append("C2-modified")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('Nc1ncnc2c1nc([*])n2')):
        modifications.append("C8-modified")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('[*]Nc1ncnc2c1ncn2')):
        modifications.append("N6-modified")
        
    # Check for ribose modifications
    if mol.HasSubstructMatch(Chem.MolFromSmarts('O1[CH][CH]([*])[CH]([OH])[CH]([CH2][OH])N')):
        modifications.append("2'-modified")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('O1[CH][CH]([OH])[CH]([*])[CH]([CH2][OH])N')):
        modifications.append("3'-modified")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('O1[CH][CH]([OH])[CH]([OH])[CH]([CH2][*])N')):
        modifications.append("5'-modified")
        
    if not modifications:
        modifications.append("other modifications present")
        
    return True, f"Adenosine derivative with {', '.join(modifications)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22260',
                          'name': 'adenosines',
                          'definition': 'Any purine ribonucleoside that is a '
                                        'derivative of adenosine.',
                          'parents': ['CHEBI:26399']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183880,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999728090926394}