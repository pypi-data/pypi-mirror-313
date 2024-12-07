"""
Classifies: CHEBI:22860 amino-acid betaine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_amino_acid_betaine(smiles: str):
    """
    Determines if a molecule is an amino acid betaine - an amino acid-derived zwitterion 
    with N-methylated ammonium and carboxylate.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an amino acid betaine, False otherwise
        str: Reason for classification
    """
    # Convert SMILES to molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Standardize the molecule (important for charge handling)
    uncharger = rdMolStandardize.Uncharger()
    mol = uncharger.uncharge(mol)

    # Look for carboxylate group [O-]C=O
    carboxylate_pattern = Chem.MolFromSmarts('[O-]C=O')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate group found"

    # Look for quaternary ammonium [N+](C)(C)(C)
    quat_ammonium_pattern = Chem.MolFromSmarts('[NX4+]')
    if not mol.HasSubstructMatch(quat_ammonium_pattern):
        return False, "No quaternary ammonium group found"

    # Get matches for both groups
    carboxylate_matches = mol.GetSubstructMatches(carboxylate_pattern)
    ammonium_matches = mol.GetSubstructMatches(quat_ammonium_pattern)

    # Check each ammonium nitrogen
    valid_betaine = False
    for ammonium_match in ammonium_matches:
        n_atom = mol.GetAtomWithIdx(ammonium_match[0])
        
        # Check if N has no hydrogens
        if n_atom.GetTotalNumHs() > 0:
            continue
            
        # Check if N has exactly 4 bonds
        if len(n_atom.GetBonds()) != 4:
            continue
            
        # Count methyl groups on N
        methyl_count = 0
        for neighbor in n_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                # Check if carbon is a methyl (has 3 H)
                if neighbor.GetTotalNumHs() == 3:
                    methyl_count += 1
                    
        # At least one methyl required
        if methyl_count == 0:
            continue
            
        valid_betaine = True
        break

    if not valid_betaine:
        return False, "No N-methylated quaternary ammonium found"

    # Check if carboxylate and ammonium are connected through carbon chain
    for carb_match in carboxylate_matches:
        for amm_match in ammonium_matches:
            path = Chem.GetShortestPath(mol, carb_match[1], amm_match[0])
            if path and len(path) > 2:  # Must be separated by at least one carbon
                return True, "Valid amino acid betaine structure found"

    return False, "Carboxylate and ammonium groups not properly connected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22860',
                          'name': 'amino-acid betaine',
                          'definition': 'Any amino acid-derived zwitterion - '
                                        'such as glycine betaine '
                                        '(N,N,N-trimethylammonioacetate) - in '
                                        'which the ammonium nitrogen carries '
                                        'methyl substituents and bears no '
                                        'hydrogen atoms.',
                          'parents': ['CHEBI:35284', 'CHEBI:83821']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 51385,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 0.6666666666666666,
    'f1': 0.03809523809523809,
    'accuracy': 0.9980383778744562}