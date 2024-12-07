"""
Classifies: CHEBI:131860 octadecanoid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_octadecanoid_anion(smiles: str):
    """
    Determines if a molecule is an octadecanoid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an octadecanoid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for carboxylate anion
    carboxylate = False
    carboxylate_carbon = None
    for atom in mol.GetAtoms():
        if atom.GetFormalCharge() == -1 and atom.GetSymbol() == 'O':
            # Check if connected to C=O
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C':
                    for bond in neighbor.GetBonds():
                        other_atom = bond.GetOtherAtom(neighbor)
                        if other_atom.GetSymbol() == 'O' and bond.GetBondType() == Chem.BondType.DOUBLE:
                            carboxylate = True
                            carboxylate_carbon = neighbor.GetIdx()
                            break
    
    if not carboxylate:
        return False, "No carboxylate anion group found"

    # Check carbon count (should be 18 for octadecanoid)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 18:
        return False, f"Carbon count is {carbon_count}, should be 18"
    
    # Check for longest carbon chain starting from carboxylate
    if carboxylate_carbon is not None:
        # Create a path of length 18 from carboxylate carbon
        paths = Chem.FindAllPathsOfLengthN(mol, 18, useBonds=False, useHs=False)
        valid_path = False
        for path in paths:
            if path[0] == carboxylate_carbon:
                # Check if path consists of only carbons
                if all(mol.GetAtomWithIdx(idx).GetSymbol() == 'C' for idx in path):
                    valid_path = True
                    break
        
        if not valid_path:
            return False, "No valid 18-carbon chain found starting from carboxylate group"
        
    # Check for unsaturation (must have at least one double bond)
    double_bonds = 0
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            if bond.GetBeginAtom().GetSymbol() == 'C' and bond.GetEndAtom().GetSymbol() == 'C':
                double_bonds += 1
    
    if double_bonds == 0:
        return False, "No carbon-carbon double bonds found"
    
    return True, f"Octadecanoid anion with {double_bonds} C=C double bond(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131860',
                          'name': 'octadecanoid anion',
                          'definition': 'An unsaturated fatty acid anion '
                                        'obtained by the deprotonation of the '
                                        'carboxy group of any octadecanoid.',
                          'parents': ['CHEBI:2580', 'CHEBI:57560']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.13461538461538464 is too low.\n'
               'True positives: '
               "[('C(CCCCCCC\\\\C=C/C=C/[C@@H](CCCCC)O)(=O)[O-]', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('CCCCCCCCC\\\\C=C/C\\\\C=C/CCCC([O-])=O', 'Octadecanoid anion "
               "with 2 C=C double bond(s)'), "
               "('O1[C@@H](CCCCCCCC([O-])=O)[C@@H]1[C@H](/C=C\\\\CCCCC)O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('[H]C(CCCCCCCC([O-])=O)=CC([H])=CCCCCCC', 'Octadecanoid anion "
               "with 2 C=C double bond(s)'), "
               "('C([O-])(=O)CCCCCCC/C=C\\\\[C@@H]1[C@@H]2[C@@H](C[C@]1([C@H](CC)O2)[H])O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('C(CCC(C/C=C\\\\C/C=C\\\\CC)O)CCCCCC(=O)[O-]', 'Octadecanoid "
               "anion with 2 C=C double bond(s)'), "
               "('CCCCC\\\\C=C/C\\\\C=C/[C@H](O)CC[C@@H](O)CCCC([O-])=O', "
               "'Octadecanoid anion with 2 C=C double bond(s)')]\n"
               "False positives: [('CCCC\\\\C=C/CCCCCCCCCCCC([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CC\\\\C=C/C\\\\C=C/C=C/C(O)CCCCCCCC([O-])=O', 'Octadecanoid "
               "anion with 3 C=C double bond(s)'), "
               "('C(\\\\CCCCCCC(C(=O)[O-])O)=C\\\\CCCCCCCC', 'Octadecanoid "
               "anion with 1 C=C double bond(s)'), "
               "('[C@@H]1([C@@H](C[C@H]([C@@H](O1)C)O)O)OCCCCCCCCC\\\\C=C\\\\C(=O)[O-]', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CCCCCCC(O)C\\\\C=C\\\\CCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('CCCCCCC(C\\\\C=C\\\\CCCCCCCC([O-])=O)OP([O-])([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('OC(=O)[C@@H]1CC(=C\\\\C=[N+]2/[C@@H](Cc3cc(oc(=O)c23)C(O)=O)C([O-])=O)/C=C(N1)C(O)=O', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('C1([C@H](CCC1=O)CC(N[C@H](C([O-])=O)[C@H](CC)C)=O)C/C=C\\\\CC', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC([O-])=O', "
               "'Octadecanoid anion with 4 C=C double bond(s)'), "
               "('CC\\\\C=C\\\\C=C\\\\C=C\\\\C=C\\\\CCCCCCCC([O-])=O', "
               "'Octadecanoid anion with 4 C=C double bond(s)'), "
               "('CCCCCC\\\\C=C\\\\CCCCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('CC\\\\C=C/C=C/C=C/C=C\\\\CCCCCCCC([O-])=O', 'Octadecanoid "
               "anion with 4 C=C double bond(s)'), "
               "('CCCCCCC(C\\\\C=C/CCCCCCCC([O-])=O)OP([O-])([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCC([O-])=O', 'Octadecanoid "
               "anion with 3 C=C double bond(s)'), "
               "('[C@@]12([C@H](CCC=C1C=C[C@@H]([C@@H]2CC[C@H](C[C@H](CC(=O)[O-])O)O)C)O)[H]', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('CC\\\\C=C/C[C@H]1[C@@H](CCCCCCCC([O-])=O)C=CC1=O', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('CC(C)[C@@H](/C=C(\\\\C)/C(=O)[O-])N(C)C(=O)[C@H](C(C)C)NC(=O)[C@H](CO)NC(N)=[NH2+]', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CSC[C@H]([NH3+])C([O-])=O', "
               "'Octadecanoid anion with 3 C=C double bond(s)'), "
               "('C(C/C=C\\\\CCCCCCCCCCC)CCC(=O)[O-]', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('S(C1=C(N2C(=O)C(C2C1C)C(O)C)C(=O)O)C3CNC(C3)C(=O)N(C)C.[Na+].[Na+].O=C([O-])[O-]', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('Oc1ccc(CC(OC(=O)\\\\C=C\\\\c2ccc(O)c(O)c2)C([O-])=O)cc1O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('C/1(=C\\\\C2=CC=CC=C2)\\\\O[C@@](CC3=CC=CC=C3)(OC1=O)C(=O)[O-]', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('[C@@H]1([C@H](CCC1=O)CC(N[C@H](C([O-])=O)[C@H](CC)C)=O)C/C=C\\\\CCO', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('C(CCCCCCC/C=C\\\\C(CCCCCCC)O)([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('CCCCC[C@@H]1O\\\\C1=C/C=C\\\\CCCCCCCC([O-])=O', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('[H]C(\\\\C=C/CCCCCCCC([O-])=O)=C1O[C@H]1C\\\\C=C/CC', "
               "'Octadecanoid anion with 3 C=C double bond(s)'), "
               "('[C@@]12(CCCC=C1C=C[C@@H]([C@@H]2CC[C@H](C[C@H](CC(=O)[O-])O)O)C)[H]', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('CCCCCCCC\\\\C=C\\\\CCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC([O-])=O', 'Octadecanoid anion with "
               "1 C=C double bond(s)'), "
               "('CC\\\\C=C/C[C@@H]1[C@H](CCCCCCCC([O-])=O)C=CC1=O', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('C([O-])(=O)CCCCCCC[C@H]1C(=C(/C=C\\\\CCCCC)[H])O1', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('[Na+].CCCCCCCC\\\\C=C/CCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('CCCCC\\\\C=C/CC1OC1CCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('[Na+].[Na+].[H][C@]12SCC(CSc3nnnn3CS([O-])(=O)=O)=C(N1C(=O)[C@H]2NC(=O)[C@H](O)c1ccccc1)C([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CCCCCCC\\\\C=C\\\\CCCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('CCC\\\\C=C/[C@H](OO)\\\\C=C\\\\C=C/CCCCCCCC([O-])=O', "
               "'Octadecanoid anion with 3 C=C double bond(s)'), "
               "('CCCCCC\\\\C=C/CCCCCCCCCC([O-])=O', 'Octadecanoid anion with "
               "1 C=C double bond(s)'), "
               "('C1(=C(C(=CC(=C1)O)O)C([O-])=O)/C=C/CCCC(=O)CCC[C@@H](O)C', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('[H]C(CCCCCC)=C([H])CCCCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('C(=C\\\\C/C=C\\\\CCCCC)\\\\CCCCCC[C@H](C(=O)[O-])OO', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('O=[N+]([O-])C(=CCCCCCCCC)CCCCCCCC(=O)[O-]', 'Octadecanoid "
               "anion with 1 C=C double bond(s)'), "
               "('CCCCC\\\\C=C/CC(O)C(O)CCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('[O-]C(CCCCCCC/C=C\\\\CCCCCCC(C)O)=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('C[C@H](CCCCCCC/C=C/C([O-])=O)O[C@@H]1O[C@@H](C)[C@H](O)C[C@H]1O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CC\\\\C=C/C[C@@H]1[C@H](CCCCCCCC([O-])=O)CCC1=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('[O-]C(=O)[C@@H]1CC2=CC(=O)C(=O)C=C2N1/C=C/C3=CC(=[NH+][C@@H](C3)C([O-])=O)C([O-])=O', "
               "'Octadecanoid anion with 4 C=C double bond(s)'), "
               "('CCCC\\\\C=C\\\\O\\\\C=C\\\\C=C/CCCCCCCC([O-])=O', "
               "'Octadecanoid anion with 3 C=C double bond(s)'), "
               "('[H][C@]12SCC(CSc3nnnn3C)=C(N1C(=O)[C@H]2NC(=O)[C@H](O)c1ccccc1)C([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CC\\\\C=C/C=C/O\\\\C=C\\\\C=C/CCCCCCCC([O-])=O', "
               "'Octadecanoid anion with 4 C=C double bond(s)'), "
               "('[C@@]12(CCCC[C@@]1(C=C[C@@H]([C@@H]2CC[C@H](C[C@H](CC(=O)[O-])O)O)C)[H])[H]', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CCCCCCC(O)C\\\\C=C/CCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('C(CCCCCCC/C=C\\\\CCCCCC)(=O)NCC([O-])=O', 'Octadecanoid "
               "anion with 1 C=C double bond(s)'), "
               "('C(=CCCCCCCCC)CCCCCCCC(=O)[O-]', 'Octadecanoid anion with 1 "
               "C=C double bond(s)'), ('CCCCCC#CC\\\\C=C/CCCCCCCC([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CC\\\\C=C/C\\\\C=C/C[C@H](OO)\\\\C=C\\\\CCCCCCC([O-])=O', "
               "'Octadecanoid anion with 3 C=C double bond(s)'), "
               "('CCCCC\\\\C=C/C=C/O\\\\C=C\\\\CCCCCCC([O-])=O', 'Octadecanoid "
               "anion with 3 C=C double bond(s)'), "
               "('C(=O)(CCCC/C=C/CCCCCCCCCCC)[O-]', 'Octadecanoid anion with 1 "
               "C=C double bond(s)'), "
               "('[C@@]12(CCCCC1=C[C@H]([C@@H]([C@@H]2CC[C@H](C[C@H](CC(=O)[O-])O)O)C)O)[H]', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CC(C)=CCc1cccc2Nc3cccc(C([O-])=O)c3Nc12', 'Octadecanoid "
               "anion with 1 C=C double bond(s)'), "
               "('C(=O)([O-])[C@@H](N*)CSC/C=C(/CC/C=C(/CCC=C(C)C)\\\\C)\\\\C', "
               "'Octadecanoid anion with 3 C=C double bond(s)'), "
               "('CCCCCCCC[C@H](O)\\\\C=C\\\\CCCCCCC([O-])=O', 'Octadecanoid "
               "anion with 1 C=C double bond(s)'), "
               "('CC\\\\C=C/C[C@H]1[C@@H](CCCCCCCC([O-])=O)CCC1=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('[H][C@]12SCC(CSc3nc(=O)c(=O)[nH]n3C)=C(N1C(=O)[C@H]2NC(=O)C(=N/OC)\\\\c1csc(N)n1)C([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('C(=C\\\\C/C=C\\\\CCCC(C)O)\\\\CCCCCCCC(=O)[O-]', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC[C@@H](O)C([O-])=O', "
               "'Octadecanoid anion with 3 C=C double bond(s)'), "
               "('C(CCCCCCC(/C=C\\\\CCCCCCCC)O)([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('CCCCC\\\\C=C/CC(O)CCCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('[O-]C(CCCCCCC/C=C\\\\C[C@@H](CCCCCC)O)=O', 'Octadecanoid "
               "anion with 1 C=C double bond(s)'), "
               "('C1([C@H](CCC1=O)CC(N[C@H](C([O-])=O)[C@H](CC)C)=O)C/C=C\\\\CCO', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('C(=C\\\\C/C=C\\\\CCCCCO)\\\\CCCCCCCC(=O)[O-]', 'Octadecanoid "
               "anion with 2 C=C double bond(s)'), "
               "('OCCCCCCCC\\\\C=C/CCCCCCCC([O-])=O', 'Octadecanoid anion with "
               "1 C=C double bond(s)'), "
               "('C(CCCC([O-])=O)CCC/C=C\\\\C=C\\\\[C@H](C/C=C\\\\CC)O', "
               "'Octadecanoid anion with 3 C=C double bond(s)'), "
               "('CC\\\\C=C/C\\\\C=C/C=C/O\\\\C=C\\\\CCCCCCC([O-])=O', "
               "'Octadecanoid anion with 4 C=C double bond(s)'), "
               "('C(\\\\CCCCCC[C@H](C(=O)[O-])OO)=C\\\\CCCCCCCC', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('[H]C(CCC=C([H])C=C([H])CCCCCCCC([O-])=O)=CCC', 'Octadecanoid "
               "anion with 3 C=C double bond(s)'), "
               "('CCCCC\\\\C=C/C=C/CCCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 2 C=C double bond(s)'), "
               "('[O-]C(CCCCCCC/C=C\\\\C[C@@H](CCCCCCO)O)=O', 'Octadecanoid "
               "anion with 1 C=C double bond(s)'), "
               "('C1(O)=C([C@@](C([O-])=O)(OC1=O)CC2=CC=C(C=C2)O)C3=CC=C(C=C3)O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('Oc1ccc(C[C@@H](OC(=O)\\\\C=C\\\\c2ccc(O)c(O)c2)C([O-])=O)cc1O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CCCCCC(O)C(O)C\\\\C=C/CCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC([O-])=O', 'Octadecanoid "
               "anion with 3 C=C double bond(s)'), "
               "('[H][C@]12SCC(CSc3nnnn3CS([O-])(=O)=O)=C(N1C(=O)[C@H]2NC(=O)[C@H](O)c1ccccc1)C([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('[H]C(CCC)=CCC=C([H])C=C([H])CCCCCCCC([O-])=O', 'Octadecanoid "
               "anion with 3 C=C double bond(s)'), "
               "('[Na+].[H][C@]12SCC(CSc3nnnn3C)=C(N1C(=O)[C@H]2NC(=O)[C@H](O)c1ccccc1)C([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CCCCC[C@@H]1O[C@@H]1C\\\\C=C/CCCCCCCC([O-])=O', "
               "'Octadecanoid anion with 1 C=C double bond(s)'), "
               "('CCCCCC1OC1C\\\\C=C/CCCCCCCC([O-])=O', 'Octadecanoid anion "
               "with 1 C=C double bond(s)'), "
               "('CCC\\\\C=C/C\\\\C=C\\\\C=C/CCCCCCCC([O-])=O', 'Octadecanoid "
               "anion with 3 C=C double bond(s)'), "
               "('C1[C@]2([C@]3([C@@](/C(/C(CC3)=O)=C/C=C(\\\\O)/C(=O)[O-])(CC[C@@]2(C(=O)C1)C)[H])[H])[H]', "
               "'Octadecanoid anion with 2 C=C double bond(s)'), "
               "('[C@@H]1([C@H](CCC1=O)CC(N[C@H](C([O-])=O)[C@H](CC)C)=O)C/C=C\\\\CC', "
               "'Octadecanoid anion with 1 C=C double bond(s)')]\n"
               "False negatives: [('*C([O-])=O', 'Carbon count is 1, should be "
               "18')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 18,
    'num_true_negatives': 183835,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.18181818181818182,
    'recall': 0.5,
    'f1': 0.26666666666666666,
    'accuracy': 0.9998803443905995}