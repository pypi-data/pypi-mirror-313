"""
Classifies: CHEBI:167055 Jasmonate derivatives
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_Jasmonate_derivatives(smiles: str):
    """
    Determines if a molecule is a jasmonate derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a jasmonate derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Core structure requirements:
    # 1. Must have a cyclopentanone ring
    # 2. Must have a carboxylic acid or ester group
    # 3. Must have an alkyl chain

    # Check for cyclopentanone ring
    ring_info = mol.GetRingInfo()
    has_5_ring = False
    for ring in ring_info.AtomRings():
        if len(ring) == 5:
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if ring contains a ketone
            for atom in ring_atoms:
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 0:
                        has_5_ring = True
                        break
                if has_5_ring:
                    break

    if not has_5_ring:
        return False, "Missing cyclopentanone ring"

    # Check for carboxylic acid or ester group
    has_acid_or_ester = False
    patt_acid = Chem.MolFromSmarts('C(=O)O')
    patt_ester = Chem.MolFromSmarts('C(=O)OC')
    
    if mol.HasSubstructMatch(patt_acid) or mol.HasSubstructMatch(patt_ester):
        has_acid_or_ester = True

    if not has_acid_or_ester:
        return False, "Missing carboxylic acid or ester group"

    # Check for alkyl chain (at least 3 carbons)
    # First, make copy of molecule and remove the cyclopentanone ring
    mol_copy = Chem.RWMol(mol)
    ring_atoms = set()
    for ring in ring_info.AtomRings():
        if len(ring) == 5:
            ring_atoms.update(ring)
    
    # Count continuous carbon chain length
    max_chain = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetIdx() not in ring_atoms:
            visited = set()
            def dfs(atom_idx, chain_len):
                nonlocal max_chain
                visited.add(atom_idx)
                max_chain = max(max_chain, chain_len)
                
                atom = mol.GetAtomWithIdx(atom_idx)
                for neighbor in atom.GetNeighbors():
                    n_idx = neighbor.GetIdx()
                    if (neighbor.GetSymbol() == 'C' and 
                        n_idx not in visited and 
                        n_idx not in ring_atoms):
                        dfs(n_idx, chain_len + 1)
                        
            dfs(atom.GetIdx(), 1)

    if max_chain < 3:
        return False, "Missing required alkyl chain (minimum 3 carbons)"

    return True, "Contains cyclopentanone ring, carboxylic acid/ester group, and alkyl chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:167055',
                          'name': 'Jasmonate derivatives',
                          'definition': 'Any octanoid that is derived from '
                                        'jasmonate.',
                          'parents': ['CHEBI:36326']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_negatives': 1309,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9291282778171509}