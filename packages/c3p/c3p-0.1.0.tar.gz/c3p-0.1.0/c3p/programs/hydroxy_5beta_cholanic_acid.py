"""
Classifies: CHEBI:24663 hydroxy-5beta-cholanic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import rdDecomposition
from rdkit.Chem import rdMolDescriptors

def is_hydroxy_5beta_cholanic_acid(smiles: str):
    """
    Determines if a molecule is a hydroxy-5beta-cholanic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxy-5beta-cholanic acid, False otherwise
        str: Reason for classification
    """
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"
            
        # Check for presence of steroid core (tetracyclic)
        rings = mol.GetRingInfo()
        if len(rings.AtomRings()) < 4:
            return False, "Missing tetracyclic steroid core"
            
        # Check for carboxylic acid group
        carboxylic_acid_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
        if not mol.HasSubstructMatch(carboxylic_acid_pattern):
            return False, "Missing carboxylic acid group"
            
        # Check for hydroxyl groups
        hydroxyl_pattern = Chem.MolFromSmarts('[OX2H1]')
        hydroxy_matches = mol.GetSubstructMatches(hydroxyl_pattern)
        if len(hydroxy_matches) < 1:
            return False, "Missing hydroxyl group"
            
        # Check for 5beta stereochemistry
        # This is a simplified check - would need more sophisticated analysis for complete certainty
        # Look for characteristic ring fusion pattern
        steroid_5beta_pattern = Chem.MolFromSmarts('[C]12[C@@H]([C@H]3[C@H]([C@@H]1)[C@@H]4[C@H]([C@H]3)CC[C@@]4(C)[C@H](CCC(=O)O)C)[C@H]2')
        if not mol.HasSubstructMatch(steroid_5beta_pattern):
            return False, "Does not match 5beta-cholanic acid core structure"

        num_hydroxy = len(hydroxy_matches)
        return True, f"Hydroxy-5beta-cholanic acid with {num_hydroxy} hydroxyl groups"
        
    except Exception as e:
        return None, f"Error analyzing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24663',
                          'name': 'hydroxy-5beta-cholanic acid',
                          'definition': 'Any member of the class of '
                                        '5beta-cholanic acids carrying at '
                                        'least one hydroxy group at '
                                        'unspecified position.',
                          'parents': ['CHEBI:33822', 'CHEBI:36248']},
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
    'success': False,
    'best': True,
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}