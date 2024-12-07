"""
Classifies: CHEBI:143017 ultra-long-chain fatty acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_ultra_long_chain_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is an ultra-long-chain fatty acyl-CoA (chain length > C27).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an ultra-long-chain fatty acyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of CoA moiety
    coA_pattern = Chem.MolFromSmarts("[CH2]OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12")
    if not mol.HasSubstructMatch(coA_pattern):
        return False, "Missing CoA moiety"
        
    # Check for thioester linkage
    thioester = Chem.MolFromSmarts("C(=O)S")
    if not mol.HasSubstructMatch(thioester):
        return False, "Missing thioester linkage"
        
    # Count carbons in fatty acyl chain
    # First split molecule at thioester
    fragments = Chem.FragmentOnBonds(mol, [mol.GetSubstructMatch(thioester)[1]], addDummies=False)
    fragments = Chem.GetMolFrags(fragments, asMols=True)
    
    # Get fatty acid fragment (should be the smaller one)
    fatty_acid = min(fragments, key=lambda x: x.GetNumAtoms())
    
    # Count carbons in fatty acid chain
    carbon_count = sum(1 for atom in fatty_acid.GetAtoms() if atom.GetSymbol() == 'C')
    
    if carbon_count > 27:
        return True, f"Ultra-long-chain fatty acyl-CoA with {carbon_count} carbons"
    else:
        return False, f"Fatty acyl chain length ({carbon_count}) not greater than C27"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:143017',
                          'name': 'ultra-long-chain fatty acyl-CoA',
                          'definition': 'A very long-chain fatty acyl-CoA in '
                                        'which the fatty acyl group has a '
                                        'chain length greater than C27.',
                          'parents': ['CHEBI:61910']},
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
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 133989,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 1.0,
    'f1': 0.13793103448275862,
    'accuracy': 0.9992542711619201}