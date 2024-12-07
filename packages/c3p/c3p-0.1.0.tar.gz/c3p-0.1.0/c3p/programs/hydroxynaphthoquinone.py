"""
Classifies: CHEBI:132155 hydroxynaphthoquinone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxynaphthoquinone(smiles: str):
    """
    Determines if a molecule is a hydroxynaphthoquinone.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxynaphthoquinone, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for naphthoquinone core
    # Two fused 6-membered rings where one ring has two carbonyls
    naphthoquinone_pattern = Chem.MolFromSmarts('O=C1C=CC(=O)c2ccccc12')
    
    # SMARTS pattern for hydroxyl group
    hydroxyl_pattern = Chem.MolFromSmarts('[OH]')

    # Check for naphthoquinone core
    if not mol.HasSubstructMatch(naphthoquinone_pattern):
        return False, "No naphthoquinone core structure found"

    # Check for hydroxyl groups
    if not mol.HasSubstructMatch(hydroxyl_pattern):
        return False, "No hydroxyl groups found"

    # Get matches
    nq_matches = mol.GetSubstructMatches(naphthoquinone_pattern)
    oh_matches = mol.GetSubstructMatches(hydroxyl_pattern)

    # Get number of hydroxyl groups
    num_hydroxyls = len(oh_matches)

    # Check if hydroxyls are attached to naphthoquinone core
    hydroxyls_on_core = False
    for nq_match in nq_matches:
        nq_atoms = set(nq_match)
        for oh_match in oh_matches:
            oh_atom = mol.GetAtomWithIdx(oh_match[0])
            for neighbor in oh_atom.GetNeighbors():
                if neighbor.GetIdx() in nq_atoms:
                    hydroxyls_on_core = True
                    break
            if hydroxyls_on_core:
                break
        if hydroxyls_on_core:
            break

    if not hydroxyls_on_core:
        return False, "No hydroxyl groups attached to naphthoquinone core"

    return True, f"Hydroxynaphthoquinone with {num_hydroxyls} hydroxyl group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132155',
                          'name': 'hydroxynaphthoquinone',
                          'definition': 'Any naphthoquinone in which the '
                                        'naphthaoquinone moiety is substituted '
                                        'by at least one hydroxy group.',
                          'parents': ['CHEBI:132130', 'CHEBI:25481']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               "False negatives: [('OC1=CC(=O)c2ccccc2C1=O', 'No "
               "naphthoquinone core structure found'), "
               "('CC(C)=CC[C@@H](OC(=O)C=C(C)C)C1=CC(=O)c2c(O)ccc(O)c2C1=O', "
               "'No naphthoquinone core structure found'), "
               "('COC1=C(C)C(=O)c2c(O)cc(OC\\\\C=C(/C)CCC=C(C)C)cc2C1=O', 'No "
               "naphthoquinone core structure found'), "
               "('COC1=C(C)C(=O)c2c(O)cc(O)cc2C1=O', 'No naphthoquinone core "
               "structure found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 44123,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9977389377529563}