"""
Classifies: CHEBI:23217 cholines
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cholines(smiles: str):
    """
    Determines if a molecule is a choline or choline derivative.
    A choline is defined as a quaternary ammonium ion based on the choline ion and its substituted derivatives.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a choline, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for N+ with exactly 4 bonds
    n_plus = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetFormalCharge() == 1 and len(atom.GetBonds()) == 4:
            # Check if N+ has 3 methyl groups
            methyl_count = 0
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 1:
                    methyl_count += 1
            if methyl_count == 3:
                n_plus = True
                break
    
    if not n_plus:
        return False, "No quaternary ammonium ion (N+ with 3 methyl groups) found"

    # Look for phosphate group
    phosphate = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'P':
            phosphate = True
            break
            
    if not phosphate:
        return False, "No phosphate group found"

    # Look for O-P-O-C-C-N+ linkage
    substructure = Chem.MolFromSmarts('[O]-[P]-[O]-[C]-[C]-[N+]')
    if not mol.HasSubstructMatch(substructure):
        return False, "Missing O-P-O-C-C-N+ linkage characteristic of cholines"

    return True, "Contains quaternary ammonium ion with 3 methyl groups, phosphate group, and O-P-O-C-C-N+ linkage"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23217',
                          'name': 'cholines',
                          'definition': 'A quaternary ammonium ion based on '
                                        'the choline ion and its substituted '
                                        'derivatives thereof.',
                          'parents': ['CHEBI:35267']},
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
    'num_true_positives': 215,
    'num_false_positives': 100,
    'num_true_negatives': 124885,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.6825396825396826,
    'recall': 0.9953703703703703,
    'f1': 0.8097928436911487,
    'accuracy': 0.9991932971781375}