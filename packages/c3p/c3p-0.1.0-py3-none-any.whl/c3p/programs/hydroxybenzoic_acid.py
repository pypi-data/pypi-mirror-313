"""
Classifies: CHEBI:24676 hydroxybenzoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxybenzoic_acid(smiles: str):
    """
    Determines if a molecule is a hydroxybenzoic acid (benzoic acid with one or more phenolic hydroxy groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxybenzoic acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for carboxylic acid groups attached to aromatic rings or within a lactone
    carboxylic_patterns = [
        Chem.MolFromSmarts('[OH]-[C](=[O])-[cr5,cr6]'),  # Include both 5 and 6 membered rings
        Chem.MolFromSmarts('[O-]-[C](=[O])-[cr5,cr6]'),
        Chem.MolFromSmarts('O=[C]([O-])-[cr5,cr6]'),
        Chem.MolFromSmarts('O=[C](O)-[cr5,cr6]'),
        Chem.MolFromSmarts('O=C1O[C@@H](*)*C=2C1=C(*)*C=C(*)*2'),  # Lactone pattern
        Chem.MolFromSmarts('O=C1O[C@H](*)*C=2C1=C(*)*C=C(*)*2'),   # Lactone pattern
        Chem.MolFromSmarts('O=C1OC(*)*C=2C1=C(*)*C=C(*)*2')        # Generic lactone pattern
    ]
    
    found_carboxylic = False
    ring_carbons = set()
    
    for pattern in carboxylic_patterns:
        if pattern is None:
            continue
        matches = mol.GetSubstructMatches(pattern)
        if matches:
            found_carboxylic = True
            for match in matches:
                # Get the ring carbon - last atom in the match for direct acids,
                # or part of the ring system for lactones
                ring_carbons.update([i for i in match if mol.GetAtomWithIdx(i).IsInRing()])
            
    if not found_carboxylic:
        return False, "No carboxylic acid group found"

    # Look for hydroxy groups attached to the rings containing carboxylic groups
    hydroxy_patterns = [
        Chem.MolFromSmarts('[OH]-[cr5,cr6]'),
        Chem.MolFromSmarts('[O-]-[cr5,cr6]')
    ]
    
    phenolic_oh_count = 0
    for pattern in hydroxy_patterns:
        if pattern is None:
            continue
        matches = mol.GetSubstructMatches(pattern)
        for match in matches:
            ring_atom = match[1]
            # Check if the OH is attached to a ring that contains a carboxylic group
            for ring in mol.GetRingInfo().AtomRings():
                if ring_atom in ring and any(c in ring for c in ring_carbons):
                    phenolic_oh_count += 1
                    break
                
    if phenolic_oh_count > 0:
        return True, f"Found benzoic acid with {phenolic_oh_count} phenolic OH group(s)"
    else:
        return False, "No phenolic OH groups found on the ring system"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24676',
                          'name': 'hydroxybenzoic acid',
                          'definition': 'Any benzoic acid carrying one or more '
                                        'phenolic hydroxy groups on the '
                                        'benzene ring.',
                          'parents': ['CHEBI:22723', 'CHEBI:33853']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.2682926829268293 is too low.\n'
               'True positives: '
               "[('O1C(CCC=C(C)C)(C=CC=2C1=C(O)C=C(O)C2C(O)=O)C', 'Found "
               "benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C1C2=C(OC3=C1CO[C@@H](C3)C)C(O)=C(OC)C=C2C(=O)OC', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('CC1=C(C(O)=O)C(O)=CC(O)=C1', 'Found benzoic acid with 2 "
               "phenolic OH group(s)'), ('OC(=O)c1cccc(C(O)=O)c1O', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(O)C1=C(O)C=C(O)C=C1C(=O)C(=O)C', 'Found benzoic acid "
               "with 2 phenolic OH group(s)'), "
               "('[H][C@@]1(O[C@@](CC)(C[C@@H]1C)[C@@]1([H])CC[C@](O)(CC)[C@H](C)O1)[C@@H](CC)C(=O)[C@@H](C)[C@@H](O)[C@H](C)CCC1=C(C(O)=O)C(O)=C(C)C=C1', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('C1=2C(=C(C=C3C(N(C(C(=CC=C1)C23)=O)C=4C=CC(=C(C4)C(=O)O)O)=O)S(O)(=O)=O)N', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C1C(OC(=O)C2=C(O)C=C(O)C=C2C)=CO[C@H](C1)C', 'Found "
               "benzoic acid with 2 phenolic OH group(s)'), "
               "('C1=CC(=C(C=C1C(C(=O)O)N)C(=O)O)O', 'Found benzoic acid with "
               "1 phenolic OH group(s)'), "
               "('OC=1C(=C(CCCCCCCCC/C=C\\\\CCCC)C=CC1)C(O)=O', 'Found benzoic "
               "acid with 1 phenolic OH group(s)'), "
               "('O=C1NC2=C(O)C(=CC(=C2)O)[C@@H](NC3=CC(O)=CC(=C3)C(=O)O)CC=CC=C[C@H]([C@H]1C)O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('ClC1=C(O)C=C(O)C2=C1CC(=O)CCC(O)C[C@@H]3[C@H](C[C@H](OC2=O)C)O3', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C1N(CC=2C1=C(C(O)=C(CCC(=O)/C=C/C=C/CCCCCCC)C2O)C(=O)O)CCC(C)C', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('C(=O)(C1=CC(=C(C=C1)O)O)O', 'Found benzoic acid with 2 "
               "phenolic OH group(s)'), "
               "('[H][C@@]12CC[C@@]3(C)[C@H](Cc4cc(ccc4O)C(O)=O)C(C)=CC[C@]3([H])[C@@]1(C)CCCC2(C)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\Cc1cc(cc(O)c1O)C(O)=O', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('Cc1c(O)cc(O)c2C(=O)OC(=C)[C@](C)(O)c12', 'Found benzoic acid "
               "with 2 phenolic OH group(s)'), "
               "('ClC1=C(O)C=C(O)C2=C1[C@@H](Cl)[C@@H](C)OC2=O', 'Found "
               "benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C1O[C@H](C2=C(O)C=C(C(=O)O)C=C2O)C=3C1=C(O)C=C(O)C3', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('C12=C(NCC(=N1)CNC3=CC=C(C(O)=O)C(=C3)O)N=C(N)NC2=O', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C1O[C@H](O)C=2C1=C(OC)C(=C(O)C2C(=O)O)C', 'Found benzoic "
               "acid with 1 phenolic OH group(s)'), "
               "('OC=1C(=C(CCCCCC/C=C\\\\CCCCC)C=CC1)C(O)=O', 'Found benzoic "
               "acid with 1 phenolic OH group(s)')]\n"
               'False positives: '
               "[('O1C(C(O)C(O)C(O)C1OC2=CC(O)=C(C=C2)C(O)=O)C(O)=O', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('COC(=O)c1c(O)cc2cc3C(=O)c4cc(OC)cc(O)c4C(=O)c3c(O)c2c1C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('C=1(C=CC(=C(C1)Br)O)C([O-])=O', 'Found benzoic acid with 1 "
               "phenolic OH group(s)'), "
               "('O=C(OC1=C(C(O)=C(C)C(=C1)C)C)C2=C(O)C=C(O)C=C2C', 'Found "
               "benzoic acid with 2 phenolic OH group(s)'), "
               "('[Na+].[Na+].[Na+].Oc1ccc(cc1C([O-])=O)C(=C1C=CC(=O)C(=C1)C([O-])=O)c1ccc(O)c(c1)C([O-])=O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OC)C1=CC(O)=C([C@](O)(CCCC(O)(C)C)C)C=C1', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=C(O)C=C(C=C2)COC(=O)C3=CC(O)=C(O)C=C3)CO', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('Cc1cc(O)c(O)c(Oc2cc(C)c(C(O)=O)c(O)c2)c1', 'Found benzoic "
               "acid with 1 phenolic OH group(s)'), "
               "('[H][C@]12C[C@]3([H])O[C@@]1(C)[C@H](O)[C@@]1(C2)C=CC(=O)[C@@](C)(CCC(=O)Nc2c(O)ccc(C(=O)OC)c2O)[C@]31[H]', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C(OC)C1=C(O)C2=C(OC(C)=C[C@@]2([C@@H]3[C@@]4(OC=5C=C(C)C(=C(C5[C@H]3C=6C(O)=CC(=CC6O4)C)O)C(=O)OC)C)C)C=C1C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OCC1=CC(O)=C([C@@](O)(CCCC(C)C)C)C=C1)C2=CC(O)=C([C@@](O)(CCCC(C)C)C)C=C2', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('CC(=O)OC1=C(C=C(C=C1)C(=O)NC2=C(C=C(C=C2)O)C(=O)O)OC', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OC1=C(C(O)=C(C(=O)OC)C(=C1C)C)C)C2=C(O)C(=C(O)C(=C2C)C)C=O', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('ClC1=C(O)C(=C(O)C(=C1C)C(=O)O)C/C=C(/CCC[C@](O)(CCC=C(C)C)C)\\\\C', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C(OCC)C1=C(O)C=C(OC)C=C1CCC', 'Found benzoic acid with 1 "
               "phenolic OH group(s)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\Cc1cc(cc(O)c1O)C([O-])=O', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C1OC(=CC=2C1=C(O)C(=C(O)C2)C(=O)C3=C(O)C=C(OC)C=C3C(=O)OC)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OC1=CC(O)=CC(=C1)CCC)C2=C(O)C=C(OC)C=C2CCC', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OC)C1=CC(O)=C([C@@]2(OC(CCC2)(C)C)C)C=C1', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(O[C@H]1[C@H]2C(=C[C@@H]3C[C@@](CC3[C@@]2(C)C1)(CO)C)CO)C4=C(O)C=C(O)C=C4C', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C(OC1=C(O)C(=C(CCC)C=C1OC)C(=O)O)C2=C(O)C=C(OC)C=C2CCC', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OC1=C(C(O)=C(C(=O)O)C(=C1)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O(C1=CC(=CC(O)=C1)C(O)=O)C', 'Found benzoic acid with 1 "
               "phenolic OH group(s)'), "
               "('ClC1=C(O)C(=C(C(=O)OC)C=C1)C(=O)C2=C(O)C=C(C)C=C2O', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OC1=CC(O)=C(C(=O)O)C(=C1)CCC)C2=C(O)C=C(OC)C=C2CCCCC', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('ClC1=C(O)C=C(OC)C2=C1CC(=O)CCCC[C@@H](CC[C@@H](OC2=O)C)O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=[N+]([O-])C1=C(C(OC2=C(C(O)=CC(=C2)C)C(=O)OC[C@@H](C(=O)O)C)=C(OC)C=C1O)C(=O)OC', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('C=1(C(=CC(O)=CC1)C([O-])=O)NC(/C=C/C2=CC=C(O)C=C2)=O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('ClC1=C(OC2=C(OC)C=C(OC)C=C2C)C(=C(O)C=C1OC)C(=O)OC', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O(C=1C(=C(O)C=CC1)C(O)=O)C', 'Found benzoic acid with 1 "
               "phenolic OH group(s)'), "
               "('O=C1N([C@H](C(=O)N[C@@H](C(=O)N[C@@H](C)CC(O[C@@H]([C@@H](C(N[C@H]1[C@H](CC)C)=O)NC(=O)C(=NNC2=C(C(=O)OCCCCCCCCCC(C)C)C=C(O)C=C2)C)C3=CC=CC=C3)=O)CC=4C5=C(C(OC)=CC=C5)NC4)[C@@H](O)C6=CC=CC=C6)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O1[C@@H](O[C@@H]2OC=C3[C@]([C@H]2C=C)(CCOC3=O)[H])[C@H](OC(=O)C)[C@@H](OC(=O)C)[C@H](OC(=O)C4=C(O)C(O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO)=CC=C4)[C@H]1COC(=O)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('CCN(CC)S(=O)(=O)C1=CC(=C(C=C1)O)C(=O)OCC(=O)NC2=CC=C(C=C2)OC(F)(F)F', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OC1=C(O)C(=C(O)C=C1C)C)C2=C(O)C(=C(OC)C=C2C)C(=O)O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\COC(=O)c1ccc(O)cc1', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C1C2=C(C(O)=CC=C2OC3=C1C(OC)=CC(=C3)C)C(=O)OC', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('ClC1=C(C(=C(O)C=C1)C(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O[C@@H]3[C@@H](O)[C@@H](O[C@@H]([C@H]3O)C)O[C@@H]4[C@H]5C=CC6[C@@H](C=CC[C@@]7(C=C(C)[C@@H](C[C@]87C(=C(OC([C@]6([C@@H]5[C@@H](C)C[C@H]4C)C)=O)C(=O)O8)O)C[C@H](O)[C@@](O)(C(=O)C)C)C)C)O[C@@H]2C)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('CCN(CC)S(=O)(=O)C1=CC=CC2=CC(=C(C=C21)O)C(=O)O', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C1C2=C(C(=O)C=3C1=C(O)C(=C(C)C3)C(=O)O)C(O)=C(O)C=C2O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('ClC1=C(O)C=C(OC)C2=C1CC(=O)CCCCC(CC[C@@H](OC2=O)C)=O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('C1=CC(=CC=C1C(=O)OCC2=CC=CC=C2)O', 'Found benzoic acid with "
               "1 phenolic OH group(s)'), "
               "('O=C(O)C1=C(O)C=C(O)C=C1C2=C(C=C(O)C(=C2)O)C', 'Found benzoic "
               "acid with 2 phenolic OH group(s)'), "
               "('O=C(O)C1=CC(O)=C(/C(=C/CC[C@@H](COC(=O)C)C)/C)C=C1', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('S1C2=C(C3=C(C(O)=CC(=C3)OC)C(=O)O)C(=CC(=C2N=C1)O)C', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OC)C1=C(C(O)=CC(=C1)OC)C(=O)C2=C(O)C=C(C)C3=C2O[C@@](C=C=C4[C@@H](O)[C@]5(O[C@H]5[C@H](C4)O)CC=C(C)C)(C)C3', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C1OC2=C(C(=C(C(=O)O)C(=C2C)O)C(=CC)C)OC3=C1C(C(=CC)C)=CC(=C3C)O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(O)C1=C(O)C(C(=O)[C@@H]([C@H](O)C2=C(OC)C=CC(=C2)OC)C)=CC=C1OC', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O1[C@@]2([C@]1(C#CC=C3[C@@H](O)[C@H](OC(=O)C=4C5=C(C(=CC(OC)=C5)C)C=CC4O)C=C3C#C2)[H])[C@@]6(OC(OC6)=O)[H]', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('[O-]C(=O)c1cc(Br)c([O-])c(Br)c1', 'Found benzoic acid with 1 "
               "phenolic OH group(s)'), "
               "('Cc1cc2[C@H](O)[C@@H](O)c3c(O)c4C(=O)c5c(O)cc(O)cc5C(=O)c4c(O)c3-c2c(O)c1C(O)=O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C1O[C@](OC)(CC=2C1=C(O)C=3C4=C(O)C=5C(=O)C6=C(O)C(C(=O)O)=CC=C6OC5C(=C4CCC3C2)O)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('OC(=O)c1c(O)[nH]c2ccccc2c1=O', 'Found benzoic acid with 1 "
               "phenolic OH group(s)'), "
               "('ClC1=C(O)C=C(O)C(=C1C)C(=O)O[C@H]2[C@@]3(O)C(=C[C@]4(O)CC(C[C@@H]4[C@@]3(C)C2)(C)C)C=O', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C(N1C(CCC1)C(=O)NC2=C(C=CC=C2O)C(O)=O)C(NC(=O)C3=CC=C(O)C=C3)C(C)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O[C@@H]1[C@H]2COC(=O)c3cc(O)c(O)c(O)c3-c3c(O)c(O)c(Oc4c(O)c(O)c(O)cc4C(O)=O)cc3C(=O)O[C@@H]1[C@@H](O)[C@H](OC(=O)c1cc(O)c(O)c(O)c1)O2', "
               "'Found benzoic acid with 3 phenolic OH group(s)'), "
               "('OC(=O)C(=O)CCc1c(O)cc([nH]c1=O)C(O)=O', 'Found benzoic acid "
               "with 1 phenolic OH group(s)'), "
               "('O=C1C(C2=C(C(OC)=CC(=C2)O)C(=O)O)=C(C)C[C@H]1O', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('Oc1ccc(Cl)cc1C([O-])=O', 'Found benzoic acid with 1 phenolic "
               "OH group(s)'), "
               "('O=C(O[C@H]1[C@H](O)[C@@H](O)[C@H](OC(=O)C2=C(O)C=CC=C2C)[C@H](C1)NC(=O)C3=CC(O)=CC=C3)N', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('ClC1=C(O)C(Cl)=C(C)C(=C1O)C(=O)O', 'Found benzoic acid with "
               "2 phenolic OH group(s)'), "
               "('O.O.[Na+].[Na+].Oc1ccc(cc1C([O-])=O)\\\\N=N\\\\c1ccc(cc1)C(=O)NCCC([O-])=O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C1C(OC(=O)C2=C(O)C=C(O)C=C2C)C(OC(C1O)C)OC', 'Found "
               "benzoic acid with 2 phenolic OH group(s)'), "
               "('[H][C@]1(C=C(C)CC[C@H]1C(C)=C)c1c(O)cc(CCCCC)c(C([O-])=O)c1O', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('Cc1c(O)c2C(=O)C[C@H](Oc2c(C)c1O[C@@H]1O[C@H](COC(=O)c2ccc(O)cc2)[C@@H](O)[C@H](O)[C@H]1O)c1cc(O)ccc1O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(O)C=1C2=NC=CC=C2C=C(C1)O', 'Found benzoic acid with 1 "
               "phenolic OH group(s)'), "
               "('O=C(O)C1=CC(O)=C([C@@](O)(CCCC(=C)C)C)C=C1', 'Found benzoic "
               "acid with 1 phenolic OH group(s)'), "
               "('O[C@@]1([C@H]2[C@](CC1)(CC=C(C[C@@H]2OC(=O)C3=CC=C(O)C=C3)C)C)C(C)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('ClC1=C(O)C(Cl)=CC(=C1)C(=O)OC', 'Found benzoic acid with 1 "
               "phenolic OH group(s)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C[C@H](\\\\C(=C\\\\CC\\\\C(=C\\\\CC4=C(C(=C5C(=C4O)C(OC5)=O)C)OC)\\\\C)\\\\C)O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('ClC1=C(OC)C(=C(C)C(=C1O)Cl)C(=O)O[C@H]2[C@H](O[C@@H]3O[C@H]([C@H](OC)[C@](C3)([N+](=O)[O-])C)C)C[C@H](O[C@H]4[C@H](O)C[C@@]5(O[C@@]6([C@H](O)[C@H](O[C@H]7[C@@H](OC)[C@H](O[C@H]([C@@H]7O)O[C@H]8[C@H](O)[C@H](OC)[C@H](O[C@@H]9OC[C@@H]%10O[C@@]%11(O[C@H]%10[C@H]9O)OC[C@@H](OC(=O)C%12=C(O)C=C(O)C=C%12C)[C@H]%13[C@H]%11OCO%13)O[C@@H]8COC)C)O[C@@H]([C@H]6O5)C)C)O[C@@H]4C)O[C@@H]2C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('[H][C@]12CC[C@@]3(C=CC(=O)[C@@](C)(CCC(=O)Nc4c(O)ccc(C(=O)OC)c4O)[C@]3([H])C1)[C@@H](O)C2=C', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('C1=C([C@@]2([C@@H](C[C@@]2([C@@]3([C@]1(CC(C3)(C)C)[H])[H])C)OC(C4=C(C(=C(C=C4O)O)Br)C)=O)O)CO', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('C1(=C(C(=CC(=C1)O)O)C([O-])=O)/C=C/CCCC(=O)CCC[C@@H](O)C', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('[Cl-].C1=2C=CC(=CC1=[O+]C3=C(N2)C(=CC(=C3O)O)C(=O)O)N(C)C', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C1C(=N)C(=C(O)C(=C1)C2=C(O)C(=C(N)C(=C2)OC)C(=O)O)C(=O)O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(O)C1=CC(OC2=CC(O)=CC(=C2)C)=CC(=C1)O', 'Found benzoic "
               "acid with 1 phenolic OH group(s)'), "
               "('O=C(O)C1=C(O)C2=C(OC=3C=C(C)C=C(C3[C@@H]2C=C(C)C)O)C=C1C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O[C@@H]1[C@@H](COC(=O)c2cc(O)c(O)c(O)c2)O[C@@H](OC(=O)c2cc(O)c(O)c(O)c2)[C@H](OC(=O)c2cc(O)c(O)c(O)c2)[C@H]1OC(=O)c1cc(O)c(O)c(O)c1', "
               "'Found benzoic acid with 3 phenolic OH group(s)'), "
               "('O1[C@@H]([C@H](OC(=O)C2=CC(OC)=C(O)C(OC)=C2)CC=3C1=CC(O)=CC3O)C4=CC(O)=C(O)C(O)=C4', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(O)C1=C2O[C@]3(OC)[C@H](CCCC3)[C@@H]4C2=C([C@@H]([C@@H](C)O4)C)C(=C1O)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('CCN(C1=CC=CC=C1)S(=O)(=O)C2=CC(=C(C=C2)Cl)NC(=O)COC(=O)C3=C(C(=CC=C3)OC)O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C1C2=C(CC(/C=C/C)OC2)C[C@@H]([C@@]1(OC(=O)C3=C(O)C=C(O)C=C3C)C)OC(=O)C', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O(C1CC2(C3C(C4(C(C5C(CC4)(CCC5C(C)=C)C(O)=O)CC3)C)(CCC2C(C1O)(C)C)C)C)C(=O)C6=CC(O)=C(O)C=C6', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C(O)C1=C(O)C2=C(C[C@@H](CCCCCO)O[C@@H]2OC)C=C1O', 'Found "
               "benzoic acid with 2 phenolic OH group(s)'), "
               "('OC(=O)c1ncccc1O', 'Found benzoic acid with 1 phenolic OH "
               "group(s)'), "
               "('C\\\\C=C\\\\C1=CC2=CC(=O)C(C)(OC(=O)c3c(C)cc(O)cc3O)C(=O)C2=CO1', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('C1=2C(=C(C=C3C(N(C(C(=CC=C1)C23)=O)C=4C=CC(=C(C4)C(=O)[O-])O)=O)S([O-])(=O)=O)N', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('Cc1cccc2c(cc(O)cc12)C([O-])=O', 'Found benzoic acid with 1 "
               "phenolic OH group(s)'), "
               "('ClC1=C(O)C=C(OC2=C(O)C(=C(O)C=C2/C(=C/C)/C)C)C(=C1C)C(=O)O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O1[C@@H]([C@H](OC(=O)C=2C=C(OC)C(O)=C(O)C2)CC=3C1=CC(O)=CC3O)C4=CC(O)=C(O)C(O)=C4', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('C=12C(=C3C(=C(C(=CC3=CC1C[C@H](OC2=O)C[C@@H](C[C@@H](CCCCCO)O)O)OC)C4=C(C5=C(C=6C(O[C@@H](CC6C=C5C=C4OC)C[C@@H](C[C@@H](CCCCCO)O)O)=O)O)O)O)O', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('S1C2=C(C(C3=C(C(O)=CC(=C3)OC)C(=O)O)=CC(=C2N=C1)O)C', 'Found "
               "benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(OCC1=C[C@H]2[C@H]([C@@H](O)C(C2)(C)C)[C@@]3([C@@]1(O)[C@H](O)C3)C)C4=C(O)C=C(OC)C=C4C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O(C1(C(OC=2C(=C(O)C=C(C2C(OC)=O)C)C)C(=O)C(=C(O)C1O)C)C)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C1OC23C(C=C(CCC=C(C4C(C(=C1C2=O)O)(C5C=C(CC(C5CC4C)OC6OC(C(OC(=O)C7=C(OC)C=C(O)C=C7C)C(C6O)O)C)C)C)C)C)(C=C(C(=O)O)C(C3)C)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(O[C@H](CC(=O)O)C)C1=C(O)C=C(O)C=C1C[C@H](OC(=O)C[C@H](OC(=O)C[C@@H](O)CO)C)C', "
               "'Found benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C(OC1=C(O)C(=C(OC(=O)C2=CC=C(O)C=C2)C(=C1C3=CC=C(O)C=C3)O)C4=CC=C(O)C=C4)C5=CC=C(O)C=C5', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(O)C1=CC(=C(O)C=C1)C/C=C/C(C/C=C/C(C/C=C/C(CC/C=C(\\\\C(=O)O)/C)C)C)C', "
               "'Found benzoic acid with 1 phenolic OH group(s)'), "
               "('O=C(O)C1=C(O)C2=C(C[C@@H](CCCCCCC)OC2)C(=C1O)C', 'Found "
               "benzoic acid with 2 phenolic OH group(s)'), "
               "('O=C1C=C2C=C(OC[C@H]2[C@@H]([C@@]1(OC(=O)C3=C(O)C=C(O)C=C3C)C)O)C=CCO', "
               "'Found benzoic acid with 2 phenolic OH group(s)')]\n"
               "False negatives: [('O=C1O[C@](OC)(CC=2C1=C(O)C(=C(O)C2C)C)C', "
               "'Ring is not aromatic'), "
               "('O=C1O[C@@](OC2=C(C3=C(CO[C@H]([C@@H]3C)C)C(=C2)O)C)(CC=4C1=C(O)C(=C(O)C4C)C)C', "
               "'Ring is not aromatic'), "
               "('O=C1O[C@H](CC=2C1=C(O)C=C(OC)C2O)C[C@@H]3O[C@H](CCC3)C', "
               "'Ring is not aromatic'), "
               "('O=C1O[C@@H](CC=2C1=C(O)C=CC2O)CCC[C@@H](OC(=O)C[C@](O)(CCO)C)C', "
               "'Ring is not aromatic'), ('O=C1OCC=2C1=C(C(O)=C(OC)C2O)C', "
               "'Ring is not aromatic'), "
               "('O=C1OC(CC(=O)OC(CC(=O)OC(CC=2C=C(O)C=C(C2C(OC(CC(OC(CC=3C1=C(O)C=C(O)C3)C)=O)C)=O)O)C)CO)C', "
               "'Ring is not aromatic'), "
               "('O=C1O[C@@H](CC=2C1=C(O)C=CC2O)CCC[C@@H](OC(=O)CCC(=O)O)C', "
               "'Ring is not aromatic'), "
               "('O=C1O[C@H](OC)C=2C1=C(O)C(OC)=C(O)C2C', 'Ring is not "
               "aromatic'), "
               "('O=C1O[C@](CC)(C)C=2C1=C(O)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C2)C', "
               "'Ring is not aromatic'), "
               "('O=C1O[C@H]([C@@H](O)C)C=2C1=C(O)C(=C(O)C2)C', 'Ring is not "
               "aromatic'), "
               "('O(C)C1=C(OC)C=C(C=C1OC)C(OCC=2N=C(COC(=O)C3=CC(OC)=C(C(=C3)OC)OC)C=CC2)=O', "
               "'No phenolic OH groups found on the aromatic ring'), "
               "('O=C1OC(=C)[C@@H](C)C=2C1=C(O)C=C(O)C2C=O', 'Ring is not "
               "aromatic'), ('O=C1O[C@]([C@@H](C)C=2C1=C(O)C=C(O)C2C)(CO)C', "
               "'Ring is not aromatic'), "
               "('O=C1O[C@@H]([C@@H](O)CC)CC=2C1=C(O)C=C(O)C2', 'Ring is not "
               "aromatic'), "
               "('O=C1O[C@@H](CC2=C(C=CC=C2)C(CC=3C1=C(O)C=C(O)C3)=O)C', 'Ring "
               "is not aromatic'), "
               "('O=C1O[C@H]([C@@](O)(C)C=2C1=C(O)C=C(O)C2C)CO', 'Ring is not "
               "aromatic'), "
               "('CN1C2=C(C=C(C=C2)S(=O)(=O)NC3=CC(=CC(=C3)C(=O)O)C(=O)O)C(=O)N(C1=O)C', "
               "'No phenolic OH groups found on the aromatic ring'), "
               "('Br[C@H]1C2=C(C(=O)O[C@H]1C)C(O)=CC(=C2)O', 'Ring is not "
               "aromatic'), ('O=C1O[C@@H](CCCCCC=2C1=C(O)C=C(O)C2)C', 'Ring is "
               "not aromatic'), ('O=C1O[C@H](/C=C/CCC)CC=2C1=C(O)C(=C(O)C2)C', "
               "'Ring is not aromatic')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 40,
    'num_false_positives': 100,
    'num_true_negatives': 6032,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.2857142857142857,
    'recall': 0.9523809523809523,
    'f1': 0.4395604395604395,
    'accuracy': 0.9834791059280855}