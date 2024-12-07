"""
Classifies: CHEBI:134045 polychlorinated dibenzodioxines and related compounds
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_polychlorinated_dibenzodioxines_and_related_compounds(smiles: str):
    """
    Determines if a molecule is a polychlorinated dibenzodioxine or related compound.
    This includes polychlorinated dibenzofurans and polychlorinated/brominated biphenyls.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule belongs to this class, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Count number of chlorine and bromine atoms
    num_cl = len([atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'Cl'])
    num_br = len([atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'Br'])

    # Define SMARTS patterns for the core structures
    biphenyl_pattern = Chem.MolFromSmarts('c1ccccc1-c1ccccc1')
    dioxin_pattern = Chem.MolFromSmarts('c1ccc2Oc3ccccc3Oc2c1')
    furan_pattern = Chem.MolFromSmarts('c1ccc2oc3ccccc3c2c1')

    # Check for core structures
    is_biphenyl = mol.HasSubstructMatch(biphenyl_pattern)
    is_dioxin = mol.HasSubstructMatch(dioxin_pattern)
    is_furan = mol.HasSubstructMatch(furan_pattern)

    # For biphenyls, require at least 4 chlorines or bromines
    if is_biphenyl:
        if num_cl >= 4:
            return True, f"Polychlorinated biphenyl with {num_cl} chlorine atoms"
        elif num_br >= 4:
            return True, f"Polybrominated biphenyl with {num_br} bromine atoms"

    # For dioxins and furans, require at least 4 chlorine
    if is_dioxin and num_cl >= 4:
        return True, f"Polychlorinated dibenzodioxin with {num_cl} chlorine atoms"
    
    if is_furan and num_cl >= 4:
        return True, f"Polychlorinated dibenzofuran with {num_cl} chlorine atoms"

    return False, "Does not match structural requirements for this class"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134045',
                          'name': 'polychlorinated dibenzodioxines and related '
                                  'compounds',
                          'definition': 'Organochlorine compounds that are '
                                        'polychlorinated dibenzodioxines and '
                                        'structurally related entities that '
                                        'are persistant organic pollutants. '
                                        'These include polychlorinated '
                                        'dibenzofurans as well as '
                                        'polychlorinated and polybrominated '
                                        'biphenyls  They vary widely in their '
                                        'toxicity, but their toxic mode of '
                                        'action is through the aryl '
                                        'hydrocarbon receptor.',
                          'parents': ['CHEBI:17792']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.10714285714285715 is too low.\n'
               "True positives: [('Clc1ccc(-c2cc(Cl)c(Cl)c(Cl)c2)c(Cl)c1Cl', "
               "'Polychlorinated biphenyl with 6 chlorine atoms'), "
               "('ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C', "
               "'Polychlorinated biphenyl with 4 chlorine atoms'), "
               "('Clc1cccc(c1)-c1cc(Cl)c(Cl)c(Cl)c1Cl', 'Polychlorinated "
               "biphenyl with 5 chlorine atoms'), "
               "('Clc1cc(Cl)c(Cl)c(c1)-c1cc(Cl)cc(Cl)c1Cl', 'Polychlorinated "
               "biphenyl with 6 chlorine atoms'), "
               "('Clc1ccc(cc1Cl)-c1cc(Cl)c(Cl)cc1Cl', 'Polychlorinated "
               "biphenyl with 5 chlorine atoms'), "
               "('Clc1cc2oc3cc(Cl)c(Cl)c(Cl)c3c2c(Cl)c1Cl', 'Polychlorinated "
               "dibenzofuran with 6 chlorine atoms')]\n"
               'False positives: '
               "[('Brc1ccc2c(c[nH]c2c1)[C@H]1CNC(=O)C(=N1)c1c[nH]c2cc(Br)ccc12', "
               "'Polybrominated aromatic compound with 2 bromine atoms'), "
               "('ClC1=C(O)C=C2OC3=C(O)C=CC(=C3)[C@@H](NC)C(N[C@H]4C(N[C@H](C1=C2)C(=O)N[C@H]5C(=O)N[C@@H]6C(=O)N[C@H](C(=O)NC(C(=O)O)C=7C(C8=CC6=CC(Cl)=C8O[C@@H]9O[C@H]([C@H](O)[C@H]([C@H]9O)O)CO)=C(O)C=C(O)C7)[C@@H](O[C@@H]%10O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]%10NC(=O)CCCCCCCCC)O)C%11=CC(=C(OC=%12C=C5C=C(OC%13=C(C=C([C@H]4O)C=C%13)Cl)C%12O[C@@H]%14O[C@H]([C@H](O)[C@H]([C@H]%14O)O)CO)C(Cl)=C%11)Cl)=O)=O', "
               "'Polychlorinated biphenyl with 5 chlorine atoms'), "
               "('ClC1=CC(=C(NC(=O)CN2CCC(CC2)C)C=C1)C(=O)C=3C(Cl)=CC=CC3', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('[H+].[H+].[Cl-].[Cl-].COc1ccc2nc3cc(Cl)ccc3c(NC(C)CCCN(CCCl)CCCl)c2c1', "
               "'Polychlorinated aromatic compound with 5 chlorine atoms'), "
               "('CC(C)(C)C1=CC=C(C=C1)C(=O)NC2=CC(=C(C=C2C(=O)O)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1=CC(=CN=C1)C(=O)N[C@@H]2C=C[C@H](O[C@@H]2CO)CC(=O)NCC3=CC(=C(C=C3)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C[C@@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)CC3=CC(=C(C=C3)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('N1=C2C(=C(C3=C1C=CC(=C3)OC)[NH2+]CCC[NH2+]CCCl)C=CC(=C2)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1=CC(=CC(=C1)OCC2=C(C=C(C=C2)Cl)Cl)C=C3C(=O)N(C(=S)S3)CC(=O)O', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('NC(=N)NCCCCNC(=O)[C@@]1(O)[C@H](c2c[nH]c3cc(Br)ccc23)[C@@](O)(Cc2c[nH]c3cc(Br)ccc23)C(=O)N1CCCCNC(N)=N', "
               "'Polybrominated aromatic compound with 2 bromine atoms'), "
               "('CC1=C(C=CC(=C1)[N+](=O)[O-])NS(=O)(=O)C2=C(C=CC(=C2)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(C=2OC3=C(C=C(Cl)C=C3)C(NC2C(=C1)C(=O)N)=O)C', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(C=2OC3=C(C=C(Cl)C=C3)C(NC2C(=C1)C(=O)O)=O)C', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('Oc1cc(Cl)c(cc1Cl)-c1ccccc1Cl', 'Polychlorinated biphenyl "
               "with 3 chlorine atoms'), "
               "('O\\\\N=C1\\\\Cc2cc(Br)c(Oc3cc(C\\\\C(C(=O)NCCc4cc(Br)c(O)c(Oc5ccc(CCNC1=O)cc5Br)c4)=N/O)cc(Br)c3O)c(Br)c2', "
               "'Polybrominated aromatic compound with 5 bromine atoms'), "
               "('Clc1ccc(NC(=O)Nc2ccc(Cl)c(Cl)c2)cc1', 'Polychlorinated "
               "aromatic compound with 3 chlorine atoms'), "
               "('BrC1=CC=2NC=3C=C(Br)C=CC3C2C=C1', 'Polybrominated aromatic "
               "compound with 2 bromine atoms'), "
               "('C=1C2=C(C(=CC1Cl)Cl)OC(C=C2)C=3C=CC=CC3', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('C1=CC=C(C(=C1)COC2=C(C=C(C=C2)Br)C=C3C(=O)NC(=S)S3)Br', "
               "'Polybrominated aromatic compound with 2 bromine atoms'), "
               "('[H]C(=CC([H])=C1N(CC)c2cc(Cl)c(Cl)cc2N1CC)c1n(CC)c2cc(Cl)c(Cl)cc2[n+]1CC', "
               "'Polychlorinated aromatic compound with 4 chlorine atoms'), "
               "('COC1=CC=C(C=C1)C(C(=O)NC2CCCCC2)N(C3=CC(=CC=C3)Cl)C(=O)CCl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)N(C)C)O[C@H]1CN(C)CC3=CC(=C(C=C3)Cl)Cl)[C@@H](C)CO', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1=CC=NC(=C1)C=NNC(=O)C2=CC(=C(C=C2)Cl)Cl', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('CN(C)CC(O)Cn1c2ccc(Br)cc2c2cc(Br)ccc12', 'Polybrominated "
               "aromatic compound with 2 bromine atoms'), "
               "('ClC(Cl)CCC[C@@H]1C2=C(O)C=C([C@H](OC(=O)N)[C@H](CCCC[C@H](CCCC(Cl)Cl)C3=C(C=C(C[C@H](CCCC1)C)C=C3O)O)C)C=C2O', "
               "'Polychlorinated aromatic compound with 4 chlorine atoms'), "
               "('OC(=O)C(O)(c1ccc(Cl)cc1)c1ccc(Cl)cc1', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(O)C(Cl)=C2[C@@H](CC)OC(C2=C1OC3=C(OC)C=C(O)C(=C3CCC)Cl)=O', "
               "'Polychlorinated aromatic compound with 3 chlorine atoms'), "
               "('C[C@]12CC[C@H]3[C@@H](CCc4cc(OC(=O)Cc5ccc(cc5)N(CCCl)CCCl)ccc34)[C@@H]1CC[C@@H]2OC(=O)Cc1ccc(cc1)N(CCCl)CCCl', "
               "'Polychlorinated aromatic compound with 4 chlorine atoms'), "
               "('ClC1=C2OC3=C(Cl)C(O)=C(Cl)C(=C3C(C2=C(O)C(=C1O)Cl)=O)C', "
               "'Polychlorinated aromatic compound with 4 chlorine atoms'), "
               "('OC(=O)c1nn(Cc2ccc(Cl)cc2Cl)c2ccccc12', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('C1=CC=C2C(=C1)C=CC=C2CC(=O)NC(C(Cl)(Cl)Cl)NC(=S)NC3=CC=CC=C3Cl', "
               "'Polychlorinated aromatic compound with 4 chlorine atoms'), "
               "('ClC1=C(O)C2=C(OC=3N([C@@H]4O[C@@H]([C@@H](O)[C@@H]([C@H]4O)O)CO)C(=CC3C2=O)Cl)C(=C1)C', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=CC2=CC=C1OC=3C(O)=C4C=C([C@@](NC([C@@]5([H])NC(=O)[C@](CC=6C=C(Cl)C(O4)=CC6)([H])NC(=O)[C@H](NS(=O)(=O)C=7C=CC=CC7)C=8C=C(C(=CC8)O)OC=9C=C5C=C(C9)O)=O)(C(N[C@]%10([H])C%11=CC=C(O)C(=C%11)C%12=C(C=C(C=C%12O)O)[C@H](C(=O)O)NC(=O)[C@@]([H])([C@]2([H])O[C@@H]%13O[C@H](CO)[C@H]([C@@H]([C@H]%13NC(=O)C)O)O)NC%10=O)O)[H])C3', "
               "'Polychlorinated biphenyl with 2 chlorine atoms'), "
               "('Cl.[H][C@]1(CC[C@H](NC)c2ccccc12)c1ccc(Cl)c(Cl)c1', "
               "'Polychlorinated aromatic compound with 3 chlorine atoms'), "
               "('ClC1=C(OC)C(Cl)=CC(=C1)COC(=O)C2=CC(Cl)=C(O)C(=C2)Cl', "
               "'Polychlorinated aromatic compound with 4 chlorine atoms'), "
               "('CN[C@H]1CC[C@@H](C2=CC=CC=C12)C3=CC(=C(C=C3)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('Clc1cc(Cl)c2C(c3ccccc3CCc2c1)n1ccnc1', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('O[N+]([O-])=O.Clc1ccc([C@@H](Cn2ccnc2)OCc2c(Cl)cccc2Cl)c(Cl)c1', "
               "'Polychlorinated aromatic compound with 4 chlorine atoms'), "
               "('CC1=C(C(=NO1)C2=C(C=CC=C2Cl)Cl)COC(=O)C3=CC=C(C=C3)[N+](=O)[O-]', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('CC1(C)C(C=C(Cl)c2ccc(Cl)cc2)C1C(=O)OC(C#N)c1ccc(F)c(Oc2ccccc2)c1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(O)C(Cl)=C2[C@@H](CC)OC(C2=C1OC3=C(OC)C=C(OC)C(=C3CCC)Cl)=O', "
               "'Polychlorinated aromatic compound with 3 chlorine atoms'), "
               "('C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CN3C=NN=N3)O[C@@H]1CN(C)CC4=CC(=C(C=C4)Cl)Cl)[C@@H](C)CO', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C2OC3=C(C=C(O)C=C3CCC)OC(C2=C(CCC)C(=C1O)Cl)=O', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('COC1=CC2=C(C=C1)N(C(=O)C1=C(Cl)C(Cl)=CC=C1)C(C)=C2CCN1CCOCC1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('CC(C)N=c1cc2n(-c3ccc(Cl)cc3)c3ccccc3nc2cc1Nc1ccc(Cl)cc1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C[C@@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC4=C(C=C3)OCO4)[C@@H](C)CO)C)CN(C)CC5=CC(=C(C=C5)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('Cc1cc(cc(Br)c1O)C1(OS(=O)(=O)c2ccccc12)c1cc(C)c(O)c(Br)c1', "
               "'Polybrominated aromatic compound with 2 bromine atoms'), "
               "('C[C@@H](CN([C@H](C)CO)C(=O)NC1=CC=C(C=C1)F)[C@@H](CN(C)C(=O)C2=CC(=CC(=C2)Cl)Cl)OC', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(OC)C(=C(C)C(=C1O)Cl)C(=O)O[C@H]2[C@H](O[C@@H]3O[C@H]([C@H](OC)[C@](C3)([N+](=O)[O-])C)C)C[C@H](O[C@H]4[C@H](O)C[C@@]5(O[C@@]6([C@H](O)[C@H](O[C@H]7[C@@H](OC)[C@H](O[C@H]([C@@H]7O)O[C@H]8[C@H](O)[C@H](OC)[C@H](O[C@@H]9OC[C@@H]%10O[C@@]%11(O[C@H]%10[C@H]9O)OC[C@@H](OC(=O)C%12=C(O)C=C(O)C=C%12C)[C@H]%13[C@H]%11OCO%13)O[C@@H]8COC)C)O[C@@H]([C@H]6O5)C)C)O[C@@H]4C)O[C@@H]2C', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(O)C(Cl)=C(CCCCC)C(=C1O)C(=O)OC2=CC(OC)=C(C(=O)O)C(=C2)CCCCC', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC(c1ccccc1)c1ccccc1Cl', 'Polychlorinated aromatic compound "
               "with 2 chlorine atoms'), "
               "('C1=CC=C2C(=C1)C(=NN2CC3=CC(=C(C=C3)Cl)Cl)C(=O)O', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1C[C@@H]([C@@H](O[C@@H]1CCNC(=O)C2=CC(=CC(=C2)Cl)Cl)CO)NC(=O)CC3=CC=CC=N3', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(OC)C(C2=C3C(=O)C=4C(=O)C5=C(O)C=C(O)C=C5C(C4C(C3=C(Cl)C(=C2)OC)=O)(C)C)=C(C)C=C1OC', "
               "'Polychlorinated biphenyl with 2 chlorine atoms'), "
               "('C1=CC(=CC=C1NC(=O)OCC2=CN(N=N2)C3=CC=C(C=C3)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('CC1=CC=CC=C1C(=O)NN=C(C)CC(=O)NC2=C(C(=CC=C2)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('CCN1CCC(CC1)N2C=C(N=N2)CNC3=CC(=C4C(=C3)C(=C(C=N4)C#N)NC5=CC(=C(C=C5)F)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1=CC(=CC(=C1)Cl)NC(=O)CSC2=NC(=O)NC(=N2)C3=CC=C(C=C3)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('O.[Cl-].[Cl-].CCO.[H][C@@]12[C@@H](C)c3cccc(O)c3C(=O)C1=C(O)[C@]1(O)C(=O)C(C(N)=O)=C(O)[C@@H]([NH+](C)C)[C@]1([H])[C@H]2O.[H][C@@]12[C@@H](C)c3cccc(O)c3C(=O)C1=C(O)[C@]1(O)C(=O)C(C(N)=O)=C(O)[C@@H]([NH+](C)C)[C@]1([H])[C@H]2O', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('CC1=C(N(N=C1C(=O)NN2CCOCC2)C3=C(C=C(C=C3)Cl)Cl)C4=CC=C(C=C4)I', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('FC(F)(F)C1=NC=CC=C1C(=O)NC1CCC1C1=C(Cl)C=C(Cl)C=C1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('CSC1=NC2=C(S1)C=C(C=C2)NS(=O)(=O)C3=C(C=CC=C3Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(O)C=CC(=C1)C2NC(=O)[C@H](N(C(=O)[C@@H](NC(=O)[C@@H](C)CC(=C[C@@H]([C@H](OC([C@H]2O)=O)C)C)C)C)C)CC3=C(Cl)NC4=C3C=CC=C4', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('OCC(c1ccc(Cl)cc1)c1ccc(Cl)cc1', 'Polychlorinated aromatic "
               "compound with 2 chlorine atoms'), "
               "('Oc1cc(Cl)c(cc1Cl)-c1cc(Cl)c(Cl)cc1Cl', 'Polychlorinated "
               "biphenyl with 5 chlorine atoms'), "
               "('COC1=CC=C(C=C1)NC(=O)N[C@H]2CC[C@@H](O[C@H]2CO)CCNC(=O)C3=CC(=CC(=C3)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1CN(CCN1C2=C3C=CC(=CC3=NC=C2)Cl)C(=O)C4=CC=C(C=C4)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1=CC(=C(C=C1Cl)Cl)CN=C(N)NC(=O)C2=C(N=C(C(=N2)Cl)N)N', "
               "'Polychlorinated aromatic compound with 3 chlorine atoms'), "
               "('ClC=1C=2NC3=C(C=C4NC5=C(C(=O)C4=C3)C=CC=C5Cl)C(=O)C2C=CC1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C[C@H]1CN(C(=O)C2=C(C(=CC=C2)NS(=O)(=O)C)O[C@H]1CN(C)CC3=CC(=C(C=C3)Cl)Cl)[C@H](C)CO', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3CCCCC3)[C@H](C)CO)C)CN(C)CC4=CC(=C(C=C4)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1=CC(=C(C=C1Cl)Cl)NN2C=NC3=NN=CC3=C2N', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('[Cl-].[Cl-].CC1COCC(C)N1C(=O)C[n+]1ccc(cc1)-c1cc[n+](CC(=O)N2C(C)COCC2C)cc1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('Nc1ccc(Oc2ccc(N)c(Cl)c2)cc1Cl', 'Polychlorinated aromatic "
               "compound with 2 chlorine atoms'), "
               "('Clc1ccc(CSC(Cn2ccnc2)c2ccc(Cl)cc2Cl)cc1', 'Polychlorinated "
               "aromatic compound with 3 chlorine atoms'), "
               "('ClC1=C(O)C(O[C@H]2OC[C@H](N(C)C)[C@@H](C2)O)=CC3=C1NC=4C=5N(C=6C(Cl)=CC=CC6C5C7=C(C34)C(=O)N(C)C7=O)[C@@H]8O[C@@H]([C@H](OC)[C@@H]([C@H]8O)O)CO', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(O)C(Cl)=CC(=C1)C=2C(=O)C3=C(C=C(O)C=C3)OC2', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1CCC(CC1)NC(=O)C(C2=CN=CC=C2)N(C3=CC(=CC=C3)Cl)C(=O)CCl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1=CC=C(C=C1)N=C(C2=CC=CC=N2)NN=CC3=C(C=C(C=C3)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('Clc1ccc([C@@H](Cn2ccnc2)OCc2ccc(Sc3ccccc3)cc2)c(Cl)c1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('Cc1cc(C(C#N)c2ccc(Cl)cc2)c(Cl)cc1NC(=O)c1cc(I)cc(I)c1O', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(Cl)C=CC2=C1N(C=3C=NC=CC23)C', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('CCOC(=O)Nc1ccc(SC[C@H]2CO[C@@](Cn3ccnc3)(O2)c2ccc(Cl)cc2Cl)cc1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)C3=CC=NC=C3)O[C@H]1CN(C)CC4=CC(=C(C=C4)Cl)Cl)[C@H](C)CO', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('Clc1ccc(c(Cl)c1)C(=O)n1cnc2ccccc12', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('C[C@H](CN([C@H](C)CO)C(=O)NC1=CC=C(C=C1)F)[C@@H](CN(C)C(=O)C2=CC(=CC(=C2)Cl)Cl)OC', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('Cl.CN(C)C(=O)C(CCN1CCC(O)(CC1)c1ccc(Cl)cc1)(c1ccccc1)c1ccccc1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C[C@H]1CN[C@H](COC2=C(C=C(C=C2)NC(=O)NC3=CC(=C(C=C3)Cl)Cl)C(=O)N(C[C@@H]1OC)C)C', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=C(Cl)C=CC2=C1N(C=3C(=O)NC=CC23)C', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('ClC(Cl)[C@H](O)CC=1OC(=O)C=2C(O)=CC(=CC2C1)OC', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC1=CC=C(C=C1)\\\\C=N\\\\N\\\\C(=N\\\\N=C\\\\C2=CC=C(Cl)C=C2)\\\\N', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('CC1COC2(N1CC(=O)Nc1ccc(Cl)cc21)c1ccccc1Cl', 'Polychlorinated "
               "aromatic compound with 2 chlorine atoms'), "
               "('CC(C)N1CCN(CC1)c1ccc(OC[C@H]2CO[C@@](Cn3cncn3)(O2)c2ccc(Cl)cc2Cl)cc1', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1C[C@H]([C@H](O[C@@H]1CCNC(=O)C2=CC=C(C=C2)F)CO)NC(=O)NC3=CC(=C(C=C3)Cl)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C1CC(=O)N[C@@H](COC(=O)[C@@H](CC=C1)CC(=O)NCC2=CC=C(C=C2)Cl)C3=CC=C(C=C3)Cl', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('Oc1c(Br)cc(Br)cc1-c1cc(Br)cc(Br)c1OP(O)(O)=O', "
               "'Polybrominated biphenyl with 4 bromine atoms'), "
               "('C1C[C@H]([C@H](O[C@H]1CC(=O)NCC2=CC(=C(C=C2)Cl)Cl)CO)NC(=O)C3=CN=CC=C3', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('C[NH2+][C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C([O-])=O)c3O)c(Cl)c2', "
               "'Polychlorinated biphenyl with 2 chlorine atoms'), "
               "('C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NS(=O)(=O)C)O[C@H]1CN(C)CC3=CC(=C(C=C3)Cl)Cl)[C@H](C)CO', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms'), "
               "('ClC(Cl)C(O)CC=1OC(=O)C=2C(O[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@H]3O)O)CO)=CC(=CC2C1)OC', "
               "'Polychlorinated aromatic compound with 2 chlorine atoms')]\n"
               'False negatives: []',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 36,
    'num_true_negatives': 183830,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.14285714285714285,
    'recall': 1.0,
    'f1': 0.25,
    'accuracy': 0.9998042116254786}