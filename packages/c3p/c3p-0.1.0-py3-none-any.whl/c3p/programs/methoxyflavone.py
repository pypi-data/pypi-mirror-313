"""
Classifies: CHEBI:25241 methoxyflavone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_methoxyflavone(smiles: str):
    """
    Determines if a molecule is a methoxyflavone (flavone with at least one methoxy substituent).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a methoxyflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for flavone core structure
    flavone_pattern = Chem.MolFromSmarts('[#6]1(=O)c2c(O[#6]1[#6]1=cc=cc=c1)cc([#6,#8,#1])cc2')
    if not mol.HasSubstructMatch(flavone_pattern):
        return False, "No flavone core structure found"

    # Check for methoxy group
    methoxy_pattern = Chem.MolFromSmarts('CO')
    if not mol.HasSubstructMatch(methoxy_pattern):
        return False, "No methoxy substituent found"

    # Count number of methoxy groups
    methoxy_matches = len(mol.GetSubstructMatches(methoxy_pattern))

    # Verify methoxy groups are attached to aromatic rings
    methoxy_aromatic = Chem.MolFromSmarts('COc1ccccc1')
    if not mol.HasSubstructMatch(methoxy_aromatic):
        return False, "Methoxy groups not attached to aromatic ring"

    return True, f"Methoxyflavone with {methoxy_matches} methoxy group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25241',
                          'name': 'methoxyflavone',
                          'definition': 'Any member of the class of flavones '
                                        'with at least one methoxy '
                                        'substituent.',
                          'parents': ['CHEBI:24043', 'CHEBI:25698']},
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
    'num_true_negatives': 183739,
    'num_false_negatives': 19,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9998966031410877}