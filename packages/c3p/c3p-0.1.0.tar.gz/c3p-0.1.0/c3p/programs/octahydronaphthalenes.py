"""
Classifies: CHEBI:138397 octahydronaphthalenes
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_octahydronaphthalenes(smiles: str):
    """
    Determines if a molecule is an octahydronaphthalene or derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an octahydronaphthalene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Create SMARTS patterns for decalin core with different saturation patterns
    # Allow for different arrangements of single/double bonds
    patterns = [
        # Basic decalin cores with varying degrees of unsaturation
        "C1CCC2CCCCC2C1",  # Fully saturated
        "C1CC=C2CCCCC2C1", # One double bond
        "C1CCC2C=CCCC2C1", # One double bond in different position
        "C1C=CC2CCCCC2C1", # One double bond in different position
        # Additional patterns with different bond arrangements
        "C1CCC2CCCC=C2C1",
        "C1CC=C2CC=CCC2C1",
        "[#6]1~[#6]~[#6]~[#6]2~[#6]~[#6]~[#6]~[#6]~[#6]2~[#6]1" # Generic carbon backbone
    ]

    found_match = False
    matched_pattern = None
    for pattern in patterns:
        patt = Chem.MolFromSmarts(pattern)
        if patt and mol.HasSubstructMatch(patt):
            found_match = True
            matched_pattern = patt
            break

    if not found_match:
        return False, "Does not match octahydronaphthalene core structure"

    # Get all atoms in the matching substructure
    matches = mol.GetSubstructMatches(matched_pattern)
    if not matches:
        return False, "Does not match octahydronaphthalene core structure"

    # Check the first match (we only need one valid match)
    match_atoms = set(matches[0])
    
    # Count double bonds in the matched core
    double_bonds_in_core = 0
    for bond in mol.GetBonds():
        if bond.GetBeginAtomIdx() in match_atoms and bond.GetEndAtomIdx() in match_atoms:
            if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                double_bonds_in_core += 1

    # Allow up to 2 double bonds in the core to account for various substitution patterns
    if double_bonds_in_core > 2:
        return False, "Too many double bonds in core structure"

    # Check that matched atoms are carbons (but allow for substitution)
    core_carbons = 0
    for atom_idx in match_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'C':
            core_carbons += 1

    if core_carbons < 8:  # Need at least 8 carbons in the core
        return False, "Insufficient carbon atoms in core structure"

    return True, "Matches octahydronaphthalene core structure with valid substitution pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138397',
                          'name': 'octahydronaphthalenes',
                          'definition': 'Any carbobycyclic compound that is an '
                                        'octahydronaphthalene or a compound '
                                        'obtained from an octahydronaphthalene '
                                        'by formal substitution of one or more '
                                        'hydrogens.',
                          'parents': ['CHEBI:36785']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.13675213675213674 is too low.\n'
               'True positives: '
               "[('[H]C1(CCOC1=O)CC[C@@]1(C)[C@H](C)CC[C@@]2(C)C(=CCC[C@]12[H])C(O)=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C=1CC[C@@H]([C@@]2(C1CC[C@H](C2)C(C)=C)C)C', 'Matches "
               'octahydronaphthalene core structure with valid substitution '
               "pattern'), "
               "('C[C@@H]1[C@@H](C[C@@H](O)C2=CC[C@H](C[C@]12C)C(C)=C)OC(C)=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@]12C=C(CC[C@]1(C)CCCC2=C)C(C)C', 'Matches "
               'octahydronaphthalene core structure with valid substitution '
               "pattern'), ('C12=CCC[C@H]([C@]1(C[C@@H](CC2)C(=C)C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), ('C[C@H]1CCC[C@@]2(C)CCC=CC12', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CC1=C(CC[C@H]2C(=C)CC[C@H]3C(C)(C)[C@@H](O)CC[C@]23C)[C@@]2(C)CCC(=O)C(C)(C)[C@@H]2CC1=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CC(C)=CCCC(=C)[C@H]1CC[C@@]2(C)CCC=C(C)[C@@H]2C1', 'Matches "
               'octahydronaphthalene core structure with valid substitution '
               "pattern')]\n"
               'False positives: '
               "[('[H][C@@]12CC[C@@]3([H])C(C)(C)CCC[C@]3(C)[C@@]11CC[C@H](C1)C(C)=C2', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@@]12CC(C)(C)CC[C@@]1(CC[C@]1(C)C2=CC[C@]2([H])[C@@]3(C)CC[C@H](O)[C@@](C)(C(O)=O)[C@]3([H])CC[C@@]12C)C(O)=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@@]12CC[C@](C)(CC1=CC[C@@]1([H])[C@@](C)(CO)CCC[C@]21C)C=C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C[C@@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]3[C@@H](O)[C@@H](O)CO[C@H]3O[C@H]3CC[C@@]4(C)[C@@H](CC[C@]5(C)[C@@H]4CC=C4[C@@H]6CC(C)(C)CC[C@@]6(CC[C@@]54C)C(O)=O)C3(C)C)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@H](O)[C@H]1O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C2=C([C@]3(CCC(C([C@@H]3C1)(C)C)=O)C)CC[C@]4([C@]2(CC[C@@H]4[C@H](C(=O)O)CCC(=C)C(C)C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O1[C@H]2[C@]3([C@]4([C@@]([C@](C[C@H]4O)([C@@H](C5OC(=O)C(=C(C5)C)C)C)[H])([C@@H](O)C[C@@]3([C@@]6([C@@](O)([C@@H]12)CC=CC6=O)C)[H])C)[H])[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)[H])[H])(CC[C@@]4([C@@H](CCC([O-])=O)C)[H])[H])C)[H])C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CC(C)=CCC[C@](C)(O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H]1CC[C@]2(C)[C@@H]1[C@H](O)C[C@@H]1[C@@]3(C)CC[C@H](O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4O)C(C)(C)[C@@H]3CC[C@@]21C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CC1(C)O[C@@H]2C[C@H]3[C@@H]4C[C@H](F)C5=CC(=O)C=C[C@]5(C)[C@H]4[C@@H](O)C[C@]3(C)[C@@]2(O1)C(=O)CO', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C(O)C1=C(O)C2=C(O[C@@]3(CC[C@@H]4[C@@]([C@H]3C2)(CC[C@@H](C4(C)C)OC(=O)C)C)C)C=C1C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O[C@@H]1[C@](C2[C@@]([C@@]3([C@]([C@]4(C([C@@]5([C@@](CC4)(CC[C@@](C5)(C)C(O)=O)C(O)=O)[H])=CC3)C)(CC2)C)[H])(CC1)C)(CO)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CC(=C)[C@H]1CC2=C(C)C(=O)CC[C@@]2(C)CC1O', 'Matches "
               'octahydronaphthalene core structure with valid substitution '
               "pattern'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)O[C@H]1CC[C@]2(C)[C@H]3CC[C@]4(C)[C@H](CC[C@H]4[C@@H]3CC=C2C1)[C@H](C)CC[C@H](O)C(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('OC1C2(C3(C(C4(C(CC3)C(C(O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@@H]7OC[C@H](O)[C@H](O)[C@H]7O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8O)CO)[C@H]6O)CO)C(O)=O)CC4)(C)C)C)CC=C2C9C(C1O)(C(OC(=O)/C(/C)=C\\\\C)CC(C9)(C)C)CO)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@]12CC=C3[C@]4([H])[C@@H](C)[C@H](C)CC[C@@]4(CC[C@@]3(C)[C@]1(C)CC[C@@]1(O)C(C)(C)[C@@H](O)[C@H](O)C[C@]21C)C(O)=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[C@@]12([C@]3([C@](C[C@@]1([C@]4([H])CC[C@H]([C@]4(C3)[H])C)C=O)(C=C2C(C)C)[H])CO[C@]5([C@H]([C@@H]([C@@H]([C@H](O5)C)O)O)O)[H])C(O)=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('FC1=C2C[C@]3(C[C@@]4([C@](O)(C(=O)C3=C(O)C2=C(O)C(NC(=O)CN5CCCC5)=C1)C(O)=C(C(=O)[C@H]4N(C)C)C(=O)N)[H])[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O[C@@H]1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H]([C@H](O)CC=C(C)C)CO)CC4)(C)CC3)C)CC2)(C)CC1)(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C2=C([C@]3(CCC(C([C@@H]3C1)(C)C)=O)C)CC[C@]4([C@]2(CC[C@@H]4[C@H](CO)CC/C=C(/CO)\\\\C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CO[C@@H]1[C@@H](O)[C@H](C)O[C@@H](O[C@H]2CC[C@@]3(C=O)[C@H](CC[C@@H]4[C@@H]3[C@@H]3O[C@@H]3[C@]3(C)[C@H](CC[C@]43O)C3=CC(=O)OC3)C2)[C@H]1OC(C)=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C[C@]12CC[C@H]3[C@@H](CCC4=C[C@@H](O)CC[C@]34C)[C@@H]1CC[C@@H]2O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@@]12CCC(=C)[C@@H](CC\\\\C(C)=C\\\\COP([O-])(=O)OP([O-])([O-])=O)[C@@]1(C)CCCC2(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@]2(CC(C1)=O)[H])[H])(CC[C@@H]4O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C(=O)O)O)O)O)[H])C)[H])C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C(OC)C1=CC(O)=C2O[C@@]3(CC2=C1)[C@]4([C@@H](C(CCC4)(C)C)CC[C@@H]3C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C[C@H](C[C@H](O)[C@H]1OC1(C)C)C1=C2C[C@H](O)[C@H]3[C@@]4(C)CCC(=O)C(C)(C)[C@@H]4CC[C@]3(C)[C@@]2(C)CC1', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('OC1C(C2(C(C3C(C4C(=CC3)C(C(OC5OC(C(O)C(O)C5O)COC6OC(C(O)C(O)C6O)CO)CC4)(C)C)(C(=O)C2)C)(C1)C)C)C(O)(C(O)CCC(O)(C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('OCC12C(C3(C(C4(C(C5(C(CC4)C(C(=O)CC5)(C)C)C)CC3)C)=CC1)C)CC(CC2)(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@@]12CCC3CC(=O)CC[C@]3(C)[C@@]1([H])C(=O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1[C@](O)(C(=O)[C@H]2C(=C([C@]1(C(=O)OC)[C@@]3([C@@H]2[C@@]45C(=O)O[C@@H](C3)[C@@H]4C([C@@H](OC(=O)C)CC5)(C)C)C)C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1[C@@H](O[C@@H]2C(OC([C@H]2O)=O)(C)C)CC[C@]3(C1CC[C@@H]4[C@@]3(C=5NC=6C=CC=CC6C5C4)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C(C2C3(C4(C3)C(C5(C(CC4)(C(CC5)C(CC(O)/C=C(/C)\\\\C(O)=O)C)C)C)CC2)CC1)(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C2=C[C@@](C=C)(CC[C@@H]2[C@@]3(O)[C@H](O)CCC(C3=C1)(C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C(OC[C@]1(O)[C@H]2C[C@@]3([C@@]4([C@H]([C@]5([C@H](OC(C)(C)OC5)CC4)C)CC[C@H]3C2)C)CC1)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1[C@@]2(O[C@@H]2[C@]3(CCCC([C@@H]3C1)(C)C)C)C(=O)O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3([C@@H]1OC(=O)C)C)C(=O)C)C)[C@@H](O)C[C@@H]4[C@@]2(CC[C@@H](C4(C)C)O)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1[C@H](O)C2=C(CC[C@@]([C@@H]2O)(C=C)C)[C@@]3([C@@H]1C(CC[C@H]3O)(C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[C@@]12([C@](CC[C@@H]([C@]13OC=4[C@](C3)(C(=C(C(C4C)=O)C(=O)[O-])C)C)C)([H])C(C(CC2)=O)(C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O1[C@@]2([C@]([C@]3([C@@]([C@@]4([C@@](CC3)(CC5=C4NC6=C5C=7C[C@@]8([C@](C(OC8(C)C)(C)C)(C(=O)C7C=C6)[H])[H])[H])C)(CC2)C)[H])([C@H](O)C[C@]1(C(O)(C)C)[H])C)[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C1[C@@]2([C@@]([C@@]3([C@](C[C@H](OS([O-])(=O)=O)CC3)(C1)[H])C)(CC[C@@]4([C@H](CC[C@@]24[H])O)C)[H])[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@@]1(CC[C@@]2([H])C3=CC[C@]4([H])[C@](C)(CC[C@H](O)[C@@]4(C)C(O)=O)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1[C@]2(C(=C)[C@@](C[C@H]3[C@]2(CC[C@H]([C@@]3(CCC(=O)OC)C)C(O)(C)C)C)(C)C([C@]1(O)C)=O)C(=O)OC', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[C@@]12([C@]3([C@](CC[C@@]1([C@@]4(C(C[C@H](CC4)O)=CC2)C)[H])([C@](CC3)([C@H](C)CC[C@@H](C(C)C)OS([O-])(=O)=O)[H])C)[H])[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1[C@]2([C@]([C@]3([C@@]([C@H](CC3)C(=O)CO)(C1)CO)[H])(CC[C@]4([C@@]2(CC[C@@H](O)C4)C)[H])[H])[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O[C@]12[C@@]([C@H]3[C@H](O)C[C@@]4([C@@H]([C@@H]([C@@H]5[C@]([C@@H](C(C)C)C)(C)C5)C)CC[C@H]4[C@@H]3C[C@H]1O)C)(CC[C@@H](C2)O)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C(C1=CC[C@@H]2[C@@]1([C@H](O)C[C@@H]3[C@@]4(C(=C[C@H](O)[C@H](C4)O)CC=C23)C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O[C@@]12[C@]([C@]3([C@](CC1)([C@@H](O)CC3)C)[H])(CCC=4[C@]2(C)C=CC(=O)C4)[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O1[C@@]([C@H]2C[C@H]3O[C@@H]1[C@@]42[C@@H]3[C@]5(O)[C@@H](O)C[C@H]6C[C@@H](O)CC[C@@]6([C@H]5CC4)C)(CCC(=C)C(C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C(=C[C@H]2[C@@H](C(C)C)CC[C@]([C@H]2C1)(O)C)CO', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C\\\\1C[C@]2([C@]3([C@@]([C@@]4(C(=CC3)C[C@@H](O)CC4)C)(CC[C@@]2(/C1=C(\\\\C)/C(=O)CC[C@H](CO)C)C)[H])[H])[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C(C2C(C3C(C4(C(C5C(CC4)(CCC5C(CO)=C)C)=CC3)C)(CC2)C)(C)C=C1)(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1OC[C@@H]2[C@]1([C@@H]3[C@@H](C=C2)C[C@@H](COC(=O)C)CC3)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@H](O)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CC[C@H](O)C2', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@@]1(O[C@@H]2C[C@]3([H])[C@H](O)C[C@]4([H])[C@]([H])(CC[C@@]5(C)[C@@]4([H])C[C@]4([H])O[C@]6(CC[C@@H](C)CO6)[C@@H](C)[C@]54[H])[C@@]3(C)C[C@H]2O)O[C@H](CO)[C@H](O[C@]2([H])O[C@H](CO)[C@@H](O)[C@H](O[C@]3([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@H]2O[C@]2([H])O[C@H](CO)[C@@H](O)[C@H](O[C@]3([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@H]2O)[C@H](O)[C@H]1O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C(O)=C2[C@@]([C@H](OC(=O)C)C[C@@H]3[C@]2(C3)[C@@]4(C1=C[C@@](C=C)(CC4)C)O)(COC(=O)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C1[C@]2([C@]3([C@@]([C@@]4(C(=CC(CC4)=O)[C@H](C3)C)C)(CC[C@@]2([C@@](C1)(O)C(=O)C)C)[H])[H])[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1[C@@H](O)[C@H]([C@@]2(CC3C(C2([C@@H]1C)CC3)=C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C[C@H]1[C@@H]2[C@H]3CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]4(C)[C@]3(C)CC[C@@]2(C)CCC1=C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O[C@]1([C@@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(C[C@H](O)C=C4)[H])C)(CC2)[H])[H])(CC1)[H])C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[C@]12(CC[C@H](CC2C[C@@H](C3C4[C@](CCC13)(C(CC4)[C@@H](C(CCC(O)=O)O)O)C)O)O)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CC(=O)OCC(=O)[C@H]1CC[C@@H]2[C@@]1(CC(=O)[C@H]3[C@H]2CC[C@@H]4[C@@]3(CC[C@H](C4)O)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C(O)=C2[C@@]([C@H](O)C[C@@H]3[C@]2(C3)[C@@]4(C1=C[C@@](C=C)(CC4)C)O)(COC(=O)C(C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O[C@]([C@@]1([C@@]2([C@]([C@]3([C@@]([C@@]4([C@@](CC3)(CC(=O)CC4)[H])C)(CC2)[H])[H])(CC1=O)[H])C)[H])(CCCC(C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[C@@]12(C([C@@]3(CC(CC[C@@]3([C@H](C1)O)C([O-])=O)(C)C)[H])=CC[C@]4([C@]2(CC[C@@]5([C@@]4(CC[C@@H](C5(C)C)O)C)[H])C)[H])C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C[C@H](CCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@@]1(CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)OS(O)(=O)=O)[C@H](C)CCC(=O)NCCS(O)(=O)=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CC(C)=CCC[C@](C)(O[C@@H]1O[C@H](CO[C@@H]2OC[C@H](O)[C@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@H]1O)[C@H]1CC[C@]2(C)[C@@H]1[C@H](O)C[C@@H]1[C@@]3(C)CC[C@H](O)C(C)(C)[C@@H]3CC[C@@]21C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@]12O[C@]11CC[C@]3([H])C(C)(C)CCC[C@@]3(C)[C@]1([H])[C@@]1([H])O[C@]11OC(=O)C(CO)=C21', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C[C@@]1(CC[C@@]2(O)C(=C1)C(=O)C1=C3[C@@](C)(CC[C@@H](O)[C@]23C)CO1)C=C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O[C@@H]1[C@@]([C@]2([C@@]([C@@]3([C@]([C@]4(C([C@]5([C@@](CC4)(CCC(C5)(C)C)C(O)=O)[H])=CC3)C)(CC2)C)[H])(C[C@@H]1O)C)[H])(C)C(O)=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C12=C3C(=CC(=C2C(O[C@@H]([C@@H]1OC(C)=O)C)=O)O)O[C@@]4([C@]([C@]5(C=CC(C([C@@]5(C[C@@H]4O)[H])(C)C)=O)C)(C3)[H])C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@]1(COC(=O)C1)[C@@]1([H])CC[C@]2(O)[C@]3([H])CC[C@]4([H])C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O[C@H]3C[C@H](O)[C@H](O)[C@@H](C)O3)[C@@H](C)O2)[C@@H](C)O1', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1[C@H]2[C@H](C=C(C1)C(=O)O)[C@@H](C(C)C)CC[C@@H]2C(=O)O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O(CC1=C(O)C2=C(C[C@H]3[C@@]2(CC[C@@H]4[C@@]3(CCCC4(C)C)C)C)C(=C1)O)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1O[C@H](C)[C@@]2([C@@]13C(=C)[C@](C[C@@H]4[C@@]3(CC[C@H]5[C@]4([C@H](O)[C@H]6C(=O)O[C@]5(C)C6)C)C)(C)C2=O)O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O1CC2(C3(C(C4(C(CC3)C(C(O)CC4)(C)C)C)CCC2C(C(OC(=O)C)CC5OC(=O)C(C5)C)C)C)CC1=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CC(=O)[C@H]1CC[C@H]2[C@@H]3CC[C@@H]4CC(=O)CC[C@]4(C)[C@H]3[C@H](O)C[C@]12C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C2=C(OC(=C1)C)O[C@]3(CC[C@H]4[C@]([C@@H]3C2)(CC[C@@H]5[C@@]4(CCC(C5(C)C)=O)C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC[C@@H](C)C(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O[C@H]1[C@]2([C@]3([C@@]([C@](CC3)([C@@H](CC(O)=O)C)[H])(CC[C@@]2([C@@]4([C@]([C@@H]1O)(C[C@H](O)CC4)[H])C)[H])C)[H])[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C=C2[C@@]3([C@H](C(C(=O)CC3)(C)C)C[C@@H]4[C@]2(O4)[C@]5([C@]1([C@@H](C(O)(CC(=O)CC(C(=O)O)C)C)CC5=O)C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O([C@]1([C@]2([C@](CC[C@H]1OC(=O)C(O)(C(OC(=O)C)C)C)(CC(=O)C(C2)=C(C)C)C)[H])C)C(=O)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O1C2C(C3(C(C4C(CC3)C5(C(=CC4)CC(O)CC5O[C@@H]6OC[C@H](OC(=O)C(O)C(CC)C)[C@H](O)[C@H]6O[C@@H]7O[C@H]([C@H](O)[C@@H](O)[C@H]7O)C)C)C2)C)C(C18OCC(CC8)=C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@](CC3)([C@@]5(C(=CC4)C[C@@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O[C@@H]7O[C@H]([C@H](O)[C@@H](O)[C@H]7O)C)CO)CC5)C)[H])[H])(C2)[H])C)([C@@H]([C@]18OC[C@@H](CC8)C)C)[H])[H]', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O1C2C(C3(C(C4C(CC3)C5(C(=CC4)CC(OC6OC(C(O)C(O)C6O)COC7OC(C(O)C(O)C7OC8OC(C(O)C(O)C8O)C)CO)CC5)C)C2)C)C(C1(O)CCC(COC9OC(C(O)C(O)C9O)CO)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C(=C[C@H]2[C@H](C(=C)CO)CC[C@]([C@H]2C1)(O)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C[C@]1(CC[C@H]2C(CC[C@@H]3[C@]2(C)CCC[C@@]3(C)C(O)=O)=C1)C=C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)OS([O-])(=O)=O)[H])[H])(CC[C@@]4([C@H](C)CCC([O-])=O)[H])[H])C)[H])C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@]1(O)C[C@@]2(C)[C@@]([H])(CC[C@]2(C)O)[C@]2([H])CCC3=CC(=O)CC[C@]3(C)[C@@]12F', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C2=C(C3=C(NC4=C3C[C@@H]5CC[C@@]6([C@@]([C@@]45C)(CC[C@H]7[C@@]68O[C@@H]8[C@@H]9O[C@H](C%10OC%10(C)C)OC([C@H]9O7)(C)C)C)O)C=C2)C[C@@H]%11[C@@H]1C(OC%11(C)C)(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O(C1C2(C(C3(C(C(C(O)CC3)(C)C)C1)C)CCC4(C2=CC(OC4C=5C=COC5)=O)C)C)C(=O)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CC(=O)C=C[C@@H]1[C@]2(CCCC(C2CC[C@@]1(C)O)(C)C)C', 'Matches "
               'octahydronaphthalene core structure with valid substitution '
               "pattern'), "
               "('O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CCC(C3(C)C)O)C)[C@@]4([C@H](O)C[C@@H]([C@]4([C@@H]1O)C)[C@@H](CC(=O)C[C@@H](C(=O)O)C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@@]12CC=C3C[C@H](CC[C@]3(C)[C@@]1([H])CC[C@]1(C)C(=CC[C@@]21[H])c1cccnc1)OC(C)=O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('CCN1C[C@]2(C)CC[C@H](O)[C@]34C1[C@H](C[C@H]23)[C@@]12C[C@H]([C@@H](O)C[C@@H]41)C(=C)[C@H]2O', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('C1[C@H](O)C([C@@]2(CC[C@@]3([C@](CC=C4[C@]3(CC[C@@]5([C@]4(C[C@@](C[C@@H]5O)(C(O)=O)C)[H])C)C)([C@]2(C1)C)[H])C)[H])(C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('[H][C@]1(O[C@@H](O[C@H](CO)[C@]2([H])O[C@@H](OCC(=C)C3CC[C@]4(C)C[C@@H](CC(C)=C4C3)O[C@@H]3O[C@]([H])([C@H](O)[C@H]3O)[C@@H](CO)O[C@@H]3O[C@@]([H])([C@H](O)CO)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)CO', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C(O)C1=C[C@H]2[C@@H](C(=C)CC[C@@H]2[C@H](C(=O)O)C)CC1', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('OC1CC2C(C3C(C4C(C(CC4)C(CCC(CC)C(C)=C)C)(CC3)C)=CC2)(CC1)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C(O)/C(=C/CC[C@H]([C@@H]1[C@@]2([C@@]([C@H]3[C@@]([C@@H](C(=C(C)C)CC3)CCCO)(C)CC2)(C)CC1)C)C)/C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern'), "
               "('O=C1C=C[C@@]2([C@H]3[C@]4([C@@]56[C@@H](C(=O)OC5)[C@@H](O)[C@@](C4)(C)C([C@@]6(C3)C)=O)CC[C@H]2C1(C)C)C', "
               "'Matches octahydronaphthalene core structure with valid "
               "substitution pattern')]\n"
               'False negatives: '
               "[('[C@H]1(COP([O-])([O-])=O)C(=CC[C@@]2([C@]1(C)CCCC2(C)C)[H])C', "
               "'Does not match octahydronaphthalene core structure')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 9,
    'num_false_positives': 100,
    'num_true_negatives': 795,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.08256880733944955,
    'recall': 1.0,
    'f1': 0.15254237288135594,
    'accuracy': 0.8893805309734514}