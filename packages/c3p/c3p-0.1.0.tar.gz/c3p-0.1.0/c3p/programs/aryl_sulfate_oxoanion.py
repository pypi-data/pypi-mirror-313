"""
Classifies: CHEBI:139371 aryl sulfate oxoanion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aryl_sulfate_oxoanion(smiles: str):
    """
    Determines if a molecule is an aryl sulfate oxoanion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aryl sulfate oxoanion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of sulfate oxoanion group (-OS([O-])(=O)=O)
    sulfate_pattern = Chem.MolFromSmarts('OS([O-])(=O)=O')
    if not mol.HasSubstructMatch(sulfate_pattern):
        return False, "No sulfate oxoanion group found"
        
    # Get matches for sulfate group
    matches = mol.GetSubstructMatches(sulfate_pattern)
    
    # Pattern for aromatic rings (excluding heterocycles)
    aromatic_pattern = Chem.MolFromSmarts('c1ccccc1')
    
    for match in matches:
        # Get the oxygen atom that connects to the aromatic ring
        o_atom_idx = match[0]
        o_atom = mol.GetAtomWithIdx(o_atom_idx)
        
        # Get the atom connected to oxygen that's not the sulfur
        for neighbor in o_atom.GetNeighbors():
            if neighbor.GetIdx() != match[1]:  # If not the sulfur atom
                # Check if this atom is part of an aromatic ring
                if neighbor.GetIsAromatic():
                    # Find the ring this atom belongs to
                    for ring in mol.GetRingInfo().AtomRings():
                        if neighbor.GetIdx() in ring:
                            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
                            # Check if all atoms in ring are aromatic carbons
                            if all(atom.GetIsAromatic() for atom in ring_atoms):
                                # Check if this is a simple aryl sulfate
                                if len(matches) == 1:
                                    return True, "Contains sulfate oxoanion group attached to aromatic ring"
                                else:
                                    # For multiple sulfate groups, ensure they're on different rings
                                    other_matches = [m for m in matches if m != match]
                                    for other_match in other_matches:
                                        other_o = mol.GetAtomWithIdx(other_match[0])
                                        for other_neighbor in other_o.GetNeighbors():
                                            if other_neighbor.GetIdx() != other_match[1]:
                                                if other_neighbor.GetIsAromatic():
                                                    return True, "Contains sulfate oxoanion group attached to aromatic ring"
                    
    return False, "Sulfate group not properly attached to aromatic ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139371',
                          'name': 'aryl sulfate oxoanion',
                          'definition': 'An organosulfate oxoanion obtained by '
                                        'deprotonation of the sulfo group of '
                                        'any aryl sulfate. The R group in this '
                                        'structure represents an aromatic '
                                        'ring.',
                          'parents': ['CHEBI:58958']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.18604651162790695 is too low.\n'
               "True positives: [('C(CC=1C=C(C=CC1)OS([O-])(=O)=O)C([O-])=O', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C=1C(=CC=C(C1OC)OS([O-])(=O)=O)C=C', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('C1(=C(C=C(C)C=C1)OS([O-])(=O)=O)C(C)C', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('[O-]S(OC=1C=CC(=CC1OC)C=CC)(=O)=O', 'Contains sulfate "
               "oxoanion group attached to aromatic ring')]\n"
               'False positives: '
               "[('[Na+].[H][C@]12CC[C@]3(C)C(=O)CC[C@@]3([H])[C@]1([H])CCc1cc(OS([O-])(=O)=O)ccc21', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[H][C@]12CC[C@]3(C)C(=O)CC[C@@]3([H])[C@]1([H])CCc1cc(OS([O-])(=O)=O)ccc21', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C=1(C=CC(=CC1)CC[NH3+])OS([O-])(=O)=O', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('C=1C=C(C=CC1C[C@@H](C(*)=O)N*)OS([O-])(=O)=O', 'Contains "
               "sulfate oxoanion group attached to aromatic ring'), "
               "('O[C@@H]1[C@@H](COS([O-])(=O)=O)O[C@@H](Oc2cc(O)c3c(c2)occ(-c2ccc(OS([O-])(=O)=O)cc2)c3=O)[C@H](O)[C@H]1O', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[O-]S(=O)(=O)Oc1cccc2c1ccc1ccccc21', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('C1=C(OS([O-])(=O)=O)C=CC2=C1CC[C@]3([C@@]4(CC[C@]([C@]4(CC[C@@]32[H])C)(C#C)O)[H])[H]', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C=1(C[C@@H](C(=O)[O-])[NH3+])C=C(C(OC2=CC(I)=C(OS([O-])(=O)=O)C(=C2)I)=CC1)I', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('COc1ccc(cc1O)-c1c2c3cc(OC)c(OS([O-])(=O)=O)cc3oc(=O)c2n2ccc3cc(OC)c(OC)cc3c12', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[O-]S(=O)(=O)Oc1cccc2ccc3ccccc3c12', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('[Na+].COc1ccc(cc1O)-c1c2c3cc(OC)c(OS([O-])(=O)=O)cc3oc(=O)c2n2ccc3cc(OC)c(OC)cc3c12', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C([C@H](CCC(=O)N)NC([C@H]([C@@H](C)O)NC([C@H](CC1=CC=C(C=C1)OS(=O)(=O)[O-])NC([C@H]([C@H](CC)C)NC([C@H](CC2=CC=C(C=C2)OS(=O)(=O)[O-])[NH3+])=O)=O)=O)=O)(=O)[O-]', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C1[C@]2([C@]3([C@@](C4=C(C=C(OS([O-])(=O)=O)C(=C4)O)CC3)(CC[C@@]2([C@@H](O)C1)C)[H])[H])[H]', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C1=C2C(CC[C@]3([C@@]4(CC[C@@H]([C@]4(CC[C@@]32[H])C)O)[H])[H])=CC(=C1)OS([O-])(=O)=O', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[O-]S(=O)(=O)Oc1ccc2ccc3ccccc3c2c1', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('[O-]S(=O)(=O)Oc1cc2ccccc2c2ccccc12', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('[O-]S(OC1=C(C=CC(=C1)CC[NH3+])O)(=O)=O', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('Oc1cc(OS([O-])(=O)=O)cc2occ(-c3ccc(OS([O-])(=O)=O)cc3)c(=O)c12', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C=1C=C(C=CC1OS([O-])(=O)=O)O', 'Contains sulfate oxoanion "
               "group attached to aromatic ring'), "
               "('O=C([O-])[C@@H]([NH3+])CC=1C=CC(=CC1)OS([O-])(=O)=O', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C=1(C[C@@H](C(=O)[O-])[NH3+])C=C(C(OC2=CC(I)=C(OS([O-])(=O)=O)C=C2)=C(C1)I)I', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[O-]S(=O)(=O)Oc1ccc2c(ccc3ccccc23)c1', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('C=1(C(=CC(=CC1)CC[NH3+])O)OS([O-])(=O)=O', 'Contains sulfate "
               "oxoanion group attached to aromatic ring'), "
               "('[NH3+][C@@H]1c2ccc(OS([O-])(=O)=O)c(Oc3cc(O)cc(c3)[C@@H]3NC(=O)[C@H](Cc4ccc(Oc5cc6cc(Oc7ccc(cc7Cl)[C@@H](O)[C@@H]7NC(=O)[C@H](NC(=O)[C@@H]6NC3=O)c3cc(Cl)c(O)c(c3)-c3c(O)cc(O)cc3[C@@H](NC7=O)C([O-])=O)c5[O-])c(Cl)c4)NC1=O)c2', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[Na+].[Na+].[O-]S(=O)(=O)Oc1ccc(cc1)C(c1ccc(OS([O-])(=O)=O)cc1)c1ccccn1', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[O-]S(=O)(=O)Oc1ccc2ccc3ccccc3c2c1OS([O-])(=O)=O', 'Contains "
               "sulfate oxoanion group attached to aromatic ring'), "
               "('Oc1c(OC(OC(C=O)C([O-])=O)C=O)ccc2occ(-c3ccccc3OS([O-])(=O)=O)c(=O)c12', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[H][C@]12[C@@H](O)C[C@H]([NH3+])C(=O)N1CC1=C(C=CC(OS([O-])(=O)=O)=C1O)[C@H]2O', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C(CC=1C=C(C(=CC1)OS([O-])(=O)=O)OC)[NH3+]', 'Contains "
               "sulfate oxoanion group attached to aromatic ring'), "
               "('[Na+].C[C@]12CC[C@H]3C(=CCc4cc(OS([O-])(=O)=O)ccc34)[C@@H]1CCC2=O', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[O-]S(=O)(=O)Oc1c(OS([O-])(=O)=O)c2ccccc2c2ccccc12', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C=1(C[C@@H](C(=O)[O-])[NH3+])C=C(C(OC2=CC(I)=C(OS([O-])(=O)=O)C=C2)=CC1)I', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('C=1C=CC=C(C1OS([O-])(=O)=O)O', 'Contains sulfate oxoanion "
               "group attached to aromatic ring'), "
               "('CC12CCC3C(CCC4=CC(OS([O-])(=O)=O)=CC=C34)C1CCC2[*]', "
               "'Contains sulfate oxoanion group attached to aromatic ring'), "
               "('[Na+].CCCCCOc1ccc(cc1)-c1cc(no1)-c1ccc(cc1)C(=O)N[C@H]1C[C@@H](O)[C@@H](O)NC(=O)[C@@H]2[C@@H](O)[C@@H](C)CN2C(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H]2C[C@@H](O)CN2C(=O)[C@@H](NC1=O)[C@@H](C)O)[C@H](O)[C@@H](O)c1ccc(O)c(OS([O-])(=O)=O)c1)[C@H](O)CC(N)=O', "
               "'Contains sulfate oxoanion group attached to aromatic ring')]\n"
               'False negatives: []',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 34,
    'num_true_negatives': 183855,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.10526315789473684,
    'recall': 1.0,
    'f1': 0.1904761904761905,
    'accuracy': 0.9998151098736765}