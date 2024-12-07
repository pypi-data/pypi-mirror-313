"""
Classifies: CHEBI:136716 N-(fatty acyl)-L-alpha-amino acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_N__fatty_acyl__L_alpha_amino_acid_anion(smiles: str):
    """
    Determines if a molecule is an N-(fatty acyl)-L-alpha-amino acid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule matches the class, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Pattern for N-acyl amino acid anion core structure
    # Matches: R-C(=O)-N-CH-C([O-])=O where R is any carbon
    core_pattern = Chem.MolFromSmarts('[#6]C(=O)N[CH1,CH2]C([O-])=O')
    
    # Pattern that should not be present (cyclic amino acids)
    cyclic_pattern = Chem.MolFromSmarts('[#6]1[#6][#6][#6][#6]N1C(=O)')
    
    if mol.HasSubstructMatch(cyclic_pattern):
        return False, "Contains cyclic amino acid structure"
    
    if not mol.HasSubstructMatch(core_pattern):
        # Special handling for wildcards (*) in SMILES
        if '*' in smiles and 'NC(=O)*' in smiles and '[O-]' in smiles:
            return True, "Valid N-(fatty acyl)-L-alpha-amino acid anion with wildcard"
        return False, "Missing N-acyl-amino acid anion core structure"
    
    # Get matches for the core pattern
    matches = mol.GetSubstructMatches(core_pattern)
    
    for match in matches:
        # Check for carboxylate group
        carboxylate_c = match[-2]  # Carbon attached to [O-]
        
        # Check for alpha carbon
        alpha_c = match[-2]  # The carbon between N and C([O-])=O
        alpha_atom = mol.GetAtomWithIdx(alpha_c)
        
        # Check acyl group
        acyl_c = match[0]  # First carbon of acyl group
        acyl_chain_length = 0
        
        # Traverse the acyl chain
        visited = set()
        stack = [(acyl_c, 0)]
        
        while stack:
            current_atom, depth = stack.pop()
            if current_atom in visited:
                continue
            visited.add(current_atom)
            
            atom = mol.GetAtomWithIdx(current_atom)
            if atom.GetSymbol() == 'C':
                acyl_chain_length += 1
                
            for neighbor in atom.GetNeighbors():
                if (neighbor.GetIdx() not in visited and 
                    neighbor.GetSymbol() == 'C' and 
                    neighbor.GetIdx() not in match):
                    stack.append((neighbor.GetIdx(), depth + 1))
        
        # Check chirality if specified
        chiral_centers = Chem.FindMolChiralCenters(mol)
        for center in chiral_centers:
            if center[0] == alpha_c and center[1] == 'R':
                return False, "Incorrect stereochemistry - should be L/S configuration"
        
        if acyl_chain_length >= 2 or '*' in smiles:
            return True, "Valid N-(fatty acyl)-L-alpha-amino acid anion"
    
    return False, "Requirements not met for N-(fatty acyl)-L-alpha-amino acid anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:136716',
                          'name': 'N-(fatty acyl)-L-alpha-amino acid anion',
                          'definition': 'The conjugate base of a '
                                        'N-fatty-acyl-L-alpha-amino acid '
                                        'arising from deprotonation of the '
                                        'carboxy group; major species at pH '
                                        '7.3.',
                          'parents': ['CHEBI:229684', 'CHEBI:59874']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.05555555555555556 is too low.\n'
               'True positives: '
               "[('C(\\\\CCCCCCCC(=O)N[C@H](C([O-])=O)[C@H](CC)C)=C\\\\CCCCCCCC', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(CCCCCC(NCC(=O)[O-])=O)C', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C(CCCCCC(NCC(=O)[O-])=O)CCCCC', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion')]\n"
               'False positives: '
               "[('[C@@H](NC([C@H]1[NH2+]CCC1)=O)(C(=O)[O-])C', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('N1([C@@H](CCC1)C(=O)N[C@H](C(=O)N[C@@H](CCC(=O)[O-])C(N2[C@@H](CCC2)C(=O)N[C@@H]([C@H](CC)C)C([O-])=O)=O)C(C)C)C([C@H](CC3=CC=C(C=C3)O)[NH3+])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[NH3+]CCCC[C@H]([NH3+])C(=O)NCC([O-])=O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C[C@H](NC(=O)[C@@H]([NH3+])CCCC[NH3+])C([O-])=O', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('Nc1nc2NC[C@H](CNc3ccc(cc3)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O)Nc2c(=O)[nH]1', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('CSCC[C@H]([NH3+])C(=O)N[C@@H](CC1=CC=CC=C1)C(=O)N[C@@H](CCSC)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(=[NH2+])(NCCC[C@@H](C(=O)N1[C@H](C(N2[C@H](C(=O)NCC(N[C@H](C(N[C@H](C(=O)N3[C@H](C(=O)N[C@H](C(N[C@H](C([O-])=O)CCCNC(=[NH2+])N)=O)CC=4C=CC=CC4)CCC3)CO)=O)CC=5C=CC=CC5)=O)CCC2)=O)CCC1)[NH3+])N', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('OC[C@H]1C(OC[C@@H](C([O-])=O)NC(=O)C2=C3C(=CC(=C2)[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O[Fe-]5(OC6=C(C=C(C=C6O5)[C@H]7[C@@H]([C@H]([C@@H]([C@H](O7)CO)O)O)O)C(=O)N1)O3)=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H]C(=O)N1[C@@H](CNc2ccc(cc2)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O)CNc2nc(N)[nH]c(=O)c12', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C[NH2+][C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C([O-])=O)c3O)c(Cl)c2', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[O-]C(=O)[C@H](CCCNC(=O)c1ccccc1)NC(=O)c1ccccc1', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C([C@H]1NC(CC1)=O)(=O)N[C@H](C([O-])=O)CCC(=O)N', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[NH2+]([C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)[O-])C)=O)CCCC[NH3+])=O)CCC(N)=O)=O)CCCNC(N)=[NH2+])=O)CO)=O)C(C)C)=O)CC(C)C)=O)C)=O)CO)=O)CCCNC(N)=[NH2+])=O)CCC(N)=O)=O)CCCC[NH3+])=O)CO)=O)CCCC[NH3+])=O)C(C)C)=O)CCCC[NH3+])=O)CC(C)C)=O)CCCC[NH3+])=O)[C@@H](C)CC)=O)CO)=O)CC1=CNC=N1)CO)=O)CO)=O)CCCC[NH3+])=O)CC(C)C)=O)CCCC[NH3+])=O)CC(C)C)C(=O)CCCC[C@@H]2[C@]3([C@@](CS2)(NC(N3)=O)[H])[H]', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C1([C@H](CCC1=O)CC(N[C@H](C([O-])=O)[C@H](CC)C)=O)C/C=C\\\\CC', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[O-]C([C@H](CCC(N[C@H](C([O-])=O)CS*)=O)[NH3+])=O', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O)[H])[H])(CC[C@@]4([C@@H](CCC(NCC([O-])=O)=O)C)[H])[H])C)O)[H])C', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])CC[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCC(=O)NCC([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C=1C=C(C=CC1C(NCC([O-])=O)=O)O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C(=O)([C@@H]([NH3+])CC1=CC=CC=C1)N[C@H](C(=O)[O-])CC=2NC=NC2', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C[NH2+][C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O[C@H]5C[C@](C)([NH3+])[C@@H](O)[C@H](C)O5)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C([O-])=O)c3O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@H]1C[C@](C)([NH3+])[C@@H](O)[C@H](C)O1)c(Cl)c2', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H+].[H+].[H+].[H+].[H+].[H+].[Ga+3].CC(C)(C)[Si]([18F])(C1=CC=C(C=C1)C(=O)NC[C@@H](NC(=O)CC[C@H](N1CCN(CC([O-])=O)CCN(CC([O-])=O)CCN(CC([O-])=O)CC1)C([O-])=O)C(=O)N[C@H](CCCCNC(=O)CCC(=O)NCCC[C@@H](NC(=O)CC[C@H](NC(=O)N[C@@H](CCC([O-])=O)C([O-])=O)C([O-])=O)C([O-])=O)C([O-])=O)C(C)(C)C', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(*)(=O)[C@@H](N*)CCC(N[C@H](C(=O)[O-])CCC(=O)[O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('NC(=O)CC[C@H](NC(=O)Cc1ccccc1)C([O-])=O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C[C@H](OP([O-])(=O)OC[C@@H](O)[C@@H](O)[C@@H](O)Cn1c2cc(O)ccc2cc2c1nc(=O)[n-]c2=O)C(=O)N[C@@H](CCC(=O)N[C@@H](CCC(=O)N[C@@H](CCC([O-])=O)C([O-])=O)C([O-])=O)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[NH3+][C@H](C([O-])=O)CCC(=O)NCC(=O)[O-]', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C(CCCCCCCCCC)CCCCC(N[C@H](C([O-])=O)O)=O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('O=C([O-])C(NC(=O)CC=1C=2C=CC=CC2NC1)CCC(=O)N', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(NCC([O-])=O)(=O)C1=C([131I])C=CC=C1.[Na+]', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(NCC([O-])=O)(=O)C1=C(C=CC=C1)I.[Na+]', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('[NH3+]CCCC[C@H](NC(=O)CC[C@H](N-*)C([O-])=O)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('Nc1ccc(cc1)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('CSCC[C@H](NC(=O)[C@H](CC1=CC=CC=C1)NC(=O)CNC(=O)CNC(=O)[C@@H]([NH3+])CC1=CC=C(O)C=C1)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[O-]C(=O)[C@H](CCC(=O)N[C@@H](CCCC=O)C([O-])=O)N-*', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('CC(C)C[C@H]([NH3+])C(=O)N[C@@H](CC(C)C)C([O-])=O', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(CCCCCCC)(=O)N[C@H](C([O-])=O)O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('[C@@H]1(N(C([C@@H](NC([C@@H](NC([C@@H](NC([C@H](CC2=CC=C(O)C=C2)NC([C@@H](NC([C@H]3NC(=O)CC3)=O)CC(C)C)=O)=O)CCC([O-])=O)=O)CC(N)=O)=O)CCCC[NH3+])=O)CCC1)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(CCCCCCCCCCC)(=O)N[C@H](C([O-])=O)O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('[NH3+][C@H](C(=O)N1[C@H](C(=O)[O-])CCC1)CC=2N=CNC2', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCC(=O)NCC([O-])=O)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CC[C@@H](O)C2', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(=O)([C@H](CCC(=O)N[C@@H](C(C)C)C(=O)[O-])[NH3+])[O-]', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C([C@H](CCCC[NH3+])NC([C@H](CC(C)C)NC([C@H](CCCC[NH3+])NC(=O)[C@H]1N(CCC1)C([C@H](CCCNC(=[NH2+])N)NC([C@H]([C@H](CC)C)NC([C@H](CCCNC(=[NH2+])N)NC([C@H](CCCNC(=[NH2+])N)NC([C@H](CC(C)C)NC([C@H](CC2=CC=CC=C2)NC(=O)CNC(=O)CNC([C@H](CC3=CC=C(C=C3)O)[NH3+])=O)=O)=O)=O)=O)=O)=O)=O)=O)(=O)[O-]', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[Na+].[Na+].Nc1nc(=O)c2c(CCc3ccc(cc3)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O)c[nH]c2[nH]1', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('O=C(N[C@@H](CC([O-])=O)C([O-])=O)[C@@H]([NH3+])CCC([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[NH2+]([C@H](C(N[C@H](C(NC(C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)[O-])CC(N)=O)=O)CCC(C)=O)=O)CCCC[NH3+])=O)CCCNC(N)=[NH2+])=O)CCCC[NH3+])=O)C(C)C)=O)CC(C)C)=O)CCC(=O)N)=O)CO)=O)CCCNC(N)=[NH2+])=O)CC(C)C)=O)CCCC[NH3+])=O)C(C)C)=O)C(C)C)=O)C(C)C)=O)CCCC[NH3+])=O)CC(C)C)=O)CCCC[NH3+])=O)C(C)C)=O)C(C)C)=O)CC1=CNC=N1)CCCC[NH3+])=O)[C@H](CC)C)=O)CCCC[NH3+])=O)CCC(=O)N)=O)CCCC[NH3+])=O)CC(C)C)C(CCCC[C@@H]2[C@]3([C@@](CS2)(NC(N3)=O)[H])[H])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C[N+](C)(C)[C@@H](Cc1c[nH]c([Se]C[C@H](NC(=O)CC[C@H]([NH3+])C([O-])=O)C([O-])=O)n1)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[NH3+][C@@H](CC1=CNC=N1)C(=O)NCC([O-])=O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3([C@@H](C[C@@]2(C[C@@H](C1)O)[H])O)[H])(CC[C@@]4([C@@H](CCC(NCC([O-])=O)=O)C)[H])[H])C)[H])C.[Na+]', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C([C@H](CO)NC(=O)C1=C2C(=CC=C1)O[Fe+]O2)([O-])=O', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(NCC(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)[O-])CCCNC(=[NH2+])N)C(C)C)=O)CCC(=O)[O-])C)CC(C)C)(NC([C@@H](NC(CNC([C@@H](NC(=O)CNC(=O)[C@@H](NC(=O)[C@@H]([NH3+])CC([O-])=O)CO)CCC([O-])=O)=O)=O)CC(=O)[O-])=O)CC1=CC=CC=C1', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('CSCC[C@H](NC(=O)[C@@H]([NH3+])CC1=CC=CC=C1)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H][C@]1(Nc2c(N[C@H]1C)nc(N)[nH]c2=O)[C@@H](C)Nc1ccc(C[C@H](O)[C@H](O)[C@H](O)CO[C@H]2O[C@H](COP([O-])(=O)O[C@@H](CCC([O-])=O)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O)[C@@H](O)[C@H]2O)cc1', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('O=C([O-])[C@@H](NC(CC1=CNC2=CC=CC=C12)=O)CC(=O)[O-]', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[NH3+][C@H](C(=O)NCC(=O)[O-])CC(C)C', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('[H][C@@]12CC[C@H](N1C(=O)C2)C([O-])=O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('[NH3+][C@H](C(=O)N[C@H](C(=O)[O-])C)CC=1N=CNC1', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H]C(=O)N(C[C@H]1CNC2=C(N1)C(=O)NC(N)=N2)C1=CC=C(C=C1)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H][C@]1([NH2+][C@@H](C([O-])=O)C(C)(C)S1)[C@H](NC(=O)Cc1ccccc1)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(CNC(=O)CC(C)C)(=O)[O-]', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('[C@@H]1([C@H](CCC1=O)CC(N[C@H](C([O-])=O)[C@H](CC)C)=O)C/C=C\\\\CCO', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(CCCCCCC(=O)NCC([O-])=O)CCCCCCCCCCCCCCCC', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C1(/C(/NC([C@@H](N1)CCCNC(N)=[NH2+])=O)=C/C2=CC=C(C(=C2)OCC[C@H](NC(=O)C[C@](CC([O-])=O)(C(=O)[O-])O)C(=O)[O-])OC)=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('Nc1nc2NCC(CNc3ccc(cc3)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O)Nc2c(=O)[nH]1', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])CC[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@@H](C2)OS([O-])(=O)=O)[C@H](C)CCC(=O)NCC([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(=O)([C@@H]([NH3+])CCC(=O)N[C@H](C(=O)[O-])CCC(N)=O)[O-]', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H][C@]12CNc3nc(N)[nH]c(=O)c3[N+]1=CN(C2)c1ccc(cc1)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C([C@H](CO)NC(=O)C1=C(C(=CC=C1)O)O)(OC[C@@H](C(OC[C@@H](C([O-])=O)NC(=O)C2=C(C(=CC(=C2)[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O)O)=O)NC(=O)C4=C(C(=CC=C4)O)O)=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(=[NH2+])(NCCC[C@@H](C(=O)N1[C@H](C(N2[C@H](C(=O)NCC(N[C@H](C(N[C@H](C(=O)N3[C@H](C(=O)N[C@H](C([O-])=O)CC=4C=CC=CC4)CCC3)CO)=O)CC=5C=CC=CC5)=O)CCC2)=O)CCC1)[NH3+])N', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[O-]C([C@H](CC(C)C)NC([C@H](CCCC[NH3+])NC(=O)[C@H]1N(CCC1)C([C@H](CCCNC(=[NH2+])N)NC([C@H]([C@H](CC)C)NC([C@H](CCCNC(=[NH2+])N)NC([C@H](CCCNC(=[NH2+])N)NC([C@H](CC(C)C)NC([C@H](CC2=CC=CC=C2)NC(=O)CNC(=O)CNC([C@H](CC3=CC=C(C=C3)O)[NH3+])=O)=O)=O)=O)=O)=O)=O)=O)=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H]C(=O)N(CC1CNC2=C(N1)C(=O)NC(N)=N2)C1=CC=C(C=C1)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[Na+].[Na+].CN(Cc1cnc2nc(N)nc(N)c2n1)c1ccc(cc1)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('NC1=NC(=O)C2=NC(CNC3=CC=C(C=C3)C(=O)N[C@@H](CCC(=O)N[C@@H](CCC(=O)N[C@@H](CCC(=O)N[C@@H](CCC(=O)N[C@@H](CCC([O-])=O)C([O-])=O)C([O-])=O)C([O-])=O)C([O-])=O)C([O-])=O)=CN=C2N1', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCC(=O)NCC([O-])=O)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CC[C@H](C2)OS([O-])(=O)=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[C@@H]1(N(C([C@@H](NC([C@@H](NC([C@@H](NC([C@H](CC2=CC=C(O)C=C2)NC([C@@H](NC([C@H]3NC(=O)CC3)=O)CC(C)C)=O)=O)CCC([O-])=O)=O)CC(N)=O)=O)CCCC[NH3+])=O)CCC1)C(N[C@H](C(N[C@H](C(N4[C@H](C([O-])=O)CCC4)=O)CCCNC(N)=[NH2+])=O)CCCNC(N)=[NH2+])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(CC[C@@H](C(N1[C@@H](CCC1)C(=O)N[C@@H]([C@H](CC)C)C([O-])=O)=O)NC([C@H](C(C)C)NC([C@H](CC2=CC=CC=C2)NC(=O)[C@H]3N(CCC3)C([C@H](CC4=CC=C(C=C4)O)[NH3+])=O)=O)=O)(=O)[O-]', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[NH2+]([C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)[O-])CO)=O)CCCC[NH3+])=O)[C@@H](C)CC)=O)CC(=O)N)=O)CCC(N)=O)=O)CCCC[NH3+])=O)C(C)O)=O)CCCNC(N)=[NH2+])=O)C(C)C)=O)C)=O)CC(C)C)=O)C)=O)CC(=O)N)=O)CCCNC(N)=[NH2+])=O)C)=O)CCCNC(N)=[NH2+])=O)C)=O)CC(C)C)=O)CC1=CC=CC=C1)=O)C(O)C)=O)CC2=CC=C(C=C2)O)CCCC[NH3+])=O)CC(=O)N)=O)CCCNC(N)=[NH2+])=O)CC(C)C)=O)CCC(N)=O)=O)C(C)O)C(=O)CCCC[C@@H]3[C@]4([C@@](CS3)(NC(N4)=O)[H])[H]', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('Nc1nc2NC[C@H](CNc3ccc(cc3)C(=O)N[C@@H](CCC(=O)N[C@@H](CCC(=O)N[C@@H](CCC([O-])=O)C([O-])=O)C([O-])=O)C([O-])=O)Nc2c(=O)[nH]1', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C=1(C=CC=CC1C(NCC(=O)[O-])=O)O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C[C@@H](Nc1ccc(C[C@H](O)[C@H](O)[C@H](O)CO[C@H]2O[C@H](COP([O-])(=O)O[C@@H](CCC([O-])=O)C(=O)N[C@@H](CCC([O-])=O)C(=O)N[C@@H](CC([O-])=O)C([O-])=O)[C@@H](O)[C@H]2O)cc1)c1c[nH]c2nc(N)nc(=O)c2n1', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[O-]C(=O)CNC(=O)c1ccccc1', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('[NH2+]([C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)[O-])CC1=CNC=N1)=O)CCCNC(N)=[NH2+])=O)CCCNC(=[NH2+])N)=O)C(C)C)=O)C(C)C)=O)C(C)C)=O)C(C)C)=O)CO)=O)C(C)C)=O)CCC(=O)N)=O)C(C)C)=O)CCCC[NH3+])=O)CCCC[NH3+])=O)CCCC[NH3+])=O)[C@H](CC)C)=O)CC(C)C)=O)CC(=C)N)=O)CC(C)C)=O)CCC(=C)N)=O)CC(C)C)=O)CCC(=C)N)CC(C)C)=O)CCCC[NH3+])=O)CCCC[NH3+])=O)CCCC[NH3+])=O)CCCC[NH3+])=O)CCCC[NH3+])C(=O)CCCC[C@@H]2[C@]3([C@@](CS2)(NC(N3)=O)[H])[H]', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('OC=1C=C(C(=O)NCC([O-])=O)C=CC1', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('[O-]C(=O)[C@H](CC1=CC=CC=C1)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@@H]2CCCN2C(=O)[C@H](CCCC[NH3+])NC(=O)[C@@H]3CCCN3C(=O)[C@@H]([NH3+])CCCNC(N)=[NH2+]', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('COc1cc(\\\\C=C\\\\C(=O)NCC([O-])=O)ccc1O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('N([C@H](C(N[C@H](C(=O)[O-])CCC(=O)[O-])=O)CCC(=O)[O-])C([C@@H](N*)*)=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(=O)([C@@H]([NH3+])C)N1[C@H](C(=O)NCC(=O)[O-])CCC1', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C[C@H](NC(=O)[C@@H](C)O[C@H]1[C@H](O)[C@@H](CO)OC(OP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@@H]1NC(C)=O)C(=O)N[C@H](CCC([O-])=O)C(=O)N[C@@H](CCCC[NH3+])C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('O[C@](CC(=O)NCCC(N1C(=O)CCC1(O)C([O-])=O)C([O-])=O)(CC(=O)OCCN1C(=O)CCC1(O)C([O-])=O)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('OC[C@H](NC(=O)c1cccc(O)c1O)C([O-])=O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('[Na+].C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O)[H])[H])(CC[C@]4([H])[C@@H](CCC(NCC([O-])=O)=O)C)[H])C)O)[H])C', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(CCC)C[C@@H](\\\\C=C\\\\C=C/C/C=C\\\\C/C=C\\\\CCCC(NCC([O-])=O)=O)OO', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(N[C@H](C([O-])=O)O)(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(NCC([O-])=O)(=O)C1=C(C=CC=C1)I', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C([C@H](CO)NC(=O)C1=C(C(=CC=C1)O)O)(OC[C@@H](C(OC[C@@H](C([O-])=O)NC(=O)C2=C(C(=CC(=C2)[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O)O)=O)NC(=O)C4=C(C(=CC(=C4)[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O)O)O)=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C(CCCCC)(=O)N[C@H](C([O-])=O)O', 'Valid N-(fatty "
               "acyl)-L-alpha-amino acid anion'), "
               "('C[NH2+][C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C([O-])=O)c3O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@H]1C[C@](C)([NH3+])[C@H](O)[C@H](C)O1)c(Cl)c2', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('CCCCCCCCCCCCCCCC(=O)N[C@@H](CCC(=O)NCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCC(=O)NCCCC[C@H](NC(=O)[C@@H](NC(=O)[C@@H]1CCCN1C(=O)[C@H](CC1=CC=C(O)C=C1)NC(=O)[C@H](CCC([O-])=O)NC(=O)[C@H](CC1=CNC2=C1C=CC=N2)NC(=O)[C@H](CC1=CC=C(O)C=C1)NC(=O)[C@@H](NC(=O)[C@H](CC([O-])=O)N(C)C(=O)[C@@H]1CC(=O)NCCCC[C@H](NC(C)=O)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](CCC([O-])=O)C(=O)N[C@@H](CCCNC(N)=[NH2+])C(=O)N[C@@H](CC2=CC=CC=C2)C(=O)N1)C(C)(C)C)C1CCCCC1)C([O-])=O)C([O-])=O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('O=C1NC=2C(C1CC(=O)NC(CC([O-])=O)C([O-])=O)=CC=CC2', 'Valid "
               "N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('[Na+].O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](C[C@H]3O)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCC(=O)NCC([O-])=O)C)[H])[H])C.O', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3([C@@H](C[C@@]2(C[C@@H](C1)O)[H])O)[H])(CC[C@]4([H])[C@@H](CCC(N[C@H](C(=O)[O-])CC=5N=CNC5)=O)C)[H])C)O)[H])C', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion'), "
               "('C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3([C@@H](C[C@@]2(C[C@@H](C1)O)[H])O)[H])(CC[C@]4([H])[C@@H](CCC(N[C@H](C(=O)[O-])CO)=O)C)[H])C)O)[H])C', "
               "'Valid N-(fatty acyl)-L-alpha-amino acid anion')]\n"
               "False negatives: [('[NH3+]CCCC[C@H](NC(=O)*)C(=O)[O-]', "
               "'Missing N-acyl-amino acid pattern'), "
               "('C=1NC=2C=CC=CC2C1C[C@]([H])(NC(*)=O)C(=O)[O-]', 'Missing "
               "N-acyl-amino acid pattern')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 15734,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 0.8,
    'f1': 0.07339449541284404,
    'accuracy': 0.9936233348064903}