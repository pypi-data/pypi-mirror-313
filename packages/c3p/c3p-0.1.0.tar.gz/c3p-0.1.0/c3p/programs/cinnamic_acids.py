"""
Classifies: CHEBI:23252 cinnamic acids
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_cinnamic_acids(smiles: str):
    """
    Determines if a molecule is a cinnamic acid or derivative.
    Cinnamic acids are alpha,beta-unsaturated monocarboxylic acids based on the cinnamic acid skeleton.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cinnamic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Look for conjugated double bond pattern (alpha,beta-unsaturated)
    conjugated_pattern = Chem.MolFromSmarts('C(=O)[OH]C=C')
    if not mol.HasSubstructMatch(conjugated_pattern):
        return False, "No conjugated double bond found"

    # Look for aromatic ring connected to conjugated system
    aromatic_pattern = Chem.MolFromSmarts('C(=O)[OH]C=Cc1ccccc1')
    if not mol.HasSubstructMatch(aromatic_pattern):
        return False, "No aromatic ring connected to conjugated system"

    # Count substituents on aromatic ring
    substituents = []
    aromatic_matches = mol.GetSubstructMatches(Chem.MolFromSmarts('c1ccccc1'))
    
    if aromatic_matches:
        ring_atoms = set(aromatic_matches[0])
        for atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms:
                    if neighbor.GetSymbol() != 'H':  # Ignore hydrogens
                        substituents.append(neighbor.GetSymbol())

    # Classify based on substituents
    if len(substituents) == 0:
        return True, "Unsubstituted cinnamic acid"
    else:
        return True, f"Substituted cinnamic acid with substituents on aromatic ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23252',
                          'name': 'cinnamic acids',
                          'definition': 'Any alpha,beta-unsaturated '
                                        'monocarboxylic acid based on the '
                                        'cinnamic acid skeleton and its '
                                        'substituted derivatives.',
                          'parents': ['CHEBI:78840', 'CHEBI:79020']},
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
    'num_true_negatives': 183604,
    'num_false_negatives': 33,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998202976524339}