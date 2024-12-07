"""
Classifies: CHEBI:142605 medium-chain primary fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_medium_chain_primary_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is a medium-chain primary fatty alcohol (C6-C12).
    Primary fatty alcohols have a single OH group at the end of a straight aliphatic chain.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a medium-chain primary fatty alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of primary alcohol group
    primary_alcohol = Chem.MolFromSmarts("[CH2][OH]")
    matches = mol.GetSubstructMatches(primary_alcohol)
    if len(matches) != 1:
        return False, "Must have exactly one primary alcohol group"
    
    # Get the carbon atom of the CH2OH group
    ch2_idx = matches[0][0]
    
    # Check if molecule is aromatic
    if any(atom.GetIsAromatic() for atom in mol.GetAtoms()):
        return False, "Contains aromatic rings"
        
    # Check for presence of non C,H,O atoms
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in ['C', 'O', 'H']:
            return False, "Contains elements other than C, H, O"
            
    # Check for carboxylic acids
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[CX3](=O)[OX2H1]")):
        return False, "Contains carboxylic acid group"
        
    # Check for esters
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[#6][CX3](=O)[OX2H0][#6]")):
        return False, "Contains ester group"
        
    # Check for ketones/aldehydes
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[CX3]=[OX1]")):
        return False, "Contains carbonyl group"

    # Check for presence of rings
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 0:
        return False, "Contains rings"
        
    # Check for unsaturation
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[#6]=[#6]")) or \
       mol.HasSubstructMatch(Chem.MolFromSmarts("[#6]#[#6]")):
        return False, "Contains unsaturated bonds"

    # Check for branching
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            neighbors = [n for n in atom.GetNeighbors() if n.GetSymbol() == 'C']
            if len(neighbors) > 2:
                return False, "Contains branched carbons"

    # Count carbons in longest chain containing the primary alcohol
    def get_chain_length(atom, visited):
        if atom.GetIdx() in visited:
            return 0
        visited.add(atom.GetIdx())
        max_length = 0
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                length = get_chain_length(neighbor, visited)
                max_length = max(max_length, length)
        return max_length + 1

    ch2_atom = mol.GetAtomWithIdx(ch2_idx)
    chain_length = get_chain_length(ch2_atom, set())

    if chain_length < 6 or chain_length > 12:
        return False, f"Carbon chain length ({chain_length}) outside C6-C12 range"

    # Count number of OH groups
    oh_groups = len(mol.GetSubstructMatches(Chem.MolFromSmarts("[OH]")))
    if oh_groups > 2:  # Allow up to 2 OH groups for diols
        return False, "Too many OH groups"

    return True, f"Medium-chain primary fatty alcohol with {chain_length} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:142605',
                          'name': 'medium-chain primary fatty alcohol',
                          'definition': 'Any primary fatty alcohol with a '
                                        'chain length between C6 and C12.',
                          'parents': ['CHEBI:142622']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.04545454545454545 is too low.\n'
               "True positives: [('CCCCCC(O)CCCCCCO', 'Medium-chain primary "
               "fatty alcohol with 12 carbons')]\n"
               "False positives: [('OC(CCCCCCCC)CO', 'Medium-chain primary "
               "fatty alcohol with 10 carbons'), ('CC(C)CCCCCCO', "
               "'Medium-chain primary fatty alcohol with 8 carbons'), "
               "('C(CCCCCCC)CCCO', 'Medium-chain primary fatty alcohol with 11 "
               "carbons'), ('CCCCCC[C@H](O)CO', 'Medium-chain primary fatty "
               "alcohol with 8 carbons'), ('OCCC(CC(C)(C)C)C', 'Medium-chain "
               "primary fatty alcohol with 6 carbons'), ('OCCCCCC(C)C', "
               "'Medium-chain primary fatty alcohol with 7 carbons'), "
               "('CCCCCCCCCO', 'Medium-chain primary fatty alcohol with 9 "
               "carbons'), ('CC(CCCCCCCCO)C', 'Medium-chain primary fatty "
               "alcohol with 10 carbons'), ('OCCCC(CCCC)C', 'Medium-chain "
               "primary fatty alcohol with 8 carbons'), ('OCCCC(CCCCC)C', "
               "'Medium-chain primary fatty alcohol with 9 carbons'), "
               "('CC(C)CCCCCCCCCCO', 'Medium-chain primary fatty alcohol with "
               "12 carbons'), ('OCC(CCCCCCCC(O)(C)C)(C)C', 'Medium-chain "
               "primary fatty alcohol with 11 carbons'), ('OC(CCCCC)CCO', "
               "'Medium-chain primary fatty alcohol with 8 carbons'), "
               "('OCC(CCCCCC)(C)C', 'Medium-chain primary fatty alcohol with 8 "
               "carbons'), ('CCCC(O)CCCCCCO', 'Medium-chain primary fatty "
               "alcohol with 10 carbons'), ('CCC(C)CCC(CO)C(C)C', "
               "'Medium-chain primary fatty alcohol with 7 carbons'), "
               "('OC(CCCCO)C', 'Medium-chain primary fatty alcohol with 6 "
               "carbons'), ('CC[C@H](C)CCCCCO', 'Medium-chain primary fatty "
               "alcohol with 8 carbons'), ('OC(CCCC(CCO)C)(C)C', 'Medium-chain "
               "primary fatty alcohol with 8 carbons'), ('CC(C)CCCC(C)CO', "
               "'Medium-chain primary fatty alcohol with 7 carbons'), "
               "('CCCCC(CC)CO', 'Medium-chain primary fatty alcohol with 6 "
               "carbons'), ('CCCCCC[C@@H](O)CO', 'Medium-chain primary fatty "
               "alcohol with 8 carbons'), ('OCC(CCCCCCCC)CCCCCC', "
               "'Medium-chain primary fatty alcohol with 10 carbons'), "
               "('C(CCCCCCC)CCO', 'Medium-chain primary fatty alcohol with 10 "
               "carbons'), ('CCCCCCCCCCCCO', 'Medium-chain primary fatty "
               "alcohol with 12 carbons'), ('OCCC(CCCC(C)C)C', 'Medium-chain "
               "primary fatty alcohol with 8 carbons'), ('CCCCCCC(CO)CCCC', "
               "'Medium-chain primary fatty alcohol with 8 carbons'), "
               "('CCCCCCC(CCCCCC)CO', 'Medium-chain primary fatty alcohol with "
               "8 carbons'), ('CC(C)CCCC(C)CCCC(C)CCO', 'Medium-chain primary "
               "fatty alcohol with 12 carbons'), ('CC(O)CCCCCCCCO', "
               "'Medium-chain primary fatty alcohol with 10 carbons'), "
               "('OCCC[C@H](CC)C', 'Medium-chain primary fatty alcohol with 6 "
               "carbons'), ('OCC(CCCCCCCCCC)CC', 'Medium-chain primary fatty "
               "alcohol with 12 carbons'), ('CCCCCCCC(CCO)O', 'Medium-chain "
               "primary fatty alcohol with 10 carbons'), ('C(CCCCCC)O', "
               "'Medium-chain primary fatty alcohol with 7 carbons'), "
               "('CC(C)CCC[C@H](C)CO', 'Medium-chain primary fatty alcohol "
               "with 7 carbons'), ('CCCC(O)C(CC)CO', 'Medium-chain primary "
               "fatty alcohol with 6 carbons'), ('CC(C)CCC[C@@H](C)CO', "
               "'Medium-chain primary fatty alcohol with 7 carbons'), "
               "('CCC[C@@H](C)CCCO', 'Medium-chain primary fatty alcohol with "
               "7 carbons'), ('CCCCCCCCO', 'Medium-chain primary fatty alcohol "
               "with 8 carbons'), ('CCCCCCC(O)CO', 'Medium-chain primary fatty "
               "alcohol with 8 carbons'), ('CCCCCCO', 'Medium-chain primary "
               "fatty alcohol with 6 carbons')]\n"
               "False negatives: [('OCCCCCCCCCCCCO', 'Must have exactly one "
               "primary alcohol group')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 16,
    'num_true_negatives': 183899,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.058823529411764705,
    'recall': 0.5,
    'f1': 0.10526315789473684,
    'accuracy': 0.9999075670003317}