"""
Classifies: CHEBI:16180 N-acylglycine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_N_acylglycine(smiles: str):
    """
    Determines if a molecule is an N-acylglycine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-acylglycine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Pattern for N-acylglycine: R-C(=O)-NH-CH2-C(=O)-OH
    # SMARTS pattern to match N-acylglycine core structure
    pattern = Chem.MolFromSmarts('[#6,*]C(=O)NCC(=O)O')
    
    if not mol.HasSubstructMatch(pattern):
        return False, "Does not contain N-acylglycine core structure"
    
    # Get all matches
    matches = mol.GetSubstructMatches(pattern)
    
    for match in matches:
        # Get relevant atoms
        r_group = mol.GetAtomWithIdx(match[0])  # R group
        acyl_c = mol.GetAtomWithIdx(match[1])   # Acyl carbon
        n_atom = mol.GetAtomWithIdx(match[3])   # Nitrogen atom
        ch2_c = mol.GetAtomWithIdx(match[4])    # CH2 carbon
        carboxyl_c = mol.GetAtomWithIdx(match[5]) # Carboxyl carbon
        carboxyl_o = mol.GetAtomWithIdx(match[6]) # Carboxyl oxygen

        # Verify nitrogen connectivity
        if n_atom.GetDegree() != 2:
            continue
            
        # Verify CH2 group
        if ch2_c.GetDegree() != 2 or ch2_c.GetTotalNumHs() != 2:
            continue
            
        # Verify acyl carbon
        if acyl_c.GetDegree() != 3:
            continue
            
        # Verify carboxyl group
        if carboxyl_c.GetDegree() != 3 or carboxyl_o.GetDegree() != 1:
            continue

        # If all checks pass, determine substituent type
        if r_group.GetIsAromatic():
            return True, "N-acylglycine with aromatic substituent"
        else:
            return True, "N-acylglycine with aliphatic substituent"
            
    return False, "Structure does not match N-acylglycine requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16180',
                          'name': 'N-acylglycine',
                          'definition': 'An N-acyl-amino acid in which amino '
                                        'acid specified is glycine.',
                          'parents': [   'CHEBI:140325',
                                         'CHEBI:24373',
                                         'CHEBI:51569']},
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
               'False negatives: '
               "[('O1C(C=2C=C([N+]([O-])=O)C=CC2)=CC=C1/C=C(\\\\NC(=O)C3=CC=C(C=C3)C)/C(=O)NCCCN(C)C', "
               "'Does not contain N-acylglycine core structure'), "
               "('O=C(NC(C(=O)N(CCCNC(=O)C1=C(O)C(O)=CC=C1)CCCCNC(=O)C2=C(O)C(O)=CC=C2)C(O)C)C3=C(O)C=CC=C3', "
               "'Does not contain N-acylglycine core structure'), "
               "('OC(=O)CNC(=O)Cc1ccc(O)cc1', 'Structure does not match "
               "N-acylglycine requirements'), ('N(CC(O)=O)C(*)=O', 'Structure "
               "does not match N-acylglycine requirements'), "
               "('C\\\\C=C(/C)C(=O)NCC(O)=O', 'Structure does not match "
               "N-acylglycine requirements'), ('N(CC(O)=O)C(*)=O', 'Structure "
               "does not match N-acylglycine requirements'), "
               "('CCC(C)C(=O)NCC(O)=O', 'Structure does not match "
               "N-acylglycine requirements'), ('CC(C)CC(=O)NCC(O)=O', "
               "'Structure does not match N-acylglycine requirements'), "
               "('OC(=O)CNC(=O)CC1=CNC2=CC=C(O)C=C12', 'Structure does not "
               "match N-acylglycine requirements'), "
               "('ClC=1C=C(C(=O)NCC(O)=O)C=CC1', 'Structure does not match "
               "N-acylglycine requirements'), ('CC(C)C(=O)NCC(O)=O', "
               "'Structure does not match N-acylglycine requirements'), "
               "('O1C=CC=C1C(NCC(O)=O)=O', 'Structure does not match "
               "N-acylglycine requirements')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 10,
    'num_false_positives': 100,
    'num_true_negatives': 17719,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 0.8333333333333334,
    'f1': 0.16393442622950818,
    'accuracy': 0.9942796253715439}