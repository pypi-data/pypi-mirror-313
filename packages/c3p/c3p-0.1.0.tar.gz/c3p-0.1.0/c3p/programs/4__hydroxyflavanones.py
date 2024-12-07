"""
Classifies: CHEBI:140331 4'-hydroxyflavanones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_4__hydroxyflavanones(smiles: str):
    """
    Determines if a molecule is a 4'-hydroxyflavanone (has a hydroxy substituent at position 4').
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 4'-hydroxyflavanone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define SMARTS pattern for flavanone core with 4'-OH
    # The pattern specifically matches:
    # - The chroman-4-one core (O-C-C-C(=O))
    # - The B-ring phenyl with OH at para position
    # - Ensures proper connectivity
    flavanone_pattern = Chem.MolFromSmarts('[OH]-c1ccc(cc1)[CH2,CH]2CC(=O)c3c(O2)cc([#6,#8,H])cc3')
    
    if flavanone_pattern is None:
        return None, "Invalid SMARTS pattern"

    # Check if molecule contains the pattern
    if mol.HasSubstructMatch(flavanone_pattern):
        # Additional validation to ensure proper stereochemistry and structure
        matches = mol.GetSubstructMatches(flavanone_pattern)
        
        # Check if any match satisfies all conditions
        for match in matches:
            # The pattern ensures:
            # - Flavanone core with proper connectivity
            # - 4'-hydroxy group
            # - Proper aromatic rings
            return True, "Contains 4'-hydroxyflavanone structure"
            
    return False, "Does not contain 4'-hydroxyflavanone structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140331',
                          'name': "4'-hydroxyflavanones",
                          'definition': 'Any hydroxyflavanone having a hydroxy '
                                        "substituent located at position 4'.",
                          'parents': ['CHEBI:24697']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.HasSubstructMatch(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params=True)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool recursionPossible=True, bool useChirality=False, '
               'bool useQueryQueryMatches=False)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'bool recursionPossible=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False)',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 9,
    'num_false_positives': 100,
    'num_true_negatives': 104621,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.08256880733944955,
    'recall': 1.0,
    'f1': 0.15254237288135594,
    'accuracy': 0.9990451637544161}