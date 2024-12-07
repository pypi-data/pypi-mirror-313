"""
Classifies: CHEBI:24978 ketose
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ketose(smiles: str):
    """
    Determines if a molecule is a ketose sugar.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a ketose, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for required elements (C, H, O only)
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    allowed = {'C', 'H', 'O'}
    if not set(atoms).issubset(allowed):
        return False, "Contains elements other than C,H,O"
        
    # Count carbons and oxygens
    num_carbons = len([a for a in mol.GetAtoms() if a.GetSymbol() == 'C'])
    num_oxygens = len([a for a in mol.GetAtoms() if a.GetSymbol() == 'O'])
    
    if num_carbons < 3:
        return False, "Too few carbons for a ketose"
        
    if num_oxygens < 3:
        return False, "Too few oxygens for a ketose"

    # Check for hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts('[OH1]')
    hydroxyls = len(mol.GetSubstructMatches(hydroxyl_pattern))
    
    if hydroxyls < 2:
        return False, "Insufficient hydroxyl groups for a ketose"

    # Pattern for cyclic hemiketal ketose
    cyclic_ketose = Chem.MolFromSmarts('[C;R]1-[O;R]-[C;R]([O;H1,OH1])([CH2]O)-[C;R]-[C;R]-[C;R]1')
    furanose = Chem.MolFromSmarts('[C;R]1-[O;R]-[C;R]([O;H1,OH1])([CH2]O)-[C;R]-[C;R]1')
    
    # Pattern for open-chain ketose
    open_chain = Chem.MolFromSmarts('[CH2]([OH1])-[CH1](-[OH1])-[CH1](-[OH1])-C(=O)-[CH2]([OH1])')
    
    if mol.HasSubstructMatch(cyclic_ketose):
        return True, "Pyranose form of ketose"
    elif mol.HasSubstructMatch(furanose):
        return True, "Furanose form of ketose"
    
    # Check if it's a ring sugar with appropriate substituents
    rings = mol.GetRingInfo()
    if rings.NumRings() > 0:
        for ring in rings.AtomRings():
            if len(ring) in [5, 6]:  # furanose or pyranose
                ring_atoms = set(ring)
                # Count oxygen atoms in ring
                ring_oxygens = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetSymbol() == 'O')
                if ring_oxygens == 1:  # One oxygen in the ring
                    # Check for hydroxyl and CH2OH substituents
                    hydroxyl_count = 0
                    ch2oh_count = 0
                    for atom_idx in ring:
                        atom = mol.GetAtomWithIdx(atom_idx)
                        if atom.GetSymbol() == 'C':
                            for neighbor in atom.GetNeighbors():
                                if neighbor.GetSymbol() == 'O' and neighbor.GetIdx() not in ring_atoms:
                                    if neighbor.GetTotalNumHs() == 1:
                                        hydroxyl_count += 1
                                    elif len([a for a in neighbor.GetNeighbors() if a.GetSymbol() == 'C']) == 1:
                                        ch2oh_count += 1
                    
                    if hydroxyl_count >= 2 and ch2oh_count >= 1:
                        return True, f"{'Furanose' if len(ring) == 5 else 'Pyranose'} form of ketose"

    # Check for open chain form
    ketone_pattern = Chem.MolFromSmarts('C-C(=O)-C')
    if mol.HasSubstructMatch(ketone_pattern):
        # Verify it has hydroxyl groups and CH2OH group
        ch2oh_pattern = Chem.MolFromSmarts('[CH2][OH1]')
        if mol.HasSubstructMatch(ch2oh_pattern) and hydroxyls >= 3:
            return True, "Open-chain ketose"

    return False, "Structure does not match ketose patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24978',
                          'name': 'ketose',
                          'definition': 'Ketonic parent sugars (polyhydroxy '
                                        'ketones H[CH(OH)]nC(=O)[CH(OH)]mH) '
                                        'and their intramolecular hemiketals.',
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
               'Attempt failed: F1 score of 0.037037037037037035 is too low.\n'
               "True positives: [('[H]C(=O)C(=O)C[C@H](O)[C@H](O)CO', "
               "'Open-chain ketose'), ('C(O)C(=O)[C@@H](O)[C@H](O)CO', "
               "'Open-chain ketose')]\n"
               'False positives: '
               "[('O=C1C2=C([C@H](O)[C@@H](CCC)OC2)[C@H](O)[C@@H]3[C@H]1O3', "
               "'Open-chain ketose'), "
               "('O[C@H]1[C@@H]([C@@H](CCCCCCCCC(O)=O)C(=O)C1)/C=C/[C@@H](O)CCCCC', "
               "'Open-chain ketose'), "
               "('O=C1C=C2[C@@]3(C(C(C(=O)CC3)(C)C)C[C@H]4[C@@]2(O4)[C@]5([C@]1(C(=C[C@H]5O)C(O)(CC(=O)CC(C(=O)O)C)C)C)C)C', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(O[C@@]3(C[C@@H](O[C@@H]3C2)C=C(CCCC(C(=O)O)C)C)C)CC[C@H]1O', "
               "'Open-chain ketose'), ('OC(=O)CC(=O)\\\\C=C\\\\C(O)=O', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(O)C=3C(=CC(OC)=C(C3C)C(=O)OC)C=C2C(=O)[C@]4([C@]1(O)C(OC)=CC(=O)[C@@H]4OC)O', "
               "'Open-chain ketose'), "
               "('O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3(C1)C)/C(=C/C(=O)C(O)C(C(=O)O)C)/C)C)[C@@H](O)CC4[C@@]2(CC[C@@H](C4(C)C)O)C', "
               "'Open-chain ketose'), "
               "('O=C1C2[C@@](O)([C@]3(CC[C@@H](CC3C1)O)C)CC[C@]4([C@@]2(O)CC[C@H]4C(/C=C/[C@@H](C(C)C)C)C)C', "
               "'Open-chain ketose'), "
               "('O=C1[C@]2([C@](OCC1)(C=C[C@@]3([C@@H]2[C@@H](O)C[C@@H](C3)C)O)C)C', "
               "'Open-chain ketose'), "
               "('OC1(C(C(C(CCCC(CO)C)C)=CC1)CC2=C(O)C(O)CCC2=O)C', "
               "'Open-chain ketose'), "
               "('O=C1C2=C([C@]3(CCC(C([C@@H]3C1)(C)C)=O)C)[C@H](O)C[C@]4([C@]2(CC[C@@H]4[C@@H](CCC(O)C(O)(CO)C)C)C)C', "
               "'Open-chain ketose'), "
               "('C=1(C=C(C(=C(C1C)O)C=O)CC(/C=C/C(=C/[C@H](CC)C)/C)=O)O', "
               "'Open-chain ketose'), "
               "('O=C1C=C[C@H](C)[C@]23[C@]1(C[C@H](O)[C@H]2[C@@H]4[C@](CC[C@@]4(C3)C)(CO)C)C', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(O)C3=C(O)C=C(C)C=C3[C@@H]([C@]24C=C[C@H]1C5=C6O[C@@](C(=O)OC)([C@H]7OC(=O)CC7)CC(C6=C(O)C=C5C4)=O)O', "
               "'Open-chain ketose'), "
               "('O[C@H]1C([C@@]2([C@@](CC1=O)(C=3C(=CC2)[C@H](O)[C@@](C(=O)C3)(C)C=C)C)[H])(C)C', "
               "'Open-chain ketose'), "
               "('O=C1C(=C(O)[C@]2([C@H]3C(=C(O)C(=C([C@]3(O[C@]2([C@]1(O)C)O)C)O)C)C(=O)CC/C=C/C)C)C(=O)CC/C=C/C', "
               "'Open-chain ketose'), "
               "('O=C1C([C@H]2[C@](C=3C([C@]4([C@]([C@@H]([C@H](C(=O)O)CCC(=C)C(C)C)[C@@H](C4)O)(C)CC3)C)=C[C@@H]2O)(C)CC1)(C)C', "
               "'Open-chain ketose'), "
               "('O=C1C(C2=CC(OC)=CC(=C2)O)=C(C)C[C@H]1O', 'Open-chain "
               "ketose'), "
               "('O=C1[C@]2([C@@](O)([C@H](C)[C@H]([C@H]1O)O)[C@@H](O)[C@H]3[C@@H]2CC3(C)C)C', "
               "'Open-chain ketose'), "
               "('O=C1[C@@](O)(C2C(C(=O)CCC=CC)=C([C@]1(C(C(=O)CCC=CC)[C@H]2[C@@]3(OC(=O)C(=C3O)C)C)C)O)C', "
               "'Open-chain ketose'), "
               "('O=C1[C@@H](O)C2=C(O)C=C3C=4C=CC(=C5C4C(C3=C2[C@@H]6[C@H]1O6)=CC=C5O)O', "
               "'Open-chain ketose'), "
               "('O=C1[C@H]([C@@]2([C@H]([C@](C(=O)O)([C@@H](O)CC2)C)CC1)C)C[C@H](OC(=O)C)[C@@]3(C(=O)CC[C@H]3[C@@H](CCC(=C)C(C)C)C)C', "
               "'Open-chain ketose'), "
               "('CC1(C)CC[C@@H]2C(=O)C[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O[C@@H]7O[C@H](CO)[C@H](O)[C@H](O)[C@H]7O[C@@H]7O[C@H](CO)[C@@H](O)[C@H](O)[C@H]7O)[C@H]6O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O)[C@H]6O)C(O)=O)C(C)(C)[C@@H]5CC[C@@]34C)[C@]2(O)C1', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(O)C(=CC=C2C(=O)C3=C1C=C(OC)C4=C3C(=O)C[C@@](O)(C)C4)[C@@H]5O[C@@H]([C@H]6O[C@@H]7O[C@@H](C)C(C[C@@H]7O[C@@H]6C5)=O)C', "
               "'Open-chain ketose'), "
               "('O=C1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H]([C@@H](O)C/C=C(/CO)\\\\C)C)CC4)(C)CC3)C)CC2)(C)CC1)(C)C', "
               "'Open-chain ketose'), "
               "('CC(C)[C@@H]1C[C@@H](OC(C)=O)[C@H]2[C@@]1(CO)CC[C@@]1(C)[C@@H]3[C@@H](O)C[C@H]4C(C)(C)C(=O)CC[C@]4(C)C3=CC[C@]21C', "
               "'Open-chain ketose'), "
               "('[H][C@@]12[C@H](O)C(C)=C[C@@]3([H])[C@]4([H])C(C)(C)[C@]4(OC(=O)C(C)C)[C@H](OC(=O)c4ccccc4)[C@@H](C)[C@]3(O)[C@]1([H])C=C(C)C2=O', "
               "'Open-chain ketose'), "
               "('C[C@@]12C[C@H](OC(=O)[C@@H]1CC[C@]1(CO[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@H]2CC=CC1=O)c1ccoc1', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(OC([C@H]1O)(C)C)[C@H](O)[C@]3(O)C[C@@H](O[C@H]3C2)C(O)(C)C', "
               "'Open-chain ketose'), "
               "('C=1[C@]2([C@]3([C@@]([C@H](OC(=O)CCCCCCCCCCCCC)[C@H]([C@@]2([C@]4([C@@](C(=O)C(=C4)C)(CC1CO)O)[H])O)C)(C3(C)C)OC(=O)C)[H])[H]', "
               "'Open-chain ketose'), "
               "('C(\\\\[C@H](CCCC([O-])=O)O)=C\\\\C=C\\\\C=C\\\\[C@@H](C\\\\C=C/C=C/C(CC)=O)O', "
               "'Open-chain ketose'), "
               "('C[C@H](CCCCC(=O)CC(O)=O)O[C@@H]1O[C@@H](C)[C@H](O)C[C@H]1O', "
               "'Open-chain ketose'), "
               "('O=C1C[C@@](C2=CC=C(C(=O)OCC[C@@](O)(CC(=O)O)C)CC2)(C)C(C1)(C)C', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(OC3=C1C4=C(OC[C@@H]([C@H]4O)C(=C)C)C(=C3)C)C(=CC=C2O)CC(=O)C(C)C', "
               "'Open-chain ketose'), "
               "('O[C@@H]1C[C@H](O)[C@H](C\\\\C=C/CCCC(O)=O)[C@H]1CCC(=O)CCCCC(O)=O', "
               "'Open-chain ketose'), "
               "('O=C1C([C@H]2[C@](C=3C([C@]4([C@]([C@@H]([C@@H](CC[C@H](OC(=O)/C(=C\\\\C(=O)C5=C(O)C=CC(=C5)O)/CCC=C(CCC=C(CO)C)C)C(O)(CO)C)C)CC4)(C)CC3)C)=CC2)(C)CC1)(C)C', "
               "'Open-chain ketose'), ('O=C(C(O)C)CCC(C(=C)CCC(O)CO)(C)C', "
               "'Open-chain ketose'), "
               "('O[C@@H]1[C@@H]([C@H](C(C1)=C)/C=C/C(=O)CCCCC)C/C=C\\\\CCCC(O)=O', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(O)C3=C(O)C(=C(O[C@@H]4O[C@@H]([C@H](O)[C@@H](C4)O[C@H]5O[C@H]([C@@H](OC)[C@@H](C5)O)C)C)C=C3C=C2C[C@H]([C@@H]1O[C@@H]6O[C@@H]([C@@H](O)[C@@H](C6)O[C@@H]7O[C@@H]([C@H](O)[C@@H](C7)O[C@@H]8O[C@H]([C@H](O)[C@](C8)(O)C)C)C)C)[C@H](OC)C(=O)[C@H](O)[C@H](O)C)C', "
               "'Open-chain ketose'), "
               "('O=C1[C@@H](OC)[C@@]2(O)[C@@](O)(CO[C@@H]([C@@]2(O)C)CC=C(C)C)CC1', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(OC3=C1C(=CC(=C3)O)C)C=C(O)C=C2CC(=O)C[C@H](O)C', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CC[C@@H]([C@@]3(COC(=O)C[C@@](O)(CC(=O)O)C)C)O)C)[C@@]4(C(=O)C[C@@H]([C@]4([C@@H]1O)C)[C@@H](CCC=C(C(=O)O)C)C)C', "
               "'Open-chain ketose'), "
               "('[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])C[C@@H](C(=O)OC)[C@]1(O)C(=O)CO', "
               "'Open-chain ketose'), ('O1CC(O)C(=O)C(O)=C1C', 'Open-chain "
               "ketose'), "
               "('O=C1C(O)=C(C(=O)C(=C1C2=CC=C(OC)C=C2)O)C3=CC=C(O)C=C3', "
               "'Open-chain ketose'), "
               "('O(C=1C(C2=C(O)C3=C(C(=O)C2=O)C(O)=CC=C3)=C(C=C(C1)C)C(O)=O)C', "
               "'Open-chain ketose'), "
               "('CO[C@@H]([C@@H]1Cc2cc3cc(O[C@H]4C[C@@H](O[C@H]5C[C@@H](O)[C@H](O)[C@@H](C)O5)[C@H](O)[C@@H](C)O4)c(C)c(O)c3c(O)c2C(=O)[C@H]1O[C@H]1C[C@@H](O[C@H]2C[C@@H](O[C@H]3C[C@](C)(O)[C@H](O)[C@@H](C)O3)[C@@H](O)[C@@H](C)O2)[C@H](O)[C@@H](C)O1)C(=O)[C@@H](O)C(C)=O', "
               "'Open-chain ketose'), "
               "('O1[C@@]23[C@@]([C@@]4([C@]([C@@]5(O)[C@@]([C@@](O)(CC5)[C@](O)([C@@]6(OC(=O)C(=C(C6)C)C)[H])C)(CC4)C)(C[C@@]12[H])[H])[H])(C(=O)[C@@H]7O[C@@H]7C3)C', "
               "'Open-chain ketose'), "
               "('O=C1[C@]2([C@]3([C@@]([C@](CC3)([C@@H](CCC(O)=O)C)[H])(CC[C@@]2([C@@]4([C@](C1)(C[C@H](O)CC4=O)[H])C)[H])C)[H])[H]', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(C(=O)C=3C1=C(O)C4=C([C@@H](C(=O)OC)[C@@](O)(CC)C[C@@H]4OC5OC(C(OC6OC(C7OC8OC(C)C(CC8OC7C6)=O)C)CC5)C)C3)C(O)=CC=C2O', "
               "'Open-chain ketose'), ('[H][C@](O)(CO)[C@@]([H])(O)C(=O)C=O', "
               "'Open-chain ketose'), "
               "('CC(=O)C1=C(O)C=C[C@@](C)(C1=O)c1c(O)c(C)c(O)c(C(C)=O)c1O', "
               "'Open-chain ketose'), "
               "('C([C@@](CC(C(O)=O)=O)(C(=O)O)O)C(O)=O', 'Open-chain "
               "ketose'), "
               "('O=C1C=C[C@H](O)[C@]2([C@@]1(O2)C(=O)C3=C(O)C=C(C)C=C3O)C(=O)OC', "
               "'Open-chain ketose'), "
               "('O[C@@H]1C=2[C@]3([C@@]([C@](CC3=O)([C@@H](CCC(O)=O)C)[H])(CC(=O)C2[C@@]4([C@@](C1)(C(C(=O)CC4)(C)C)[H])C)C)C', "
               "'Open-chain ketose'), "
               "('O=C1O[C@@H]([C@@H]([C@H](O)[C@@H](CC(=C[C@@H]([C@@H](O)[C@@H](C(=O)CC)C)C)C)C)C)CC=C(C)CC2(OC(C1)=C(C2=O)CC)C', "
               "'Open-chain ketose'), "
               "('C[C@H]1[C@H]2[C@@H](C[C@@]3(C)[C@@H]4CC=C5[C@@H](C=C(O)C(=O)C5(C)C)[C@]4(C)C(=O)C[C@]23C)O[C@@H](CC1=O)C(C)(C)O', "
               "'Open-chain ketose'), "
               "('O=C1C2=C[C@H](O)[C@@H](C)[C@@]([C@]2(O)C)(CC[C@@]3(C)[C@H](CC[C@@]4([C@@H]1O4)C)O3)C', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(C(O)=C(O)C(=C2C)O)C[C@@]3([C@]1(O)C(=O)C(C)=C3C)C', "
               "'Open-chain ketose'), "
               "('COC1=C(C=C(C=C1)C=CC(=O)CC(=O)C=CC2=C(C(=CC=C2)O)OC)O', "
               "'Open-chain ketose'), "
               "('O=C1O[C@@H](C([C@@H]2O[C@H]2CCC(=O)[C@](C[C@@H](C([C@H](C=C1)C)O[C@@H]3O[C@@H](C[C@]4([C@H]3O)OC(=O)O[C@H]4C)C)C)(O)C)CO[C@@H]5O[C@@H]([C@@H](O)[C@H]([C@H]5OC)OC)C)C', "
               "'Open-chain ketose'), ('OC[C@H](O)CC(=O)C([O-])=O', "
               "'Open-chain ketose'), "
               "('[H][C@]12CC[C@@]3([H])[C@]45[C@@H](O)CCC(C)(C)[C@@]4([H])[C@H](O)[C@@]4(O)O[C@]5([H])O[C@]1([H])[C@@]34C(=O)C2=C', "
               "'Open-chain ketose'), "
               "('C[C@H]1[C@H](O)CCC2=CC(=O)[C@@]3(O[C@@H]3[C@]12C)C(=C)CO', "
               "'Open-chain ketose'), "
               "('O=C1C2=C([C@@]3([C@@H](O)C[C@@H]([C@]3(C1)C)[C@@H](CC(O)C=C(C(=O)O)C)C)C)[C@@H](O)CC4[C@@]2(CC[C@@H](C4(C)C)O)C', "
               "'Open-chain ketose'), "
               "('O=C1O[C@H](C[C@@H]2C(=C(O)C(C2)=O)C[C@@H]3[C@@H](C=4C1=C(O)C=C(OC)C4)O3)C', "
               "'Open-chain ketose'), "
               "('O=C1[C@@H](O)[C@@](O)([C@]2(OC2)CC1)[C@]3(O[C@@H]3CC=C(C)C)C', "
               "'Open-chain ketose'), "
               "('O=C1C(O)=C2C=C[C@H]([C@@H]([C@@H]2C1)OC(C(=O)OCC(=C)C(O)C(=O)CCCCC)=C)O', "
               "'Open-chain ketose'), "
               "('O=C1OC(C2=CC=C(O)C=C2)=CC(=C1CC3=C(O)C=C(O)C(=C3)C4(C5=CC=C(O)C=C5)C(=O)C(CC6=CC=C(O)C=C6)=C(C4=O)CC7=CC=C(O)C=C7)CC8=CC=C(O)C=C8', "
               "'Open-chain ketose'), "
               "('O1C([C@H]([C@@]2([C@@]3([C@](C=4[C@@]([C@@]5([C@](C[C@@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O[C@@H]7O[C@H]([C@H](O)[C@@H](O)[C@H]7O)C)CO)CC5)(C(=O)C4)[H])C)(CC3)[H])(CC2)[H])C)[H])C)CCC(C1O)C', "
               "'Open-chain ketose'), "
               "('OCC(=O)[C@@H](O)[C@H](O)[C@@H](O)C([O-])=O', 'Open-chain "
               "ketose'), "
               "('[H][C@@]12C=C(CO)C[C@]3(O)C(=O)C(C)=C[C@@]3([H])[C@@]1(O)[C@H](C)C[C@]1(OC(=O)CCCCCCCCCCCCCCC)[C@@]2([H])C1(C)C', "
               "'Open-chain ketose'), "
               "('[C@H]1(C(C[C@]([C@H]([C@@H]1O)O)(O)CO)=O)O', 'Open-chain "
               "ketose'), ('OC1(C(CC(=O)C=C1CO)(C)C)/C=C/C(/C)=C/C(O)=O', "
               "'Open-chain ketose'), "
               "('O=C1C2=C([C@@]3([C@@H](O)C=C([C@]3(C1)C)[C@@H](CO)C)C)[C@@H](O)C[C@@H]4[C@@]2(CC[C@@H](C4(C)C)O)C', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(OC(=C1)C3(OC3C4OC4)C)C=5C(=C(O)C=6C(=O)C7(C8OC(C(O)C(C8)=O)C)C(C(C6C5)=O)O7)C=C2C', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CC[C@@H](C3(C)C)O)C)[C@@]4(C(=O)CC([C@]4(C1)C)=C(CC(=O)CC(C(=O)O)C)C)C', "
               "'Open-chain ketose'), "
               "('CC(=O)C1=C(O)C=C2Oc3c(C(C)=O)c(O)c(C)c(O)c3[C@]2(C)C1=O', "
               "'Open-chain ketose'), "
               "('O=C1C(=C(C)C)[C@]2(C(=O)O)[C@@]3(C=O)[C@@H]4CC[C@H]([C@H]4C[C@@]2([C@@H]1C3)CO[C@@H]5O[C@@H]([C@@H](OC)[C@H]([C@@H]5O)O)C)C', "
               "'Open-chain ketose'), "
               "('O[C@@]12C(C1(C)C)C3[C@](O)(C(C2O)C)C4[C@](O)(CC(=C3)CO)C(=O)C(=C4)C', "
               "'Open-chain ketose'), "
               "('CC(=O)O[C@@H](C[C@@H]1C(C)=CCC(=O)C1(C)C)C(\\\\C)=C\\\\[C@H](O)C\\\\C=C(/C)CC[C@H]1C(C)(C)[C@@H](O)CC[C@]1(C)OC(C)=O', "
               "'Open-chain ketose'), "
               "('O=C1C([C@H]2[C@]3(C4=C([C@@]5(C(=O)C[C@@H]([C@]5(C[C@]4([C@H]3C1)O)C)[C@@H](CCC(=O)O)C)C)[C@H](C2)O)C)(C)C', "
               "'Open-chain ketose'), "
               "('O=C1C=C2C=C(OC[C@H]2[C@@H]([C@@]1(O)C)O)/C=C/C(=C/[C@H](CC)C)/C', "
               "'Open-chain ketose'), ('O=C1C(C(=O)CC(C1)O)=C(O)CCC', "
               "'Open-chain ketose'), "
               "('C[C@@H]1OC=C2C(O)=C(C(O)=O)C(=O)C(C)=C2[C@H]1C', 'Open-chain "
               "ketose'), "
               "('O=C1[C@@H]([C@]([C@H](C)CC1)(C[C@@H](OC(=O)C)/C(=C/CC2=C(O)C(=C(C)C=C2O)C=O)/C)C)C', "
               "'Open-chain ketose'), "
               "('O[C@H]1[C@@H]([C@@H](C(=O)C1)CC)/C=C/[C@@H](O)C/C=C\\\\C/C=C\\\\C/C=C\\\\CCC(O)=O', "
               "'Open-chain ketose'), "
               "('O=C1C=C(OC)[C@@]2([C@]3(C(=O)[C@](C([C@H]4[C@@]2([C@@]1(O[C@]43OC)C)O)=O)(O)C)C)C', "
               "'Open-chain ketose'), "
               "('O[C@]1([C@@]2([C@H]([C@H]3[C@H]([C@@H](O)C2)[C@@]4(C(CC3)=CC(=O)C=C4)C)CC1)C)C(O)C(OC)=O', "
               "'Open-chain ketose'), "
               "('COC1=C(O)C=CC(\\\\C=C\\\\C(=O)CC(=O)\\\\C=C\\\\C2=CC(OC)=C(O)C=C2)=C1', "
               "'Open-chain ketose'), "
               "('O1C23C4C5(CC(OC(=O)C5C)C3(OC(=O)C2(O)CCC6C(C4(O)C1=O)C=CC=7C6(C)C(=O)C=CC7)C)C', "
               "'Open-chain ketose'), ('O=C1C=C(CC)[C@H]([C@@H]1O)O', "
               "'Open-chain ketose'), "
               "('O=C1C2C(C3C(C4C(C(CC4)C(CCC(O)=O)C)(CC3)C)C1)(CCC(O)C2)C', "
               "'Open-chain ketose'), "
               "('O=C(/C(=C/C(C(OC1OC(C(O)C(C1O)O)CO)/C(=C/C(C(OC2OC(C(O)C(C2O)O)CO)/C(=C/C(CC)C)/C)C)/C)C)/C)CC', "
               "'Open-chain ketose'), "
               "('O1C23C1(OC=4C(C2C(=O)C5(OC6=C(C3C5)C=CC(O)=C6)C)=C(O)C=C(C4)/C=C/C7=C(O)C=C(O)C=C7)C8=C(O)C=C(O)C=C8', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(O)C=3C(=CC(OC)=C(C3C)C(=O)OC)C(=C2C(=O)[C@@]4([C@@]1(O)C(=O)C=C(OC)[C@H]4O)O)O', "
               "'Open-chain ketose'), "
               "('O=C1O[C@@H]2C[C@@]3(C(C(=O)C[C@H]3C(C)C)=C[C@]([C@@]2(C1)C)(O)C(=C)CO)C', "
               "'Open-chain ketose'), "
               "('[H][C@]12O[C@@]1(C(=C)CO)C(=O)C=C1[C@@H](CC[C@H](C)[C@@]21C)OC(=O)C(O)(CO)CC(C)CC(C)CC', "
               "'Open-chain ketose'), "
               "('O=C1C(=O)C(=C(C=2OC(C=C(C)C)=CC2CCC/C(=C/CC3=C(O)C=C(C)C=C3O)/C)C(=C1C/C=C(/CC/C=C(/CC(=O)C=C(C)C)\\\\C)\\\\C)O)C', "
               "'Open-chain ketose'), "
               "('O=C1C2=C(OC3(CC=C(C3C2)C(CCC(O)C(O)(C)C)C)C)CCC1OC', "
               "'Open-chain ketose')]\n"
               "False negatives: [('OC[C@]1(O)OC[C@H](O)[C@@H](O)[C@@H]1O', "
               "'No ketone or hemiketal group found'), "
               "('OC[C@H]1O[C@@](O)(CO)[C@H](O)[C@H]1O', 'No ketone or "
               "hemiketal group found'), "
               "('OC[C@]1(O)OC[C@@H](O)[C@H](O)[C@@H]1O', 'No ketone or "
               "hemiketal group found'), "
               "('OC[C@@H]1O[C@@](O)(CO)[C@H](O)[C@H]1O', 'No ketone or "
               "hemiketal group found')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 13698,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9927557229788467}