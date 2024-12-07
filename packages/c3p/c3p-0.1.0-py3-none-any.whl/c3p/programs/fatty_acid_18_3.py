"""
Classifies: CHEBI:132502 fatty acid 18:3
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_fatty_acid_18_3(smiles: str):
    """
    Determines if a molecule is a fatty acid with 18 carbons and 3 double bonds.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a fatty acid 18:3, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Count total carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 18:
        return False, f"Contains {carbon_count} carbons, not 18"

    # Count double bonds
    double_bond_count = 0
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
            # Don't count the carboxylic acid double bond
            if not (bond.GetBeginAtom().GetSymbol() == 'O' or 
                   bond.GetEndAtom().GetSymbol() == 'O'):
                double_bond_count += 1

    # Check for allene pattern (C=C=C)
    allene_pattern = Chem.MolFromSmarts('C=C=C')
    has_allene = mol.HasSubstructMatch(allene_pattern)
    if has_allene:
        # Allene counts as 2 double bonds in SMILES but represents 1 unsaturation
        double_bond_count -= 1

    # Check for triple bonds
    triple_bond_pattern = Chem.MolFromSmarts('C#C')
    if mol.HasSubstructMatch(triple_bond_pattern):
        return False, "Contains triple bonds"

    # Check total number of double bonds
    if double_bond_count != 3:
        return False, f"Contains {double_bond_count} double bonds, not 3"

    # Check for cyclic structures
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Contains cyclic structures"

    # Check if the molecule contains only C, H, and O atoms
    valid_atoms = {'C', 'O', 'H'}
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in valid_atoms:
            return False, f"Contains non-C/H/O atom: {atom.GetSymbol()}"

    return True, "Fatty acid with 18 carbons and 3 double bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132502',
                          'name': 'fatty acid 18:3',
                          'definition': 'Any trienoic fatty acid containing 18 '
                                        'carbons.',
                          'parents': ['CHEBI:73155']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.23076923076923078 is too low.\n'
               'True positives: '
               "[('OC(=O)C\\\\C=C\\\\CCCC/C=C\\\\C/C=C\\\\CCCCC', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C/CC', 'Fatty acid with 18 "
               "carbons and 3 double bonds'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC(O)=O', 'Fatty acid with "
               "18 carbons and 3 double bonds'), "
               "('CC(O)\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCC(O)=O', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('C(CC=C=CCCCC(O)=O)CCCCCC\\\\C=C\\\\C', 'Fatty acid with 18 "
               "carbons and 3 double bonds'), "
               "('OC(=O)CCCCC/C=C\\\\C=C/C/C=C\\\\CCCCC', 'Fatty acid with 18 "
               "carbons and 3 double bonds')]\n"
               'False positives: '
               "[('C(=O)(O)[C@@H](N*)CSC/C=C(/CC/C=C(/CCC=C(C)C)\\\\C)\\\\C', "
               "'Fatty acid with 18 carbons and 3 double bonds'), "
               "('CC\\\\C=C/C\\\\C=C/C=C/[C@H](CCCCCCCC(O)=O)OO', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('C(CCCC(O)=O)CCC/C=C\\\\C=C\\\\[C@H](C/C=C\\\\CC)O', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('C(CCCCCCC/C=C\\\\[C@@H](/C=C\\\\C/C=C\\\\CC)OO)(=O)O', "
               "'Fatty acid with 18 carbons and 3 double bonds'), "
               "('C(CCCCCCC/C=C\\\\[C@H](/C=C\\\\C/C=C\\\\CC)OO)(=O)O', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('OC(=O)CCCCCCC/C=C\\\\C=C\\\\O\\\\C=C\\\\CCCC', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('C(CCCCCCC[C@@H](/C=C/C=C\\\\C=C\\\\[C@H](CC)OO)OO)(O)=O', "
               "'Fatty acid with 18 carbons and 3 double bonds'), "
               "('C(CC=C=CCCCC(O)=O)CCCCCCCCC', 'Fatty acid with 18 carbons "
               "and 3 double bonds'), "
               "('CC\\\\C=C/C[C@H](OO)\\\\C=C\\\\C=C/CCCCCCCC(O)=O', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('C(CC(=O)O)CCCCC/C=C\\\\C=C\\\\[C@H](/C=C\\\\CCC)OO', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('C(/C=C\\\\CCCCCCCC(=O)O)=C\\\\[C@@H](C/C=C\\\\CC)OO', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('CC\\\\C=C/C\\\\C=C/C=C/C(CCCCCCCC(O)=O)OO', 'Fatty acid with "
               "18 carbons and 3 double bonds'), "
               "('C(CC=[C@]=C([H])CCCC(O)=O)CCCCCCCCC', 'Fatty acid with 18 "
               "carbons and 3 double bonds'), "
               "('C(C(O)=O)CC/C=C\\\\C/C=C\\\\CCCCC/C=C\\\\CC', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('CC\\\\C=C/C\\\\C=C/C=C/[C@@H](CCCCCCCC(O)=O)OO', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC[C@@H](O)C(O)=O', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('CCCCC\\\\C=C/C=C/O\\\\C=C\\\\CCCCCCC(O)=O', 'Fatty acid with "
               "18 carbons and 3 double bonds'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC[C@@H](OO)C(O)=O', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('CCCCCC(O)\\\\C=C\\\\C=C/C\\\\C=C/CCCCC(O)=O', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('BrC=C=C[C@@H](O)C/C=C\\\\CCCCCCCCCCC(=O)O', 'Fatty acid with "
               "18 carbons and 3 double bonds'), "
               "('C(\\\\C=C/CCCCCCCC(=O)O)=C/C(C/C=C\\\\CC)OO', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('CCCCC\\\\C=C/CC(OO)\\\\C=C\\\\C=C/CCCCC(O)=O', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CSC[C@H](N)C(O)=O', "
               "'Fatty acid with 18 carbons and 3 double bonds'), "
               "('CCCCC\\\\C=C/C[C@@H](OO)\\\\C=C\\\\C=C/CCCCC(O)=O', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('CCCC\\\\C=C\\\\C=C\\\\C=C/CCCCC(=O)CCC(O)=O', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('OC(=O)CCC/C=C/CC/C=C\\\\C/C=C\\\\CCCCC', 'Fatty acid with 18 "
               "carbons and 3 double bonds'), "
               "('OC(=O)CCCCCCC/C=C\\\\C\\\\C=C\\\\C=C\\\\C(OO)CC', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('C\\\\C(CO)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CSC[C@H](N)C(O)=O', "
               "'Fatty acid with 18 carbons and 3 double bonds'), "
               "('C(=C\\\\[C@H](C[C@@H](C[C@H](CC(O)=O)N)O)O)/C=C/C=C/CCCCC', "
               "'Fatty acid with 18 carbons and 3 double bonds'), "
               "('CC\\\\C=C/CC(O)\\\\C=C\\\\C=C/CCCCCCCC(O)=O', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('O(O)C(C/C=C\\\\CCCCCCCC(O)=O)/C=C/C=C/CC', 'Fatty acid with "
               "18 carbons and 3 double bonds'), "
               "('OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCC(C)C', 'Fatty acid "
               "with 18 carbons and 3 double bonds'), "
               "('C(CC=[C@@]=C([H])CCCC(O)=O)CCCCCCCCC', 'Fatty acid with 18 "
               "carbons and 3 double bonds'), "
               "('O=C(O)CCCCCCCC=C=C[C@@H](O)[C@@H](O)CCCCC', 'Fatty acid with "
               "18 carbons and 3 double bonds'), "
               "('C(CCCC(O)=O)CCC[C@@H](/C=C/C=C\\\\C/C=C\\\\CC)O', 'Fatty "
               "acid with 18 carbons and 3 double bonds'), "
               "('CC\\\\C=C/C\\\\C=C/C=C/C(O)CCCCCCCC(O)=O', 'Fatty acid with "
               "18 carbons and 3 double bonds'), "
               "('O=C(N[C@@H](CCCN=C(N)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CCCN=C(N)N', "
               "'Fatty acid with 18 carbons and 3 double bonds'), "
               "('CC\\\\C=C/C\\\\C=C/C[C@H](OO)\\\\C=C\\\\CCCCCCC(O)=O', "
               "'Fatty acid with 18 carbons and 3 double bonds'), "
               "('BrC=C=C[C@H](O)/C=C/CCCCCCCCCCCC(=O)O', 'Fatty acid with 18 "
               "carbons and 3 double bonds')]\n"
               "False negatives: [('OC(CCCCCCCC(O)=O)/C=C/C=C/C=C/C(=O)CC', "
               "'Contains conjugated system with oxygen')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 31,
    'num_true_negatives': 183834,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.16216216216216217,
    'recall': 0.8571428571428571,
    'f1': 0.27272727272727276,
    'accuracy': 0.9998259658893143}