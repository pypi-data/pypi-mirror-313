"""
Classifies: CHEBI:23247 cinnamamides
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_cinnamamides(smiles: str):
    """
    Determines if a molecule is a cinnamamide derivative.
    Cinnamamides contain:
    - An amide group (-C(=O)N-)
    - A double bond conjugated with the amide carbonyl
    - A phenyl ring conjugated with the double bond
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cinnamamide, False otherwise
        str: Reason for classification
    """
    
    # Check valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for amide group
    amide_pattern = Chem.MolFromSmarts('[CX3](=[OX1])[NX3]')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide group found"

    # Look for conjugated double bond and phenyl pattern
    cinnamamide_pattern = Chem.MolFromSmarts('[CX3](=[OX1])[NX3]-,=[#6]-[#6]=[#6]-[cX3]1[cX3][cX3][cX3][cX3][cX3]1')
    
    if not mol.HasSubstructMatch(cinnamamide_pattern):
        return False, "Missing required cinnamamide substructure (conjugated double bond and phenyl ring)"

    # Get the matches
    matches = mol.GetSubstructMatches(cinnamamide_pattern)
    
    # Check stereochemistry of double bond if explicit
    has_explicit_stereochem = False
    for match in matches:
        bond_atoms = mol.GetBondBetweenAtoms(match[3], match[4])
        if bond_atoms.GetStereo() in [Chem.BondStereo.STEREOE, Chem.BondStereo.STEREOZ]:
            has_explicit_stereochem = True
            
    stereo_msg = " (with explicit double bond stereochemistry)" if has_explicit_stereochem else " (no explicit double bond stereochemistry)"

    # Look for substituents
    base_cinnamamide = Chem.MolFromSmiles("NC(=O)C=Cc1ccccc1")
    if Chem.MolToSmiles(mol) == Chem.MolToSmiles(base_cinnamamide):
        return True, "Unsubstituted cinnamamide" + stereo_msg
    else:
        return True, "Substituted cinnamamide derivative" + stereo_msg


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23247',
                          'name': 'cinnamamides',
                          'definition': 'An enamide which is cinnamamide or a '
                                        'derivative of cinnamamide obtained by '
                                        'replacement of one or more of its '
                                        'hydrogens.',
                          'parents': ['CHEBI:51751']},
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
    'num_true_negatives': 146702,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9992643552891493}