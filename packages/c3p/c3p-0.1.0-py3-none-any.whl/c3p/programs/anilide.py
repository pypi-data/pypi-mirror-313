"""
Classifies: CHEBI:13248 anilide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_anilide(smiles: str):
    """
    Determines if a molecule is an anilide (aromatic amide obtained by acylation of aniline).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an anilide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for anilide:
    # - Aromatic ring (c1ccccc1) connected to
    # - Nitrogen (can be substituted or not)
    # - Connected to C(=O)
    # - The C(=O) is not part of an aromatic ring
    anilide_pattern = Chem.MolFromSmarts('[cR1]1[cR1][cR1][cR1][cR1][cR1]1[N]C(=O)[#6]')
    
    matches = mol.GetSubstructMatches(anilide_pattern)
    
    if not matches:
        return False, "No anilide group found"
    
    # For each match, verify additional conditions
    for match in matches:
        # Get relevant atoms
        ar_carbon = mol.GetAtomWithIdx(match[0])  # First carbon of aromatic ring
        n_atom = mol.GetAtomWithIdx(match[6])     # Nitrogen atom
        c_atom = mol.GetAtomWithIdx(match[7])     # Carbonyl carbon
        o_atom = mol.GetAtomWithIdx(match[8])     # Oxygen atom
        
        # Verify the aromatic ring is a benzene ring
        ring_info = mol.GetRingInfo()
        for ring in ring_info.AtomRings():
            if ar_carbon.GetIdx() in ring and len(ring) == 6:
                ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
                if all(atom.GetIsAromatic() for atom in ring_atoms):
                    # Verify the carbonyl carbon is not part of an aromatic ring
                    if not c_atom.GetIsAromatic():
                        # Verify the C=O bond
                        co_bond = mol.GetBondBetweenAtoms(c_atom.GetIdx(), o_atom.GetIdx())
                        if co_bond is not None and co_bond.GetBondType() == Chem.BondType.DOUBLE:
                            # Verify N-C bond
                            nc_bond = mol.GetBondBetweenAtoms(n_atom.GetIdx(), c_atom.GetIdx())
                            if nc_bond is not None and nc_bond.GetBondType() == Chem.BondType.SINGLE:
                                return True, "Found anilide group: aromatic ring connected to N-C(=O)"
    
    return False, "Structure does not match anilide requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13248',
                          'name': 'anilide',
                          'definition': 'Any aromatic amide obtained by '
                                        'acylation of aniline.',
                          'parents': ['CHEBI:22712', 'CHEBI:62733']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.37037037037037035 is too low.\n'
               'True positives: '
               "[('CC1=CC(=NC=C1)NC2=NC(=CS2)C3=CC=C(C=C3)NC(=O)C', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('CCC1=CC=C(C=C1)NC(=O)C2CC(=O)N=C(S2)N', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('CC1=C(C(=CC=C1)C)NC(=O)COC(=O)C2=NON=C2N', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('CC1=NC(=C(C=C1)OCC(=O)NC2=CC=C(C=C2)F)[N+](=O)[O-]', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCC(=O)Nc1ccccc1', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=C(C=C(C=C1)NC(=O)CSC2=NC=CN2CC3=CC=CC=C3)C', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('S(CC(=O)NC1=CC=C(C2CCCCC2)C=C1)C3=CC=C(C=C3)C', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('CN1[C@H]2CC[C@H](O[C@H]2COC3=C(C1=O)C=C(C=C3)NC(=O)C4CCOCC4)CC(=O)NC5=CC(=CC=C5)OC', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC(=O)NC1=CC=C(C=C1)NC=C2C(=O)NC(=O)N(C2=O)CCC3=CC(=C(C=C3)OC)OC', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC(=CC(=C1)OCC(=O)NC2=CC=CC(=C2)C3=NN=C(O3)C4=CC=CO4)C', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1C=CCC(C1C(=O)NC2=CC(=C(C=C2)F)F)C(=O)O', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('C1=C(C=C(C=C1Cl)NC(CSC=2N=C(C=CN2)C=3N=C(SC3)C4=CC=CC=C4)=O)Cl', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC(=NO1)C2=NC(=C(S2)C3=NN=C(N3C)SCC(=O)NC4=CC(=CC(=C4)Cl)Cl)C', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CCCOCCN(C(=O)CCl)c1c(CC)cccc1CC', 'Found anilide group: "
               "aromatic ring connected to N-C(=O)'), "
               "('CC(O)(C=C)C(=O)Nc1cc(Cl)cc(Cl)c1', 'Found anilide group: "
               "aromatic ring connected to N-C(=O)'), "
               "('CC1=C(C=C(C=C1)NC(=O)COC2=C(C=C(C=C2)C=NNC(=S)N)OC)C', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC(=CC=C1)NC(=O)CSC2=NN=C(C=C2)C3=CC=CO3', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('CCC1=CC=C(C=C1)NC(=O)C2C3C2C=CCCCC3', 'Found anilide group: "
               "aromatic ring connected to N-C(=O)'), "
               "('[As](O[Bi]=O)(=O)(O)C1=CC=C(NC(CO)=O)C=C1', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC=CC=C1OCC(=O)NC2=CC=CC=C2SC', 'Found anilide group: "
               "aromatic ring connected to N-C(=O)'), "
               "('Cc1occc1C(=O)Nc1ccccc1', 'Found anilide group: aromatic ring "
               "connected to N-C(=O)'), "
               "('N(C(C)=O)C1=CC([As](=O)(O)O)=CC=C1O', 'Found anilide group: "
               "aromatic ring connected to N-C(=O)'), "
               "('C=1C(=C(C=C(C1)Cl)Cl)NC(C2(C(O)=O)CC2)=O', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('CCOC1=CC=CC=C1NC(=O)C(C)OC2=CC=C(C=C2)OC', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('N(C(C)=O)C=1C=C(C=CC1O)[As]2SC(CS2)CO', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('COC1=CC=CC=C1NC(=O)CSC2=NN=C(N2CC3=CC=CO3)C4=CC=CO4', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('CSC1=CC=CC=C1NC(=O)COC2=C(C=C(C=C2)Cl)Cl', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('CC(C)COCN(C(=O)CCl)c1c(C)cccc1C', 'Found anilide group: "
               "aromatic ring connected to N-C(=O)'), "
               "('COC1=CC=C(C=C1)NC(=O)C2C3C2CCC=CCC3', 'Found anilide group: "
               "aromatic ring connected to N-C(=O)'), "
               "('CC1=C(C(c2ccccc2Cl)C(C(=O)OCCc2ccccn2)=C(C)N1)C(=O)Nc1ccccc1', "
               "'Found anilide group: aromatic ring connected to N-C(=O)')]\n"
               'False positives: '
               "[('C[C@H]1CN(C(=O)C2=C(C(=CC=C2)NC(=O)NC3=CC=C(C=C3)OC)O[C@H]1CN(C)C(=O)NC(C)C)[C@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1CC1CC(=O)N2[C@@H]([C@H](C23CN(C3)C(=O)NC4=CC=CC=C4F)C5=CC=CC=C5)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)NC(C)C)O[C@H]1CN(C)C(=O)NC3=CC=C(C=C3)F)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('COC1=CC=C(C=C1)C=CC(=O)NC2=CC=CC=C2C(=O)O', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CCC(F)(F)F)O[C@@H]1CN(C)C(=O)NC3=CC=C(C=C3)OC)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('ClC1=CC(=C(NC(=O)CN2CCC(CC2)C)C=C1)C(=O)C=3C(Cl)=CC=CC3', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1=CC(=CN=C1)C2=CC=C(C=C2)[C@H]3[C@@H](N([C@@H]3C#N)C(=O)NC4=CC=C(C=C4)F)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC(=O)N1CCN(CC1)C2CCC(CC2)N3C4=C(C(=N3)C5=CC(=C(C=C5)NC(=O)C6=CC7=CC=CC=C7N6C)OC)C(=NC=N4)N', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN(C(=O)C2=C(C(=CC=C2)NC(=O)C3=CC=NC=C3)O[C@H]1CN(C)C(=O)NC4=CC=C(C=C4)OC)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN([C@H](COC2=C(C=CC(=C2)NC(=O)NC3=CC(=CC=C3)F)C(=O)N(C[C@H]1OC)C)C)C', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)N(C)C)O[C@@H]1CN(C)C(=O)NC3=CC=C(C=C3)F)[C@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1C[C@H]2[C@@H](COC[C@@H](CN2C(=O)NC3=CC=CC=C3)O)O[C@H]1CC(=O)NCC4=NC=NC=C4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C(=C1C(N(N=C1C)C2=CC=C(C(=O)O)C=C2)=O)([H])C=3OC(=CC3)C4=CC(=C(C=C4[N+]([O-])=O)C)C', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C=1C=C(OCC)C=CC1NC(C)=O', 'Found anilide group: aromatic "
               "ring connected to N-C(=O)'), "
               "('Cl.CCCCN1CCCC[C@H]1C(=O)Nc1c(C)cccc1C', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('C1COCCN1C(=O)C[C@H]2C[C@H]3[C@@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)NC5=CC=C(C=C5)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CN=CC=C3)O[C@@H]1CN(C)C(=O)NC4=CC=CC=C4)[C@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN(C(=O)C2=C(C(=CC=C2)NC(=O)NC3=CC=CC=C3)O[C@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)C)[C@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('O=C(O)C1=C(NC(=O)[C@@H](NC(=O)[C@H](N(C(=O)[C@@H](N)[C@@H](CC)C)C)CC2=CC=CC=C2)C(C)C)C=CC=C1', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CON(C(=O)OC)c1ccccc1COc1c(C)c(nn1C)-c1ccccc1', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1=CC=C(C=C1)CN2C3=C(C=C(C=C3)Cl)N(C(=O)C2=O)CC(=O)NC4=CC(=CC=C4)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC=C(C=C1)NC(=O)CSC2=NN=C(N2C)C3=CC=C(C=C3)S(=O)(=O)N4CCOCC4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CN1C=C(N=C1)CCNC(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@H](CN3C(=O)NC4=CC=C(C=C4)C(F)(F)F)O', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC(C(=O)NC1=CC=CC=C1C2=CC=CC=C2)N3CCN(CC3)C(=O)C4=CC=CC=C4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=CC=C3)[C@H](C)CO)C)CN(C)S(=O)(=O)C4=CC=C(C=C4)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1C[C@H]([C@H](O[C@H]1CCNC(=O)CC2=CC=NC=C2)CO)NC(=O)NC3=CC(=CC=C3)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('COC1=CC=C(C=C1)NC(=O)NC2=CC3=C(C=C2)O[C@@H]4[C@H]3C[C@H](O[C@H]4CO)CC(=O)NCC5=CC=CC=N5', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1[C@H](O[C@@H]([C@@H]2[C@H]1C3=C(O2)C=CC(=C3)NC(=O)NC4=CC=C(C=C4)C(F)(F)F)CO)CC(=O)NCC5=CC=CC=N5', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN([C@@H](COC2=C(C=CC(=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)C(=O)NC3=CC=CC=C3F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('COC(=O)C[C@@H]1C[C@H]2[C@@H]([C@H](O1)CO)OC3=C2C=C(C=C3)NC(=O)NC4=CC=CC=C4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1C[C@@H]([C@@H](O[C@H]1CC(=O)NCC2CC2)CO)NC(=O)NC3=CC(=CC=C3)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('Clc1ccc(NC(=O)Nc2ccc(Cl)c(Cl)c2)cc1', 'Found anilide group: "
               "aromatic ring connected to N-C(=O)'), "
               "('CCCN1CCCC2=C1C=CC(=C2)CN(CCCN3CCOCC3)C(=O)NC4=CC=C(C=C4)OCC', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1CCC(CC1)NC(=O)C[C@@H]2C[C@H]3[C@@H]([C@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)NC5=CC=CC=C5F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=CC=C3)[C@@H](C)CO)C)CN(C)CC4CC4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN(C(=O)CCCN2C=C(CO[C@H]1CN(C)C(=O)NC3=CC(=CC=C3)OC)N=N2)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1C[C@H]([C@@H](O[C@H]1CC(=O)NCC2=CC=CC=N2)CO)NC(=O)NC3=C(C=CC(=C3)F)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=C(C=C3)C(F)(F)F)[C@@H](C)CO)C)CN(C)C', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)NC3=CC=C(C=C3)OC)O[C@@H]1CNC)[C@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('COC1=CC2=C(C=C1)C3=C(N2)[C@H](N(CC34CN(C4)C(=O)CC5=CC=CC=C5)C(=O)NC6=CC=C(C=C6)F)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1C[C@H]([C@@H](O[C@H]1CC(=O)NC2=CC=C(C=C2)C3=CC=CC=C3)CO)NC(=O)C4=CC=CC=C4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)NC3=CC=CC=C3F)C(=O)N(C[C@H]1OC)C)C)C(=O)C', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CN1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)NC5=CC=C(C=C5)C(F)(F)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('COC(=O)C[C@H]1CC[C@H]([C@@H](O1)CO)NC(=O)NC2=CC=C(C=C2)C(F)(F)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CCOC(=O)C1(C(C(=O)C(=O)N1C2=CC=CC=C2)N=NC3=CC=CC=C3)C', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC(=C(C=C1)OC)NC(=O)NC2=NC=C(C=C2)Br', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('C1C[C@H]([C@@H](O[C@H]1CCNC(=O)C2CCOCC2)CO)NC(=O)NC3=CC(=CC=C3)Cl', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=CC=C3)[C@H](C)CO)C)CN(C)CC4=CC=NC=C4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C=CCN1C(=NN=C1SCC(=O)NC2=CC(=CC=C2)S(=O)(=O)N)COC3=CC=C(C=C3)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=CC=C3)[C@H](C)CO)C)CN(C)CC4=CC=NC=C4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('N=1N(C(=CC1Br)C(=O)NC2=C(C=C(C=C2C)C#N)C(=O)NC)C=3N=CC=CC3Cl', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CN1CCN(CC1)C(=O)C[C@@H]2C=C[C@H]([C@H](O2)CO)NC(=O)NC3=CC=CC=C3F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CN1[C@H]2CC[C@H](O[C@@H]2COC3=C(C1=O)C=C(C=C3)NC(=O)NC4=CC(=CC=C4)OC)CC(=O)NCCC5=CC=CC=C5', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C#CCN(C)C)O[C@@H]1CN(C)C(=O)NC3=CC=C(C=C3)OC)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1CN(CCN1C2CC(=O)N(C2=O)C3=CC=C(C=C3)F)C4=CC=CC(=C4)C(F)(F)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1C2C=CC1C3C2C(=O)N(C3=O)C4=CC=C(C=C4)C(=O)NC5=CC=C(C=C5)C6=NC7=CC=CC=C7O6', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC(C)C)[C@H](C)CO)C)CN(C)C(=O)NC3=CC=CC=C3', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN([C@@H](COC2=C(C=CC(=C2)NC(=O)NC3=CC=CC=C3F)C(=O)N(C[C@H]1OC)C)C)CCC(F)(F)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1CC1C(=O)OCC(=O)NC2=CC=C(C=C2)OC3=CC=CC=C3', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC(=CC=C1)N2C(=O)C3=CC=CC=C3C(=CC4=CC(=CC=C4)OC)C2=O', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('COC1=CC=CC(=C1)NC(=O)N2C[C@H]3[C@H]([C@H](N3C(=O)C2)CO)C4=CC=C(C=C4)C#CCC5CCCC5', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CN1C(C(N(C1=O)C)NC(=O)NC2=CC=CC=C2)NC(=O)NC3=CC=CC=C3', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=C(C=C3)F)[C@@H](C)CO)C)CNC', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('COC1=CC(=C(C=C1NC(=O)C2=NOC(=C2)C3CC3)OC)Cl', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('CN1C2=C(C(=CC=C2)OC)C(=C(C1=O)C(=O)N(C)C3=CC=C(C=C3)C(F)(F)F)O', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)NC(=O)NC3=CC=C(C=C3)C(F)(F)F)O[C@@H]1CN(C)CC4CC4)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C=1C=CC=C(C1NC(C)=O)OS(O)(=O)=O', 'Found anilide group: "
               "aromatic ring connected to N-C(=O)'), "
               "('CC(C)NC(=O)NCC[C@@H]1CC[C@H]([C@@H](O1)CO)NC(=O)NC2=CC=CC=C2', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)NC3=CC=C(C=C3)C(F)(F)F)O[C@H]1CN(C)S(=O)(=O)C4=CC=CC=C4)[C@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1CCN2[C@@H](CN(C1)C(=O)NC3=CC=C(C=C3)F)[C@H]([C@@H]2CO)C4=CC=C(C=C4)C5=CC=C(C=C5)C#N', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CN(C)C(=O)C[C@@H]1C[C@@H]2[C@H]([C@H](O1)CO)OC3=C2C=C(C=C3)NC(=O)NC4=CC=C(C=C4)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@@H]1CN(C)C(=O)NC4=CC=CC=C4OC)C5=CC=CC=C5N2C)[C@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1=CC=C(C(=C1)NC(=O)C2=C(N=CN2)C(=O)NC3=CC=C(C=C3)F)[N+](=O)[O-]', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H](CN(CC1=CC=CC=C1Cl)[C@H](C)CO)[C@H](CN(C)C(=O)NC2=CC=C(C=C2)C(F)(F)F)OC', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC=C(C=C1)N2C(=O)CC(C2=O)SC3=NC=NN3', 'Found anilide "
               "group: aromatic ring connected to N-C(=O)'), "
               "('Cn1cc(C(=O)Nc2ccccc2[C@@H]2C[C@H]2C2CC2)c(n1)C(F)F', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1C[C@@H]([C@@H](O[C@@H]1CCNC(=O)C2=CC=CC=C2F)CO)NC(=O)NC3=CC=C(C=C3)C(F)(F)F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN(C(=O)CCCN2C=C(CO[C@H]1CN(C)C(=O)NC3=CC(=CC=C3)OC4=CC=CC=N4)N=N2)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1[C@@H](O[C@H]([C@@H]2[C@H]1C3=C(O2)C=CC(=C3)NC(=O)NC4=CC=C(C=C4)C(F)(F)F)CO)CC(=O)NCC5=CC=CC=N5', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1=CC=C2C(=C1)N=C(N2CC(=O)NC3=CC=CC=C3F)C4=CSC=N4', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC=C(C=C1)NC(=O)C2=CC=CC=C2NC(=O)C3=CN=CC=C3', 'Found "
               "anilide group: aromatic ring connected to N-C(=O)'), "
               "('CSC1=C(C=CC=N1)C(=O)OCC(=O)NC2=C(C=CC(=C2)C(F)(F)F)N3CCOCC3', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CCCC1=CN(N=N1)CC[C@H]2CC[C@@H]([C@@H](O2)CO)NC(=O)NC3=CC=CC=C3F', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC(=NN1)CN2CCCC(C2)C(=O)NC3=CC=C(C=C3)C4=NC5=CC=CC=C5N4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1CCC(C1)(C2=CN(N=N2)CC[C@@H]3CC[C@H]([C@H](O3)CO)NC(=O)NC4=CC=C(C=C4)Cl)O', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('S(=O)(=O)(CC[C@H](NC(=O)C1=NC=2C(=O)N(C(=O)N(C2N=C1)C)C)C(=O)NC3=C(C(=O)OC)C=CC=C3)C', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN(C(=O)C2=C(C=CC(=C2)N(C)C)O[C@@H]1CN(C)C(=O)NC3=CC=C(C=C3)OC)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC=CC1=CC2=C(C=C1)S(=O)(=O)N(C[C@H]([C@@H](O2)CN(C)C(=O)NC3=CC(=CC=C3)F)C)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CN(C)C(=O)[C@H]1[C@@H]([C@H]2CN3C(=CC=C(C3=O)C4=CCCC4)[C@@H]1N2C(=O)NC5=CC=CC=C5)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('CC1=CC=C(C=C1)S(=O)(=O)N(C)C[C@H]([C@@H](C)CN([C@H](C)CO)C(=O)NC2=CC=CC=C2F)OC', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)NC3=CC=C(C=C3)C(F)(F)F)O[C@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)F)[C@@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H](C1=CC=CC=C1)NC(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC(=CC=C4)Cl)O', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)NC3=CC=C(C=C3)F)O[C@H]1CN(C)CC4CCCCC4)[C@H](C)CO', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H](C#CC1=CC=C(C=C1)[C@H]2[C@@H]3CN(CCCCN3[C@@H]2CO)C(=O)NC4=CC=CC=C4)O', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1=CC(=CC(=C1)N2C=CC=C2C=C3C(=O)N(C(=O)N3)C4=CC(=CC=C4)Cl)C(=O)O', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('COC1=CC=CC=C1NC(=O)N[C@@H]2CC[C@H](O[C@@H]2CO)CCN3C=C(N=N3)C4=CN=CC=C4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=C(C=C3)F)[C@H](C)CO)C)CN(C)CC4CCCCC4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C1CC(C1)NC(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC(=C(C=C4)Cl)Cl)O', "
               "'Found anilide group: aromatic ring connected to N-C(=O)'), "
               "('C[C@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)NC3=C(C=CC(=C3)F)F)C(=O)N(C[C@H]1OC)C)C)C(=O)C4=CC=CC=N4', "
               "'Found anilide group: aromatic ring connected to N-C(=O)')]\n"
               "False negatives: [('CC(C)N(C(=O)C(O)=O)c1ccccc1', 'No anilide "
               "group found'), "
               "('OC1=CC=C(Cl)C=C1C(=O)NC1=C(Cl)C=C(C=C1)[N+]([O-])=O', 'No "
               "anilide group found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 32,
    'num_false_positives': 100,
    'num_true_negatives': 7649,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.24242424242424243,
    'recall': 1.0,
    'f1': 0.3902439024390244,
    'accuracy': 0.9871481814676777}