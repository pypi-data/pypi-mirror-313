"""
Classifies: CHEBI:23855 divalent carboacyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_divalent_carboacyl_group(smiles: str):
    """
    Determines if a molecule contains a divalent carboacyl group.
    A divalent carboacyl group is formed by loss of OH from two carboxy groups 
    of a polycarboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains a divalent carboacyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for C(=O)* pattern (carbonyl with attachment point)
    carbonyl_pattern = Chem.MolFromSmarts('C(=O)*')
    matches = mol.GetSubstructMatches(carbonyl_pattern)
    
    if len(matches) < 2:
        return False, "Does not contain at least 2 carbonyls with attachment points"

    # Find carbonyls that are connected through a carbon chain
    carbonyl_carbons = [match[0] for match in matches]
    
    # Create a copy of the molecule for path finding
    mol_copy = Chem.Mol(mol)
    
    for i in range(len(carbonyl_carbons)):
        for j in range(i+1, len(carbonyl_carbons)):
            if carbonyl_carbons[i] == carbonyl_carbons[j]:
                continue
                
            try:
                # Find shortest path between carbonyls
                path = Chem.GetShortestPath(mol_copy, carbonyl_carbons[i], carbonyl_carbons[j])
                if path and len(path) >= 2:  # Path must have at least 2 atoms
                    # Check if path contains only carbons (excluding the carbonyl carbons)
                    path_atoms = [mol.GetAtomWithIdx(idx) for idx in path[1:-1]]
                    if all(atom.GetSymbol() == 'C' for atom in path_atoms):
                        return True, f"Contains divalent carboacyl group with {len(path)-1} atoms in connecting chain"
            except:
                continue

    return False, "No carbonyls connected through carbon chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23855',
                          'name': 'divalent carboacyl group',
                          'definition': 'A divalent carboacyl group is a group '
                                        'formed by loss of OH from two carboxy '
                                        'groups of a polycarboxylic acid.',
                          'parents': ['CHEBI:37838']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Invariant Violation\n'
               '\t\n'
               '\tViolation occurred on line 341 in file '
               'Code/GraphMol/Matrices.cpp\n'
               '\tFailed Expression: aid1 != aid2\n'
               '\tRDKIT: 2024.03.6\n'
               '\tBOOST: 1_85\n',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 561,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 0.5714285714285714,
    'f1': 0.07207207207207209,
    'accuracy': 0.8458083832335329}