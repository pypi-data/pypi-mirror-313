"""
Classifies: CHEBI:22645 arenecarboxamide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_arenecarboxamide(smiles: str):
    """
    Determines if a molecule is an arenecarboxamide (a monocarboxylic acid amide 
    in which the amide linkage is bonded directly to an arene ring system).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an arenecarboxamide, False otherwise
        str: Reason for classification
    """
    # Convert SMILES to RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for amide groups
    amide_pattern = Chem.MolFromSmarts('[C;!$(C=[!#6])]=O[NH][#6]')
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    
    if not amide_matches:
        return False, "No amide groups found"

    # For each amide group, check if carbonyl carbon is directly bonded to an aromatic ring
    for match in amide_matches:
        carbonyl_carbon = mol.GetAtomWithIdx(match[0])
        
        # Get neighbors of carbonyl carbon
        neighbors = [n for n in carbonyl_carbon.GetNeighbors() if n.GetIdx() not in match]
        
        # Check if any neighbor is part of an aromatic ring
        for neighbor in neighbors:
            if neighbor.GetIsAromatic():
                # Get the aromatic ring containing this atom
                ring_info = mol.GetRingInfo()
                for ring in ring_info.AtomRings():
                    if neighbor.GetIdx() in ring:
                        # Verify all atoms in ring are aromatic
                        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
                        if all(atom.GetIsAromatic() for atom in ring_atoms):
                            return True, "Found amide group directly bonded to aromatic ring"

    return False, "No amide groups directly bonded to aromatic rings found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22645',
                          'name': 'arenecarboxamide',
                          'definition': 'A monocarboxylic acid amide in which '
                                        'the amide linkage is bonded directly '
                                        'to an arene ring system.',
                          'parents': ['CHEBI:29347', 'CHEBI:62733']},
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
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.0}