"""
Classifies: CHEBI:144712 N-(very-long-chain fatty acyl)-sphingoid base
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_N__very_long_chain_fatty_acyl__sphingoid_base(smiles: str):
    """
    Determines if a molecule is an N-(very-long-chain fatty acyl)-sphingoid base.
    These are ceramides with acyl chain length > C22.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule matches the class, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for amide group
    amide_pattern = Chem.MolFromSmarts('[NX3][CX3](=O)')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide group found"

    # Check for sphingoid base backbone pattern
    # [OH]-C-C-N pattern characteristic of sphingoid bases
    sphingoid_pattern = Chem.MolFromSmarts('[OX2][CX4][CX4][NX3]')
    if not mol.HasSubstructMatch(sphingoid_pattern):
        return False, "No sphingoid base backbone pattern found"

    # Find the amide carbonyl carbon
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    if not amide_matches:
        return False, "Could not locate amide group"

    # For each amide group found, analyze the acyl chain
    for amide_match in amide_matches:
        amide_C = amide_match[1]  # Get the carbonyl carbon atom index
        
        # Count carbons in the acyl chain
        visited = set()
        def count_chain_carbons(atom_idx, prev_idx=None):
            if atom_idx in visited:
                return 0
            visited.add(atom_idx)
            
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() != 'C':
                return 0
                
            count = 1
            total_branches = 0
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() != prev_idx and neighbor.GetIdx() != amide_match[0]:  # Exclude nitrogen
                    branch_count = count_chain_carbons(neighbor.GetIdx(), atom_idx)
                    total_branches += branch_count
            return count + total_branches

        # Start counting from the carbonyl carbon
        acyl_carbons = count_chain_carbons(amide_C)
        
        # Check if any asterisk (*) is present in the SMILES, indicating undefined atoms
        if '*' in smiles:
            return True, "N-(very-long-chain fatty acyl)-sphingoid base with undefined acyl chain"
        
        if acyl_carbons > 22:
            return True, f"N-(very-long-chain fatty acyl)-sphingoid base with C{acyl_carbons} acyl chain"
    
    return False, f"Acyl chain length (C{acyl_carbons}) is not > C22"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:144712',
                          'name': 'N-(very-long-chain fatty acyl)-sphingoid '
                                  'base',
                          'definition': 'A ceramide where the acyl chain chain '
                                        'length is greater than C22 and the '
                                        'sphingoid base is undefined',
                          'parents': ['CHEBI:50860', 'CHEBI:83273']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.03809523809523809 is too low.\n'
               'True positives: '
               "[('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain')]\n"
               'False positives: '
               "[('[C@@]1(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])(C(O)=O)O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCC=CCCCCCCCC)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)CC(=O)N[C@H](Cc1ccccc1)C(=O)N[C@H]([C@@H](C)OC1O[C@@H](C)[C@@H](O)[C@@H](O)[C@H]1O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O[C@@H]2O[C@@H]3CO[C@@](C)(O[C@H]3[C@H](OC)[C@H]2O)C(O)=O)[C@H]1O)C(=O)N[C@H](C)C(=O)N[C@@H](C)COC1O[C@@H](C)[C@H](OC)[C@@H](OC)[C@H]1O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C32 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC[C@H](O)C(=O)N[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C23 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)CC(=O)N[C@H](Cc1ccccc1)C(=O)N[C@H]([C@@H](C)OC1O[C@@H](C)[C@@H](O)[C@@H](O)[C@H]1O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O[C@@H]2O[C@@H](C)[C@@H](OC(C)=O)[C@@H](OC)[C@@H]2OC)[C@H]1O)C(=O)N[C@H](C)C(=O)N[C@@H](C)COC1O[C@@H](C)[C@H](OC)[C@@H](OC)[C@H]1O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C32 acyl "
               "chain'), "
               "('C(CCCCCCCC[C@H]([C@H]([C@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)NC(=O)C(CCCCCCCCCCCCCCCCCCCCCCCC)O)O)O)CCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C28 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)CC(=O)N[C@H](Cc1ccccc1)C(=O)N[C@H]([C@@H](C)OC1O[C@@H](C)[C@@H](O)[C@@H](O)[C@H]1O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O[C@@H]2O[C@@H](C)[C@@H](O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H](C)[C@@H](OC(C)=O)[C@@H](OC)[C@@H]4OC)[C@H](O)[C@H]3O)C(O)=O)[C@@H](OC)[C@@H]2OC)[C@H]1O)C(=O)N[C@H](C)C(=O)N[C@@H](C)COC1O[C@@H](C)[C@H](OC)[C@@H](OC)[C@H]1O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C32 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](COP(O)(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](COP(O)(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@@H]3CO)OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCCC)[C@H](O)/C=C\\\\CCCCCCCCCCCCC)[C@@H]1O)CO)[C@]4(OC([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O[C@]5(OC([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C25 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C25 acyl "
               "chain'), "
               "('O1[C@@H]([C@@H](O)C(O)C(O)[C@@H]1OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCC)[C@H](O)/C=C/CCCCCCCCCCCCC)CO', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('C(CCCCCCCCCC)CCCC[C@@H](O)[C@@H](NC(=O)C(O)CCCCCCCCCCCC/C=C\\\\CCCCCCCC)CO', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('O([C@@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)OCC=2C=CC(=CC2)C(C)(C)C)O)O)C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C28 acyl "
               "chain'), "
               "('C(CCCCCCCCCC)CC\\\\C=C\\\\[C@@H](O)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCO)CO', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C30 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C28 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COP(O)(=O)OCCN)NC(=O)CCCCCCCCCCCCC\\\\C=C/CCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CNC(=O)c2ccccc2)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('[C@@H](C(CCCCCCCCCCCCCCC)=O)(CO)NC(=O)CCCCCCCCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('O=C(N[C@H]([C@H](O)[C@H](O)CCCCCCCCCCCCCC)CO)C(O)C(O)CCCCCCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('C(CCCCCCCCCCCCCCCCCCCCCCCC)(N[C@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)COP(OCC[N+](C)(C)C)(=O)[O-])=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C25 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(O)C(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](COP(O)(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('O=C1N2C3=C4O[C@H]([C@@H]2[C@@H](C1)OC)C=CC=CC[C@H](OC(=O)[C@H](NC(=O)CC(C)C)C)[C@@H]([C@H](C(=CCCC4=CC(=C3)O)C)O)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C23 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(O)=O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(O)C(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('[H][C@]12[C@H](CC(N)=O)[C@@]3(C)CCC(=O)NC[C@@H](C)OP([O-])(=O)O[C@H]4[C@@H](O)[C@H](O[C@@H]4CO)n4c[n+](c5cc(C)c(C)cc45)[Co--]456N1C3=C(C)C1=[N+]4C(=CC3=[N+]5C(=C(C)C4=[N+]6[C@]2(C)[C@@](C)(CC(N)=O)[C@@H]4CCC(N)=O)[C@@](C)(CC(N)=O)[C@@H]3CCC(N)=O)C(C)(C)[C@@H]1CCC(N)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC[C@H](O)C(=O)N[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)[C@@H](O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C23 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('O=C(N[C@H]([C@H](O)[C@H](O)CCCCCCCCCCCCCC)CO)[C@H](O)CCCCCCCCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C25 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O)[C@H]4O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](COP(O)(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('[C@@]1(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])(C(O)=O)O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCCCCCCCCCCC)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('OC(C(O)C(NC(=O)C(O)CCCCCCCCCCCCCCCCCCCCCCCC)CO)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C28 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C30 acyl "
               "chain'), ('O=C(NCCO)CCCCCCCCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](COC(=O)Nc2ccc(Cl)cc2)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('P(OCC(NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCC)C(O)CCCCC)(OCC[N+](C)(C)C)([O-])=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('P(OC1C(O)C(O)C(O)C(O)C1O)(OCC(NC(=O)C(O)CCCCCCCCCCCCCCCCCCCCCCCC)C(O)C(O)CCCCCCCCCCCCCC)(O)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('O[C@H](CCCCCCCCCCCCCCC)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCCC)CO', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C25 acyl "
               "chain'), "
               "('[H][C@]12[C@H](CC(N)=O)[C@@]3(C)CCC(=O)NC[C@@H](C)OP([O-])(=O)O[C@@H]4[C@@H](COP(O)(O)=O)O[C@@H]([C@@H]4O)n4c[n+](c5cc(C)c(C)cc45)[Co-3]456(C[C@H]7O[C@H]([C@H](O)[C@@H]7O)n7cnc8c(N)ncnc78)N1C3=C(C)C1=[N+]4C(=CC3=[N+]5C(=C(C)C4=[N+]6[C@]2(C)[C@@](C)(CC(N)=O)[C@@H]4CCC(N)=O)[C@@](C)(CC(N)=O)[C@@H]3CCC(N)=O)C(C)(C)[C@@H]1CCC(N)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC=2C=CC=CC2)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C31 acyl "
               "chain'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O)NC(=O)CCCCCCCCCCCCC\\\\C=C/CCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C28 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C27 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('C(=C/CCCCCCCCCCCCC)\\\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCCCC)=O)CO', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C25 acyl "
               "chain'), "
               "('O=C1O[C@@H](CC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@@H](C)C(N2[C@@H](C(N[C@@H](C(N[C@H](C(N[C@H]1[C@H](OC)C)=O)C(C)C)=O)[C@H](CC)C)=O)CCC2)=O)C(C)C)[C@H](O)C)CCCCCCCCCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('O([C@@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)OCCCCCCC=2C=CC=CC2)O)O)C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)[C@@H](O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](COP(O)(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCC[C@@H]1C[C@H]1CCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])([O-])=O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('C(CCCCCCCCCCCCCCCCCCCC)CC(=O)N[C@H]([C@@H](/C=C/*)O)COP(OCC[N+](C)(C)C)(=O)[O-]', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C23 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCC[C@@H](O)C(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCC\\\\C=C\\\\CCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C27 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)NC(CO[C@@H]1O[C@H](COP(O)(=O)OCCN)[C@@H](O)[C@H](O)[C@H]1O)C(O)C(O)CCCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCC[C@@H](O)[C@H](O)C(=O)N[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)[C@@H](O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](COP([O-])(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C30 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)[C@@H](O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('C12(CCO[C@@H]3[C@@H]([C@H]([C@H](O[C@@H]3CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O)O)O)C[C@@H]4CC(C1)C[C@H](C4)C2', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C23 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC[C@@H](O)[C@H](O)C(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCC[C@H](O)C(=O)N[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCCCC\\\\C=C/CCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](COP(O)(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)/C=C/CCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C30 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](COP([O-])(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('O[C@@H]([C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCC)C)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCC(=O)NC1=CC=C(CCCCC)C=C1', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('O([C@@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)OCCC)O)O)C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)OC[C@@H]([C@@H]([C@@H](CCCCCCCC=2C=CC=CC2)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('O[C@@H]([C@@H](NC(=O)CCCCCCCCCCCCCCC/C=C\\\\CCCCCCCC)C)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](COP(O)(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C26 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C28 acyl "
               "chain'), "
               "('P(OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCC)[C@H](O)CCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C24 acyl "
               "chain'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(CC(=O)N[C@H](Cc1ccccc1)C(=O)N[C@H]([C@@H](C)O[C@@H]1O[C@@H](C)[C@@H](O)[C@@H](OC)[C@H]1O)C(=O)N[C@H](C)C(=O)N[C@@H](C)CO[C@@H]1O[C@@H](C)[C@H](OC)[C@@H](OC)[C@H]1OS(O)(=O)=O)OC', "
               "'N-(very-long-chain fatty acyl)-sphingoid base with C28 acyl "
               "chain')]\n"
               'False negatives: '
               "[('CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC([*])=O', 'Acyl chain "
               "length (C1) is not > C22')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 5564,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9823539791776954}