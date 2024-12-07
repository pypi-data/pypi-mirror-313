"""
Classifies: CHEBI:26819 sulfuric ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_sulfuric_ester(smiles: str):
    """
    Determines if a molecule is a sulfuric ester (ester of an alcohol and sulfuric acid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sulfuric ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Look for sulfuric ester pattern: R-O-S(=O)(=O)-O
    pattern = Chem.MolFromSmarts('[C,c]-[O;X2][S;X4](=[O;X1])(=[O;X1])[O;X2,X1]')
    if not mol.HasSubstructMatch(pattern):
        return False, "No sulfuric ester group found"

    # Count number of sulfate groups
    matches = mol.GetSubstructMatches(pattern)
    num_sulfates = len(matches)

    # Get atoms involved in sulfate groups
    sulfate_atoms = []
    for match in matches:
        sulfate_atoms.extend(match)
    
    # Verify connectivity
    for match in matches:
        s_atom = mol.GetAtomWithIdx(match[2])  # Sulfur atom
        o_atoms = [mol.GetAtomWithIdx(i) for i in [match[1], match[3], match[4]]]  # Oxygen atoms
        
        # Check sulfur oxidation state (+6)
        if s_atom.GetTotalValence() != 6:
            return False, "Invalid sulfur oxidation state"
            
        # Check oxygen connectivity
        for o_atom in o_atoms:
            if o_atom.GetTotalValence() > 2:
                return False, "Invalid oxygen connectivity"

    if num_sulfates == 1:
        return True, "Contains 1 sulfuric ester group"
    else:
        return True, f"Contains {num_sulfates} sulfuric ester groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26819',
                          'name': 'sulfuric ester',
                          'definition': 'An ester of an alcohol and sulfuric '
                                        'acid.',
                          'parents': ['CHEBI:35701', 'CHEBI:37826']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
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
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 79,
    'num_false_positives': 100,
    'num_true_negatives': 12970,
    'num_false_negatives': 30,
    'num_negatives': None,
    'precision': 0.441340782122905,
    'recall': 0.7247706422018348,
    'f1': 0.548611111111111,
    'accuracy': 0.9901358221412854}