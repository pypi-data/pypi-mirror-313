"""
Classifies: CHEBI:18179 phosphoinositide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phosphoinositide(smiles: str):
    """
    Determines if a molecule is a phosphoinositide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phosphoinositide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of inositol ring
    inositol_pattern = Chem.MolFromSmarts('[C@H]1[C@H](O)[C@H](O)[C@@H]([C@H]([C@H]1O)O)O')
    if not mol.HasSubstructMatch(inositol_pattern):
        return False, "No inositol ring found"
        
    # Check for glycerol backbone with phosphate link
    glycerol_phosphate = Chem.MolFromSmarts('CC(=O)OCC(COP(O)(=O)O)OC(=O)C')
    if not mol.HasSubstructMatch(glycerol_phosphate):
        return False, "No glycerophosphate backbone found"

    # Count phosphate groups
    phosphate_pattern = Chem.MolFromSmarts('OP(O)(O)=O')
    matches = mol.GetSubstructMatches(phosphate_pattern)
    
    # Need at least 1 phosphate group on inositol
    if len(matches) < 1:
        return False, "No phosphate groups found on inositol"
        
    # Check fatty acid chains
    fatty_acid = Chem.MolFromSmarts('C(=O)CCCCC')
    if not mol.HasSubstructMatch(fatty_acid):
        return False, "No fatty acid chains found"
        
    num_phosphates = len(matches) - 1 # Subtract 1 for glycerol phosphate

    # Find inositol ring atoms
    inositol_matches = mol.GetSubstructMatches(inositol_pattern)
    if len(inositol_matches) > 0:
        inositol_atoms = list(inositol_matches[0])
        
        # Count phosphates attached to inositol ring
        positions = []
        for match in matches:
            for atom_idx in match:
                atom = mol.GetAtomWithIdx(atom_idx)
                if atom.GetSymbol() == 'O':
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetIdx() in inositol_atoms:
                            pos = inositol_atoms.index(neighbor.GetIdx()) + 1
                            positions.append(str(pos))
                            break
    
    positions = list(set(positions))
    positions.sort()
    
    if len(positions) == 0:
        return False, "No phosphate groups found on inositol ring"
    
    return True, f"Phosphoinositide with {len(positions)} phosphate group(s) at position(s) {','.join(positions)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18179',
                          'name': 'phosphoinositide',
                          'definition': 'Any phosphatidylinositol that is '
                                        'phosphorylated at one or more of the '
                                        'hydroxy groups of inositol.',
                          'parents': ['CHEBI:28874']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.rdmolops' has no attribute "
               "'FindAtomRings'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 38636,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9974186886938565}