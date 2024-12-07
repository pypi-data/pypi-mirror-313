"""
Classifies: CHEBI:21507 N-acetyl-D-galactosaminyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_N_acetyl_D_galactosaminyl_group(smiles: str):
    """
    Determines if a molecule contains an N-acetyl-D-galactosaminyl group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains N-acetyl-D-galactosaminyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for pyranose ring (6-membered sugar ring)
    rings = mol.GetRingInfo()
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered sugar ring found"
        
    # Pattern for N-acetyl-D-galactosaminyl group core structure
    # [C] represents any carbon (for potential glycosidic linkages)
    pattern = Chem.MolFromSmarts('[C][C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1NC(=O)C')
    
    if mol.HasSubstructMatch(pattern):
        # Check configuration and substituents
        matches = mol.GetSubstructMatches(pattern)
        for match in matches:
            # Check for acetyl group
            n_idx = [i for i, idx in enumerate(match) if mol.GetAtomWithIdx(idx).GetSymbol() == 'N'][0]
            n_atom = mol.GetAtomWithIdx(match[n_idx])
            
            has_acetyl = False
            for neighbor in n_atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C':
                    for c_neighbor in neighbor.GetNeighbors():
                        if c_neighbor.GetSymbol() == 'O' and c_neighbor.GetNumExplicitHs() == 0:
                            has_acetyl = True
                            break
            
            if not has_acetyl:
                continue
                
            # Check for glycosidic linkages
            glycosidic_bonds = 0
            for atom in mol.GetAtoms():
                if atom.GetSymbol() == 'O' and not atom.IsInRing():
                    if len(atom.GetNeighbors()) == 2:
                        c1, c2 = atom.GetNeighbors()
                        if c1.GetSymbol() == 'C' and c2.GetSymbol() == 'C':
                            glycosidic_bonds += 1
            
            if glycosidic_bonds > 0:
                return True, "N-acetyl-D-galactosaminyl group with additional glycosidic linkages"
            else:
                return True, "N-acetyl-D-galactosaminyl group"
                
    return False, "No N-acetyl-D-galactosaminyl group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21507',
                          'name': 'N-acetyl-D-galactosaminyl group',
                          'definition': 'A galactosaminyl group '
                                        '(D-configuration) in which the amino '
                                        'group at C-2 is acetylated. The group '
                                        'may be substituted with further mono- '
                                        'or oligo-saccharide groups.',
                          'parents': ['CHEBI:24160']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 2,
    'num_true_negatives': 183905,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.3333333333333333,
    'recall': 0.5,
    'f1': 0.4,
    'accuracy': 0.9999836875846206}