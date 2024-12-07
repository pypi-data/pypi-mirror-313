"""
Classifies: CHEBI:22682 azobenzenes
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_azobenzenes(smiles: str):
    """
    Determines if a molecule is an azobenzene (contains two phenyl rings linked by N=N).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an azobenzene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for N=N double bond
    azo_pattern = Chem.MolFromSmarts('[N]=[N]')
    if not mol.HasSubstructMatch(azo_pattern):
        return False, "No N=N double bond found"
    
    # Look for phenyl-N=N-phenyl pattern
    azobenzene_pattern = Chem.MolFromSmarts('c1ccccc1[N]=[N]c1ccccc1')
    if not mol.HasSubstructMatch(azobenzene_pattern):
        return False, "No phenyl-N=N-phenyl pattern found"

    # Get matches for the azobenzene pattern
    matches = mol.GetSubstructMatches(azobenzene_pattern)
    
    # Look for substituents on the phenyl rings
    substituents = []
    for match in matches:
        # Get the atoms in the phenyl rings (first 6 and last 6 atoms in match)
        ring1_atoms = set(match[:6])
        ring2_atoms = set(match[-6:])
        
        # Check substituents on both rings
        for ring_atoms in [ring1_atoms, ring2_atoms]:
            for atom_idx in ring_atoms:
                atom = mol.GetAtomWithIdx(atom_idx)
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetIdx() not in ring_atoms and neighbor.GetIdx() not in match:
                        # Add substituent type to list
                        substituent = neighbor.GetSymbol()
                        if substituent not in substituents:
                            substituents.append(substituent)

    if len(substituents) > 0:
        return True, f"Azobenzene with substituents: {', '.join(substituents)}"
    else:
        return True, "Unsubstituted azobenzene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22682',
                          'name': 'azobenzenes',
                          'definition': 'Any member of the wide class of '
                                        'molecules that share the core '
                                        'azobenzene structure, comprising two '
                                        'phenyl rings linked by a N=N double '
                                        'bond, which may have different '
                                        'functional groups extending from the '
                                        'rings.',
                          'parents': ['CHEBI:22712', 'CHEBI:37533']},
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
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 142106,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 0.875,
    'f1': 0.12173913043478259,
    'accuracy': 0.9992898026917181}