"""
Classifies: CHEBI:15489 3-oxo-fatty acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_3_oxo_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a 3-oxo-fatty acyl-CoA.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if molecule is a 3-oxo-fatty acyl-CoA, False otherwise
        str: Reason for classification
    """
    
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for key substructures
    
    # CoA core structure pattern (including both protonated and deprotonated phosphates)
    coa_pattern = Chem.MolFromSmarts("[#16]CCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O,OH])(=O)OP([O,OH])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O,OH])([O,OH])=O)n1cnc2c(N)ncnc12")
    
    # 3-oxo fatty acyl pattern - thioester with ketone at position 3
    oxo_pattern = Chem.MolFromSmarts("[C,H]CC(=O)CC(=O)S")
    
    # Check for CoA core
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "Missing coenzyme A core structure"
        
    # Check for 3-oxo fatty acyl group
    if not mol.HasSubstructMatch(oxo_pattern):
        return False, "Missing 3-oxo fatty acyl group"

    # Check for thioester linkage between CoA and fatty acid
    thioester = Chem.MolFromSmarts("C(=O)SC")
    if not mol.HasSubstructMatch(thioester):
        return False, "Missing thioester linkage"

    # Find the fatty acid chain length
    matches = mol.GetSubstructMatches(oxo_pattern)
    if matches:
        # Get atoms in fatty acid chain before the 3-oxo group
        chain_atoms = set()
        def trace_chain(atom, visited):
            if atom.GetIdx() in visited:
                return
            visited.add(atom.GetIdx())
            if atom.GetSymbol() == 'C':
                chain_atoms.add(atom.GetIdx())
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() in ['C', 'H'] and neighbor.GetIdx() not in matches[0]:
                        trace_chain(neighbor, visited)
                        
        start_idx = matches[0][0] # First carbon in matching pattern
        trace_chain(mol.GetAtomWithIdx(start_idx), set())
        chain_length = len(chain_atoms)
        
        if chain_length < 2:  # Changed minimum chain length requirement
            return False, "Fatty acid chain too short"
            
        return True, f"3-oxo-fatty acyl-CoA with chain length of approximately {chain_length} carbons"
        
    return False, "Invalid 3-oxo-fatty acyl-CoA structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15489',
                          'name': '3-oxo-fatty acyl-CoA',
                          'definition': 'An oxo fatty acyl-CoA that results '
                                        'from the formal condensation of the '
                                        'thiol group of coenzyme A with the '
                                        'carboxy group of any 3-oxo-fatty '
                                        'acid..',
                          'parents': ['CHEBI:61903']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.10619469026548672 is too low.\n'
               'True positives: '
               "[('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 24 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 16 "
               "carbons'), "
               "('CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 12 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 22 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 26 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 34 "
               "carbons')]\n"
               'False positives: '
               "[('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 16 "
               "carbons'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCCCC([O-])=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 8 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 16 "
               "carbons'), "
               "('CCCCCC(=O)CC(=O)CC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 8 "
               "carbons'), "
               "('CCCC\\\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 12 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 26 "
               "carbons'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCCCCCC(O)=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 10 "
               "carbons'), "
               "('CC(C)=CCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 5 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 16 "
               "carbons'), "
               "('CCCC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 16 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 28 "
               "carbons'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 28 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 4 "
               "carbons'), "
               "('C[C@H](CCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 9 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 10 "
               "carbons'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)CC(CCC/C=C\\\\CCCCCCCC)=O)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 12 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 10 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 22 "
               "carbons'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 20 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 32 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 34 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 34 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 15 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 14 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 24 "
               "carbons'), "
               "('CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 10 "
               "carbons'), "
               "('[H]C(=O)CC([H])=C([H])CC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 4 "
               "carbons'), "
               "('[H][C@@](C)(CCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 22 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 24 "
               "carbons'), "
               "('[H][C@@](C)(CCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 22 "
               "carbons'), "
               "('C[C@H](CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 6 "
               "carbons'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCC(O)=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 6 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 15 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 14 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 13 "
               "carbons'), "
               "('CC\\\\C=C/C[C@H]1[C@@H](CCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)n2cnc3c(N)ncnc23)CCC1=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 12 "
               "carbons'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCC([O-])=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 6 "
               "carbons'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(C(CC\\\\C(=C\\\\CC4=C(C(=C5C(=C4O)C(OC5)=O)C)OC)\\\\C)=O)C)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 14 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 16 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 16 "
               "carbons'), "
               "('CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 18 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 11 "
               "carbons'), "
               "('[H]C(CC(O)=O)=C([H])CC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 4 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 26 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 7 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 18 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 18 "
               "carbons'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(CC(CCC(C(CCC([O-])=O)=O)C)=O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 7 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 18 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 14 "
               "carbons'), "
               "('S(CCNC(=O)CCNC(=O)[C@H](O)C(COP(OP(OC[C@H]1O[C@@H](N2C3=NC=NC(N)=C3N=C2)[C@H](O)[C@@H]1OP(O)(O)=O)(O)=O)(O)=O)(C)C)C(=O)CC(=O)C/C=C/CC(O)=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 4 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 4 "
               "carbons'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 26 "
               "carbons'), "
               "('CC(C)C(=C)CC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 5 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 32 "
               "carbons'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 22 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 17 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 20 "
               "carbons'), "
               "('C[C@H](CCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 5 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 8 "
               "carbons'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCCCCCCCC([O-])=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 12 "
               "carbons'), "
               "('C[C@H](CCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 7 "
               "carbons'), "
               "('C[C@H](CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 8 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 12 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 20 "
               "carbons'), "
               "('S(CCNC(=O)CCNC(=O)[C@H](O)C(COP(OP(OC[C@H]1O[C@@H](N2C3=NC=NC(N)=C3N=C2)C(O)C1OP(O)(O)=O)(O)=O)(O)=O)(C)C)C(=O)CC(=O)CCCCCCCCC', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 8 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 12 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 26 "
               "carbons'), "
               "('C[C@H](CCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 7 "
               "carbons'), "
               "('CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 14 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 10 "
               "carbons'), "
               "('CC\\\\C=C/C[C@H]1[C@@H](CC(=O)CC(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)n2cnc3c(N)ncnc23)CCC1=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 10 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 6 "
               "carbons'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C4=C5CCC([C@]5(CCC4=O)C)=O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 7 "
               "carbons'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCCCCCCCC(O)=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 12 "
               "carbons'), "
               "('CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 8 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 30 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 30 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 15 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 16 "
               "carbons'), "
               "('S(C(=O)CC(C/C=C\\\\CCCCCCCC)=O)CCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 10 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 17 "
               "carbons'), "
               "('CC(C)CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 13 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 28 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 32 "
               "carbons'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCC([O-])=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 4 "
               "carbons'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 16 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 11 "
               "carbons'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 20 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 28 "
               "carbons'), "
               "('[H]C(=O)CC([H])=C([H])CC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 4 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 9 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 12 "
               "carbons'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 8 "
               "carbons'), "
               "('C[C@H](CCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 9 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 10 "
               "carbons'), "
               "('C[C@H](CCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 15 "
               "carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 20 "
               "carbons'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 24 "
               "carbons'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C(C)C(CC[C@]([C@@]4([C@]5(CC[C@@]6([C@]7(CC[C@H](C[C@]7(C[C@H]([C@]6([C@@]5(CC4)[H])[H])O)[H])O)C)[H])C)[H])(C)[H])=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'3-oxo-fatty acyl-CoA with chain length of approximately 22 "
               "carbons')]\n"
               'False negatives: '
               "[('CCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Fatty acid chain too short (less than 4 carbons)')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 120736,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.9991724799947038}