"""
Classifies: CHEBI:25990 phenylethanolamines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phenylethanolamines(smiles: str):
    """
    Determines if a molecule is a phenylethanolamine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phenylethanolamine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Look for the core pattern: phenyl-C(OH)-C-N
    pattern = Chem.MolFromSmarts('c1ccccc1[CH1]([OH1])[CH2][NH2,NH1,NH0]')
    if not mol.HasSubstructMatch(pattern):
        return False, "Missing core phenylethanolamine structure (phenyl-C(OH)-C-N)"
        
    # Get matches
    matches = mol.GetSubstructMatches(pattern)
    
    # Check each match
    for match in matches:
        phenyl_atoms = match[0:6]  # First 6 atoms are phenyl ring
        c_oh = match[6]  # Carbon with OH
        c_n = match[7]   # Carbon next to N
        n_atom = match[8] # N atom
        
        # Verify phenyl ring is aromatic
        phenyl_aromatic = all(mol.GetAtomWithIdx(i).GetIsAromatic() for i in phenyl_atoms)
        if not phenyl_aromatic:
            continue
            
        # Check if hydroxyl carbon is chiral (optional)
        c_oh_atom = mol.GetAtomWithIdx(c_oh)
        if c_oh_atom.GetChiralTag() != Chem.ChiralType.CHI_UNSPECIFIED:
            chirality = "with defined stereochemistry"
        else:
            chirality = "without defined stereochemistry"
            
        # Check for substitutions on phenyl ring
        phenyl_substituents = []
        for atom_idx in phenyl_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in phenyl_atoms and neighbor.GetIdx() != c_oh:
                    phenyl_substituents.append(neighbor.GetSymbol())
                    
        if phenyl_substituents:
            phenyl_desc = f"substituted phenyl ({', '.join(set(phenyl_substituents))})"
        else:
            phenyl_desc = "unsubstituted phenyl"
            
        return True, f"Phenylethanolamine {chirality} with {phenyl_desc} group"
        
    return False, "Structure does not match phenylethanolamine requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25990',
                          'name': 'phenylethanolamines',
                          'definition': 'An ethanolamine compound having a '
                                        'phenyl (substituted or unsubstituted) '
                                        'group on the carbon bearing the '
                                        'hydroxy substituent.',
                          'parents': ['CHEBI:23981']},
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
    'num_true_negatives': 87110,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9988533688024583}