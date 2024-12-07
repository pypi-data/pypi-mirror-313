"""
Classifies: CHEBI:176910 fatty acyl-L-carnitine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import rdMolDescriptors

def is_fatty_acyl_L_carnitine(smiles: str):
    """
    Determines if a molecule is a fatty acyl-L-carnitine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a fatty acyl-L-carnitine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carnitine core structure with L configuration
    carnitine_pattern = Chem.MolFromSmarts('[C@H,C@@H](CC([O-])=O)C[N+](C)(C)C')
    if not mol.HasSubstructMatch(carnitine_pattern):
        return False, "Missing L-carnitine core structure"

    # Check for ester linkage
    ester_pattern = Chem.MolFromSmarts('[C@H,C@@H](CC([O-])=O)OC(=O)')
    if not mol.HasSubstructMatch(ester_pattern):
        return False, "Missing ester linkage"

    # Find the acyl group
    acyl_pattern = Chem.MolFromSmarts('C(=O)C')
    matches = mol.GetSubstructMatches(acyl_pattern)
    
    if matches:
        carbon_count = 0
        visited = set()
        
        def count_carbons(atom_idx, mol, visited):
            if atom_idx in visited:
                return 0
            visited.add(atom_idx)
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() != 'C':
                return 0
            count = 1
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C':
                    count += count_carbons(neighbor.GetIdx(), mol, visited)
            return count

        # Start counting from the carbonyl carbon
        for match in matches:
            visited.clear()
            start_idx = match[1]  # Get the carbon after C=O
            current_count = count_carbons(start_idx, mol, visited)
            carbon_count = max(carbon_count, current_count)

        # Check for unsaturation
        double_bond_pattern = Chem.MolFromSmarts('CC=CC')
        has_double_bonds = mol.HasSubstructMatch(double_bond_pattern)
        
        fatty_acid_type = ""
        if has_double_bonds:
            fatty_acid_type = "unsaturated"
        else:
            fatty_acid_type = "saturated"

        # Any acyl chain can be considered a fatty acid for this class
        return True, f"Valid fatty acyl-L-carnitine with {fatty_acid_type} fatty acid ({carbon_count} carbons)"

    return False, "Missing fatty acid component"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:176910',
                          'name': 'fatty acyl-L-carnitine',
                          'definition': 'Any O-acylcarnitine in which the '
                                        'carnitine component has '
                                        'L-configuration and the acyl group is '
                                        'a fatty acid.',
                          'parents': ['CHEBI:61697', 'CHEBI:75659']},
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
               "[('CCCCCCCCCCCCCCCC(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', 'Acyl "
               "chain too short to be considered a fatty acid'), "
               "('C[N+](C)(C)C[C@@H](CC([O-])=O)OC([*])=O', 'Acyl chain too "
               "short to be considered a fatty acid'), "
               "('C[N+](C)(C)C[C@@H](CC([O-])=O)OC([*])=O', 'Acyl chain too "
               "short to be considered a fatty acid'), "
               "('O([C@@H](C[N+](C([2H])([2H])[2H])(C)C)CC([O-])=O)C(=O)CC', "
               "'Acyl chain too short to be considered a fatty acid'), "
               "('C[N+](C)(C)C[C@@H](CC([O-])=O)OC([*])=O', 'Acyl chain too "
               "short to be considered a fatty acid'), "
               "('[C@H](OC(*)=O)(C[N+](C([2H])([2H])[2H])(C)C)CC(=O)[O-]', "
               "'Acyl chain too short to be considered a fatty acid'), "
               "('CCCC\\\\C=C/CCCCCCCC(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', "
               "'Acyl chain too short to be considered a fatty acid')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 98915,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.9989901234069197}