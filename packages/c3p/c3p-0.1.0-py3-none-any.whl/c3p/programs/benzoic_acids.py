"""
Classifies: CHEBI:22723 benzoic acids
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_benzoic_acids(smiles: str):
    """
    Determines if a molecule is a benzoic acid (benzene with at least one carboxy substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a benzoic acid, False otherwise
        str: Reason for classification
    """
    # Convert SMILES to RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Check for presence of benzene ring
    benzene_pattern = Chem.MolFromSmarts('c1ccccc1')
    if not mol.HasSubstructMatch(benzene_pattern):
        return False, "No benzene ring found"

    # Get matches for both patterns
    acid_matches = mol.GetSubstructMatches(carboxylic_acid_pattern)
    benzene_matches = mol.GetSubstructMatches(benzene_pattern)

    # Check if carboxylic acid is directly attached to benzene ring
    for acid_match in acid_matches:
        acid_carbon = acid_match[0]  # Get carbon atom index of COOH
        for benzene_match in benzene_matches:
            if acid_carbon in [mol.GetAtomWithIdx(i).GetNeighbors()[0].GetIdx() for i in benzene_match]:
                # Count number of carboxylic acid groups attached to benzene
                acid_count = sum(1 for match in acid_matches 
                               if match[0] in [mol.GetAtomWithIdx(i).GetNeighbors()[0].GetIdx() 
                                             for i in benzene_match])
                
                # Get other substituents on benzene ring
                substituents = []
                for ring_atom_idx in benzene_match:
                    atom = mol.GetAtomWithIdx(ring_atom_idx)
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetIdx() not in benzene_match:
                            if neighbor.GetSymbol() != 'H':  # Ignore hydrogens
                                substituents.append(neighbor.GetSymbol())
                
                if acid_count == 1:
                    if len(substituents) > 1:  # Has other substituents besides COOH
                        return True, f"Substituted benzoic acid with {len(substituents)} substituents"
                    else:
                        return True, "Unsubstituted benzoic acid"
                else:
                    return True, f"Benzoic acid with {acid_count} carboxylic acid groups"
                
    return False, "Carboxylic acid group not directly attached to benzene ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22723',
                          'name': 'benzoic acids',
                          'definition': 'Any aromatic carboxylic acid that '
                                        'consists of benzene in which at least '
                                        'a single hydrogen has been '
                                        'substituted by a carboxy group.',
                          'parents': ['CHEBI:22712', 'CHEBI:33859']},
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
    'num_true_positives': 27,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.2125984251968504,
    'f1': 0.35064935064935066,
    'accuracy': 0.2125984251968504}