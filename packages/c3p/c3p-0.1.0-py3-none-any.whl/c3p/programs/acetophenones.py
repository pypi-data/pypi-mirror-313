"""
Classifies: CHEBI:22187 acetophenones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_acetophenones(smiles: str):
    """
    Determines if a molecule is an acetophenone (PhC(=O)CH3) or substituted derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an acetophenone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # SMARTS pattern for acetophenone core structure:
    # Aromatic ring connected to C(=O)CH3
    acetophenone_pattern = Chem.MolFromSmarts('c1ccccc1C(=O)C')
    
    if not mol.HasSubstructMatch(acetophenone_pattern):
        return False, "No acetophenone core structure found"
        
    # Find all matches of the acetophenone pattern
    matches = mol.GetSubstructMatches(acetophenone_pattern)
    
    # For each match, check if it's a valid acetophenone
    for match in matches:
        # Get the aromatic ring atoms
        ring_atoms = match[:6]
        # Get the carbonyl carbon
        carbonyl_carbon = match[6]
        # Get the methyl carbon
        methyl_carbon = match[8]
        
        # Verify carbonyl group
        carbonyl_atom = mol.GetAtomWithIdx(carbonyl_carbon)
        if not any(bond.GetBondType() == Chem.BondType.DOUBLE and 
                  bond.GetOtherAtomIdx(carbonyl_carbon) != methyl_carbon
                  for bond in carbonyl_atom.GetBonds()):
            continue
            
        # Check substituents on aromatic ring
        ring_substituents = []
        for ring_atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(ring_atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms and \
                   neighbor.GetIdx() != carbonyl_carbon:
                    ring_substituents.append(neighbor.GetSymbol())
                    
        # If we get here, we found a valid acetophenone
        if len(ring_substituents) > 0:
            return True, f"Substituted acetophenone with ring substituents: {', '.join(set(ring_substituents))}"
        else:
            return True, "Unsubstituted acetophenone"
            
    return False, "Structure contains phenyl and carbonyl groups but not in acetophenone arrangement"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22187',
                          'name': 'acetophenones',
                          'definition': 'A class or aromatic ketone consisting '
                                        'of acetophenone, PhC(=O)CH3, and its '
                                        'substituted derivatives.',
                          'parents': ['CHEBI:51867', 'CHEBI:76224']},
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
    'num_true_positives': 13,
    'num_false_positives': 100,
    'num_true_negatives': 2879,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.11504424778761062,
    'recall': 0.7222222222222222,
    'f1': 0.19847328244274812,
    'accuracy': 0.964964964964965}