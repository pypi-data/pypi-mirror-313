"""
Classifies: CHEBI:25018 L-leucine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_L_leucine_derivative(smiles: str):
    """
    Determines if a molecule is an L-leucine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an L-leucine derivative, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Create uncharger to neutralize molecule
    uncharger = rdMolStandardize.Uncharger()
    mol = uncharger.uncharge(mol)
    
    # L-leucine core SMARTS patterns
    l_leucine_core = '[C@@H](CC(C)C)(N)[C@@H](=O)O'
    l_leucine_modified = '[C@@H](CC(C)C)(N[*,#1])[C@@H](=O)[OH1,O-,OR,NR,N]'
    
    # Check for L-leucine core or modified core
    core_pat = Chem.MolFromSmarts(l_leucine_core)
    modified_pat = Chem.MolFromSmarts(l_leucine_modified)
    
    if core_pat is not None and mol.HasSubstructMatch(core_pat):
        return True, "Contains L-leucine core structure"
        
    if modified_pat is not None and mol.HasSubstructMatch(modified_pat):
        # Additional checks for derivatives
        for atom in mol.GetAtoms():
            if atom.GetSymbol() == 'N':
                # Check for N-substitution
                if atom.GetDegree() > 1:
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetSymbol() == 'C' and neighbor.GetChiralTag() == Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
                            isobutyl_pat = Chem.MolFromSmarts('CC(C)C')
                            if mol.HasSubstructMatch(isobutyl_pat):
                                return True, "L-leucine derivative with modified amino or carboxyl group"
                                
    # Check specifically for methyl ester
    methyl_ester_pat = Chem.MolFromSmarts('[C@@H](CC(C)C)(N)C(=O)OC')
    if methyl_ester_pat is not None and mol.HasSubstructMatch(methyl_ester_pat):
        return True, "L-leucine methyl ester"
        
    # Check for N-acyl derivatives
    n_acyl_pat = Chem.MolFromSmarts('[C@@H](CC(C)C)(NC(=O)[*,#1])C(=O)[OH1,O-,OR,NR,N]')
    if n_acyl_pat is not None and mol.HasSubstructMatch(n_acyl_pat):
        return True, "N-acyl L-leucine derivative"
        
    # Check for peptide bonds
    peptide_pat = Chem.MolFromSmarts('[C@@H](CC(C)C)(N)C(=O)N[C@@H]')
    if peptide_pat is not None and mol.HasSubstructMatch(peptide_pat):
        return True, "L-leucine-containing peptide"
    
    return False, "Not an L-leucine derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25018',
                          'name': 'L-leucine derivative',
                          'definition': 'A proteinogenic amino acid derivative '
                                        'resulting from reaction of L-leucine '
                                        'at the amino group or the carboxy '
                                        'group, or from the replacement of any '
                                        'hydrogen of L-leucine by a '
                                        'heteroatom.',
                          'parents': ['CHEBI:47003', 'CHEBI:83811']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.019417475728155338 is too low.\n'
               "True positives: [('[C@@H](CC(C)C)(NC(=O)C)C(O)=O', 'L-leucine "
               "derivative')]\n"
               'False positives: '
               "[('C=1C=2C[C@@H]3[C@]4([C@@](C2C=C(C1)OC)(CCCC4)CCN3C)[H]', "
               "'L-leucine derivative'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)CC(O)CCCCCCC)CC(C)C)CC(=O)O)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](C(N[C@@H](C(N[C@H](C(N[C@H](C(N[C@H]1CC(=O)O)=O)[C@H](CC)C)=O)[C@H](CC)C)=O)CO)=O)CC(C)C)CO)CC(C)C)CC(C)C)C', "
               "'L-leucine derivative'), "
               "('P(O[C@H](C(=O)N[C@H]([C@]1(OC(=O)C2=C(C1)C=CC=C2O)[H])CC(C)C)[C@@H](O)[C@@H](N)CC(=O)N)(O)(O)=O', "
               "'L-leucine derivative'), "
               "('COC1=CC=CC=C1C2=CC=C3[C@H]4[C@H]([C@@H]([C@H](N4CC5CC5)CN3C2=O)CO)C(=O)N6CCOCC6', "
               "'L-leucine derivative'), "
               "('CC=CC1=CC=C2[C@H]3[C@@H](CN2C1=O)[C@@H]([C@H](N3CC4=CN=CN=C4)C(=O)NCC5=CC=C(C=C5)F)CO', "
               "'L-leucine derivative'), ('C[C@H](C[C@H](N)C(O)=O)C(O)=O', "
               "'L-leucine derivative'), "
               "('CCNC(=O)[C@@H]1[C@H]([C@@H]2CN3C(=CC=C(C3=O)C4=CC=CC=C4)[C@@H]2N1CC)CO', "
               "'L-leucine derivative'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)O)CCCNC(=N)N)CC(=O)NCCCC[C@@H]2NC(=O)[C@@H](NC([C@H]([C@H](OC(C[C@H]3C(N[C@H](C(N[C@H]1CCC(=O)OC[C@H](NC(=O)[C@H]4C(C(=O)[C@@H](NC2=O)CC5=CC=CC=C5)CCC4)C(=O)N3)=O)CC(C)C)=O)=O)C)NC(=O)[C@@H](NC(=O)[C@H]6N(C(=O)[C@@H](N)C(C)C)CCC6)CC=7C8=C(C=CC=C8)NC7)=O)CC9=CC=C(O)C=C9', "
               "'L-leucine derivative'), "
               "('O=C1[C@@]2(O)[C@H]3O[C@H]3[C@H]([C@@H]1[C@@H](O)[C@H](C2)NC(=O)/C=C/CCCCCCCCC(=O)O)O', "
               "'L-leucine derivative'), "
               "('[Na+].CCCCCOc1ccc(cc1)-c1cc(no1)-c1ccc(cc1)C(=O)N[C@H]1C[C@@H](O)[C@@H](O)NC(=O)[C@@H]2[C@@H](O)[C@@H](C)CN2C(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H]2C[C@@H](O)CN2C(=O)[C@@H](NC1=O)[C@@H](C)O)[C@H](O)[C@@H](O)c1ccc(O)c(OS([O-])(=O)=O)c1)[C@H](O)CC(N)=O', "
               "'L-leucine derivative'), "
               "('O=C1O[C@@H]([C@H](NC(=O)CC(C)C)C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@@H](C(N[C@@H](C(N[C@H](C(N[C@H]1C)=O)CC(C)C)=O)CC(C)C)=O)CC(C)C)CC(C)C)C)C', "
               "'L-leucine derivative'), "
               "('ClC1=C(OC)C=C(O)C2=C1[C@](O[C@@H]3O[C@H]([C@H](OC)[C@](C3)(NO)C)C)([C@H]4C[C@@]5(O)[C@H](N(C)C)C(=O)C(=C([C@]5(C(C4=C2O)=O)O)O)C(=O)N)C', "
               "'L-leucine derivative'), "
               "('CC(C)(C)NC(=O)[C@@H]1C[C@@H]2CCCC[C@H]2CN1C[C@H]([C@H](CC3=CC=CC=C3)NC(=O)[C@H](CC(=O)N)NC(=O)C4=NC5=CC=CC=C5C=C4)O', "
               "'L-leucine derivative'), "
               "('O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)[C@@H](C(=O)N[C@@H](CCCCN=C(N)N)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC(=O)C)CC2=CC=CC=C2)C)/C)=O)C)C[C@H](CC)C)C', "
               "'L-leucine derivative'), "
               "('C1(C(=C([C@H]([C@@]2(C[C@@]3(CC4=C(C=C(C(=C4C(C3=C([C@]12O)O)=O)O)NC(C[NH2+]C(C)(C)C)=O)N(C)C)[H])[H])[NH+](C)C)[O-])C(=O)N)=O', "
               "'L-leucine derivative'), "
               "('CC=CC1=CC=C(C=C1)[C@H]2[C@H](N(C23CN(C3)C(=O)COC)CCC(F)(F)F)CO', "
               "'L-leucine derivative'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)C[C@@H](O)CCCCCCC)CC(C)C)CC(=O)O)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](C(N[C@@H](C(N[C@H](C(N[C@H](C(N[C@H]1CCC(=O)O)=O)C(C)C)=O)CC(C)C)=O)CCC(=O)N)=O)CC(C)C)CO)CC(C)C)CC(C)C)C', "
               "'L-leucine derivative'), "
               "('CC=CC1=CC=C2[C@H]3[C@@H](CN2C1=O)[C@@H]([C@H](N3CC4=CC=CC=C4OC)C(=O)N5CCOCC5)CO', "
               "'L-leucine derivative'), "
               "('O=C1[C@@]23C(=O)N[C@H]([C@@H]2[C@H](C)C(=C[C@@H]3C=C(CCCC(C[C@H]1CC(=O)C)=O)C)C)CC(C)C', "
               "'L-leucine derivative'), "
               "('O=C1O[C@@H](C(=O)N([C@H](C(=O)O[C@@H](C(O)N([C@H](C(O[C@@H](C(N([C@H]1C(C)C)C)=O)C(C)C)=O)CC(C)C)C)C(CC)C)C(C)C)C)C(C)C', "
               "'L-leucine derivative'), "
               "('O=C1N([C@H](C(=O)N2[C@H](C(=O)N([C@H](C(=O)NCC(=O)O[C@@H]([C@@H](C(N[C@@H](C(N3[C@@H](C(N[C@H]1CCC(C)C)=O)C[C@@H](C)C3)=O)CC(C)C)=O)N(C(=O)[C@H]4N(C(=O)[C@@H](N(C(=O)C(=O)CC)C)C(C)C)C[C@H](C4)CC)C)C)CC(C)C)C)CCC2)C(C)C)C', "
               "'L-leucine derivative'), "
               "('CC[C@@H](C)[C@@H]1OC(=O)[C@H](C(C)C)N(C)C(=O)[C@H](CC(C)C)NC(=O)[C@H](C(C)C)N(C)C(=O)[C@H](NC(=O)[C@@H]2CCCN2C(=O)[C@H](Cc2ccccc2)N(C)C(=O)[C@H](Cc2ccccc2)NC(=O)C(NC1=O)C(C)C)[C@H](C)C(C)C', "
               "'L-leucine derivative'), "
               "('S(CC(=O)N[C@H](C(=O)O[C@@H]([C@@H]1NC(=O)[C@@H](N(C(=O)[C@@H](NC(=O)C(N(C(=O)[C@H](OC([C@H]([C@H](OC([C@@H](N(C1=O)C)[C@H](OC)C)=O)C)NC(=O)C)=O)CC2=CC=CC=C2)C)=C)C)C)C)C(C)C)[C@H](O)C(C)C)C', "
               "'L-leucine derivative'), "
               "('O=C/1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CCCN=C(N)N)C(NC([C@@H](C(N[C@H](CCC(N\\\\C1=C\\\\C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)C[C@H](CC)C)C', "
               "'L-leucine derivative'), "
               "('O1[C@@H]2N([C@H]3C4=C(O)C(=C(OC)C(=C4[C@@H](CO)N5[C@H]3[C@@H]6[C@H]2C[C@H]([C@H]5C#N)N6C)O)C)CC1', "
               "'L-leucine derivative'), "
               "('O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)[C@@H](C(=O)N[C@@H](CC2=CC=C(O)C=C2)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)C=CC(=C[C@@H]([C@@H](OC)CC3=CC=CC=C3)C)C)=O)C)CC(C)C)CC(C)C', "
               "'L-leucine derivative'), "
               "('O=C1O[C@H]([C@H](NC(=O)[C@@](O)(C23O[C@@H](C([C@H](O2)C)CC3)C)C)C(=O)N4NCCC[C@@H]4C(=O)N(O)[C@@H](C)C(N5[C@@H](C(N6[C@H](C(N[C@H]1[C@H](O)C)=O)CCCN6)=O)CCCN5)=O)C(C)C', "
               "'L-leucine derivative'), "
               "('CCNC(=O)[C@@H]1[C@H]([C@@H]2CN3C(=CC=C(C3=O)C=CC)[C@H]1N2CC4=CC(=CC=C4)Cl)CO', "
               "'L-leucine derivative'), "
               "('CC=CC1=CC=C2[C@H]3[C@@H](CN2C1=O)[C@@H]([C@H](N3C(=O)C4CC4)C(=O)N5CCC6=CC=CC=C6C5)CO', "
               "'L-leucine derivative'), "
               "('S1SC(N)C(=O)N[C@H](C(=O)N[C@@]([C@@H](CC)C)(C(=O)N[C@H](C(=O)NC(C(=O)N[C@@H](C(=O)N2[C@H](CCC2)C(=O)N[C@H](CC(C)C)C(O)=O)C1)CC(=O)N)CCC(=O)N)[H])CC3=CC=C(O)C=C3', "
               "'L-leucine derivative'), "
               "('COC1=CC=C(C=C1)C2=CC=C3[C@H]4[C@@H](CN3C2=O)[C@@H]([C@H](N4)C(=O)N5CCOCC5)CO', "
               "'L-leucine derivative'), "
               "('C/C=C\\\\1/CN2[C@]3(C[C@@]1(C4([C@@]2(CC5(C6=CC=CC=C6N(C)[C@]35[H])[C@@]4(OC(\\\\C=C\\\\C7=CC(=C(C(=C7)OC)OC)OC)=O)[H])[H])C(=O)OC)[H])[H]', "
               "'L-leucine derivative'), "
               "('O=C1O[C@@]23C(=O)N[C@H]([C@@H]2C(C)=C([C@H]([C@@H]3C=CC[C@H](C)CCCC(C=C1)=O)O)C)CC4=CC=CC=C4', "
               "'L-leucine derivative'), "
               "('O=C1C=C[C@H](O)CCC[C@H](CC=C[C@@H]2[C@@]13C(=O)N[C@H]([C@@H]3[C@H](C)C(=C2)C)CC4=CC=CC=C4)C', "
               "'L-leucine derivative'), "
               "('O=C1N2[C@@]3(C(=O)NC14C(C(C5=[N+]([O-])C6=C(C75[C@@H]4N8C(=O)[C@@]9%10N(CCC9)C(C8%11C(C(C)(C)C=%12[C@]([C@H]7%11)(O)C%13=C(C%14=C(OC(C)(C)C=C%14)C=C%13)[N+]%12[O-])C%10)=O)C=CC%15=C6C=CC(O%15)(C)C)(C)C)C3)CCC2', "
               "'L-leucine derivative'), "
               "('CC[C@H](C)[C@@H](C(=O)N[C@@]1(CCCC=CCCC[C@](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC1=O)CC(C)C)CS)CCCNC(=N)N)(C)C(=O)N[C@@H](CC2=CNC=N2)C(=O)N[C@@H](CC3=CNC=N3)C(=O)N[C@@H](CO)C(=O)N[C@@H]([C@@H](C)O)C(=O)N)C)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CCC(=O)O)NC(=O)[C@H](CC4=CNC5=CC=CC=C54)NC(=O)CCNC(=O)C', "
               "'L-leucine derivative'), "
               "('OC(=O)[C@H](CCCC(=O)NCC(=O)NC1=CC=CC=C1)C[C@H](N)C(O)=O', "
               "'L-leucine derivative'), "
               "('[H][C@@]12C[C@H]3[C@H](CC)[C@@H](O)N1[C@H]1C[C@@]4([C@H](OC(C)=O)C31)c1ccccc1N[C@@]24[H]', "
               "'L-leucine derivative'), "
               "('CC(C)C[C@@H]1NC(=O)[C@H](NC(=O)[C@@H]2CCCN2C(=O)[C@@H](CC(O)=O)NC(=O)[C@@H](Cc2c[nH]c3ccccc23)NC1=O)c1cccs1', "
               "'L-leucine derivative'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC2=CC=CC=C2)CC(C)C)CC(=O)N)CCCCN)CO)CC(=O)NCC(=O)N[C@H](C(=O)NCC(N[C@H](C(N[C@H](C(N[C@H]1CC=3C4=C(C=CC=C4)NC3)=O)C)=O)CC(=O)N)=O)CC5=CC=C(O)C=C5', "
               "'L-leucine derivative'), "
               "('O1[C@H](O[C@H]2[C@H](O)[C@@H](O)C(O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]([C@H]1CO)O[C@H]3O[C@@H]([C@@H](N[C@@H]4[C@H](O)[C@@H](O)[C@H](O)[C@]5([C@@H]4O5)CO)[C@@H]([C@H]3O)O)CO', "
               "'L-leucine derivative'), "
               "('CC(C)C[C@H](NC(=O)[C@@H](N)[C@@H](C)O)C(O)=O', 'L-leucine "
               "derivative'), "
               "('S([C@H]1C(=O)[C@@]23C(=O)N[C@H]([C@@H]2C(C)=C([C@H]([C@@H]3C=C(C)CCCC(C1)=O)O)C)CC(C)C)C', "
               "'L-leucine derivative'), "
               "('O=C1C2=C[C@H]3[C@@H]([C@@H](O)[C@](O)(C(=O)C)[C@H](C3)C)[C@H]([C@]24C(=O)N[C@H]([C@@H]4C(=C1C)C)CC5=CC=CC=C5)OC(=O)C', "
               "'L-leucine derivative'), "
               "('O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)[C@@H](C(=O)N[C@@H](C(C)C)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)C)CC(C)C)C', "
               "'L-leucine derivative'), "
               "('CC1=C2N3[C@H]([C@H](CC(N)=O)[C@@]2(C)CCC([O-])=O)[C@]2(C)[N+]4=C([C@@H](CCC(N)=O)[C@]2(C)CC(N)=O)C(C)=C2[N+]5=C(C=C6[N+](=C1[C@@H](CCC(N)=O)C6(C)C)[Co--]345C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc3c(N)ncnc13)[C@@H](CCC(N)=O)[C@]2(C)CC(N)=O', "
               "'L-leucine derivative'), "
               "('CC[C@H](C)[C@H](N(C)C)C(=O)N[C@H]1[C@@H](Oc2ccc(cc2)\\\\C=C/NC(=O)[C@H](CC(C)C)NC1=O)C(C)C', "
               "'L-leucine derivative'), "
               "('ClC(Cl)CCCCCC[C@@H](N)CC(=O)N[C@H](C(=O)N[C@H](C(=O)N([C@H](C(=O)N1[C@H](C(=O)O)CCC1)CC2=CC=C(O)C=C2)C)CC(C)C)CC3=CC=C(O)C=C3', "
               "'L-leucine derivative'), "
               "('COC([C@@H]1C[C@@]23CCCN4CCC5(C6=CC=CC=C6N(C)[C@]15CC2)[C@]34[H])=O', "
               "'L-leucine derivative'), "
               "('O=C1OC([C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C[C@@H](O)CCCCCCCCC)CC(C)C)CCC(=O)O)C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(N[C@H](C(N[C@@H](C(N[C@H]1C(CC)C)=O)CO)=O)CC(C)C)=O)CO)CC(C)C)C(C)C)C', "
               "'L-leucine derivative'), "
               "('CC(C)C[C@H](NC(=O)[C@H](CC1=CC=CC=C1)NC(=O)CNC(=O)CNC(=O)[C@@H](N)CC1=CC=C(O)C=C1)C(O)=O', "
               "'L-leucine derivative'), "
               "('O=C1N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](CO)C(N[C@@H](C(N[C@H](C(NC(CC(O[C@@H]([C@@H]1NC(=O)C(NC(=O)[C@H](NC(=O)CC(O)CCCCCCC)CC(C)C)CC(=O)O)C)=O)C(=O)O)=O)[C@H](CC)C)=O)CC(C)C)=O)CC(C)C)CO)CC(C)C)CC(C)C', "
               "'L-leucine derivative'), "
               "('O=C/1NCC(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CCCN=C(N)N)C(N[C@H]([C@@H](C(N[C@H](CCC(N\\\\C1=C/C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC(=O)C)CC2=CC=CC=C2)C)/C)=O)CC(C)C', "
               "'L-leucine derivative'), "
               "('CC(C)NC(=O)N1CC2(C1)[C@@H]([C@H](N2CCC(F)(F)F)CO)C3=CC=CC=C3', "
               "'L-leucine derivative'), "
               "('C1[C@@H]2[C@H]([C@@H]([C@@H](N2C(=O)C3=NC=CN=C3)C4=CC=CC(=O)N41)C(=O)NCC5=CC(=CC(=C5)F)F)CO', "
               "'L-leucine derivative'), "
               "('C([C@H](CC1=CC=CC=C1)NC(=O)[C@H]2N(CCC2)C([C@H](CCSC)NC(=O)[C@H]3N(CCC3)C(=O)CNC([C@H](CCCC[NH3+])NC([C@H](CC4=CN=CN4)NC([C@H](CO)NC([C@H](CC(C)C)NC([C@H](CCCNC(=[NH2+])N)NC(=O)[C@H]5N(CCC5)C([C@H](CCCNC(=[NH2+])N)NC([C@H]6NC(=O)CC6)=O)=O)=O)=O)=O)=O)=O)=O)(=O)[O-]', "
               "'L-leucine derivative'), "
               "('CCCCCC[C@H](C)C[C@H](C)[C@H]1OC(=O)[C@H](C)NC(=O)[C@H](C)NC(=O)[C@H](CC(C)C)NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H]1C)C(C)C', "
               "'L-leucine derivative'), "
               "('O=C(NC[C@@H]1N2C[C@@H]([C@](C1)(CC2)[H])CC)C=3OC=CC3', "
               "'L-leucine derivative'), "
               "('O=C1[C@@]23C(=O)N[C@H]([C@@H]2[C@H](C)C(=C[C@@H]3CC(C)=CC[C@H](C1)O)C)CC(C)C', "
               "'L-leucine derivative'), "
               "('C12=CC=CC=C1NC3=C2[C@]4([C@H]([C@](CC[C@@]4(C3(C)C)[H])(C)C=C)[N+]#[C-])[H]', "
               "'L-leucine derivative'), "
               "('ClC=1C(=O)C(Cl)=CC2(C1)OC(O)[C@H](C2)NC(=O)/C=C/C(=C/C(CCCCCC)C)/C', "
               "'L-leucine derivative'), "
               "('O=C(N[C@H](C(=O)OC[C@@H](NC(=O)C1=CC=CC=C1)CC2=CC=CC=C2)CC(C)C)C3=CC=CC=C3', "
               "'L-leucine derivative'), "
               "('CN1[C@H]2[C@H](CN3C2=CC=C(C3=O)C4=CC=CC=C4F)[C@H]([C@@H]1C(=O)NCC(F)(F)F)CO', "
               "'L-leucine derivative'), "
               "('O=C1[C@@]23C(=O)N[C@H]([C@@H]2[C@H](C)C(=C[C@@H]3C=C(CC[C@H]([C@H]([C@@H](C1)OC)O)O)C)C)CC(C)C', "
               "'L-leucine derivative'), "
               "('ClC(Cl)CCCCCC[C@@H](N)[C@@H](O)C(=O)N[C@H](C(=O)N([C@H](C(=O)N1[C@H](C(=O)N[C@H](C(=O)O)CC2=CC=C(O)C=C2)CCC1)CC(C)C)C)[C@H](CC)C', "
               "'L-leucine derivative'), "
               "('CC(C)C[C@H](NC(=O)[C@H](C)N)C(=O)N[C@@H](C)C(=O)N1CCC[C@H]1C(O)=O', "
               "'L-leucine derivative'), "
               "('C1C=2C=3C(NC2[C@]4(N5[C@@]1([C@]([C@](C4)(/C(/C5)=C(\\\\C)/[H])[H])(CO)C(OC)=O)[H])[H])=CC=CC3', "
               "'L-leucine derivative'), "
               "('O=C/1N[C@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O[C@@H](CC(N[C@H](C(N[C@H](C(N[C@H](C(N\\\\C1=C\\\\C)=O)CCN)=O)CC(C)C)=O)CN)=O)CCCCCCCCC)CC(=O)O)C(O)(C)C)CC2=CC=CC=C2)CN)[C@H](O)C', "
               "'L-leucine derivative'), ('*C([C@H](C1C(C)C1)N*)=O', "
               "'L-leucine derivative'), "
               "('CCN1[C@@H]2CN3C(=CC=C(C3=O)C=CC)[C@H]1[C@H]([C@@H]2CO)C(=O)N4CCC5=CC=CC=C5C4', "
               "'L-leucine derivative'), "
               "('O=C1O[C@@]23C(=O)N[C@H]([C@@H]2[C@H](C)C(=C[C@@H]3C=CC[C@@H](C([C@@H](C=C1)C)O)C)C)CC4=CC=C(O)C=C4', "
               "'L-leucine derivative'), "
               "('O=C1C=CCCC(=C[C@H](CC=C[C@@H]2[C@@]13C(=O)N[C@H]([C@@H]3[C@H](CC)C(=C2)C)[C@@H](C=4C5=C(C=CC=C5)NC4)C)C)C', "
               "'L-leucine derivative'), "
               "('CCS(=O)(=O)N1CC2(C1)[C@H]([C@H](N2CC3=CC=C(C=C3)F)CO)C4=CC=CC=C4', "
               "'L-leucine derivative'), "
               "('CCCNC(=O)[C@@H]1[C@H]([C@@H]2CN3C(=CC=C(C3=O)C=CC)[C@H]1N2C(=O)NC4=C(C=CC(=C4)F)F)CO', "
               "'L-leucine derivative'), "
               "('O=C1C(=C[C@H](CC=C[C@@H]2C3(C=4C1=CNC4)C(=O)N[C@H]([C@@H]3[C@H](C)C([C@H]2O)=C)CC=5C6=C(C=CC=C6)NC5)C)C', "
               "'L-leucine derivative'), "
               "('O=C(N[C@H](C(=O)N[C@H](CN)CC(C)C)[C@H](CC)C)C(NC(=O)[C@@H](NC(=O)C(NC(=O)[C@@H](NC(=O)[C@H]1N(C(=O)[C@H]2N(C(=O)CCCCCCCCC)C[C@@H](C2)O)C[C@@H](C1)O)C(C)C)(C)C)CCC(=O)N)(C)C', "
               "'L-leucine derivative'), "
               "('O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC=O)[C@@H](CC)C)C(=O)N[C@@H](C(=O)N[C@H](C(C)C)C(N2[C@H](C(N[C@H](C(N([C@H]1C(C)C)C)=O)CC(C)C)=O)C[C@H](O)CN2)=O)CC3=CC=C(OC)C=C3)C', "
               "'L-leucine derivative'), "
               "('[H][C@@]1(Cc2ccc(O)cc2)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CC(N)=O)NC(=O)[C@@H](Cc2ccccc2)NC(=O)[C@H](Cc2c[nH]c3ccccc23)NC(=O)[C@]2([H])CCCN2C(=O)[C@@H](Cc2ccccc2)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCCN)NC(=O)[C@@H](NC1=O)C(C)C', "
               "'L-leucine derivative'), "
               "('[C@@H]1(C(=O)N[C@H](C(N[C@@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(=O)N1)CCC(=O)O)C(C)O)=O)CCC(O)=O)=O)CO)=O)CC(C)C)=O)CC(C)C)=O)CCCCN)C(O)C', "
               "'L-leucine derivative'), "
               "('CC(C)CCCCC(=O)N[C@@H](CCN)C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](CCN)C(=O)N[C@H]1CCNC(=O)[C@@H](NC(=O)[C@H](CCN)NC(=O)[C@H](CCN)NC(=O)[C@H](CC(C)C)NC(=O)[C@@H](CC(C)C)NC(=O)[C@H](CCN)NC1=O)[C@@H](C)O', "
               "'L-leucine derivative'), "
               "('CC(C)C[C@H](NC(=O)[C@H](CO)NC(=O)[C@@H]1CCCN2N1C(=O)[C@H](CCC2=O)NC(=O)[C@H](C)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@H](CC1CCCCC1)NC(C)=O)C(N)=O', "
               "'L-leucine derivative'), "
               "('COCCOC(=O)N1C2=C(C=C(C=C2)C#CCC(C(=O)OC)C(=O)OC)[C@@]3(C1=O)[C@H]([C@@H]4C(=O)O[C@H]([C@H](N4[C@H]3C5=CC=CC=C5OCCO)C6=CC=CC=C6)C7=CC=CC=C7)C(=O)N8CCN(CC8)C9=NC=CC=N9', "
               "'L-leucine derivative'), "
               "('O=C(N1[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](CO)CC(C)C)CCC(=O)N)C)CC(C)C)C[C@H](C1)O)C(NC(=O)CCCCCCCCCCCCC)(C)C', "
               "'L-leucine derivative'), "
               "('O=C(N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC(C)C)[C@H](CC)C)C)[C@](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CNC(=O)CCCCCCC)C)CC(C)C)(CC)C', "
               "'L-leucine derivative'), "
               "('O=C1O[C@@]23C(=O)N[C@H]([C@@H]2[C@H](C)C([C@H]([C@@H]3C=CC[C@H](C)CCC[C@H](C=C1)O)O)=C)CC4=C(O)C=CC=C4', "
               "'L-leucine derivative'), "
               "('CC(C)C[C@H](N)C(=O)N[C@@H](CC(C)C)C(O)=O', 'L-leucine "
               "derivative'), "
               "('C1CCC(C1)C(=O)N2CC3(C2)[C@@H]([C@H](N3CC4CC4)CO)C5=CC=CC=C5', "
               "'L-leucine derivative'), "
               "('CC(C)C[C@H](NC(=O)[C@@H](N)CC(O)=O)C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](CC(O)=O)C(O)=O', "
               "'L-leucine derivative'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C[C@H](O)CCCCCCCCC)CC(C)C)CCC(=O)O)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(N[C@H](C(N[C@@H](C(N[C@H]1[C@H](CC)C)=O)CO)=O)CC(C)C)=O)CO)CC(C)C)[C@H](CC)C)C', "
               "'L-leucine derivative'), "
               "('O=C1O[C@H]([C@H](CCCCCC)C)CC(=O)N[C@@H](C(C)C)C(N[C@H](C(N[C@@H]1CC(C)C)=O)C)=O', "
               "'L-leucine derivative'), "
               "('C(=O)([C@@H](N)CCC(=O)O)N[C@H](C(=O)N[C@H](C(=O)O)CC(C)C)CC(=O)O', "
               "'L-leucine derivative'), "
               "('ClCCCCCCC[C@@H](N)[C@@H](O)C(=O)N[C@H](C(=O)N([C@H](C(=O)N1[C@H](C(=O)N[C@H](C(=O)O)CC2=CC=C(O)C=C2)CCC1)CC(C)C)C)[C@H](CC)C', "
               "'L-leucine derivative'), "
               "('C[C@H]1[C@H]2[C@H](Cc3c[nH]c4ccccc34)NC(=O)[C@@]22[C@@H](\\\\C=C\\\\C[C@H](C)\\\\C=C(C)\\\\[C@@H](OC(C)=O)C(=O)\\\\C=C\\\\C2=O)C2O[C@]12C', "
               "'L-leucine derivative'), "
               "('O=C/1N[C@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O[C@@H](CC(N[C@H](C(N[C@H](C(N[C@H](C(N\\\\C1=C\\\\C)=O)CCN)=O)CC(C)C)=O)CN)=O)CCCCCC(C)C)CC(=O)O)C(C)C)CC2=CC=CC=C2)CN)[C@H](O)C', "
               "'L-leucine derivative'), "
               "('CCC(=O)N1CC2(C1)[C@@H]([C@H](N2S(=O)(=O)C)CO)C3=CC=C(C=C3)C4=CC(=CC=C4)C', "
               "'L-leucine derivative'), "
               "('O=C(N[C@H](C(=O)N[C@H](CN)CC(C)C)CC(C)C)C(NC(=O)[C@@H](NC(=O)C(NC(=O)[C@@H](NC(=O)[C@H]1N(C(=O)[C@H]2N(C(=O)CCCCCCCCC)C[C@@H](C2)O)C[C@@H](C1)O)C(C)C)(C)C)CCC(=O)N)(C)C', "
               "'L-leucine derivative'), "
               "('O=C1NC=2C(C(=O)[C@H]3OC3(C)C)=CC=CC2[C@@]14C([C@]5(O)C[C@@H]6CCC[C@H](N6C[C@]5(C4)NC)C)(C)C', "
               "'L-leucine derivative'), "
               "('O=C1N([C@H](C(=O)N([C@H](C(=O)N[C@H](C(=O)N(C)[C@H](C(N([C@@H](C(N[C@@H](C(N[C@@H]1[C@H](CC)C)=O)[C@H](O)C(C)C)=O)C)C)=O)C)CC(C)C)CC(C)C)C)C)C', "
               "'L-leucine derivative'), "
               "('O=C(N1[C@H](C(=O)N[C@H](C(=O)NC(C(=O)N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)NC(C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](CO)CC(C)C)C)CCC(=O)N)(C)C)(C)C)CCC(=O)N)CCC(=O)N)(C)C)CC2=CC=CC=C2)CCC1)C(NC(=O)CCCCCCCCC)(C)C', "
               "'L-leucine derivative'), "
               "('O=C1[C@@H](O)CC(=O)O[C@@]23C(=O)N[C@H]([C@@H]2[C@H](C)C(=C[C@@H]3C=C(CC[C@H]1O)C)C)CC(C)C', "
               "'L-leucine derivative')]\n"
               "False negatives: [('COC(=O)[C@@H](N)CC(C)C', 'Not an L-leucine "
               "derivative')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 5136,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9809087437953418}