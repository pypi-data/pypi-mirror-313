"""
Classifies: CHEBI:17517 phosphatidylglycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_phosphatidylglycerol(smiles: str):
    """
    Determines if a molecule is a phosphatidylglycerol.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phosphatidylglycerol, False otherwise
        str: Reason for classification
    """
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"

        # Check for presence of phosphorus
        atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
        if 'P' not in atoms:
            return False, "No phosphorus atom found"
            
        # Check for presence of phosphate group
        phosphate_pattern = Chem.MolFromSmarts('[P](=O)([O,OH])[O,OH]')
        if not mol.HasSubstructMatch(phosphate_pattern):
            return False, "No phosphate group found"
            
        # Check for glycerol backbone with phosphate
        glycerol_phosphate = Chem.MolFromSmarts('[#6]-[#6]-[#6]-O-P(=O)([O,OH])-O-[#6]-[#6]-[#6]')
        if not mol.HasSubstructMatch(glycerol_phosphate):
            return False, "No glycerol-phosphate backbone found"

        # Check for ester linkages
        ester_pattern = Chem.MolFromSmarts('C(=O)-O')
        ester_count = len(mol.GetSubstructMatches(ester_pattern))
        if ester_count < 1:
            return False, "Missing ester linkages"

        # Look for terminal glycerol moiety
        terminal_glycerol = Chem.MolFromSmarts('O-C-C(O)-CO')
        if not mol.HasSubstructMatch(terminal_glycerol):
            # Try alternative pattern for masked terminal groups
            alt_terminal = Chem.MolFromSmarts('O-C-C-C-O')
            if not mol.HasSubstructMatch(alt_terminal):
                return False, "Missing terminal glycerol group"

        # Special check for generic/masked structures
        if '*' in smiles:
            return True, "Valid phosphatidylglycerol structure with masked groups"

        # Check for fatty acid chains or their masked representations
        carbon_chain = Chem.MolFromSmarts('CCCC')  # Shorter chain requirement
        if not mol.HasSubstructMatch(carbon_chain) and '*' not in smiles:
            return False, "No acyl chains found"

        return True, "Valid phosphatidylglycerol structure identified"

    except Exception as e:
        return None, f"Error analyzing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17517',
                          'name': 'phosphatidylglycerol',
                          'definition': 'A glycerophosphoglycerol that is '
                                        'glycerol in which the hydrogen of one '
                                        'of the primary hydroxy groups has '
                                        'been replaced by a phosphatidyl '
                                        'group.',
                          'parents': ['CHEBI:24360']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.4126984126984127 is too low.\n'
               'True positives: '
               "[('C([C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC(C)C)COC(=O)CCCCCCCC(O)/C=C/C=C/C/C=C/CC)(OC[C@@H](O)COP(O)(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OC[C@@H](O)COP(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@@H](O)COP(O)(O)=O)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@@H](O)CO)OC(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)OCC(COP(O)(=O)OCC(O)CO)OC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@@H](O)CO)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCC)(OC[C@@H](O)COP(OC[C@H](OC(=O)CCCCCCC)COC(=O)CCCCCCC)(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OC[C@H](O)COP(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C(OP(=O)(OCC(CO)O)O)[C@@H](COC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)OC(C/C=C/CCCCCCCCCCCC)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCC(=O)OCC(COP(O)(=O)OCC(O)CO)OC(=O)CCCCCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCC(O)COP(O)(=O)OC[C@H](O)COC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCC(=O)/C=C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCC(CC)C)(OC[C@@H](O)COP(O)(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@@H](O)CO)OC(=O)CCCCCCCCCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCC(O)/C=C/C=O)COC(=O)CCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC(C)C)COC(=O)CCCC(=O)/C=C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('O(P(OCC(COP(OC[C@@H](COC(CCCCCCCC=CCCCCCC)=O)OC(CCCCCCCC=CCCCCCC)=O)(O)=O)O)(O)=O)C[C@@H](COC(CCCCCCCC=CCCCCCC)=O)OC(CCCCCCCC=CCCCCCC)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\\\C=C/CCCCCCCC)COP(O)(=O)OC[C@@H](O)CO', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC(C)C)COC(=O)CCCCCCCCC(CC)C)(OC[C@@H](O)COP(O)(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified')]\n"
               'False positives: '
               "[('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCC)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C(CCCCCCC/C=C\\\\CCCCCCCC)(=O)O[C@@H](COP(=O)(OCCN)O)CO/C=C\\\\CCCCCCCCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCCCCCCCCCCCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCC)COC(=O)CCCCCCCCCCCCCCCC)([O-])=O.[NH4+]', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(=O)[H])COCCCCCCCCCCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('O(C[C@@H](COP([O-])(=O)OC[C@H](COC(CCCCCCCCCCCCC)=O)O)O)C(CCCCCCCCCCCCC)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C[C@H]1[C@@H](O)CC(O[C@@H]1/C=C/[C@@H](O)CCCCC)O)COC(=O)CCCCCCCCCCCCCCCC(C)C)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@](COC(=O)CCCCCCCCCCCCCCCCCCCC)(OC(=O)CCCCCCCCCCCCCCC)([H])COP(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCC\\\\C=C\\\\C[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@H]1([C@H]([C@@H]([C@H]([C@@H]([C@@H]1O)OP(OC[C@H](COC(CCCCCCC)=O)OC(CCCCCCC)=O)(=O)O)O)OP(=O)(O)O)OP(O)(=O)O)O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)COC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@](COC(=O)CCCCCCC/C=C\\\\CCCC)(OC(=O)CCCCCCCCCCCCC/C=C\\\\CCCCCCCC)([H])COP(OCC[N+](C)(C)C)([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](O)COCC(OC)CCCCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@@H](COC(=O)CCCCCCCCCCCCCCC)(COP(OCC[N+](C)(C)C)(=O)[O-])O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)O*)OP(OC[C@H](CO*)OC(*)=O)(=O)[O-])O[C@@H]2[C@H]([NH3+])[C@@H](O)[C@@H]([C@H](O2)CO)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO*)O)O)O[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)COP([O-])(=O)OCCNC([C@@H](N*)CO)=O)O)O)O*)O*)O*)O*', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(=O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCC[C@@H](CCCCCCCC)C)(OCCN)O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OC[C@@H](O)CO', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCCCCCC/C=C\\\\CCCCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)OC(=O)*)OP(OC[C@H](CO*)OC(=O)*)(=O)[O-])O[C@@H]2[C@H]([NH3+])[C@@H](O)[C@@H]([C@H](O2)CO)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)COP([O-])(=O)OCC[NH3+])O)O)O[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)COP([O-])(=O)OCC[NH3+])O)O)O)O)O)OP([O-])(=O)OCC[NH3+]', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[S+](CCOP(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)([O-])=O)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C(C(COC(CCCCCCCCC/C=C\\\\CCCCCCCC)=O)O/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\CCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@](COC(=O)CCCCCCC/C=C\\\\CCCC)(O)([H])COP(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OCCN)OC(=O)CCCCCCCCCCCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCC)([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCC)([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COCCCCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC(OC(=O)CCCCCCCCC/C=C\\\\CCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[H]C(=O)CCCC(=O)O[C@H](COC(=O)CCCCC)COP(O)(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCCCCCC/C=C\\\\CCCCC)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC)COP([O-])(=O)OCC(O)COP([O-])(=O)OC[C@@H](COC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC)OC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@](COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)([H])COP(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(C)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCNC)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCCCC(=O)O[C@H](CO)COP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('O([C@H](COC(=O)CCCCCCCCCCCCCCC)COP(OCC[N+](C)(C)C)(=O)[O-])C(=O)CCCCCCCCO', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@](COC(=O)CCCCCCC/C=C\\\\CCCCCC)(O)([H])COP(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OCC(O)COP([O-])(=O)OC[C@H](O)COC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC(OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\\\CCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@@H](OC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(COC(=O)CCCCCCCCCCCCCCC)COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@@H](CO/C=C\\\\CCCCCCCCCCCCCCCC)OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(=O)(OCCN)O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCC\\\\C=C\\\\CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCC\\\\C=C\\\\CCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@@H](O)CO)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(=O)(O)(OCCN)OC[C@@H](CO)OC(CCC/C=C\\\\C[C@H]1[C@@H]2C[C@H]([C@@H]1/C=C/[C@H](CCCCC)OO)OO2)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('OC1C(O)C(O)C(OP([O-])(=O)OCC(COC=C[*])OC([*])=O)C(O)C1O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCC[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCCCC)([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCC[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[H]/C(/CC)=C(/[H])\\\\C/C(/[H])=C(\\\\[H])/C/C(/[H])=C(\\\\[H])/C/C(/[H])=C(\\\\[H])/C/C(/[H])=C(\\\\[H])/CCCCCC(=O)OC[C@]([H])(COP(O)(=O)OCCN)O/C(/[H])=C(\\\\[H])/CCCCCC/C(/[H])=C(\\\\[H])/CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@](COC(=O)CCCCCCCCCCCCCCC)(O)([H])COP(OCCN*)(=O)[O-]', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCCCCCCCC/C=C\\\\CCCCCC)=O)[H])(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCC=1OC(=C(C1C)C)CCCCC)COC(=O)CCCCC(=O)C[C@@H]2[C@H]([C@H](O)C[C@@H]2O)/C=C/[C@@H](O)CCCCC)(OCC[N+](C)(C)C)([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCCCC)COC(=O)CCCCCCCCCCCCCC)([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('O(P(=O)(OCC[N+](C)(C)C)[O-])C[C@H](O)COC(CCCCCCCC(O)=O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('O(P(OC[C@H]1O[C@@H](N2C=3N=CN=C(N)C3N=C2)[C@@H]([C@@H]1O)O)(=O)O)C(CCCCCCCCCCCCCCCCCCC4=CC=C(C=C4)O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCCCCCC(=O)NCCOP([O-])(=O)OC[C@H](O)COC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC(OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OCCNC)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@@H](CO)OC(CCCCCCC/C=C\\\\CC(CCCCCC)O)=O)(=O)(OCC[N+](C)(C)C)[O-]', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[H][C@@]1(O[C@H](O[C@@H]2[C@H](O)[C@@H](O[C@@H]3[C@@H](C[C@@](O)(O[C@]3([H])[C@H](O)CO)C(O)=O)O[C@@]3(C[C@@H](O)[C@@H](O)[C@]([H])(O3)[C@H](O)CO)C(O)=O)O[C@]([H])([C@@H](O)CO)[C@H]2O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2NC(C)=O)[C@@H](OP(O)(=O)OCCN)[C@@H]1O)[C@@H](O)CO', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[H][C@@](COC(=O)CCCCCCCCCCCCCCC)(COP(O)(=O)OCCN)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('N(CCOP(OC[C@@H](COC(CCCCCCCCCCCCCCCC)=O)OC(CCCCCCCCCCCCCCCC)=O)(=O)O)C(=O)CCCCCCC/C=C\\\\CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)NCCOP([O-])(=O)OC[C@H](O)COC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[H][C@](COP(OC[C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(=O)O)(C(O)=O)N', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP(O)(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('[C@](COC(=O)CCCCCCC/C=C\\\\CCCC)(O/C=C\\\\CCCCCCCCCCCCCC)([H])COP(OCC[N+](C)(C)C)([O-])=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('C(C(COC(CCCCCCCCCCCCC)=O)O/C=C\\\\CCCCCCCCCCCCCCCC)OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('O=P([O-])(O[C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O)O)O)O)O)OC[C@@H](COC(CCCCCCC/C=C\\\\CCCCCCCC)=O)OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCCCC)COC(=O)CCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OCCN)OC(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC', "
               "'Valid phosphatidylglycerol structure identified'), "
               "('CCCCCC\\\\C=C/CCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CC', "
               "'Valid phosphatidylglycerol structure identified')]\n"
               "False negatives: [('C(=O)(OCC(COP(=O)(OCC(CO)O)O)OC(*)=O)*', "
               "'No long carbon chains found'), "
               "('C(=O)(OC[C@H](COP(=O)(OCC(CO)O)O)OC(*)=O)*', 'No long carbon "
               "chains found'), ('C(=O)(OCC(COP(=O)(OCC(CO)O)O)OC(*)=O)*', 'No "
               "long carbon chains found'), "
               "('O(P(=O)(OCC(COP(=O)(O)O)O)O)CC(OC(*)=O)COC(*)=O', 'No long "
               "carbon chains found'), "
               "('C(=O)(OCC(COP(=O)(OCC(CO)O)O)OC(*)=O)*', 'No long carbon "
               "chains found'), "
               "('*C(O[C@@H](COP(OCC(COP(OC[C@H](OC(*)=O)COC(*)=O)(O)=O)O)(O)=O)COC(*)=O)=O', "
               "'No long carbon chains found'), "
               "('*C(O[C@@H](COP(OCC(COP(OC[C@H](OC(*)=O)COC(*)=O)(O)=O)O)(O)=O)COC(*)=O)=O', "
               "'No long carbon chains found'), "
               "('OC(COP(O)(=O)OC[C@@H](COC([*])=O)OC([*])=O)COP(O)(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'No long carbon chains found'), "
               "('C(=O)(OCC(COP(=O)(OCC(CO)O)O)OC(*)=O)*', 'No long carbon "
               "chains found'), ('C(=O)(OCC(COP(=O)(OCC(CO)O)O)OC(*)=O)*', 'No "
               "long carbon chains found'), "
               "('C(=O)(OCC(COP(=O)(OCC(CO)O)O)OC(*)=O)*', 'No long carbon "
               "chains found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 50,
    'num_false_positives': 100,
    'num_true_negatives': 8981,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.3333333333333333,
    'recall': 1.0,
    'f1': 0.5,
    'accuracy': 0.989048297010185}