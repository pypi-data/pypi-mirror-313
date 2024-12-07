"""
Classifies: CHEBI:138261 very long-chain fatty acyl-CoA(4-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_very_long_chain_fatty_acyl_CoA_4__(smiles: str):
    """
    Determines if a molecule is a very long-chain fatty acyl-CoA(4-).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a very long-chain fatty acyl-CoA(4-), False otherwise 
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for CoA structure components
    if not all(substructure in smiles for substructure in ['COP([O-])', 'OP([O-])', 'n1cnc2c(N)ncnc12']):
        return False, "Missing characteristic CoA structure components"

    # Check for 4 negative charges (phosphate deprotonation)
    charge = Chem.GetFormalCharge(mol)
    if charge != -4:
        return False, f"Total charge is {charge}, not -4"

    # Check for thioester linkage
    thioester_pattern = Chem.MolFromSmarts('C(=O)SC')
    if not mol.HasSubstructMatch(thioester_pattern):
        return False, "Missing thioester linkage"

    # Count carbons in the fatty acid chain
    fatty_acid_pattern = Chem.MolFromSmarts('CCCCCCCCCCCCCCCCCCCCCC(=O)SC')  # Pattern for C22 or longer
    if not mol.HasSubstructMatch(fatty_acid_pattern):
        return False, "Fatty acid chain length is less than 22 carbons"

    # Check for steroid-like structures (which should be excluded)
    steroid_pattern = Chem.MolFromSmarts('C1CCC2C(C1)CCC1C3CCCC3CCC12')
    if mol.HasSubstructMatch(steroid_pattern):
        return False, "Contains steroid-like structure"

    # Count carbons in the main chain
    def count_chain_carbons(mol, start_idx):
        visited = set()
        stack = [(start_idx, 0)]
        max_length = 0
        
        while stack:
            current_idx, length = stack.pop()
            if current_idx in visited:
                continue
                
            visited.add(current_idx)
            current_atom = mol.GetAtomWithIdx(current_idx)
            
            if current_atom.GetSymbol() == 'C':
                max_length = max(max_length, length)
                
                for neighbor in current_atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'C' and neighbor.GetIdx() not in visited:
                        if not any(pattern in Chem.MolToSmiles(Chem.PathToSubmol(mol, [neighbor.GetIdx()])) 
                                 for pattern in ['n1cnc', 'OP', 'NC(=O)']):
                            stack.append((neighbor.GetIdx(), length + 1))
                            
        return max_length

    # Find the thioester carbon and count chain length
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)
    if not thioester_matches:
        return False, "Could not identify thioester carbon"
        
    chain_length = count_chain_carbons(mol, thioester_matches[0][0])
    
    if chain_length >= 28:  # Only classify as true if chain length is 28 or more
        return True, f"Very long-chain fatty acyl-CoA(4-) with approximately {chain_length} carbons in chain"
    else:
        return False, f"Fatty acid chain length ({chain_length}) is less than 28 carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138261',
                          'name': 'very long-chain fatty acyl-CoA(4-)',
                          'definition': 'A fatty acyl-CoA(4-) arising from '
                                        'deprotonation of the phosphate and '
                                        'diphosphate OH groups of any very '
                                        'long-chain fatty acyl-CoA; major '
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:77636']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.05660377358490566 is too low.\n'
               'True positives: '
               "[('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain')]\n"
               'False positives: '
               "[('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 26 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('C[C@H](CCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3C[C@H](O)[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 36 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 34 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 36 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 26 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CC[C@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 36 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 36 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 34 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 26 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 34 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('[H][C@@](C)(CC[C@@H](O)[C@@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 26 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('C[C@H](CCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 38 "
               "carbons in chain'), "
               "('CC(=CCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCC(O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('C[C@H](CCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 38 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('C[C@H](C=CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('[H][C@@](C)(CCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('[H][C@@](C)(CCC[C@@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 36 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 36 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 34 "
               "carbons in chain'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('[H][C@@](C)(CCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])CC[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 38 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 26 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 38 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 38 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 26 "
               "carbons in chain'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C)C(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 26 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 34 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 26 "
               "carbons in chain'), "
               "('[H][C@@](C)(CCC[C@@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 26 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 34 "
               "carbons in chain'), "
               "('C[C@H](CCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 36 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('[H][C@@](C)(CC\\\\C=C(/C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain'), "
               "('[H][C@@](C)(CCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 36 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 30 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 32 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 34 "
               "carbons in chain'), "
               "('C[C@H](CCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 22 "
               "carbons in chain'), "
               "('[H][C@@](C)(CCCC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 24 "
               "carbons in chain'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Very long-chain fatty acyl-CoA(4-) with approximately 28 "
               "carbons in chain')]\n"
               'False negatives: []',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 7,
    'num_true_negatives': 183897,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.2222222222222222,
    'recall': 0.6666666666666666,
    'f1': 0.3333333333333333,
    'accuracy': 0.9999564997525924}