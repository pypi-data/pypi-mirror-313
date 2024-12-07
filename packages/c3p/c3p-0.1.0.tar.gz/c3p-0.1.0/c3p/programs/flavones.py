"""
Classifies: CHEBI:24043 flavones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_flavones(smiles: str):
    """
    Determines if a molecule is a flavone (2-phenylchromen-4-one) or derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a flavone, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for chromen-4-one core structure using SMARTS pattern
    chromenone_pattern = Chem.MolFromSmarts('O=C1C=C(Oc2ccccc12)-c1ccccc1')
    if not mol.HasSubstructMatch(chromenone_pattern):
        return False, "Missing chromen-4-one core structure"
        
    # Check for required 2-phenyl substituent
    phenyl_pattern = Chem.MolFromSmarts('c1ccccc1')
    matches = mol.GetSubstructMatches(chromenone_pattern)
    
    if not matches:
        return False, "Missing required 2-phenyl substituent"
        
    # Check for aromatic rings
    rings = mol.GetRingInfo()
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "Missing required aromatic rings"

    # Get list of substituents
    substituents = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in ['C','H']:
            substituents.append(atom.GetSymbol())
    
    if len(set(substituents)) > 0:
        return True, f"Flavone with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted flavone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24043',
                          'name': 'flavones',
                          'definition': 'A member of the class of flavonoid '
                                        'with a 2-aryl-1-benzopyran-4-one '
                                        '(2-arylchromen-4-one) skeleton and '
                                        'its substituted derivatives.',
                          'parents': ['CHEBI:192499', 'CHEBI:47916']},
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
    'num_true_negatives': 183271,
    'num_false_negatives': 66,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999640007199856}