"""
Classifies: CHEBI:25095 L-lysine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdFMCS

def is_L_lysine_derivative(smiles: str):
    """
    Determines if a molecule is an L-lysine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an L-lysine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # L-lysine core structure SMILES (without H's)
    l_lysine = Chem.MolFromSmiles("N[C@@H](CCCCN)C(=O)O")
    
    if l_lysine is None:
        return None, None
    
    # Find maximum common substructure between input and L-lysine
    mcs = rdFMCS.FindMCS([mol, l_lysine], 
                        atomCompare=rdFMCS.AtomCompare.CompareElements,
                        bondCompare=rdFMCS.BondCompare.CompareOrder,
                        matchChiralTag=True,
                        ringMatchesRingOnly=True,
                        completeRingsOnly=True)
    
    if mcs.numAtoms < 7:  # Must contain most of L-lysine backbone
        return False, "Does not contain L-lysine core structure"
        
    # Check if the molecule has the L-lysine chiral center preserved
    smart_pattern = Chem.MolFromSmarts("[NH2][C@@H](CCCC*)*")
    if not mol.HasSubstructMatch(smart_pattern):
        return False, "Does not have correct L-lysine stereochemistry"
        
    # Check for modifications at amino groups or carboxy group
    amino_mod = False
    carboxy_mod = False
    
    # Check terminal amino group modifications
    term_nh2_pattern = Chem.MolFromSmarts("CCCCN")
    if mol.HasSubstructMatch(term_nh2_pattern):
        matches = mol.GetSubstructMatches(term_nh2_pattern)
        for match in matches:
            n_atom = mol.GetAtomWithIdx(match[-1])
            if len(n_atom.GetNeighbors()) > 2:  # Modified if more than 2 neighbors
                amino_mod = True
                
    # Check alpha amino group modifications  
    alpha_nh2_pattern = Chem.MolFromSmarts("[NH2][C@@H]")
    if not mol.HasSubstructMatch(alpha_nh2_pattern):
        amino_mod = True
        
    # Check carboxy modifications
    carboxy_pattern = Chem.MolFromSmarts("C(=O)O")
    if not mol.HasSubstructMatch(carboxy_pattern):
        carboxy_mod = True
        
    if amino_mod and carboxy_mod:
        return True, "L-lysine derivative with both amino and carboxy modifications"
    elif amino_mod:
        return True, "L-lysine derivative with amino group modification"
    elif carboxy_mod:
        return True, "L-lysine derivative with carboxy group modification"
    else:
        return False, "No modifications found on L-lysine core structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25095',
                          'name': 'L-lysine derivative',
                          'definition': 'A proteinogenic amino acid derivative '
                                        'resulting from reaction of L-lysine '
                                        'at the amino group or the carboxy '
                                        'group, or from the replacement of any '
                                        'hydrogen of L-lysine by a heteroatom.',
                          'parents': ['CHEBI:53079', 'CHEBI:83811']},
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
    'num_false_positives': 100,
    'num_true_negatives': 112565,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9990503408122693}