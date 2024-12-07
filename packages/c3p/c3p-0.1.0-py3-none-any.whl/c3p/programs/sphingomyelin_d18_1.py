"""
Classifies: CHEBI:17636 sphingomyelin d18:1
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_sphingomyelin_d18_1(smiles: str):
    """
    Determines if a molecule is a sphingomyelin d18:1 (sphingomyelin with sphingosine backbone).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a sphingomyelin d18:1, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for required functional groups
    # 1. Phosphocholine group
    phosphocholine_pattern = 'COP([O-])(=O)OCC[N+](C)(C)C'
    phos_mol = Chem.MolFromSmarts(phosphocholine_pattern)
    if not mol.HasSubstructMatch(phos_mol):
        return False, "Missing phosphocholine group"

    # 2. Sphingosine backbone with specific stereochemistry and double bond
    # Look for the core structure with amide, hydroxyl group and trans double bond
    sphingosine_patterns = [
        '[C@@H](O)[C@H](COP)NC(=O)',  # One stereochemistry possibility
        '[C@H](O)[C@@H](COP)NC(=O)'   # Alternative stereochemistry
    ]
    
    found_sphingosine = False
    for pattern in sphingosine_patterns:
        pattern_mol = Chem.MolFromSmarts(pattern)
        if pattern_mol is not None and mol.HasSubstructMatch(pattern_mol):
            found_sphingosine = True
            break
    
    if not found_sphingosine:
        return False, "Missing sphingosine backbone with correct stereochemistry"

    # 3. Check for trans double bond in correct position
    trans_db_patterns = [
        'C\C=C\[C@@H](O)[C@H]',
        'C\C=C\[C@H](O)[C@@H]',
        'C/C=C/[C@@H](O)[C@H]',
        'C/C=C/[C@H](O)[C@@H]'
    ]
    
    found_trans_db = False
    for pattern in trans_db_patterns:
        pattern_mol = Chem.MolFromSmarts(pattern)
        if pattern_mol is not None and mol.HasSubstructMatch(pattern_mol):
            found_trans_db = True
            break
            
    if not found_trans_db:
        return False, "Missing trans double bond in correct position"

    # 4. Check for long carbon chain (d18:1 requires 18-carbon sphingosine backbone)
    carbon_chain = 'CCCCCCCCCCCC'  # At least 12 carbons in chain
    chain_mol = Chem.MolFromSmarts(carbon_chain)
    if not mol.HasSubstructMatch(chain_mol):
        return False, "Missing required carbon chain length"

    return True, "Contains sphingomyelin d18:1 structure with correct stereochemistry"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17636',
                          'name': 'sphingomyelin d18:1',
                          'definition': 'Any sphingomyelin having sphingosine '
                                        'as the sphingoid component.',
                          'parents': ['CHEBI:64583']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               'False negatives: '
               "[('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COP([O-])(=O)OCC[N+](C)(C)C)NC([*])=O', "
               "'Missing sphingosine backbone with correct stereochemistry'), "
               "('CCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'Missing sphingosine backbone with correct stereochemistry'), "
               "('[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)(COP(OCC[N+](C)(C)C)(=O)[O-])NC(=O)*', "
               "'Missing sphingosine backbone with correct stereochemistry'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COP([O-])(=O)OCC[N+](C)(C)C)NC([*])=O', "
               "'Missing sphingosine backbone with correct stereochemistry'), "
               "('C(CCCCCCCCCC)CC\\\\C=C\\\\[C@@H](O)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCC)COP(=O)([O-])OCC[N+](C)(C)C', "
               "'Missing sphingosine backbone with correct stereochemistry')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 94,
    'num_true_negatives': 183812,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.050505050505050504,
    'recall': 1.0,
    'f1': 0.09615384615384615,
    'accuracy': 0.9994888832098134}