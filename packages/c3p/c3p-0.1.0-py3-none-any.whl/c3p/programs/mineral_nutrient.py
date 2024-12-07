"""
Classifies: CHEBI:167164 mineral nutrient
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_mineral_nutrient(smiles: str):
    """
    Determines if a molecule is a mineral nutrient based on presence of essential minerals
    and appropriate chemical form.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a mineral nutrient, False otherwise
        str: Reason for classification
    """
    # List of essential mineral elements and their symbols
    essential_minerals = {
        'Ca': 'Calcium',
        'Mg': 'Magnesium', 
        'K': 'Potassium',
        'Na': 'Sodium',
        'Fe': 'Iron',
        'Zn': 'Zinc',
        'Cu': 'Copper',
        'Mn': 'Manganese',
        'I': 'Iodine',
        'Se': 'Selenium',
        'Mo': 'Molybdenum',
        'Cr': 'Chromium',
        'Co': 'Cobalt',
        'F': 'Fluoride',
        'P': 'Phosphorus',
        'Cl': 'Chloride',
        'Sn': 'Tin',
        'Cs': 'Caesium'
    }

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get all atoms in molecule
    atoms = mol.GetAtoms()
    mineral_atoms = []
    
    # Find mineral elements present and check their forms
    minerals_present = set()
    has_ionic = False
    has_complex = False
    
    for atom in atoms:
        symbol = atom.GetSymbol()
        if symbol in essential_minerals:
            mineral_atoms.append(atom)
            minerals_present.add(essential_minerals[symbol])
            
            # Check ionic form
            if atom.GetFormalCharge() != 0:
                has_ionic = True
                
            # Check coordination
            if len(atom.GetNeighbors()) >= 2:
                has_complex = True

            # Special cases for common mineral forms
            if symbol in ['F', 'Cl', 'I'] and atom.GetFormalCharge() == -1:
                has_ionic = True
            if symbol in ['Na', 'K', 'Cs', 'Mg', 'Ca'] and atom.GetFormalCharge() > 0:
                has_ionic = True

    if not minerals_present:
        return False, "No essential mineral elements found"

    # For tin fluoride and similar simple compounds
    if len(mineral_atoms) >= 2 and all(atom.GetSymbol() in essential_minerals for atom in mineral_atoms):
        return True, f"Contains essential minerals: {', '.join(sorted(minerals_present))}"

    # For ionic compounds and complexes
    if has_ionic or has_complex:
        return True, f"Contains essential minerals: {', '.join(sorted(minerals_present))}"
        
    return False, "Not in an appropriate mineral form (not ionic or complexed)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:167164',
                          'name': 'mineral nutrient',
                          'definition': 'A mineral that is an inorganic '
                                        'nutrient which must be ingested and '
                                        'absorbed in adequate amounts to '
                                        'satisfy a wide range of essential '
                                        'metabolic and/or structural functions '
                                        'in the human body.',
                          'parents': ['CHEBI:46662']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.056074766355140186 is too low.\n'
               'True positives: '
               "[('[Mg++].CCCCCCCCCCCCCCCCCC([O-])=O.CCCCCCCCCCCCCCCCCC([O-])=O', "
               "'Contains essential minerals: Magnesium'), "
               "('[Pd-2](Cl)(Cl)(Cl)(Cl)(Cl)Cl.[K+].[K+]', 'Contains essential "
               "minerals: Potassium, Chloride'), ('[Cs+].[O-][N+]([O-])=O', "
               "'Contains essential minerals: Caesium')]\n"
               'False positives: '
               "[('COC1=CC=C(C=C1)S(=O)(=O)N[C@H]2CC[C@@H](O[C@H]2CO)CC(=O)NCC3=CC=CC=C3F', "
               "'Contains essential minerals: Fluoride'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Contains essential minerals: Phosphorus'), "
               "('[Cl-].O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C=C3C(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)=CC(O)=CC3=[O+]C2C5=CC(O)=C(O)C=C5)CO[C@@H]6O[C@H]([C@H](O)[C@@H](O)[C@H]6O)C', "
               "'Contains essential minerals: Chloride'), "
               "('C[C@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)CN3C=NN=N3)O[C@H]1CN(C)CC4=CC=C(C=C4)C(F)(F)F)[C@@H](C)CO', "
               "'Contains essential minerals: Fluoride'), "
               "('CS(=O)(=O)C1=CC=C(C=C1)CN2C3=C(CCCC3CC(=O)O)C4=CC(=CC(=C42)F)F', "
               "'Contains essential minerals: Fluoride'), "
               "('CC=CC1=CC=C2[C@H]3[C@@H](CN2C1=O)[C@@H]([C@H](N3CCC(F)(F)F)C(=O)N(C)C)CO', "
               "'Contains essential minerals: Fluoride'), "
               "('CN1[C@H]([C@@H]2CCN([C@@H]2C3=C1C=CC(=C3)Br)S(=O)(=O)C4=CC=CC(=C4)F)CO', "
               "'Contains essential minerals: Fluoride'), "
               "('O1C(O)[C@H](OC(CCCCCCCCCCCCCCC)=O)[C@H](O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)[O-])(=O)[O-]', "
               "'Contains essential minerals: Phosphorus'), "
               "('C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)C3CC3)O[C@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)F)[C@@H](C)CO', "
               "'Contains essential minerals: Fluoride'), "
               "('O[C@H]1[C@@H](O)C(O[C@@H]1COP([O-])([O-])=O)OP([O-])([O-])=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('OC[C@@H]1O[C@H](OP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@H]1O', "
               "'Contains essential minerals: Phosphorus'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains essential minerals: Phosphorus'), "
               "('C(C(COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)O/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Contains essential minerals: Phosphorus'), "
               "('OC(=O)C(F)(F)F.[H][C@]12C[C@H](O)CC[C@@]11CCN2Cc2cc(O)c(OC)cc12', "
               "'Contains essential minerals: Fluoride'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('Cl.CNCC[C@H](Oc1ccc(cc1)C(F)(F)F)c1ccccc1', 'Contains "
               "essential minerals: Fluoride, Chloride'), "
               "('C=1(C=CC(=CC1)[N+]([O-])=O)COP(CCCCCC(O)=O)(=O)O', 'Contains "
               "essential minerals: Phosphorus'), "
               "('C[C@H](CCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'Contains essential minerals: Phosphorus'), "
               "('C[C@@H](CN([C@@H](C)CO)S(=O)(=O)C1=CC(=CC=C1)Cl)[C@@H](CN(C)S(=O)(=O)C2=CC=C(C=C2)Cl)OC', "
               "'Contains essential minerals: Chloride'), "
               "('C[C@H](CCCCCCCCC/C=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'Contains essential minerals: Phosphorus'), "
               "('OP(O)(=S)OP(O)(O)=S', 'Contains essential minerals: "
               "Phosphorus'), "
               "('C(NC(CCNC(=O)[C@@H](C(COP(OC[C@@H](C(*)=O)N*)(=O)[O-])(C)C)O)=O)CSC(=O)C[C@@H](C/C=C\\\\CCCCCCCCCCCCCC/C=C\\\\CCCCCCCCCCCCCCCCCC)O', "
               "'Contains essential minerals: Phosphorus'), "
               "('[C@](COC(CCCCCCCCCCCCC)=O)(OC(=O)CCCCCCCCCCCCC)([H])COP(OCCC[S+](C)C)([O-])=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('C[C@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)C(=O)CCC(F)(F)F', "
               "'Contains essential minerals: Fluoride'), "
               "('C1(=CC=C2C(=C1)C(=C3C(=N2)C=4N(C3)C(C5=C(C4)[C@](C(OC5)=O)(CC)O)=O)CC)OC(=O)N6CCC(CC6)N7CCCCC7.Cl.O.O.O', "
               "'Contains essential minerals: Chloride'), "
               "('CC1=C(CCC([O-])=O)C2=[N+]3C1=Cc1c(C)c(C=C)c4C=C5C(C)=C(C=C)C6=[N+]5[Fe-]3(n14)n1c(=C6)c(C)c(CCC([O-])=O)c1=C2', "
               "'Contains essential minerals: Iron'), "
               "('C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)NC(=O)NC3=CC=CC4=CC=CC=C43)O[C@H]1CN(C)S(=O)(=O)C5=CC=CC=C5F)[C@@H](C)CO', "
               "'Contains essential minerals: Fluoride'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(-*)=O)[C@@H](OC(=O)C[NH3+])[C@H]1O', "
               "'Contains essential minerals: Phosphorus'), "
               "('C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C3=CC=C(C=C3)F)O[C@@H]1CN(C)CC4=CC=CC=C4C(=O)O)[C@@H](C)CO', "
               "'Contains essential minerals: Fluoride'), "
               "('[Na+].C[C@@H]1CCC=C(C)[C@@]1(C)CC\\\\C(C)=C\\\\CCC(CCCc1ccoc1)COS([O-])(=O)=O', "
               "'Contains essential minerals: Sodium'), "
               "('C1(C(C(CCC1)=O)C(=O)C2=C(C(=C(C=C2)S(C)(=O)=O)COCC(F)(F)F)Cl)=O', "
               "'Contains essential minerals: Fluoride, Chloride'), "
               "('C1C[C@H]([C@@H](O[C@H]1CCNC(=O)C2=CC=CC=C2F)CO)NC(=O)NC3=CC=C(C=C3)C(F)(F)F', "
               "'Contains essential minerals: Fluoride'), "
               "('Cl[C@@H]1C=C2C(=O)C3=C(O)C4=C(O)C=C3C([C@]2(CC=C(CC=C(C4)CO)C)OC1(C)C)=O', "
               "'Contains essential minerals: Chloride'), "
               "('C1(=O)NC(=NC2=C1[N+](=CN2[C@@H]3O[C@H](COP(OP(OP(OC[C@H]4O[C@H]([C@@H]([C@@H]4O)O)N5C=6N=C(NC(=O)C6N=C5)N)(=O)[O-])(=O)[O-])(=O)[O-])[C@@H](O)[C@H]3O)C)N', "
               "'Contains essential minerals: Phosphorus'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('COCCCNS(=O)(=O)C1=C(C(=C(C=C1)OC)Cl)Cl', 'Contains essential "
               "minerals: Chloride'), "
               "('P(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H](NC(=N)NCCC[C@H](NC([*])=O)C(=O)N[*])[C@H](O)[C@@H]2O)[C@@H](O)[C@H]1O', "
               "'Contains essential minerals: Phosphorus'), "
               "('CCCNC(=O)N(C)C[C@H]1[C@@H](CN(S(=O)(=O)C2=C(O1)C=C(C=C2)C3=CC=CC=C3F)[C@@H](C)CO)C', "
               "'Contains essential minerals: Fluoride'), "
               "('[Cl-].CCOC(=O)C1(CC[NH+](CC1)CCC(C#N)(c1ccccc1)c1ccccc1)c1ccccc1', "
               "'Contains essential minerals: Chloride'), "
               "('CCCNC(=O)C[C@H]1C[C@@H]2[C@H]([C@H](O1)CO)OC3=C2C=C(C=C3)NS(=O)(=O)C4=CC=C(C=C4)F', "
               "'Contains essential minerals: Fluoride'), "
               "('C[C@@H](N)P(=O)(C[C@H](C)C(O)=O)OP(O)(O)=O', 'Contains "
               "essential minerals: Phosphorus'), "
               "('C(NC(CCNC(=O)[C@@H](C(COP(O)(=O)O)(C)C)O)=O)CSC(=O)CCCCC', "
               "'Contains essential minerals: Phosphorus'), "
               "('OC(CO\\\\C([*])=C(\\\\[*])[*])COP(O)(O)=O', 'Contains "
               "essential minerals: Phosphorus'), "
               "('C(CCCCCCCCCC)CCCCC(OP(O)(=O)O)=O', 'Contains essential "
               "minerals: Phosphorus'), "
               "('C[C@@H]1O[C@H](OP([O-])([O-])=O)[C@@H](O)[C@H](O)[C@@H]1O', "
               "'Contains essential minerals: Phosphorus'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)C(C(C(C(C(C(C(C(C(C(C(C(C([2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])COC(=O)C(C(C(C(C(C(C(C(C(C(C(C(C([2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([O-])=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('C(CCCCCCCCCC)CC\\\\C=C\\\\[C@@H](O)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCC)COP(=O)([O-])OCC[N+](C)(C)C', "
               "'Contains essential minerals: Phosphorus'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('[Na+].CCCCCC([O-])=O', 'Contains essential minerals: "
               "Sodium'), "
               "('ClC1=C(OC)C(OC)=C2N(C)[C@H]3[C@](C2=C1)(O)[C@@H](O)[C@@]4(SC)C(=O)N(C)[C@@](C(N34)=O)(SC)C', "
               "'Contains essential minerals: Chloride'), "
               "('C1C[C@H]([C@H](O[C@H]1CC(=O)NCCC2=CC=NC=C2)CO)NS(=O)(=O)C3=CC=C(C=C3)F', "
               "'Contains essential minerals: Fluoride'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCC)([O-])=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('O=P([O-])(OCC)NC(C)C', 'Contains essential minerals: "
               "Phosphorus'), ('ClC1C([N+]#[C-])=CC(C1O)(O)C(O)C', 'Contains "
               "essential minerals: Chloride'), "
               "('[NH3+][C@@H](CCOP([O-])([O-])=O)C([O-])=O', 'Contains "
               "essential minerals: Phosphorus'), "
               "('CC(C)CCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@@H]([NH3+])COP([O-])(=O)OCC[N+](C)(C)C', "
               "'Contains essential minerals: Phosphorus'), "
               "('Cl.CNCC[C@@H](Oc1ccc(cc1)C(F)(F)F)c1ccccc1', 'Contains "
               "essential minerals: Fluoride, Chloride'), "
               "('C1[C@H](O[C@H]([C@@H]2[C@H]1C3=C(O2)C=CC(=C3)NC(=O)NC4=CC=C(C=C4)C(F)(F)F)CO)CC(=O)NCC5=CN=CC=C5', "
               "'Contains essential minerals: Fluoride'), "
               "('ClC1=C(O)C=CC(=C1)C[C@H]2C(=O)O\\\\C(\\\\[C@@]2(O)C(C)C)=C/C3=CC=C(OC)C=C3', "
               "'Contains essential minerals: Chloride'), "
               "('C=12N([C@@H]3O[C@H](COP(OP([O-])([O-])=O)([O-])=O)[C@H]([C@H]3O)O)C=NC1C(NC(=N2)NC(C([H])=O)O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('CCNC(=O)[C@@H]1[C@H]([C@@H]2CN3C(=CC=C(C3=O)C4=CC=CC=C4)[C@H]1N2CCC(F)(F)F)CO', "
               "'Contains essential minerals: Fluoride'), "
               "('Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)O[C@H]2O[C@@H](CO)[C@@H](O)[C@@H](O)[C@@H]2O)[C@@H](O)[C@H]1O', "
               "'Contains essential minerals: Phosphorus'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COP([O-])(=O)OCC[N+](C)(C)C)NC(=O)CCCCCCCCC\\\\C=C/CCCCCC', "
               "'Contains essential minerals: Phosphorus'), "
               "('P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('OC[C@H]1O[C@H]([C@H](OP([O-])([O-])=O)[C@@H]1O)n1ccc(=O)[nH]c1=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)NC(=O)NC3=C(ON=C3C)C)O[C@H]1CN(C)C(=O)NC4=CC=C(C=C4)C(F)(F)F)[C@H](C)CO', "
               "'Contains essential minerals: Fluoride'), "
               "('S(C(=O)\\\\C=C\\\\C/C=C\\\\CCCCCCCC)CCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('*C(OC(COP(OP(O)(=O)O)(=O)O)COC(*)=O)=O', 'Contains essential "
               "minerals: Phosphorus'), "
               "('C1C2C3C4C1C5C2C6C3C4C5(N6CCC7=CC(=CC=C7)F)O', 'Contains "
               "essential minerals: Fluoride'), "
               "('CN(C)C1=C(C(=O)OC(=C1)C2=CC=C(C=C2)[N+](=O)[O-])Cl', "
               "'Contains essential minerals: Chloride'), "
               "('CCCCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\\\C=C/CCCCCCCC)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('C1C[C@H]2[C@@H](COC[C@H](CN2S(=O)(=O)C3=CC=CC=C3F)O)O[C@H]1CC(=O)N4CCC(CC4)CC5=CC=CC=C5', "
               "'Contains essential minerals: Fluoride'), "
               "('F[C@@]12[C@]([C@]3([C@@](C[C@@H]1O)(C)[C@](CC3)(C(COC(C)=O)=O)OC(C)=O)[H])(C[C@H](C=4[C@]2(C)C=C(C(C4)=O)Br)F)[H]', "
               "'Contains essential minerals: Fluoride'), "
               "('CC(C)(COP(O)([O-])=O)[C@@H](O)C(=O)NCCC([O-])=O', 'Contains "
               "essential minerals: Phosphorus'), "
               "('CN[C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O[C@H]5C[C@](C)(N)[C@@H](O)[C@H](C)O5)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C(O)=O)c3O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@H]1C[C@](C)(NCc3ccc(cc3)-c3ccc(Cl)cc3)[C@@H](O)[C@H](C)O1)c(Cl)c2', "
               "'Contains essential minerals: Chloride'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCC)=O)(OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Contains essential minerals: Phosphorus'), "
               "('P(OC[C@H](OC(=O)CCC(O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('CCN(CC)S(=O)(=O)C1=CC(=C(C=C1)N2CCCC2)NS(=O)(=O)C3=CC=C(C=C3)F', "
               "'Contains essential minerals: Fluoride'), "
               "('C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1C)[C@H]([C@@H]9CCC([O-])=O)C)[Mg-2]753)CC(C8C6*)=O)C(=C4C)C*)C(=C2C)C(O)C', "
               "'Contains essential minerals: Magnesium'), "
               "('P(OCC(O)COP(O)(O)=O)(OCC(O)CO)(O)=O', 'Contains essential "
               "minerals: Phosphorus'), "
               "('CC1C=NC(=N1)S(=O)(=O)N2CC[C@H]3[C@@H]2C4=C(C=CC(=C4)C5=CC=CC=C5F)N([C@@H]3CO)C', "
               "'Contains essential minerals: Fluoride'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCC(O)/C=C/C=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('C1=CC(C2=CC=C(N=NC3=CC(=C4C(=C3N)C=CC=C4)S([O-])(=O)=O)C=C2)=CC=C1N=NC5=CC(=C6C(=C5N)C=CC=C6)S([O-])(=O)=O.[Na+].[Na+]', "
               "'Contains essential minerals: Sodium'), "
               "('O=P(SC(C)CC)(SC(C)CC)[O-]', 'Contains essential minerals: "
               "Phosphorus'), "
               "('CCCCCCCCCCC[C@@H](O)[C@H](COP([O-])(=O)OCC[N+](C)(C)C)NC([*])=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('[H][C@@]1(O[C@@H](OP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO', "
               "'Contains essential minerals: Phosphorus'), "
               "('Cl[C@H]1[C@](C=C)([C@]2([N+]#[C-])[C@]3(O)C=4C=5C(=CC=CC5C([C@H]3C1)(C)C)NC4C([C@H]([C@@H]2O)O)(C)C)C', "
               "'Contains essential minerals: Chloride'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H](OP([O-])([O-])=O)[C@H](O)[C@@H]2O)[C@@H](O)[C@H]1O', "
               "'Contains essential minerals: Phosphorus'), "
               "('N[C@@H](COP(O)(=O)OC[C@H](O)CO)C(O)=O', 'Contains essential "
               "minerals: Phosphorus'), "
               "('CC1(C)[C@H](C=C(Cl)Cl)[C@@H]1C(=O)O[C@H](C#N)c1cccc(Oc2ccccc2)c1', "
               "'Contains essential minerals: Chloride'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCNC)(O)=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC)([O-])=O', "
               "'Contains essential minerals: Phosphorus'), "
               "('ClC=1C(=O)N(C)[C@@]2(C1Cl)OC=3C(=C(O)C=CC3C2=O)CCC[C@H](CC)C', "
               "'Contains essential minerals: Chloride'), "
               "('CCCCCCCCCCCC(=O)OC[C@H](COP([O-])([O-])=O)OC(=O)CCCCCCCCCCC', "
               "'Contains essential minerals: Phosphorus'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Contains essential minerals: Phosphorus'), "
               "('COC1=CC2=C(C=C1)C3=C(N2)[C@@H](N(CC34CN(C4)C(=O)NC5=CC(=CC=C5)F)CC6=CC=CC=C6)CO', "
               "'Contains essential minerals: Fluoride'), "
               "('Oc1ccc(Oc2c(I)cc(CC(=O)C([O-])=O)cc2I)cc1I', 'Contains "
               "essential minerals: Iodine'), "
               "('C1CCC(CC1)CNC(=O)C[C@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3S(=O)(=O)C4=CC=C(C=C4)F)O', "
               "'Contains essential minerals: Fluoride'), "
               "('C\\\\C=C\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Contains essential minerals: Phosphorus')]\n"
               "False negatives: [('F[Sn]F', 'Not in an appropriate mineral "
               "form (not ionic or complexed)')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 629,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.8635743519781719}