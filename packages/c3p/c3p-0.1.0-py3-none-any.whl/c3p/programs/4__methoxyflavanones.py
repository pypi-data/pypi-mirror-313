"""
Classifies: CHEBI:140332 4'-methoxyflavanones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_4__methoxyflavanones(smiles: str):
    """
    Determines if a molecule is a 4'-methoxyflavanone (methoxyflavanone with methoxy at position 4').
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 4'-methoxyflavanone, False otherwise
        str: Reason for classification
    """
    # Check if SMILES is valid
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define flavanone core SMARTS pattern
    # Matches the basic flavanone skeleton with B-ring (4' position) marked with [#0]
    flavanone_pattern = Chem.MolFromSmarts('[O;H0]1[c;H0]2[c;H0]([cH,$(c(C))]([cH,$(c(C))])([cH,$(c(C))])[cH,$(c(C))])C(=O)C[CH]([#0]3[cH,$(c(C))][cH,$(c(C))][cH,$(c(C))][cH,$(c(C))][cH,$(c(C))]3)O2')
    
    # Define methoxy group SMARTS pattern
    methoxy_pattern = Chem.MolFromSmarts('OC')

    # Check if molecule contains flavanone core
    matches = mol.GetSubstructMatches(flavanone_pattern)
    if not matches:
        return False, "Not a flavanone structure"

    # For each flavanone core match found
    for match in matches:
        # Get the atom index corresponding to the 4' position (marked with [#0] in SMARTS)
        b_ring_pos = None
        for i, idx in enumerate(match):
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() == 0:  # Dummy atom in SMARTS
                b_ring_pos = idx
                break
                
        if b_ring_pos is None:
            continue

        # Find all methoxy groups
        methoxy_matches = mol.GetSubstructMatches(methoxy_pattern)
        
        # Check if any methoxy group is attached to 4' position
        for methoxy_match in methoxy_matches:
            # Get the oxygen atom of methoxy group
            o_atom = mol.GetAtomWithIdx(methoxy_match[0])
            
            # Check if this methoxy is attached to the 4' position
            for neighbor in o_atom.GetNeighbors():
                if neighbor.GetIdx() == b_ring_pos:
                    return True, "Found methoxy group at 4' position of flavanone"

    return False, "No methoxy group found at 4' position of flavanone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140332',
                          'name': "4'-methoxyflavanones",
                          'definition': 'Any methoxyflavanone having a methoxy '
                                        "substituent located at position 4'.",
                          'parents': ['CHEBI:25240']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': False,
    'best': True,
    'error': 'Python argument types in\n'
             '    Mol.GetSubstructMatches(Mol, NoneType)\n'
             'did not match C++ signature:\n'
             '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
             'query, RDKit::SubstructMatchParameters params)\n'
             '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
             'RDKit::SubstructMatchParameters params)\n'
             '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
             'query, bool uniquify=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False, unsigned int maxMatches=1000)\n'
             '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
             'bool uniquify=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False, unsigned int maxMatches=1000)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}