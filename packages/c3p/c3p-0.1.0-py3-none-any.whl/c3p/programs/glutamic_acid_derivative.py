"""
Classifies: CHEBI:24315 glutamic acid derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_glutamic_acid_derivative(smiles: str):
    """
    Determines if a molecule is a glutamic acid derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glutamic acid derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for glutamic acid backbone: NH2-CH(R)-CH2-CH2-COOH
    glu_backbone = Chem.MolFromSmiles("NCC(CCC(=O)O)C(=O)O")
    if glu_backbone is None:
        return None, "Could not generate glutamic acid pattern"
        
    # Get matches to glutamic acid backbone
    matches = mol.GetSubstructMatches(glu_backbone)
    if not matches:
        return False, "No glutamic acid backbone found"
        
    # Check for modifications at amino group or carboxy groups
    for match in matches:
        amino_n = mol.GetAtomWithIdx(match[0])
        alpha_c = mol.GetAtomWithIdx(match[1])
        gamma_c = mol.GetAtomWithIdx(match[4])
        alpha_carb_c = mol.GetAtomWithIdx(match[6])
        
        # Check for modifications at amino group
        if amino_n.GetDegree() > 2:  # Modified amino group
            return True, "Modified at amino group"
            
        # Check for modifications at carboxyl groups
        for carb_c in [gamma_c, alpha_carb_c]:
            for neighbor in carb_c.GetNeighbors():
                if neighbor.GetSymbol() == 'O':
                    if neighbor.GetDegree() > 1:  # Modified carboxyl
                        return True, "Modified at carboxyl group"
                        
        # Check for heteroatom substitutions
        for atom_idx in match:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() not in ['C','N','O','H']:
                return True, "Contains heteroatom substitution"
                
    # Check if it's just a peptide containing glutamic acid
    peptide_pattern = Chem.MolFromSmarts("[NX3,NX4+][CX4H]([*])[CX3](=[OX1])[NX3,NX4+][CX4H]([*])[CX3](=[OX1])[OH0-,OH]")
    if mol.HasSubstructMatch(peptide_pattern):
        peptide_matches = mol.GetSubstructMatches(peptide_pattern)
        for p_match in peptide_matches:
            if any(atom in p_match for match in matches for atom in match):
                return False, "Appears to be a peptide containing glutamic acid"
                
    return True, "Contains modified glutamic acid backbone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24315',
                          'name': 'glutamic acid derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of glutamic acid at the '
                                        'amino group or either of the carboxy '
                                        'groups, or from the replacement of '
                                        'any hydrogen by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing glutamic acid residues.',
                          'parents': ['CHEBI:83821']},
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
    'num_false_positives': 2,
    'num_true_negatives': 183693,
    'num_false_negatives': 24,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998584795257975}