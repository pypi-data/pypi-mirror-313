"""
Classifies: CHEBI:18133 hexose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import rdMolDescriptors

def is_hexose(smiles: str):
    """
    Determines if a molecule is a hexose (six-carbon monosaccharide).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hexose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Count total carbons and oxygens in the molecule
    total_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if total_carbons < 6:
        return False, "Insufficient carbons for a hexose"

    # Find sugar rings (5 or 6-membered rings containing oxygen)
    sugar_rings = []
    ri = mol.GetRingInfo()
    for ring in ri.AtomRings():
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        ring_elements = [atom.GetSymbol() for atom in ring_atoms]
        if ('O' in ring_elements and 
            (len(ring) == 5 or len(ring) == 6) and 
            sum(1 for elem in ring_elements if elem == 'C') >= 4):
            sugar_rings.append(ring)

    # For non-cyclic forms
    pattern_aldehyde = Chem.MolFromSmarts('[CH]=O')
    pattern_ketone = Chem.MolFromSmarts('[#6]-C(=O)-[#6]')
    has_aldehyde = len(mol.GetSubstructMatches(pattern_aldehyde)) > 0
    has_ketone = len(mol.GetSubstructMatches(pattern_ketone)) > 0

    # Helper function to count carbons in sugar chain
    def count_sugar_carbons(start_atom, visited=None):
        if visited is None:
            visited = set()
        
        if start_atom.GetIdx() in visited:
            return 0
        
        visited.add(start_atom.GetIdx())
        
        if start_atom.GetSymbol() != 'C':
            return 0
            
        count = 1
        for neighbor in start_atom.GetNeighbors():
            if (neighbor.GetSymbol() in ['C', 'O'] and 
                not neighbor.IsInRing() and 
                neighbor.GetIdx() not in visited):
                count += count_sugar_carbons(neighbor, visited)
        
        return count

    # Check linear form
    if has_aldehyde or has_ketone:
        # Find potential sugar chain starting from aldehyde/ketone group
        matches = mol.GetSubstructMatches(pattern_aldehyde if has_aldehyde else pattern_ketone)
        for match in matches:
            start_atom = mol.GetAtomWithIdx(match[0])
            sugar_carbons = count_sugar_carbons(start_atom)
            if sugar_carbons == 6:
                # Check for hydroxyl groups
                hydroxyls = sum(1 for atom in mol.GetAtoms() 
                              if atom.GetSymbol() == 'O' 
                              and len(list(atom.GetNeighbors())) == 1)
                if hydroxyls >= 4:  # Most hexoses have at least 4 OH groups
                    return True, "Aldohexose identified" if has_aldehyde else "Ketohexose identified"

    # Check cyclic form
    if sugar_rings:
        for ring in sugar_rings:
            ring_set = set(ring)
            carbons_in_ring = sum(1 for i in ring if mol.GetAtomWithIdx(i).GetSymbol() == 'C')
            
            # Count connected carbons outside ring that could be part of sugar
            extra_carbons = 0
            for ring_atom_idx in ring:
                atom = mol.GetAtomWithIdx(ring_atom_idx)
                for neighbor in atom.GetNeighbors():
                    if (neighbor.GetSymbol() == 'C' and 
                        neighbor.GetIdx() not in ring_set and 
                        not neighbor.IsInRing()):
                        extra_carbons += 1

            if carbons_in_ring + extra_carbons == 6:
                # Check for hydroxyl groups
                hydroxyls = sum(1 for atom in mol.GetAtoms() 
                              if atom.GetSymbol() == 'O' 
                              and len(list(atom.GetNeighbors())) == 1)
                if hydroxyls >= 3:  # Cyclic forms typically have at least 3 OH groups
                    return True, "Cyclic hexose form identified"

    return False, "Not a hexose structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18133',
                          'name': 'hexose',
                          'definition': 'Any six-carbon monosaccharide which '
                                        'in its linear form contains either an '
                                        'aldehyde group at position 1 '
                                        '(aldohexose) or a ketone group at '
                                        'position 2 (ketohexose).',
                          'parents': ['CHEBI:35381']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.2533333333333333 is too low.\n'
               "True positives: [('OC[C@H]1OC(O)[C@H](O)C(=O)[C@@H]1O', "
               "'Ketohexose identified'), "
               "('O=C(O[C@@H]1O[C@H]([C@H](O)[C@H]([C@H]1O)O)C)C2=C(N)C=CC=C2', "
               "'Cyclic hexose form identified'), "
               "('OC[C@]1(O)OC[C@H](O)[C@@H](O)[C@@H]1O', 'Cyclic hexose form "
               "identified'), ('C[C@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O', "
               "'Cyclic hexose form identified'), "
               "('OC[C@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@@H]1O', 'Cyclic hexose "
               "form identified'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O)C', 'Cyclic "
               "hexose form identified'), "
               "('O=C(O[C@@H]1O[C@H]([C@@H](O)[C@H]([C@H]1O)O)C)CC2=CC=CC=C2', "
               "'Cyclic hexose form identified'), "
               "('OC[C@@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O', 'Cyclic "
               "hexose form identified'), ('O1[C@@H]([C@@H](O)[C@H](O)CC1O)C', "
               "'Cyclic hexose form identified'), "
               "('OC[C@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O', 'Cyclic hexose "
               "form identified'), "
               "('OC[C@@H]1O[C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O', 'Cyclic "
               "hexose form identified'), "
               "('OC[C@@]1(O)OC[C@@H](O)[C@H](O)[C@H]1O', 'Cyclic hexose form "
               "identified'), ('C[C@H]1OC(O)[C@@H](O)[C@@H](O)[C@@H]1O', "
               "'Cyclic hexose form identified'), "
               "('O1[C@H]([C@H](O)[C@H](O)[C@@H](O)[C@@H]1O)CO', 'Cyclic "
               "hexose form identified'), "
               "('C[C@@H]1O[C@@H](O)[C@@H](O)C[C@@H]1O', 'Cyclic hexose form "
               "identified'), ('OC[C@H]1OC(O)C(=O)[C@@H](O)[C@H]1O', "
               "'Ketohexose identified'), "
               "('OC[C@@]1(O)OC[C@@H](O)[C@H](O)[C@@H]1O', 'Cyclic hexose form "
               "identified'), ('OC[C@@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@H]1O', "
               "'Cyclic hexose form identified'), "
               "('O=C(O[C@@H]1O[C@H]([C@H](O)[C@H]([C@H]1O)O)C)C2=CC=C(O)C=C2', "
               "'Cyclic hexose form identified')]\n"
               'False positives: '
               "[('O1[C@@H]([C@@H](OC2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@H](O)[C@@H](O)[C@H]1O[C@H]3[C@H](O)[C@@H](O)C(O[C@@H]3CO)O)CO', "
               "'Cyclic hexose form identified'), "
               "('CC(C)OC1=C(C=C(C(=C1)NC(=O)CS(=O)CC(=O)NC2=CC=CC(=C2)C(F)(F)F)Cl)Cl', "
               "'Cyclic hexose form identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCC)(O)=O', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@@H]1O)CO)OC)[C@@H]2O[C@H]([C@H]([C@H](O)[C@H]2O)C)C(O)=O', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@@H](O)[C@H](OC(O)[C@@H]2NC(=O)C)CO[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)CO)[C@H](O)[C@H]3NC(=O)C)CO)O[C@@H]([C@@H]1O)CO)[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('[C@H]1([C@@H]([C@@H]([C@H]([C@@H]([C@H]1O)OP(=O)([O-])[O-])O)O)OP(=O)([O-])[O-])O', "
               "'Cyclic hexose form identified'), "
               "('C1COCCC1C(=O)NC2=CC3=C(C=C2)O[C@H]4[C@@H]3C[C@H](O[C@@H]4CO)CC(=O)NCC5=CN=CC=C5', "
               "'Cyclic hexose form identified'), "
               "('CC(\\\\C=C\\\\C=C(/C)C(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=C/C=C/C=C(C)/C=C/C=C(\\\\C)C(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O', "
               "'Cyclic hexose form identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Cyclic hexose form identified'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@H]1O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO)O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('O1C(OC(CC=2C=3OC(=O)C=CC3C=CC2OC)C(CO)=C)C(O)C(O)C(O)C1C(O)=O', "
               "'Cyclic hexose form identified'), "
               "('S(OC[C@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O[C@@H]3[C@@H](NC(=O)C)[C@H](O[C@@H]([C@@H]3O)CO)O)O[C@@H]([C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O)(O)(=O)=O', "
               "'Cyclic hexose form identified'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O)[C@H]4O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCC\\\\C=C/CCCCCCCC', "
               "'Cyclic hexose form identified'), "
               "('C1=CC=C2C(=C1)N(C(=O)S2)CC(=O)NCC3=CC=CO3', 'Cyclic hexose "
               "form identified'), ('OC(=O)C1=CCCN(C1)N=O', 'Cyclic hexose "
               "form identified'), "
               "('O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO', "
               "'Cyclic hexose form identified'), "
               "('C1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)COP(=O)(O)O)O)O)O)O)O[C@@H]6[C@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O[C@@H]7[C@H]([C@H]([C@@H]([C@H](O7)CO)O)O)O)O)O)O[C@@H]8[C@H]([C@H]([C@@H]([C@H](O8)CO)O)O)O[C@@H]9[C@H]([C@H]([C@@H]([C@H](O9)COP(=O)(O)O)O)O)O)O)O)NC(C)=O)O)NC(C)=O)O', "
               "'Cyclic hexose form identified'), "
               "('O1[C@@H]([C@@H](OC2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](OC4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)[C@@H]3O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@H](O)[C@@H]1O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O)CO)[C@@H]8O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O)CO', "
               "'Cyclic hexose form identified'), "
               "('[H][C@@]1(O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O)[C@H](O)COP(O)(O)=O', "
               "'Cyclic hexose form identified'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Cyclic hexose form identified'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O[C@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCC)COC(=O)CCCCCCCCCCCCCCCC)([O-])=O.[NH4+]', "
               "'Cyclic hexose form identified'), "
               "('O1[C@@H](O[C@H]2[C@H](O)[C@H](O)[C@H](O[C@@H]2CO)O[C@@H]3[C@H](O)[C@@H](O[C@@H]([C@H]3O)CO[C@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)[C@H](O)[C@@H]4O)CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO)O)[C@H](NC(=O)C)[C@@H](O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)[C@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H]1CO', "
               "'Cyclic hexose form identified'), "
               "('C1CCC(C1)C(=O)N2[C@@H]3CN(C4=CC=CC=C4[C@@H]3[C@@H]2CO)C(=O)C5=CC=CC=C5F', "
               "'Cyclic hexose form identified'), "
               "('O1C(C(O)C(O)C(O)C1OC=2C=C3OC(=C(OC4OC(C(O)C(O)C4O)C(O)=O)C(=O)C3=C(O)C2O)C5=CC(O)=C(O)C=C5)CO', "
               "'Cyclic hexose form identified'), "
               "('C=1C=CC(=C(C1)NC(CC([O-])=O)=O)O', 'Cyclic hexose form "
               "identified'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)CO)[C@@H](NC(=O)C)CO)[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5NC(=O)C)CO)[C@H]4O)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](O)[C@@H](O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O)[C@H]3NC(=O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('C[C@@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]3[C@@H](O)[C@@H](O)CO[C@H]3O[C@H]3CC[C@@]4(C)[C@@H](CC[C@]5(C)[C@@H]4CC=C4[C@@H]6CC(C)(C)CC[C@@]6(CC[C@@]54C)C(O)=O)[C@]3(C)CO)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@H](O)[C@H]1O', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]1CO)O)[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('O1C(C(O)C(O)C(O)C1OC2=CC=C(CC(O)CO)C=C2)CO', 'Cyclic hexose "
               "form identified'), "
               "('O([C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@H]1NC(=O)C)CO)[C@@H]4[C@@H](O[C@@H]5[C@H](O)[C@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)O[C@@H]([C@H]5O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O)CO)O[C@@H]([C@@H](O)[C@@H]4O)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@@H]5O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO)[C@H]%14O[C@@H]([C@@H](O)[C@H](O)[C@@H]%14O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@@H]%17O[C@@H]([C@@H](O[C@@H]%18O[C@@H]([C@H](O)[C@H](O)[C@H]%18O)CO)[C@H](O)[C@H]%17NC(=O)C)CO)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO[C@@H]%19O[C@@H]([C@@H](O[C@@H]%20O[C@@H]([C@H](O)[C@H](O[C@@H]%21O[C@@H]([C@@H](O[C@@H]%22O[C@@H]([C@H](O)[C@H](O)[C@H]%22O)CO)[C@H](O)[C@H]%21NC(=O)C)CO)[C@H]%20O)CO)[C@H](O)[C@H]%19NC(=O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5NC(=O)C)CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]8NC(=O)C)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('[NH3+]CCCC(=O)C1=CN=C(O)C=C1', 'Ketohexose identified'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)C(O)=O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)OS(=O)(=O)O)O[C@H]5[C@H]([C@@H]([C@H]([C@H](O5)C(O)=O)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)NC(C)=O)O)OS(=O)(=O)O)NC(C)=O)O)O)O)O)O[C@H]7[C@@H]([C@H]([C@@H](OC7)*)O)O', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@@H]1O)CO[C@]2(O[C@H]([C@H](NC(=O)C)[C@@H](O)C2)[C@H](O)[C@H](O[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)O[C@@H]4[C@H](O)[C@@H](O)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](O)[C@@H](O[C@@H]5CO)O)[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)[C@H]6O)CO', "
               "'Cyclic hexose form identified'), "
               "('C[C@H](CCCCCCC(=O)CC(O)=O)O[C@@H]1O[C@@H](C)[C@H](O)C[C@H]1O', "
               "'Ketohexose identified'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C=C3OC(=C(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)C(=O)C3=C(O)C2)C5=CC(O)=C(O)C=C5)CO[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@@H](O)[C@H](OC(O)[C@@H]2NC(=O)C)CO[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)O[C@@H]([C@@H]1O)CO)[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('C1=CC=C(C(=C1)NC(=O)C2=C(N=CN2)C(=O)NC3=CC=C(C=C3)F)[N+](=O)[O-]', "
               "'Cyclic hexose form identified'), "
               "('[H]C(=O)N[C@@H]1[C@@H](C)O[C@@H](O[C@@H]2[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@@H]3[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@H]4[C@H](O)[C@@H](C)O[C@@H](O[C@@H]5[C@@H](O)[C@H](NC([H])=O)[C@@H](C)O[C@H]5O[C@@H]5[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@@H]6[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@H]7[C@H](O)[C@@H](C)O[C@@H](O[C@@H]8[C@@H](O)[C@H](NC([H])=O)[C@@H](C)O[C@H]8O[C@@H]8[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@@H]9[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@H]%10[C@H](O)[C@@H](C)O[C@@H](O[C@@H]%11[C@@H](CO)O[C@@H](O[C@H]%12[C@H](O)[C@H](O[C@@H]%13O[C@H](CO)[C@@H](O)[C@H](O)[C@H]%13O)[C@H](O[C@@H]%12CO)O[C@@H]%12[C@H](O)C[C@@](O)(O[C@]%12([H])[C@H](O)CO)C(O)=O)[C@@H](O[C@H]%12O[C@H](CO)[C@H](O)[C@H](O)[C@H]%12N)[C@H]%11O[C@H]%11O[C@H](CO)[C@@H](O)[C@H](O)[C@H]%11O)[C@@H]%10NC(C)=O)O[C@@H]9C(N)=O)O[C@@H]8C(N)=O)[C@@H]7NC(C)=O)O[C@@H]6C(N)=O)O[C@@H]5C(N)=O)[C@@H]4NC(C)=O)O[C@@H]3C(N)=O)O[C@@H]2C(N)=O)[C@H](O)[C@H]1O', "
               "'Aldohexose identified'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@@H](NC(=O)C)CO)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO', "
               "'Cyclic hexose form identified'), "
               "('COC1=CC=C(C=C1)S(=O)(=O)N2C[C@H](COC[C@@H]3[C@@H]2CC[C@@H](O3)CC(=O)N[C@@H]4CCN(C4)CC5=CC=CC=C5)O', "
               "'Cyclic hexose form identified'), "
               "('O1[C@@H]([C@@H](O)C(O)C(O)[C@@H]1OC2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC(O)=C(O)C=C4)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O)[C@H]5O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO)CO)[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@@H](O)[C@@H](O[C@@H]([C@@H]1O)CO)O[C@H]2[C@H](O)[C@@H](O)C(O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3NC(=O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('[H][C@]1(O[C@@H]2O[C@@H](C)[C@@H](NO[C@H]3C[C@H](O)[C@H](SC(=O)c4c(C)c(I)c(O[C@@H]5O[C@@H](C)[C@H](O)[C@@H](OC)[C@H]5O)c(OC)c4OC)[C@@H](C)O3)[C@H](O)[C@H]2O[C@H]2C[C@H](OC)[C@H](CO2)NCC)C#C\\\\C=C/C#C[C@]2(O)CC(=O)C(NC(=O)OC)=C1/C2=C\\\\CSSSC', "
               "'Ketohexose identified'), "
               "('O([C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@H]1NC(=O)C)CO)[C@H]4[C@@H](O)[C@H](O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)[C@@H](NC(=O)C)CO)[C@@H]4O)CO[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H](O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)[C@H]7NC(=O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('O1[C@@H]([C@@H](O)C(O)C(O)[C@@H]1OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCC)[C@H](O)/C=C/CCCCCCCCCC)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)CO)[C@@H]3O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO)[C@@H]6O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('Nc1ccc(O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]2O)cc1', "
               "'Cyclic hexose form identified'), "
               "('O[C@H]1[C@H]([C@H](O[C@H]([C@@H]1O)O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](*)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)CO)O[C@H]3[C@@H]([C@H]([C@@H](O)[C@H](O3)CO)O[C@@H]4O[C@@H]([C@@H]([C@@H]([C@H]4O)O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O)NC(C)=O)CO)NC(C)=O', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](NC(=O)C)CO)[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5NC(=O)C)CO)[C@H]4O)CO', "
               "'Cyclic hexose form identified'), "
               "('C1=CC=C(C=C1)NC(=O)NNC(=O)C2=CC(=NC3=CC=CC=C32)C4=C(C=C(C=C4)Cl)Cl', "
               "'Cyclic hexose form identified'), "
               "('O[C@@H]1[C@@H](COC(=O)CC(O)=O)O[C@@H](Oc2cc(O)cc3[o+]c(c(O[C@@H]4O[C@H](COC(=O)\\\\C=C\\\\c5ccc(O)cc5)[C@@H](O)[C@H](O)[C@H]4O)cc23)-c2cc(O)c(O)c(O)c2)[C@H](O)[C@H]1O', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1O[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)CO)C[C@H]2O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@@H](O)[C@@H](O)[C@@H]2O', "
               "'Cyclic hexose form identified'), "
               "('[H][C@@](O)(C[C@H]1O[C@@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2NC(C)=O)[C@H](NC(=O)\\\\C=C\\\\CCCCCCCCCCCC(C)C)[C@@H](O)[C@H]1O)[C@@]1([H])O[C@H]([C@H](O)[C@@H]1O)n1ccc(=O)[nH]c1=O', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@@H](O)[C@H](O[C@H](O)[C@@H]3NC(=O)C)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)O[C@@H]([C@@H]1O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H]7O)CO[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC2=C3OC=CC3=C4OC(=C(OC)C(=O)C4=C2)C5=CC=CC=C5)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)[C@@H]3O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO)CO)[C@@H]5O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O)CO', "
               "'Cyclic hexose form identified'), "
               "('C1CCC(CC1)NC(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)C5=CN=CC=C5', "
               "'Cyclic hexose form identified'), "
               "('OC[C@@H](O)[C@@H](O)[C@H](O)[C@H](O)COC1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O', "
               "'Cyclic hexose form identified'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C(=C(C=CC2)C)C(=O)C)CO', "
               "'Ketohexose identified'), "
               "('COC1=CC=C(C=C1)NC(=O)N[C@H]2CC[C@H](O[C@H]2CO)CCNC(=O)NC3=C(C=CC(=C3)F)F', "
               "'Cyclic hexose form identified'), "
               "('O1[C@H](OC2=C(OC)C(OC)=NC(=C2C)C/C=C(/C/C=C/C(=C/[C@H]([C@@H](O[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@H]3O)O)CO)/C(=C/C)/C)C)/C)\\\\C)[C@H](O)[C@@H](O)[C@@H]([C@H]1CO)O', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)[C@@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)[C@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)[C@H](O)[C@@H]%14O[C@@H]%17O[C@@H]([C@@H](O[C@@H]%18O[C@@H]([C@H](O)[C@H](O)[C@H]%18O)CO)[C@H](O)[C@H]%17NC(=O)C)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)CO)O[C@@H]3[C@@H](O)[C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]4CO)O)[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O', "
               "'Cyclic hexose form identified'), "
               "('O1C(C(O)C(O)C(O)C1OC(=O)/C=C/C2=CC(OC)=C(O)C(OC)=C2)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@@H](O)[C@H](O)[C@H](O[C@@H]1O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@H]2O)CO)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)CO)[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@@H]3CO)O', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)[C@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@@H](O)[C@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO)[C@H]%11NC(=O)C)CO)[C@H](O)[C@@H]%10O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@@H]2[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@@H]2O)CO)O)[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)CO', "
               "'Cyclic hexose form identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Cyclic hexose form identified'), "
               "('S(O[C@H]1[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)OC(=C(O)[C@@H]1O)C(O)=O)(O)(=O)=O', "
               "'Cyclic hexose form identified'), "
               "('O1[C@@H]([C@@H](O[C@@H]2OC(=C(O)[C@H](O)[C@H]2O)C(O)=O)[C@H](O)[C@@H](NS(O)(=O)=O)C1O)COS(O)(=O)=O', "
               "'Cyclic hexose form identified'), "
               "('N[C@@H]1[C@@H](O)[C@@H](O)O[C@H](CO)[C@H]1O', 'Cyclic hexose "
               "form identified'), "
               "('O([C@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)OC[C@H]2OC(O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO', "
               "'Cyclic hexose form identified'), "
               "('[C@H]1([C@H]([C@@H]([C@H]([C@@H]([C@@H]1O)OP(OC[C@H](COC(CCCCCCC)=O)OC(CCCCCCC)=O)(=O)O)O)OP(=O)(O)O)OP(O)(=O)O)O', "
               "'Cyclic hexose form identified'), ('Oc1ccccc1Oc1cccc(O)c1O', "
               "'Cyclic hexose form identified'), "
               "('CC(CCOP(O)(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(/C)CC\\\\C=C(/C)CCC=C(C)C', "
               "'Cyclic hexose form identified'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'Ketohexose identified'), "
               "('O1[C@@H]([C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](O)[C@@H]1O[C@@H]([C@@H](O)[C@H](O)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)[C@@H](NC(=O)C)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCC(=O)CC([O-])=O)[C@H](O)C[C@H]1O', "
               "'Ketohexose identified'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)OC(=O)C)[H])C([O-])=O)CO)O)[H])C([O-])=O', "
               "'Cyclic hexose form identified'), "
               "('O1C(C(O)C(O)C(O)C1OC=2C=C3[O+]=C(C(O)=CC3=C(O)C2)C4=CC(O)=C(O)C=C4)C(O)=O', "
               "'Cyclic hexose form identified'), "
               "('O(C1C(O)C(O)C(OC1OC=2C=C3C(OC4OC(C(O)C(O)C4O)CO)=CC(O)=CC3=[O+]C2C5=CC=C(O)C=C5)CO)C6OC(C(O)C(O)C6O)CO', "
               "'Cyclic hexose form identified'), "
               "('N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO[C@@H]2O[C@H](CO)[C@@H](OP(O)(O)=O)[C@H](O)[C@H]2N)O[C@@H]1OP(O)(O)=O', "
               "'Cyclic hexose form identified'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@@H]1O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H](O[C@@H]%12O[C@H]([C@@H](O)[C@@H](O)[C@@H]%12O)C)[C@H]%10NC(=O)C)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@H]1O)CO[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)[C@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@@H]8O)CO', "
               "'Cyclic hexose form identified'), "
               "('O([C@H]1[C@@H](O)[C@H](O)[C@H](O[C@@H]1OC[C@H]2O[C@H](OC[C@@H]3O[C@@H]([C@@H](O)[C@@H]3O)CO)[C@@H](O)[C@@H](O)[C@@H]2O)CO)[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('C[C@H](CN([C@@H](C)CO)S(=O)(=O)C1=CC=C(C=C1)F)[C@@H](CN(C)C(=O)C2=CC3=C(C=C2)OCO3)OC', "
               "'Cyclic hexose form identified'), "
               "('C[C@@H]1O[C@@H](OCCC([O-])=O)[C@H](O)C[C@H]1O', 'Cyclic "
               "hexose form identified'), "
               "('O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7NC(=O)C)CO)[C@H](O)[C@@H]6O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)CO', "
               "'Cyclic hexose form identified'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C3=C(O[C@@H](CC3=O)C4=CC=CC=C4)C(OC)=C(OC)C2)CO', "
               "'Ketohexose identified'), "
               "('C1CCC(C1)(C2=CN(N=N2)CC[C@@H]3CC[C@H]([C@@H](O3)CO)NC(=O)NC4=CC=C(C=C4)Cl)O', "
               "'Cyclic hexose form identified'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Cyclic hexose form identified'), "
               "('COC1=CC=C(C=C1)NC(=O)N[C@@H]2CC[C@H](O[C@H]2CO)CCN3C=C(N=N3)C4=CC=CC=N4', "
               "'Cyclic hexose form identified'), "
               "('O([C@@H]1[C@@H](O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O[C@@H]([C@@H]1O)CO)O)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO', "
               "'Cyclic hexose form identified')]\n"
               'False negatives: '
               "[('O1[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C', 'No sugar "
               "ring found'), ('OC[C@@H](O)[C@H](O)[C@H](O)[C@H](O)C=O', 'No "
               "sugar ring found'), "
               "('[H][C@@]1(O[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO', 'No sugar "
               "ring found'), "
               "('O1[C@@H]([C@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO', 'No sugar "
               "ring found'), ('O1[C@@H]([C@@H](O)[C@H](O)C1O)[C@@H](O)CO', "
               "'No sugar ring found'), "
               "('O1[C@@H]([C@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO', 'No sugar "
               "ring found'), "
               "('O1[C@H]([C@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO', 'No sugar "
               "ring found'), ('C([C@H](C([C@@H]([C@H](CO)O)O)=O)O)O', 'No "
               "sugar ring found'), "
               "('O([C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)C/C=C(/CC[C@@]1(C(=CCC[C@H]1C)C)C)\\\\C', "
               "'Found 10 carbons, hexose must have exactly 6'), "
               "('C=1C=C(C=CC1OC2C(C(C(C(O2)C(O)O)C)C)C)CC3CCC(O3)=O', 'Found "
               "7 carbons, hexose must have exactly 6'), "
               "('O1[C@@H]([C@H](O)[C@@H](O)[C@H]1O)[C@H](O)CO', 'No sugar "
               "ring found'), ('C[C@@H](O)[C@H]1O[C@H](O)[C@@H](O)[C@H]1O', "
               "'No sugar ring found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 21,
    'num_false_positives': 100,
    'num_true_negatives': 390,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.17355371900826447,
    'recall': 0.6774193548387096,
    'f1': 0.2763157894736842,
    'accuracy': 0.7888675623800384}