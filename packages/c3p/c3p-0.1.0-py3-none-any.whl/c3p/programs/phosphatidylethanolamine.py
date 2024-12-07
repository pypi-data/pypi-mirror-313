"""
Classifies: CHEBI:16038 phosphatidylethanolamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phosphatidylethanolamine(smiles: str):
    """
    Determines if a molecule is a phosphatidylethanolamine (PE).
    PE has a glycerol backbone with two fatty acid chains and a phosphoethanolamine head group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a PE, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for phosphate group connected to ethanolamine
    # Include both neutral and charged forms
    phosphoethanolamine_patterns = [
        'P(=O)(O)(O)OCCN',  # Neutral
        'P(=O)([O-])(O)OCCN',  # Mono-anion
        'P(O)(O)(OCCN)=O',  # Alternative neutral
        'P(O)(O)(OCCNC)=O',  # N-methylated
        'P(O)(O)(OCCN(C)C)=O',  # N,N-dimethylated
    ]
    
    pe_head_found = False
    for pattern in phosphoethanolamine_patterns:
        pe_pattern = Chem.MolFromSmarts(pattern)
        if mol.HasSubstructMatch(pe_pattern):
            pe_head_found = True
            break
            
    if not pe_head_found:
        return False, "No phosphoethanolamine group found"

    # Check for glycerol backbone with ester linkages
    glycerol_patterns = [
        'CC(COC(=O)*)COC(=O)*',  # Generic pattern
        '[C@H](COC(=O)*)(**)OC(=O)*',  # R stereochem
        '[C@@H](COC(=O)*)(**)OC(=O)*',  # S stereochem
        'C(COC(=O)*)(OC(=O)*)*',  # Simplified pattern
    ]
    
    glycerol_found = False
    for pattern in glycerol_patterns:
        glycerol_pattern = Chem.MolFromSmarts(pattern)
        if mol.HasSubstructMatch(glycerol_pattern):
            glycerol_found = True
            break
            
    if not glycerol_found:
        return False, "No glycerol backbone with ester linkages found"

    # Check for fatty acid chains
    fatty_acid_patterns = [
        'C(=O)CCCCC',  # Saturated chain
        'C(=O)CC=CC',  # Unsaturated chain
        'OC(=O)*',     # Wildcard chain
        'C(=O)CCC'     # Shorter chain
    ]
    
    fatty_acid_count = 0
    for pattern in fatty_acid_patterns:
        fa_pattern = Chem.MolFromSmarts(pattern)
        matches = mol.GetSubstructMatches(fa_pattern)
        fatty_acid_count += len(matches)
        
    if fatty_acid_count < 2:
        return False, "Missing required fatty acid chains"

    return True, "Valid phosphatidylethanolamine structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16038',
                          'name': 'phosphatidylethanolamine',
                          'definition': 'A class of glycerophospholipids in '
                                        'which a phosphatidyl group is '
                                        'esterified to the hydroxy group of '
                                        'ethanolamine.',
                          'parents': ['CHEBI:36314']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.15384615384615383 is too low.\n'
               "True positives: [('[C@@H](COC(=O)*)(COP(OCCN)(=O)O)OC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@](COC(=O)*)(OC(=O)*)([H])COP(OCCN)(=O)O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), ('O(C(*)=O)[C@H](COC(=O)*)COP(=O)(OCCN)O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('N(C(=O)CCCCCCC/C=C\\\\CCCCCCCC)CCOP(OC[C@@H](COC(*)=O)OC(=O)*)(=O)O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), ('O(P(=O)(OCCN)O)CC(OC(*)=O)COC(*)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('O(P(=O)(OCCN(C)C)O)C[C@H](OC(*)=O)COC(*)=O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), ('[C@](COC(=O)*)(OC(=O)*)([H])COP(OCCN)(=O)O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), ('O(P(=O)(OCCN)O)CC(OC(*)=O)COC(*)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), ('O(P(=O)(OCCN)O)CC(OC(*)=O)COC(*)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), ('O(P(=O)(OCCN)O)CC(OC(*)=O)COC(*)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@](COC(=O)*)(OC(=O)*)([H])COP(OCCN)(=O)O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), ('NCCOP(O)(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@](COC(=O)*)(OC(=O)*)([H])COP(OCCN)(=O)O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), ('[C@](COC(=O)*)(OC(=O)*)([H])COP(OCCN)(=O)O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), ('O(P(=O)(OCCN)O)CC(OC(*)=O)COC(*)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@](COC(=O)*)(OC(=O)*)([H])COP(OCCN)(=O)O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), ('O(P(=O)(OCCN)O)CC(OC(*)=O)COC(*)=O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains')]\n"
               'False positives: '
               "[('P([O-])(=O)(OC[C@@H](C(=O)[O-])[NH3+])OC[C@@H](COC(=O)*)OC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[NH3+]CCOP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(*)=O)COC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OCC(OC(*)=O)COC(=O)*OO', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[NH3+]CCOP([O-])(=O)OC[C@H](COC(=O)CC(O)[*])OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C1CCC(=C(\\\\C=C\\\\C(=C\\\\C=C/C(/C)=C/C=N\\\\CCOP(OC[C@H](OC(*)=O)COC(*)=O)(=O)[O-])\\\\C)C1(C)C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CC(\\\\C=C\\\\C1=C(C)CCCC1(C)C)=C/C=C/C(C)=C/C1C=C(C=CN1CCOP(O)(=O)OCC(COC([*])=O)OC([*])=O)\\\\C=C\\\\C=C(C)\\\\C=C\\\\C1=C(C)CCCC1(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('*N[C@H](C(=O)NCC(NCCOP(OC[C@H](OC(*)=O)COC(*)=O)(=O)[O-])=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCC(COC([*])=O)OC([*])=O)C([O-])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OCC(OC(*)=O)COC(=O)*', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('N(C(=O)CCCCCCC/C=C\\\\CCCCCCCC)CCOP(OC[C@@H](COC(*)=O)OC(=O)*)(=O)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@@H](COC(=O)*)(COP(OC[C@@H](C(=O)[O-])[NH3+])(=O)[O-])OC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP(O)(=O)OCC[N+](C)(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[N+](C)(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('O(P(=O)(OCC[NH+](C)C)[O-])CC(OC(*)=O)COC(*)=O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('[NH3+][C@@H](COP(O)(=O)OC[C@H](COC([*])=O)OC([*])=O)C([O-])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(=O)(N[C@H](C(=O)O)COP(OC[C@@H](COC(=O)*)OC(=O)*)(=O)O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@@H](COC([*])=O)COP([O-])(=O)OCC[NH3+]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('P([O-])(=O)(OC[C@@H](C(=O)[O-])NC(C[NH3+])=O)OC[C@@H](COC(=O)*)OC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[N+](C)(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCCCCCCCCCCCC(=O)NCCOP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('O(P(=O)(OCCNC)O)C[C@H](OC(*)=O)COC(*)=O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[N+](C)(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(=O)*)COC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCC[C@H](O)C\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP(O)(=O)OCC[N+](C)(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CC(\\\\C=C\\\\C1=C(C)CCCC1(C)C)=C/C=C/C(C)=C/C=N/CCOP(O)(=O)OCC(COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@H](COC([*])=O)OC([*])=O)C([O-])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCC[C@H](O)C\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[N+](C)(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[N+](C)(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@@H](COC(=O)*)(COP(OCC[N+](C)(C)C)(=O)[O-])OC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('P(OC[C@@H](COC(CCCCC)=O)OC(=O)*)(=O)(OCC[N+](C)(C)C)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[H]C(=NCCOP(O)(=O)OC[C@@H](COC([*])=O)OC([*])=O)\\\\C=C(C)\\\\C=C\\\\C=C(C)\\\\C=C\\\\C1=C(C)CCCC1(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@@H](COC(=O)*)(COP(OC[C@@H](C(=O)O)N)(=O)O)OC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@](COC(=O)*)(OC(=O)*)([H])COP(OCC[N+](C)(C)C)(=O)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('O(P(=O)(OCCNC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)[O-])C[C@H](OC(*)=O)COC(*)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@@H](COC(=O)*)(COP(OCC[NH3+])(=O)[O-])OC(=O)*', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('C([C@H](NC(*)=O)C([O-])=O)OP(=O)([O-])OC[C@H](OC(*)=O)COC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)COC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[NH3+]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCC[C@@H](O)C\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[N+](C)(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP(O)(=O)OCC[N+](C)(C)C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCC\\\\C=C/CCCCCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[NH3+]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)C([O-])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[H][C@@](COC([*])=O)(COP([O-])(=O)OCC[N+](C)(C)C)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCCCCCCCCCCCC(=O)OCC(COP([O-])(=O)OCC[N+](C)(C)C)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[H][C@@](COC([*])=O)(COP([O-])(=O)OCC[NH3+])OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[NH3+]CCOP([O-])(=O)OC[C@H](COC([*])=O)OC([*])=O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), ('[NH3+]CCOP([O-])(=O)OCC(COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[O-]P(=O)(OCCNC([*])=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('P(O)(=O)(OC[C@@H](C(=O)O)N)OC[C@@H](COC(=O)*)OC(=O)*', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@@H](COC(=O)*)(COP(OCC[N+](C)(C)C)(=O)[O-])OC(=O)CCCCCCCCCCCCCCC', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C[NH+](C)CCOP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[NH3+]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[NH3+]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('N(C(CN*)=O)CCOP(OC[C@H](OC(*)=O)COC(*)=O)(=O)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('O(P(=O)(OC[C@@H](C([O-])=O)NC(CNC(=O)[C@@H](N*)*)=O)[O-])C[C@H](OC(*)=O)COC(*)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(=O)NCCOP(O)(=O)OCC(COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@](COC(=O)CCCCCCCCCCCCCCC)(OC(=O)CCCCCCCCCCCCCCC)([H])COP(OCCN*)(=O)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('P(=O)(OC[C@@H](C(=O)[O-])[NH3+])(OC[C@@H](COC(=O)*)OC(=O)*)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('N(C(C[NH3+])=O)CCOP(OC[C@H](OC(*)=O)COC(*)=O)(=O)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCCCCCCCCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[NH3+]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OCC(OC(*)=O)COC(=O)*O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[NH3+])OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('O(P(=O)(OCC[NH3+])[O-])C[C@H](OC(*)=O)COC(=O)CCCCCCCCCCCCCCCCC', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('N[C@@H](Cc1ccc(O)c(c1)N=Nc1ccc(cc1)[As](O)(O)=O)C(=O)NCCOP(O)(=O)OCC(COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C[N+](C)(C)C)OP(OC[C@@H](COC(CCCCCCCCCCCCCCC)=O)OC(*)=O)(=O)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(=O)*)COC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C[N+](C)(C)CCOP(O)(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('[C@](COC(=O)*)(OC(=O)*)([H])COP(OCC[N+](C)(C)C)([O-])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('O(P(=O)(OC[C@@H](C([O-])=O)NC(CN*)=O)[O-])C[C@H](OC(*)=O)COC(*)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('N[C@@H](COP(O)(=O)OC[C@@H](COC([*])=O)OC([*])=O)C(O)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C(COP(=O)(OC[C@@H](C(=O)O)N)O)OC(=O)*)OC(=O)*', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('C[N+](C)(C)CCOP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C[N+](C)(C)CCOP([O-])(=O)OCC(COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C[NH2+]CCOP([O-])(=O)OCC(COC([*])=O)OC([*])=O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('N(\\\\CCOP(OC[C@H](OC(*)=O)COC(*)=O)(=O)[O-])=C/C=C(/C=C/C=C(/C=C/C1=C(CCCC1(C)C)C)\\\\C)\\\\C', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('N[C@@H](COP(O)(=O)OC[C@H](COC([*])=O)OC([*])=O)C(O)=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C[N+](C)(C)CCOP(O)(=O)OCC(COC([*])=O)OC([*])=O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('P(OC[C@@H](COC(*)=O)OC(*)=O)(=O)(OCC[N+](C)(C)C)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C[NH2+]CCOP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('C(C[N+](C)(C)C)OP(OC[C@@H](COC(CCCCCCCCCCCCCCCCC)=O)OC(*)=O)(=O)[O-]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('O(P(=O)(OCC[NH3+])[O-])C[C@H](OC(*)=O)COC(*)=O', 'Contains "
               'phosphatidylethanolamine structure with wildcard fatty acid '
               "chains'), "
               "('CCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[NH3+]', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC([*])=O', "
               "'Contains phosphatidylethanolamine structure with wildcard "
               "fatty acid chains')]\n"
               'False negatives: '
               "[('P(OCC(OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('[C@](COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)([H])COP(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\CCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCC/C=C\\\\CCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@@H](COC(CCCCCCCCCCCCCCC)=O)OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(=O)(OCCN)O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('[C@](COC(=O)CCCCCCCCCCCCCC)(OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)([H])COP(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCC)COC(=O)CCCCCCCCCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCC/C=C\\\\CCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('[C@@H](COC(=O)CCCCCCCCCCCCCCCCCC)(COP(OCCN)(=O)O)OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@@H](COC(CCCCCCCCCCCCCCCC)=O)OC(CCCCCCCCCCCCCCCC)=O)(=O)(OCCN)O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\CCCC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCC=1OC(=CC1C)CCC)COC(=O)CCCCCCCCCCC=2OC(=C(C2C)C)CCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('C(CN)OP(=O)(O)OC[C@H](OC(CCCCCCCCCCCCCC)=O)COC(=O)CCCCCCCCCCCCCCCCCCCCC', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OCCN)OC(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCC)COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@@H](COC(CCCCCCCCCCCCC)=O)OC(CCCCCCCCCCCCCCCCCCCCC)=O)(=O)(OCCN)O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCC/C=C\\\\CCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)COC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCC(=O)/C=C/C(O)=O)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCC=1OC(=C(C1C)C)CCCCC)COC(=O)CCCCCCCCCCCCC=2OC(=C(C2C)C)CCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\C(O)C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCC/C=C\\\\CCCCCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('CCCCCCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCCCCCCCCC)COP(=O)(O)OCCN', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCCN(C)C)(O)=O', "
               "'Missing required fatty acid chains'), "
               "('P(OCC(OC(=O)CCCCCCCCCCCCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(OCCNC)(O)=O', "
               "'Missing required fatty acid chains')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 114,
    'num_false_positives': 100,
    'num_true_negatives': 15013,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.5327102803738317,
    'recall': 1.0,
    'f1': 0.6951219512195121,
    'accuracy': 0.9934327181979379}