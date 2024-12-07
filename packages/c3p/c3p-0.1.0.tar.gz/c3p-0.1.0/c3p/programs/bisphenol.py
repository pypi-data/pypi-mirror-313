"""
Classifies: CHEBI:22901 bisphenol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_bisphenol(smiles: str):
    """
    Determines if a molecule is a bisphenol compound.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a bisphenol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of at least 2 phenol groups
    phenol_pattern = Chem.MolFromSmarts('[OH]c1ccc([#6])cc1')
    phenol_matches = mol.GetSubstructMatches(phenol_pattern)
    
    if len(phenol_matches) < 2:
        return False, "Does not contain at least 2 phenol groups"
    
    # Check if the phenol groups are connected through a central carbon/heteroatom
    # Pattern looks for 2 phenols connected through any atom
    bisphenol_pattern = Chem.MolFromSmarts('[OH]c1ccc([#6]([*])[#6]c2ccc([OH])cc2)cc1')
    bisphenol_matches = mol.GetSubstructMatches(bisphenol_pattern)
    
    if not bisphenol_matches:
        return False, "Phenol groups not properly connected through central atom"
        
    # Get the central connecting atom
    for match in bisphenol_matches:
        # The central atom is at position 5 in the SMARTS pattern
        central_atom = mol.GetAtomWithIdx(match[5])
        central_atom_symbol = central_atom.GetSymbol()
        
        # Count substituents on central atom
        substituents = []
        for neighbor in central_atom.GetNeighbors():
            if neighbor.GetIdx() not in [match[4], match[7]]:  # Exclude phenol carbons
                substituents.append(neighbor.GetSymbol())
                
        if central_atom_symbol == 'C':
            return True, f"Bisphenol with carbon bridge and substituents: {', '.join(substituents)}"
        else:
            return True, f"Bisphenol with {central_atom_symbol} bridge and substituents: {', '.join(substituents)}"
            
    return False, "Structure does not match bisphenol pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22901',
                          'name': 'bisphenol',
                          'definition': 'By usage, the methylenediphenols, '
                                        'HOC6H4CH2C6H4OH, commonly '
                                        'p,p-methylenediphenol, and their '
                                        'substitution products (generally '
                                        'derived from condensation of two '
                                        'equivalent amounts of a phenol with '
                                        'an aldehyde or ketone). The term also '
                                        'includes analogues in the the '
                                        'methylene (or substituted methylene) '
                                        'group has been replaced by a '
                                        'heteroatom.',
                          'parents': ['CHEBI:33853']},
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
    'num_true_positives': 0,
    'num_false_positives': 100,
    'num_true_negatives': 62562,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9983722711604749}