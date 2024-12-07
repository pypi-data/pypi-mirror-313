"""
Classifies: CHEBI:22278 alanine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_alanine_derivative(smiles: str):
    """
    Determines if a molecule is an alanine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an alanine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of basic alanine backbone
    # Look for C-C(N)-C(=O)O pattern
    alanine_pattern = Chem.MolFromSmarts('[CH3][CH1](N)[CH0](=O)O')
    if not mol.HasSubstructMatch(alanine_pattern):
        return False, "Does not contain alanine backbone"

    # Get the matches for the alanine pattern
    matches = mol.GetSubstructMatches(alanine_pattern)
    
    # For each match, analyze the substitution pattern
    for match in matches:
        carbon_idx = match[1]  # Get the alpha carbon index
        nitrogen_idx = None
        carboxyl_idx = None
        
        # Find connected N and C(=O)O atoms
        for atom in mol.GetAtomWithIdx(carbon_idx).GetNeighbors():
            if atom.GetSymbol() == 'N':
                nitrogen_idx = atom.GetIdx()
            elif atom.GetSymbol() == 'C' and atom.GetDegree() == 3:
                carboxyl_idx = atom.GetIdx()

        if nitrogen_idx is None or carboxyl_idx is None:
            continue

        # Check substitution at nitrogen
        n_atom = mol.GetAtomWithIdx(nitrogen_idx)
        n_substituted = False
        if n_atom.GetDegree() > 2:  # More than H2N-
            n_substituted = True

        # Check substitution at carboxyl
        c_atom = mol.GetAtomWithIdx(carboxyl_idx)
        c_substituted = False
        for neighbor in c_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'O' and neighbor.GetDegree() > 1:
                c_substituted = True
                break

        # Determine type of derivative
        if n_substituted and c_substituted:
            return True, "N- and C-substituted alanine derivative"
        elif n_substituted:
            return True, "N-substituted alanine derivative"
        elif c_substituted:
            return True, "C-substituted alanine derivative"
        else:
            # Check if it's a simple alanine with modified stereochemistry
            if len(Chem.FindMolChiralCenters(mol)) > 0:
                return True, "Alanine stereoisomer"
            
    # If we get here, it's not an alanine derivative
    return False, "Structure does not match alanine derivative patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22278',
                          'name': 'alanine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of alanine at the amino '
                                        'group or the carboxy group, or from '
                                        'the replacement of any hydrogen of '
                                        'alanine by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing alanine residues.',
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
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 22640,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 0.5384615384615384,
    'f1': 0.11666666666666665,
    'accuracy': 0.9953412736781962}