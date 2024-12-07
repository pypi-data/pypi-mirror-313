"""
Classifies: CHEBI:25271 methyl-branched fatty acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_methyl_branched_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a methyl-branched fatty acyl-CoA.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a methyl-branched fatty acyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for CoA substructure
    coA_pattern = Chem.MolFromSmarts('[#16]-[#6]-[#6]-[#7]-[#6](=[#8])-[#6]-[#6]-[#7]-[#6](=[#8])-[#6]-[#6](O)-[#6](C)(C)-[#6]-O-P(=[#8])(O)-O-P(=[#8])(O)-O-[#6]-[#6]-1-O-[#6](-[#6](-[#6]-1-O-P(=[#8])(O)O)O)n1cnc2c(N)ncnc12')
    if not mol.HasSubstructMatch(coA_pattern):
        return False, "Missing CoA moiety"
    
    # Check for thioester linkage
    thioester_pattern = Chem.MolFromSmarts('[#6](=O)-[#16]')
    if not mol.HasSubstructMatch(thioester_pattern):
        return False, "Missing thioester linkage"
        
    # Check for methyl branching on carbon chain
    methyl_branch_pattern = Chem.MolFromSmarts('[#6]-[#6](-[#6])-[#6]')
    if not mol.HasSubstructMatch(methyl_branch_pattern):
        return False, "No methyl branching found"
        
    # Count number of carbons in main chain
    carbon_chain_pattern = Chem.MolFromSmarts('[#6](-[#16])-[#6]-[#6]')
    matches = mol.GetSubstructMatches(carbon_chain_pattern)
    if not matches:
        return False, "No carbon chain found"
        
    # Find number of methyl branches
    branch_matches = len(mol.GetSubstructMatches(methyl_branch_pattern))
    
    return True, f"Methyl-branched fatty acyl-CoA with {branch_matches} methyl branch(es)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25271',
                          'name': 'methyl-branched fatty acyl-CoA',
                          'definition': 'A branched-chain fatty acyl-CoA that '
                                        'results from the formal condensation '
                                        'of the thiol group of coenzyme A with '
                                        'the carboxy group of any '
                                        'methyl-branched fatty acid.',
                          'parents': ['CHEBI:61912']},
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
    'num_true_negatives': 183877,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999728086490249}