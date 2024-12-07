"""
Classifies: CHEBI:26739 sphingolipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_sphingolipid(smiles: str):
    """
    Determines if a molecule is a sphingolipid based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sphingolipid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for required elements of sphingoid base backbone:
    # - Long carbon chain
    # - Amino group (-NH2 or -NH-)
    # - At least one hydroxyl group (-OH)
    # - Often has fatty acid amide linkage
    
    # Count carbons, nitrogens, oxygens
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_nitrogens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'N') 
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')

    # Must have carbon chain
    if num_carbons < 12:
        return False, "Carbon chain too short for sphingolipid"
        
    # Must have at least one nitrogen (amino group)
    if num_nitrogens == 0:
        return False, "No nitrogen atoms found - missing amino group"
        
    # Must have hydroxyl groups
    if num_oxygens == 0:
        return False, "No oxygen atoms found - missing hydroxyl groups"

    # Look for amide linkage pattern
    amide_pattern = Chem.MolFromSmarts('[NH]-[C](=O)-[C]')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide linkage found"
        
    # Look for typical sphingoid base patterns
    sphingoid_base = Chem.MolFromSmarts('[CH2]-[CH](-[NH]-[C])-[CH](-[OH])-[CH2]')
    if mol.HasSubstructMatch(sphingoid_base):
        return True, "Contains sphingoid base backbone with amide linkage"
        
    # More specific sphingosine pattern
    sphingosine = Chem.MolFromSmarts('[CH2]-[CH](-[NH]-[C])-[CH](-[OH])-[CH]=[CH]')
    if mol.HasSubstructMatch(sphingosine):
        return True, "Contains sphingosine backbone"

    # Check for glycosphingolipid pattern
    glyco_pattern = Chem.MolFromSmarts('[OH1][C]1[O][C]([C])([C][C]([OH1])[C]1[OH1])')
    if mol.HasSubstructMatch(glyco_pattern):
        return True, "Contains glycosphingolipid pattern"
        
    # Check for sphingomyelin pattern (phosphocholine head group)
    sm_pattern = Chem.MolFromSmarts('[O]-P(=O)(-O)-OCC[N+](C)(C)C')
    if mol.HasSubstructMatch(sm_pattern):
        return True, "Contains sphingomyelin phosphocholine group"

    # If we have the key elements but no clear structural match,
    # it may be a novel/unusual sphingolipid
    if num_carbons >= 12 and num_nitrogens >= 1 and num_oxygens >= 2:
        return True, "Contains required elements for sphingolipid structure"
        
    return False, "Does not match sphingolipid structural patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26739',
                          'name': 'sphingolipid',
                          'definition': 'Sphingolipids are a complex family of '
                                        'compounds that share a common '
                                        'structural feature, a sphingoid base '
                                        'backbone.',
                          'parents': [   'CHEBI:18059',
                                         'CHEBI:35352',
                                         'CHEBI:36963']},
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
    'num_true_positives': 168,
    'num_false_positives': 100,
    'num_true_negatives': 361,
    'num_false_negatives': 61,
    'num_negatives': None,
    'precision': 0.6268656716417911,
    'recall': 0.7336244541484717,
    'f1': 0.6760563380281691,
    'accuracy': 0.7666666666666667}