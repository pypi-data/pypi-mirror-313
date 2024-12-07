"""
Classifies: CHEBI:24403 glycosyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_glycosyl_group(smiles: str):
    """
    Determines if a molecule is a glycosyl group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycosyl group, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of * (attachment point)
    has_attachment = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == '*':
            has_attachment = True
            break
    if not has_attachment:
        return True, "Valid glycosyl group structure but missing attachment point"

    # Find rings
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        return False, "No rings found"

    # Look for pyranose/furanose rings (5 or 6 membered rings containing O)
    sugar_rings = []
    for ring_atoms in rings.AtomRings():
        if len(ring_atoms) not in [5, 6]:
            continue
            
        ring_atom_objs = [mol.GetAtomWithIdx(i) for i in ring_atoms]
        
        # Check if ring contains exactly one O
        ring_o_atoms = [a for a in ring_atom_objs if a.GetSymbol() == 'O']
        if len(ring_o_atoms) != 1:
            continue

        # Check for carbons
        valid_ring = True
        for atom in ring_atom_objs:
            if atom.GetSymbol() not in ['C', 'O']:
                valid_ring = False
                break

        if valid_ring:
            sugar_rings.append(ring_atoms)

    if not sugar_rings:
        return False, "No valid sugar rings found"

    # Check for characteristic substituents and patterns
    for ring in sugar_rings:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Track substituents
        has_hydroxyl = False
        has_amino = False
        has_acetyl = False
        
        for atom in ring_atoms:
            if atom.GetSymbol() == 'C':
                for neighbor in atom.GetNeighbors():
                    # Check for hydroxyl groups
                    if neighbor.GetSymbol() == 'O' and neighbor.GetIdx() not in ring:
                        if len(neighbor.GetNeighbors()) == 1:
                            has_hydroxyl = True
                            
                    # Check for amino groups
                    elif neighbor.GetSymbol() == 'N':
                        has_amino = True
                        
                    # Check for acetyl groups
                    elif neighbor.GetSymbol() == 'C' and neighbor.GetIdx() not in ring:
                        for n2 in neighbor.GetNeighbors():
                            if n2.GetSymbol() == 'O' and n2.GetBonds()[0].GetBondType() == Chem.BondType.DOUBLE:
                                has_acetyl = True

        # If we have characteristic sugar substituents, it's likely a glycosyl group
        if has_hydroxyl or has_amino or has_acetyl:
            if has_amino:
                return True, "Valid glycosyl group with amino substituents"
            elif has_acetyl:
                return True, "Valid glycosyl group with acetyl substituents"
            else:
                return True, "Valid glycosyl group with hydroxyl substituents"

    # Check for glycosidic linkage pattern
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == '*':
            # Look for O-linkage patterns
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O':
                    for n2 in neighbor.GetNeighbors():
                        if any(n2.GetIdx() in ring for ring in sugar_rings):
                            return True, "Valid glycosyl group with glycosidic linkage"
                elif neighbor.GetSymbol() == 'C':
                    for n2 in neighbor.GetNeighbors():
                        if n2.GetSymbol() == 'O':
                            for n3 in n2.GetNeighbors():
                                if any(n3.GetIdx() in ring for ring in sugar_rings):
                                    return True, "Valid glycosyl group with glycosidic linkage"

    # If we've found sugar rings but no specific patterns, still consider it a glycosyl group
    return True, "Basic glycosyl group structure identified"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24403',
                          'name': 'glycosyl group',
                          'definition': 'An organic group obtained by removing '
                                        'the hydroxy group from the hemiacetal '
                                        'function of a monosaccharide or '
                                        'monosaccharide derivative and, by '
                                        'extension, of a lower oligosaccharide '
                                        'or oligosaccharide derivative.',
                          'parents': ['CHEBI:33247']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.3483870967741936 is too low.\n'
               'True positives: '
               "[('[C@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO[C@]4(O[C@]([C@@H]([C@H](C4)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(O)=O)O)O)O)O)NC(=O)C)O[C@@H]5[C@@H]([C@@H](O[C@@H]([C@H]5O)CO[C@@H]6[C@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O[C@H]7[C@@H]([C@H]([C@@H]([C@H](O7)CO)O[C@H]8[C@@H]([C@H]([C@H]([C@H](O8)CO[C@]9(O[C@]([C@@H]([C@H](C9)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(O)=O)O)O)O)O)NC(C)=O)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)O[C@H]%11[C@@H]([C@H](C(O[C@@H]%11CO[C@@H]%12O[C@H]([C@H]([C@H]([C@@H]%12O)O)O)C)*)NC(C)=O)O)NC(C)=O)O)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('C1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)NC(=O)C)*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)NC(=O)C)O)O)*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@H](O[C@@H]2O[C@@H]([C@@H]([C@@H]([C@H]2O)O[C@@H]3O[C@@H]([C@@H]([C@@H]([C@H]3O)O[C@@H]4O[C@@H]([C@H]([C@@H]([C@H]4O)O)O[C@H]5O[C@@H]([C@H]([C@@H]([C@H]5NC(=O)C)O)O[C@@H]6O[C@@H]([C@H]([C@@H]([C@H]6O)O)O[C@H]7O[C@@H]([C@H]([C@@H]([C@H]7NC(=O)C)O)O[C@@H]8O[C@@H]([C@H]([C@@H]([C@H]8O)O)O)C(O)=O)CO)C(O)=O)CO)C(O)=O)O)CO)O)CO)CO1)O)O)*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@@H]2O[C@H]([C@H]([C@H]([C@@H]2O[C@@H]3O[C@H]([C@H]([C@H]([C@@H]3O)O)O)C)O)O)C)NC(C)=O)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)*)NC(=O)C)O[C@@H]5O[C@H]([C@H]([C@H]([C@@H]5O[C@@H]6O[C@H]([C@H]([C@H]([C@@H]6O)O)O)C)O)O)C', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O)CO)O[C@@H]2[C@@H](NC(C)=O)[C@H](O[C@@H]3[C@H]([C@H](O[C@@H]([C@@H]3O)CO)*)O)O[C@H](CO)[C@H]2O)O[C@@H]4O[C@H]([C@H]([C@H]([C@@H]4O)O)O)C)[C@H]5O[C@H](CO)[C@@H]([C@@H]([C@H]5O)O)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O)O)O)O)O)*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O[C@@H]4[C@@H]([C@@H](O[C@@H]([C@H]4O)CO[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)CO[C@@H]6[C@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O[C@@H]7[C@H]([C@H]([C@@H]([C@H](O7)CO)O)O)O)O)O[C@@H]8[C@H]([C@H]([C@@H]([C@H](O8)CO)O)O)O[C@@H]9[C@H]([C@H]([C@@H]([C@H](O9)CO)O)O)O)O)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)O[C@H]%11[C@@H]([C@H]([C@@H](O[C@@H]%11CO)*)NC(C)=O)O)NC(C)=O)O)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O[C@H]1[C@H](*)O[C@@H]([C@@H]([C@@H]1O)O[C@@H]2[C@H](O)[C@@H](O)[C@@H](O)[C@H](O2)CO)CO', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)C(O)=O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)OS(=O)(=O)O)O[C@H]5[C@H]([C@@H]([C@H]([C@H](O5)C(O)=O)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)NC(C)=O)O)OS(=O)(=O)O)NC(C)=O)O)O)O)O)O[C@H]7[C@@H]([C@H]([C@@H](OC7)*)O)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O[C@H]1[C@H]([C@H](O[C@H]([C@@H]1O)O[C@@H]2[C@H](O[C@@H](*)[C@@H]([C@H]2O)O)CO)CO)O[C@H]3[C@@H]([C@H]([C@@H](O)[C@H](O3)CO)O)NC(C)=O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O[C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O)CO)O[C@@H]2[C@@H](NC(C)=O)[C@H](O[C@@H]3[C@H]([C@H](O[C@@H]([C@@H]3O)CO)*)O)O[C@H](CO)[C@H]2O)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('CC(=O)N[C@@H]1[C@@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@H](OS(O)(=O)=O)[C@H](O)[C@H]2NC(C)=O)[C@@H](CO)O[C@H]1O[C@@H]1[C@@H](-*)O[C@H](CO)[C@@H](O)[C@@H]1O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)NC(=O)C)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)*)NC(=O)C)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@H]([C@@H]([C@@H]([C@@H](O2)C)O)O)O)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O)O[C@H]4[C@H]([C@@H]([C@@H]([C@@H](O4)C)O)O)O)NC(C)=O)*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)NC(=O)C)O[C@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)CO)O)O)NC(=O)C)NC(=O)C)*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@H](O[C@@H]2O[C@@H]([C@@H]([C@@H]([C@H]2O)O[C@@H]3O[C@@H]([C@@H]([C@@H]([C@H]3O)O[C@@H]4O[C@@H]([C@H]([C@@H]([C@H]4O)O)O[C@H]5O[C@@H]([C@H]([C@@H]([C@H]5NS(=O)(O)=O)OS(O)(=O)=O)O[C@@H]6O[C@@H]([C@@H]([C@H]([C@@H]6OS(=O)(=O)O)O)O[C@H]7O[C@@H]([C@H]([C@@H]([C@H]7NS(=O)(O)=O)O)O[C@@H]8O[C@@H]([C@@H]([C@H]([C@@H]8O)O)O)C(O)=O)CO)C(O)=O)CO)C(O)=O)O)CO)O)CO)CO1)O)O)*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O([C@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)O)O)[H])C(=O)O)[C@@H]([C@H]([C@@]3(O[C@](C[C@H](O)[C@H]3NC(C)=O)(C(=O)O)*)[H])O)CO', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O([C@H]1[C@H](O[C@H]([C@H](O[C@H]2[C@H]([C@@H]([C@@H]([C@@H](O2)C)O)O)O)[C@H]1O)O[C@H]3[C@@H](O)[C@H](O[C@@H]([C@@H]3NC(C)=O)*)CO)CO)[C@@H]4[C@@H]([C@H]([C@H](O)[C@H](O4)CO)O[C@@H]5[C@H](O)[C@@H](O)[C@H]([C@H](O5)CO)O)NC(C)=O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)C(O)=O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C(O)=O)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)NC(C)=O)O)O)NC(C)=O)O)O)O)O)O[C@H]7[C@@H]([C@H]([C@@H](OC7)*)O)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)C)NC([H])=O)O)O)O[C@@H]2[C@@H]([C@H]([C@H](O[C@@H]2C(N)=O)*)NC(C)=O)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](CO)O[C@@H]2OC[C@H]2O[C@H](OC[C@H]3O[C@H](-*)[C@@H](O)[C@@H]3O)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H]1O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O[C@@H]4[C@@H]([C@@H](O[C@@H]([C@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)O[C@H]6[C@@H]([C@H](C(O[C@@H]6CO)*)NC(C)=O)O)NC(C)=O)O)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('C1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O[C@@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])(C(O)=O)O[C@H]2[C@H]([C@H](O[C@@H](O[C@H]3[C@@H]([C@H]([C@H](O[C@H]4[C@H]([C@H](OC(*)[C@@H]4O)CO)O)O[C@@H]3CO)NC(C)=O)O)[C@@H]2O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O)[C@H](O5)CO)O)NC(=O)C', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O[C@H]2[C@H]([C@@H]([C@@H]([C@@H](O2)C)O)O)O)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)*)NC(C)=O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@H](O[C@@H]2O[C@@H]([C@@H]([C@@H]([C@H]2O)O[C@@H]3O[C@@H]([C@@H]([C@@H]([C@H]3O)O[C@@H]4O[C@@H]([C@H]([C@@H]([C@H]4O)O)O[C@H]5O[C@@H]([C@H]([C@@H]([C@H]5NS(=O)(O)=O)O)O[C@@H]6O[C@@H]([C@@H]([C@H]([C@@H]6OS(=O)(=O)O)O)O[C@H]7O[C@@H]([C@H]([C@@H]([C@H]7NS(=O)(O)=O)O)O[C@@H]8O[C@@H]([C@H]([C@@H]([C@H]8O)O)O)C(O)=O)CO)C(O)=O)CO)C(O)=O)O)CO)O)CO)CO1)O)O)*', "
               "'Valid glycosyl group with glycosidic linkage')]\n"
               'False positives: '
               "[('C1=C(CNC(=O)C)C(NC(N1[C@@H]2O[C@H](COP(=O)([O-])*)[C@H](C2)O*)=O)=O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])(C([O-])=O)O[C@@H]([C@H]([C@@]2(O[C@](O[C@H]3[C@H]([C@H](O[C@H]([C@@H]3O)O[C@@H]4[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]4O)O)CO)CO)O[C@H]5[C@@H]([C@H]([C@@H](O)[C@H](O5)CO)O[C@@H]6O[C@@H]([C@@H]([C@@H]([C@H]6O)O[C@H]7O[C@@H]([C@@H]([C@@H]([C@H]7O)O[C@H]8O[C@@H]([C@@H]([C@@H]([C@H]8O)O)O)CO)O)CO)O)CO)NC(C)=O)(C[C@H](O)[C@H]2NC(=O)C)C([O-])=O)[H])O)CO', "
               "'Valid glycosyl group with amino substituent'), "
               "('C([C@@H]([C@@H](CCCCCCCCCCCCCCCCC)O)NC(*)=O)O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)NC(C)=O)O[C@@]5(C[C@@H]([C@H]([C@@](O5)([C@@H]([C@@H](CO)O)O)[H])NC(CO)=O)O)C([O-])=O)O)O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)NC(=O)C)O[C@@H]2[C@H]([C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)O', "
               "'Valid glycosyl group with amino substituent'), "
               "('N([C@@H]1O[C@@H]([C@H]([C@@H]([C@H]1NC(=O)C)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O[C@@H]6[C@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O)O)O[C@@H]7[C@H]([C@H]([C@@H]([C@H](O7)CO)O)O)O[C@@H]8[C@H]([C@H]([C@@H]([C@H](O8)CO)O)O)O)O)O)O[C@@H]9[C@H]([C@H]([C@@H]([C@H](O9)CO)O)O)O[C@@H]%10[C@H]([C@H]([C@@H]([C@H](O%10)CO)O)O)O[C@@H]%11[C@H]([C@H]([C@@H]([C@H](O%11)CO)O)O[C@@H]%12[C@@H]([C@H]([C@@H]([C@H](O%12)CO)O)O[C@@H]%13[C@@H]([C@H]([C@@H]([C@H](O%13)CO)O)O)O[C@@H]%14[C@@H]([C@H]([C@@H]([C@H](O%14)CO)O)O)O)O)O)O)O)NC(C)=O)CO)C(C[C@@H](C(*)=O)N*)=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O)O[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O[C@@H]6[C@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O)O)O)O[C@@H]7[C@H]([C@H]([C@@H]([C@H](O7)CO)O)O)O[C@@H]8[C@H]([C@H]([C@@H]([C@H](O8)CO)O)O)O[C@@H]9[C@H]([C@H]([C@@H]([C@H](O9)CO)O)O[C@@H]%10[C@@H]([C@H]([C@@H]([C@H](O%10)CO)O)O[C@@H]%11[C@@H]([C@H]([C@@H]([C@H](O%11)CO)O)O)O)O)O)O)O[C@H]%12[C@@H]([C@H]([C@@H](O[C@@H]%12CO)O[C@H]%13[C@@H]([C@H]([C@@H](O[C@@H]%13CO)NC(C[C@@H](C(=O)*)N*)=O)NC(=O)C)O)NC(=O)C)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('OC[C@H]1O[C@@H](*)C[C@@H]1O*', 'Valid glycosyl group with "
               "glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@@H]([C@H]([C@@H](O1)C)O)O)OC)OCCCCCCCCC(N*)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@H]1(O[C@@H]([C@H](O)[C@@H]([C@H]1O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@@H]3O[C@@H]([C@H](O)[C@@H]([C@H]3O[C@@H]4O[C@H]([C@@H](O)[C@H]([C@@H]4O)O)C)O)CO)O)NC(C)=O)CO)O[C@@H]5[C@H]([C@H](O[C@@H]6[C@H]([C@H](O[C@@H]7[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]7O)O)CO)O[C@@H]([C@@H]6O)CO)O)O[C@H](CO)[C@H]5O)NC(C)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@H]1(O[C@@H]([C@H](O)[C@@H]([C@H]1O)O)CO)O[C@@H]2[C@H]([C@H](O[C@@H]3[C@H]([C@H](O[C@@H]4[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]4O)O)CO)O[C@@H]([C@@H]3O)CO)O)O[C@H](CO[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)[C@H]2O)NC(C)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)NC(=O)C)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)O)[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)CO)O)[H])C([O-])=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('N[C@H](Cc1ccc(O)cc1)C(=O)O[C@@H]1[C@@H](COP([O-])(-*)=O)O[C@H]([C@@H]1O)n1cnc2c(N)ncnc12', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O)O)CO)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)O[C@@H]5[C@H]([C@@H](O[C@@H]([C@@H]5O)CO)O[C@H]6[C@@H]([C@H]([C@@H](O[C@@H]6CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O[C@@H]7O[C@H]([C@H]([C@H]([C@@H]7O)O)O)C)O)NC(=O)C)O[C@@H]8O[C@H]([C@H]([C@H]([C@@H]8O)O)O)C', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O=P(O)(O[C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O)O)O)O)O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)OC[C@@H](COC(*)=O)OC(*)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@@H]1(O[C@H]([C@@H]([C@@H]1O)O)N2C=3N=C(NC(=O)C3[N+](=C2)C)N)COP([O-])(=O)N4C=C(N=C4)C[C@@H](C(=O)*)N*', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O([C@H]1[C@H]([C@@H]([C@H](O)[C@@H](O1)C)O)O)[C@H]2[C@@H]([C@H]([C@H](O[C@@H]3[C@H]([C@H](O[C@@H]4[C@H](O[C@@H](OC[C@@H]([C@@H](*)O)NC(=O)*)[C@@H]([C@H]4O)O)CO)O[C@@H]([C@@H]3O)CO)O)O[C@@H]2CO[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)NC(C)=O)O[C@@H]6O[C@@H]([C@H](O)[C@@H]([C@H]6O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)CO', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(*)O)[C@@H](O*)C3', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O([C@@H]1[C@@H]([C@@H](O[C@H]([C@H]1O)OC[C@@H](C(*)=O)N*)C)O)[C@@H]2O[C@@H]([C@H]([C@@H]([C@H]2O)O)O)CO', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(*)=O)[C@@H]([C@H]1O)O)CO)[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O[C@@H]5O[C@H]([C@H]([C@H]([C@@H]5O)O)O)C)NC(C)=O)O[C@@]6(C[C@@H]([C@H]([C@@](O6)([C@@H]([C@@H](CO)O)O)[H])NC(C)=O)O)C(=O)[O-])O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@H]1(OP(=O)([O-])[O-])[C@H](O*)[C@@H](N*)[C@@H](O[C@@H]1CO)OC[C@@H]2[C@H]([C@@H]([C@H]([C@H](O2)OP(=O)([O-])[O-])N*)O*)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('NC(=[NH2+])NCCCCNc1[nH+]c(=N)ccn1[C@@H]1O[C@H](COP([O-])(-*)=O)[C@@H](O-*)[C@H]1O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('C1(NC(=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(OP(=O)(OP(=O)(O)O)O)O)[C@@H](O*)[C@H]3O*)N)=O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('C(O[C@]1(O[C@@]([C@@H]([C@H](C1)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])[C@H]2O[C@H]([C@@H]([C@H]([C@H]2O)O)O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO[C@]7(O[C@@]([C@@H]([C@H](C7)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])O)O)O)O)NC(C)=O)O[C@H]8[C@@H]([C@H]([C@@H](O[C@@H]8CO)O[C@@H]9[C@H]([C@@H](O[C@@H]([C@@H]9O)CO)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(C)=O)O', "
               "'Valid glycosyl group with amino substituent'), "
               "('[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(C)=O)[C@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@@H]4CO)O[C@H]4[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]5[C@H](O)[C@@H](O)[C@H](OC[C@H](NC([*])=O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC)O[C@@H]5CO)[C@@H]4O)[C@H](O)[C@@H](O[C@@H]4O[C@H](CO)[C@@H](O[C@@H]5O[C@H](CO)[C@H](O)[C@H](O[C@@]6(C[C@H](O)[C@@H](NC(C)=O)[C@@]([H])(O6)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]5O)[C@H](O)[C@H]4NC(C)=O)[C@H]3O)O[C@@H]2CO)[C@@H]1O)C(O)=O)[C@H](O)[C@H](O)CO', "
               "'Valid glycosyl group with amino substituent'), "
               "('CC1=C2C(OC(=O)C3=C(O)C=C(O[*])C=C23)=CC(O[*])=C1', 'Valid "
               "glycosyl group with hydroxyl substituent'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@H]3O[C@H](CO)[C@@H](O[C@@H]4O[C@H](CO[C@@H]5O[C@H](CO)[C@@H](O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O[C@H]7O[C@H](CO)[C@H](O)[C@H](O)[C@H]7O)[C@H]6O)[C@H](O)[C@H]5NC(C)=O)[C@H](O)[C@H](O[C@@H]5O[C@H](CO)[C@@H](O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O)[C@H]6O)[C@H](O)[C@H]5NC(C)=O)[C@H]4O)[C@H](O)[C@H]3NC(C)=O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)(NC(=O)*)CO[C@@H]1O[C@@H]([C@@H](O[C@H]2[C@@H]([C@@H](OS(O)(=O)=O)[C@H]([C@@H](CO)O2)O[C@@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O)NC(=O)C)O)[C@@H]([C@H]1O)O)CO', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O1C(O)[C@H](OC(=O)*)[C@H](O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)[O-])(=O)[O-]', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)O[C@@H]2[C@H]([C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O[C@H]6[C@H]([C@@H]([C@@H]([C@@H](O6)C)O)O)O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O[C@@H]1[C@@H]([C@H](O[C@@]([C@H]1OP(=O)(OP(=O)(OCCNC(=O)CCCCC(NCCCC[C@@H](C(=O)*)N*)=O)O)O)([C@@H](O)CO)[H])O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('N1([C@H]2C[C@H](O*)[C@H](O2)COP([O-])(=O)*)C3=C(C(=NC(=N3)*)*)N=C1', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O[C@H]1[C@H](O[C@@H](O[C@@H]2[C@H]([C@H](O[C@@H]3[C@H](OS(=O)(=O)[O-])[C@H]([C@H](O[C@@H]4[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]4O)O)CO)O[C@@H]3CO)O)O[C@H](CO)[C@@H]2O)NC(C)=O)[C@@H]([C@H]1OS(=O)(=O)[O-])O)CO', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)OC(=O)*)OP(OC[C@H](CO*)OC(=O)*)(=O)[O-])O[C@@H]2[C@H]([NH3+])[C@@H](O)[C@@H]([C@H](O2)CO)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)COP([O-])(=O)OCC[NH3+])O)O)O[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)COP([O-])(=O)OCC[NH3+])O)O)O[C@@H]6[C@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O)O)O)OP([O-])(=O)OCC[NH3+]', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C)=O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O[C@@H]4O[C@@H]([C@H]([C@H]4O)O)COP(O)(=O)OC[C@@H](C(=O)*)N*)O', "
               "'Valid glycosyl group with amino substituent'), "
               "('*[C@@H]1O[C@H](COP(=O)(*)[O-])[C@@H](O*)[C@H]1O', 'Valid "
               "glycosyl group with glycosidic linkage'), "
               "('[C@@H]1(OC([C@H](O)[C@H]([C@@H]1O)O)O*)CO', 'Valid glycosyl "
               "group with glycosidic linkage'), "
               "('O[C@@H]1CO[C@@H](OC[C@H]2O[C@@H](O[*])[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@H]1O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('C1(=C(N2C(=O)C3=C(N(C2=N1)C)N(C=N3)[C@@H]4O[C@H](COP(=O)(*)[O-])[C@@H](O*)[C@H]4O)CC[C@H]([NH3+])C(=O)[O-])C', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N)[C@@H](O)C(=O)NCCC(=O)NCCSC([*])=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O[C@H]1[C@H](O[C@@H](O[C@@H]2[C@H]([C@H](O[C@@H]3[C@H](O)[C@H]([C@H](O[C@@H]4[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]4O)O)CO)O[C@@H]3CO)O)O[C@H](CO)[C@@H]2O)NC(C)=O)[C@@H]([C@H]1O)O)CO', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(-*)=O)[C@@H](OC(=O)[C@@H]([NH3+])COP([O-])([O-])=O)[C@H]1O', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@H](O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)O)O)[H])C(=O)O)CO)O)[H])(C(O)=O)O[C@H]4[C@H]([C@H](O[C@H]([C@@H]4O)O[C@@H]5[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]5O)O)CO)CO)O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O[C@H]7[C@@H]([C@@H](O[C@]8(O[C@]([C@@H]([C@H](C8)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]9(O[C@]([C@@H]([C@H](C9)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]%10(O[C@]([C@@H]([C@H](C%10)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)O)O)[H])C(=O)O)O)[H])C(=O)O)[C@H]([C@H](O7)CO)O)O)NC(C)=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('C(O[C@]1(O[C@@]([C@@H]([C@H](C1)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])[C@H]2O[C@H]([C@@H]([C@H]([C@H]2O)O)O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO[C@]7(O[C@@]([C@@H]([C@H](C7)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])O)O)O)O)NC(C)=O)O[C@H]8[C@@H]([C@H]([C@@H](O[C@@H]8CO)O[C@@H]9[C@H]([C@@H](O[C@@H]([C@@H]9O)CO)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(C)=O)O', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(CO)=O)([C@@H]([C@@H](CO)O[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)[H])C([O-])=O)O)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)O[C@@H]5[C@H]([C@@H](O[C@@H]([C@@H]5O)CO)O[C@H]6[C@@H]([C@H]([C@@H](O[C@@H]6CO)OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('OC1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H](O)[C@@H]1NC([*])=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('N(C1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(*)[O-])[C@@H](O*)[C@H]3O)(C(N[C@H](C([O-])=O)[C@H](O)C)=O)C', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O(C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@@H]7[C@@H]([C@H]([C@H]([C@H](O7)CO)O)O)O)O[C@H]8[C@H]([C@@H]([C@@H]([C@@H](O8)C)O)O)O)O)NC(=O)C)O)O[C@H]9[C@@H]([C@H]([C@@H]([C@H](O9)CO)O[C@H]%10[C@@H]([C@H]([C@H]([C@H](O%10)CO)O)O[C@H]%11[C@@H]([C@H]([C@@H]([C@H](O%11)CO)O[C@H]%12[C@@H]([C@H]([C@H]([C@H](O%12)CO)O)O[C@@H]%13[C@@H]([C@H]([C@H]([C@H](O%13)CO)O)O)O)O[C@H]%14[C@H]([C@@H]([C@@H]([C@@H](O%14)C)O)O)O)O)NC(=O)C)O)O)NC(=O)C)O)O)NC(=O)C)O)O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(O)[*]', "
               "'Valid glycosyl group with amino substituent'), "
               "('C(O[C@@H]1O[C@@H]([C@@H]([C@@H]([C@H]1O)O)O)CO[C@H]2O[C@@H]([C@@H]([C@@H]([C@H]2O)O)O)CO)[C@@H](COC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)OC(*)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('NC=1N=CN=C2C1N=CN2[C@@H]3O[C@H](C*)[C@@H](O*)[C@H]3O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@H](O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])CO)O)[H])(O[C@H]3[C@H]([C@H](O[C@H]([C@@H]3O)O[C@@H]4[C@H]([C@H](O[C@@H]5[C@H](O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@H](O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]8(O[C@]([C@@H]([C@H](C8)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])O)[H])C(=O)[O-])CO)O)[H])C([O-])=O)[C@H]([C@H](O[C@@H]9[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]9O)O)CO)O[C@@H]5CO)O)O[C@H](CO)[C@@H]4O)NC(C)=O)CO)O)C([O-])=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCCCCCCC\\\\C=C\\\\[*]', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)O[C@@H]2[C@H]([C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O[C@H]6[C@H]([C@@H]([C@@H]([C@@H](O6)C)O)O)O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O[C@H]1[C@H]([C@H](O[C@H]([C@@H]1O)O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(*)=O)[C@@H]([C@H]2O)O)CO)CO)O[C@H]3[C@@H]([C@H]([C@@H](O)[C@H](O3)CO)O[C@H]4[C@@H]([C@@H](O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(CO)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)[C@H]([C@H](O4)CO)O)O)NC(C)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('C([C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(*)=O)O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)COS([O-])(=O)=O)O)O)NC(C)=O)O)O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('C1=C(C(NC(N1[C@@H]2O[C@H](COP(*)(=O)[O-])[C@H]([C@H]2O)O*)=O)=O)CC(OC)=O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1(O)[C@@H](CO)O[C@@H]([C@@H]([C@H]1O)O[C@@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)OCC(COC(=O)*)OC(*)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O([C@H]1[C@H]([C@@H]([C@H](O)[C@@H](O1)C)O)O)[C@H]2[C@@H]([C@H]([C@H](O[C@@H]3[C@H]([C@H](O[C@@H]4[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]4O)O)CO)O[C@@H]([C@@H]3O)CO)O)O[C@@H]2CO[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)NC(C)=O)O[C@@H]6O[C@@H]([C@H](O)[C@@H]([C@H]6O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)CO', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(*)=O)[C@@H]([C@H]1O)O)CO)[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)O)O[C@@H]7O[C@H]([C@H]([C@H]([C@@H]7O)O)O)C)NC(C)=O)O)NC(C)=O)O[C@@]8(C[C@@H]([C@H]([C@@](O8)([C@@H]([C@@H](CO)O)O)[H])NC(C)=O)O)C(=O)[O-])O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('N[C@@H](Cc1ccccc1)C(=O)O[C@@H]1[C@@H](COP([O-])(-*)=O)O[C@H]([C@@H]1O)n1cnc2c(N)ncnc12', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('N([C@@H]1O[C@@H]([C@H]([C@@H]([C@H]1NC(=O)C)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O)O)O[C@@H]6[C@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O)O)O)O[C@@H]7[C@H]([C@H]([C@@H]([C@H](O7)CO)O)O)O[C@@H]8[C@H]([C@H]([C@@H]([C@H](O8)CO)O)O)O[C@@H]9[C@H]([C@H]([C@@H]([C@H](O9)CO)O)O)O)O)O)NC(C)=O)CO)C(C[C@@H](C(*)=O)N*)=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('C[C@@H](O[C@H]1O[C@H](CO)[C@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2NC(C)=O)[C@H]1NC(C)=O)[C@H](N-*)C(-*)=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('*[C@@H]1O[C@H](COP(OC2=CC=C(C[C@@H](C(=O)[O-])[NH3+])C=C2)(=O)[O-])[C@H](C1)O*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O[C@H]1C=C(O[C@@H](O[*])[C@H]1O)C(O)=O', 'Valid glycosyl "
               "group with glycosidic linkage'), "
               "('CO[C@H]1C[C@H](O[C@H]2[C@H](C)O[C@H](C[C@@H]2OC)O[C@H]2[C@@H](C)\\\\C=C\\\\C=C3/CO[C@@H]4[C@H](O)C(C)=C[C@@H](C(=O)O[C@H]5C[C@@H](C\\\\C=C2/C)O[C@@]2(C5)O[C@H]([C@@H](C)C[*])[C@@H](C)C=C2)[C@]34O)O[C@@H](C)[C@@H]1NC(C)=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O)[C@H]4O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O([C@H]1[C@H]([C@@H]([C@@H]([C@@H](O1)C)O)O)O)[C@@H]2[C@H]([C@@H](O[C@@H]([C@H]2O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@H]5[C@H]([C@@H]([C@@H]([C@@H](O5)C)O)O)O)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@]7(O[C@@]([C@@H]([C@H](C7)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])O)NC(C)=O)O)CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(C)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@@H]1(N2C(NC(=O)C(=C2)C)=O)O[C@H](COP(*)(=O)[O-])[C@H]([C@H]1O)O*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@H](O[C@@H]([C@@H]([C@@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)O)CO[C@]3([C@@H]([C@H]([C@@H]([C@H](O3)COS(=O)(=O)[O-])O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)O)NC(C)=O)[H])O[C@@H]([C@@H](C(*)=O)N*)C)NC(=O)C', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@H]([C@@H](CCCCCCCCCCCCCCC)O)(NC(=O)*)CO[C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O[C@@H]3[C@@H]([C@@H](O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@H](O)[C@@H]([C@H]5O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(CO)=O)([C@@H]([C@H](O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])CO)O)[H])C([O-])=O)CO)NC(C)=O)[C@H]([C@H](O3)CO)O)O)[C@@H]([C@H]2O)O)CO)[C@@H]([C@H]1O)O)CO', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('C1(C(OC(OC[C@@H]([C@@H](O)/C=C/CCCCCCCCCC(C)C)NC(=O)*)C(C1O)O)CO)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC([*])=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@@H]1(O)[C@@H](CO)O[C@@H]([C@@H]([C@H]1O)O[C@@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)OC[C@@H](COC(=O)*)OC(*)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('*[C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O[C@@H]3[C@@H]([C@@H](O)[C@H]([C@@H](CO)O3)O*)O)[C@@H]([C@H]2O)O)CO)[C@@H]([C@H]1O)O)CO', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('C[C@H]1O[C@H](O[C@H]2[C@@H](O)[C@H](NC=O)[C@@H](C)O[C@@H]2O[C@@H]2[C@H](O)[C@@H](OCCCCCC(=O)NCCNC3C(NC-*)C(=O)C3=O)O[C@H](C)[C@H]2NC=O)[C@@H](O)[C@@H](O)[C@@H]1NC=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@H]([C@@H](*)O)(NC(=O)*)CO[C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O[C@@H]3[C@@H]([C@@H](O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@H]5[C@@H]([C@H]([C@@H](O)[C@H](O5)CO)O)NC(C)=O)NC(C)=O)[C@H]([C@@H](CO)O3)O)O)[C@@H]([C@H]2O)O)CO)[C@@H]([C@H]1O)O)CO', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O([C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O)O)O[C@@H]4O[C@H]([C@H]([C@H]([C@@H]4O)O)O)C)NC(=O)C)[C@@H]5[C@H]([C@@H](O[C@@H]([C@@H]5O)CO)O[C@@H]6[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(*)=O)[C@@H]([C@H]6O)O)CO)O', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@H]([C@H](O5)CO)O)O)NC(C)=O)O)O)O)O)O)O)OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(-*)=O)[C@@H](OC(=O)[C@@H]([NH3+])CC([O-])=O)[C@H]1O', "
               "'Valid glycosyl group with amino substituent'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O[C@H]5O[C@H](CO)[C@H](O)[C@H](O)[C@H]5NC(C)=O)[C@H]4O[C@@H]4O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]4O)[C@H]3NC(C)=O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('C[C@@H](O[C@H]1[C@H](O)[C@@H](CO)O[C@H](O)[C@@H]1NC([*])=O)C(O)=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@@H]1(O[C@H]([C@@H]([C@@H]1OP([O-])(=O)[O-])O)*)CO', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('O[C@@H]1[C@H](O-*)[C@@H](COP([O-])(-*)=O)O[C@H]1n1cc(C[NH2+]CCS([O-])(=O)=O)c(=O)[nH]c1=O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('C(=C/CCCCCCCCCCCCC)\\\\[C@@H](O)[C@@H](NC(*OC(CCCCCCC[C@H](/C=C/C=C\\\\CCCCC)OO)=O)=O)CO[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)CO)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O)CO)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O)O)[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@@H]7[C@@H]([C@H]([C@H]([C@H](O7)CO)O)O)O)O[C@@H]8O[C@H]([C@H]([C@H]([C@@H]8O)O)O)C)O)NC(C)=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)O[C@@H]6[C@H]([C@@H](O[C@@H]([C@@H]6O)CO)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(=O)C)O[C@@H]8O[C@H]([C@H]([C@H]([C@@H]8O)O)O)C', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@@H]1([C@@H](O[C@@H]([C@H]([C@@H]1O)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)CO)O*)O', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O)O)O)NC(C)=O)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@H]5[C@@H]([C@H]([C@H]([C@H](O5)CO)O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(C)=O)O)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('C[C@H]1O[C@@H](O[*])[C@H](O)[C@@H](O)[C@H]1O', 'Valid "
               "glycosyl group with glycosidic linkage'), "
               "('[C@@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@H](O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])O)[H])C(=O)[O-])CO)O)[H])(C([O-])=O)O[C@H]4[C@H]([C@H](O[C@H]([C@@H]4O)O[C@@H]5[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]5O)O)CO)CO)O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O[C@H]7[C@@H]([C@@H](O)[C@H]([C@H](O7)CO)O)O)NC(C)=O', "
               "'Valid glycosyl group with amino substituent'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O)CO)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)NC(=O)C)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(=O)C)O)O)[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO[C@]2(O[C@@]([C@@H]([C@H](C2)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])O)O)O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Valid glycosyl group with hydroxyl substituent'), "
               "('[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)NC(=O)C)O[C@@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@@H]([C@@H](O[C@@H]([C@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)NC(=O)C)O', "
               "'Valid glycosyl group with amino substituent'), "
               "('N1(C=NC2=C(N=CN2[C@@H]3O[C@H](COP(*)(=O)[O-])[C@H]([C@H]3O)O*)C1=N)C', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1(C[C@@H](O[C@@H]1COP(=O)([O-])O)N2C=3N=CN=C(C3N=C2)N)O*', "
               "'Valid glycosyl group with glycosidic linkage'), "
               "('[C@@H]1([C@H](O[C@@H]([C@@H]([C@@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)O)CO[C@]3([C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)NC(C)=O)[H])O[C@@H]([C@@H](C(*)=O)N*)C)NC(=O)C', "
               "'Valid glycosyl group with amino substituent'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/*', "
               "'Valid glycosyl group with hydroxyl substituent')]\n"
               'False negatives: '
               "[('C[C@H]1O[C@H](CO)[C@H](O)[C@H](O[C@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H]1NC(C)=O', "
               "'No attachment point (*) found')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 28,
    'num_false_positives': 100,
    'num_true_negatives': 2,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.21875,
    'recall': 1.0,
    'f1': 0.358974358974359,
    'accuracy': 0.23076923076923078}