"""
Classifies: CHEBI:24317 L-glutamine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdFMCS

def is_L_glutamine_derivative(smiles: str):
    """
    Determines if a molecule is an L-glutamine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an L-glutamine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # L-glutamine core structure (without stereochemistry)
    l_gln = Chem.MolFromSmiles("NC(CCC(=O)N)C(=O)O")
    
    if l_gln is None:
        return None, "Error creating reference structure"

    # Find maximum common substructure
    mcs = rdFMCS.FindMCS([mol, l_gln], 
                        atomCompare=rdFMCS.AtomCompare.CompareElements,
                        bondCompare=rdFMCS.BondCompare.CompareOrder,
                        matchValences=True,
                        ringMatchesRingOnly=True,
                        completeRingsOnly=False,
                        timeout=1)
    
    if mcs.numAtoms < 5:  # Minimum atoms to consider it a derivative
        return False, "Structure too different from L-glutamine core"

    # Check for alpha carbon stereochemistry if present
    alpha_c_pattern = Chem.MolFromSmiles("N[C@H](CCC)C")
    if alpha_c_pattern is not None:
        matches = mol.GetSubstructMatches(alpha_c_pattern)
        if matches:
            # Check if the stereochemistry is correct (S/L configuration)
            chiral_centers = Chem.FindMolChiralCenters(mol)
            for match in matches:
                alpha_c_idx = match[1]  # Index of the alpha carbon
                for center in chiral_centers:
                    if center[0] == alpha_c_idx and center[1] == 'R':
                        return False, "Incorrect stereochemistry at alpha carbon"

    # Look for key modification patterns
    modifications = []
    
    # Check for N-terminal modifications
    n_term_pattern = Chem.MolFromSmarts("[N;!$(NC=O)]C")
    if not mol.HasSubstructMatch(n_term_pattern):
        modifications.append("N-terminal modified")
        
    # Check for C-terminal modifications
    c_term_pattern = Chem.MolFromSmarts("CC(=O)O")
    if not mol.HasSubstructMatch(c_term_pattern):
        modifications.append("C-terminal modified")
        
    # Check for side chain amide modifications
    side_chain_pattern = Chem.MolFromSmarts("CCC(=O)N")
    if not mol.HasSubstructMatch(side_chain_pattern):
        modifications.append("side chain amide modified")
    
    if not modifications:
        modifications.append("contains heteroatom substitutions")
        
    return True, f"L-glutamine derivative with {' and '.join(modifications)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24317',
                          'name': 'L-glutamine derivative',
                          'definition': 'A proteinogenic amino acid derivative '
                                        'resulting from reaction of '
                                        'L-glutamine at the amino group, the '
                                        'carboxy group, or the carboxamide, or '
                                        'from the replacement of any hydrogen '
                                        'of L-glutamine by a heteroatom.',
                          'parents': [   'CHEBI:70813',
                                         'CHEBI:83811',
                                         'CHEBI:83982']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 184,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.6515679442508711}