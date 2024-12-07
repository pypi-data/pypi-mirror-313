"""
Classifies: CHEBI:24783 imine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_imine(smiles: str):
    """
    Determines if a molecule contains an imine group (C=N-R where R = H or hydrocarbyl).
    Imines include compounds having the structure RN=CR2 (R = H, hydrocarbyl).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains imine group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for imine group: carbon double bonded to nitrogen
    # Exclude cases where:
    # - N is in ring
    # - N has >2 bonds
    # - C is part of C=O group
    imine_pattern = Chem.MolFromSmarts('[C!$(C=O)]=[$([N!R;D1,D2;!$(N=C[N,O,S])])]')
    
    matches = mol.GetSubstructMatches(imine_pattern)
    
    if not matches:
        return False, "No imine groups found"

    imine_groups = []
    for match in matches:
        c_atom = mol.GetAtomWithIdx(match[0])
        n_atom = mol.GetAtomWithIdx(match[1])
        
        # Skip if either atom is aromatic
        if c_atom.GetIsAromatic() or n_atom.GetIsAromatic():
            continue
            
        # Skip if N has more than 2 neighbors
        if len(list(n_atom.GetNeighbors())) > 2:
            continue

        # Check if it's aldimine (RCH=NR) or ketimine (R2C=NR)
        c_h_count = c_atom.GetTotalNumHs()
        if c_h_count >= 1:
            imine_type = "aldimine"
        else:
            imine_type = "ketimine"
        imine_groups.append(imine_type)

    if imine_groups:
        if len(imine_groups) == 1:
            return True, f"Contains one {imine_groups[0]} group"
        else:
            return True, f"Contains multiple imine groups: {', '.join(imine_groups)}"
    
    return False, "No imine groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24783',
                          'name': 'imine',
                          'definition': 'Compounds having the structure RN=CR2 '
                                        '(R = H, hydrocarbyl). Thus analogues '
                                        'of aldehydes or ketones, having NR '
                                        'doubly bonded to carbon; aldimines '
                                        'have the structure RCH=NR, ketimines '
                                        "have the structure R'2C=NR (where R' "
                                        'is not H). Imines include azomethines '
                                        'and Schiff bases. Imine is used as a '
                                        'suffix in systematic nomenclature to '
                                        'denote the C=NH group excluding the '
                                        'carbon atom.',
                          'parents': ['CHEBI:35352', 'CHEBI:50860']},
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
               "False negatives: [('Oc1ccccc1C=N', 'No imine groups found'), "
               "('OC(C(O)C=N)CO', 'No imine groups found'), "
               "('O=C1NC(=O)C(=C1CC)C', 'No imine groups found'), "
               "('CC(=O)N=C1C=CC(=O)C=C1', 'No imine groups found'), "
               "('C1(=C(C2=CC=C(C=C2)N(C)C)C3=CC=C(C=C3)N(C)C)C=CC(=N)C=C1', "
               "'No imine groups found'), "
               "('Oc1ccc(cc1)N=C1C=C(Cl)C(=O)C(Cl)=C1', 'No imine groups "
               "found'), ('Nc1ccc(cc1)C(c1ccc(N)cc1)=C1C=CC(=N)C=C1', 'No "
               "imine groups found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 11038,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 0.8571428571428571,
    'f1': 0.10619469026548672,
    'accuracy': 0.9909376401973979}