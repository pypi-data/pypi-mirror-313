"""
Classifies: CHEBI:23639 deoxy sugar
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_deoxy_sugar(smiles: str):
    """
    Determines if a molecule is a deoxy sugar (sugar with a hydroxy group replaced by hydrogen).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a deoxy sugar, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Basic sugar characteristics
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    
    # Check if molecule has reasonable number of C and O for a sugar
    if num_carbons < 3 or num_oxygens < 2:
        return False, "Too few carbons or oxygens to be a sugar"
        
    # Check for cyclic structure (furanose or pyranose)
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        # Check for open-chain forms
        if not any(bond.GetBondType() == Chem.BondType.DOUBLE for bond in mol.GetBonds()):
            return False, "Not a cyclic sugar and no carbonyl group found"
            
    # Count hydroxyl groups
    num_hydroxyls = len(Chem.MolFromSmarts('[OH]').GetSubstructMatches(mol))
    
    # For cyclic sugars, typically expect n-1 hydroxyls where n is number of carbons
    # For deoxy sugars, expect even fewer hydroxyls
    if rings.NumRings():
        if num_hydroxyls >= num_carbons:
            return False, "Too many hydroxyl groups to be a deoxy sugar"
            
    # Check for carbonyl groups (aldehydes, ketones)
    has_carbonyl = len(Chem.MolFromSmarts('[C;H1](=O)').GetSubstructMatches(mol)) > 0 or \
                  len(Chem.MolFromSmarts('C(=O)C').GetSubstructMatches(mol)) > 0
                  
    # Look for typical sugar patterns
    sugar_pattern = Chem.MolFromSmarts('[CH2]-[CH1](-[OH])-[CH1](-[OH])')
    deoxy_pattern = Chem.MolFromSmarts('[CH3]-[CH1](-[OH])|[CH2]-[CH1](-[OH])')
    
    if mol.HasSubstructMatch(sugar_pattern) and mol.HasSubstructMatch(deoxy_pattern):
        if rings.NumRings():
            ring_sizes = [len(ring) for ring in rings.AtomRings()]
            if 5 in ring_sizes:
                return True, "Deoxy furanose sugar"
            elif 6 in ring_sizes:
                return True, "Deoxy pyranose sugar"
        elif has_carbonyl:
            return True, "Open-chain deoxy sugar"
            
    if has_carbonyl and mol.HasSubstructMatch(deoxy_pattern):
        return True, "Deoxy sugar derivative"
        
    return False, "Does not match deoxy sugar patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23639',
                          'name': 'deoxy sugar',
                          'definition': 'Any sugar having a hydroxy group '
                                        'replaced with a hydrogen atom.',
                          'parents': ['CHEBI:16646']},
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