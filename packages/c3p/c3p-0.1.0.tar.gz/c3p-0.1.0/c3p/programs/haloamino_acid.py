"""
Classifies: CHEBI:24470 haloamino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_haloamino_acid(smiles: str):
    """
    Determines if a molecule is a haloamino acid (non-proteinogenic amino acid with at least one halogen).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a haloamino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Split salt forms if present
    fragments = Chem.GetMolFrags(mol, asMols=True)
    main_mol = max(fragments, key=lambda m: m.GetNumAtoms())
    
    # Check for amino acid pattern: has both NH2 and COOH groups
    amino_pattern = Chem.MolFromSmarts('[NX3H2,NX4H3+][CX4]')
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    
    if not (main_mol.HasSubstructMatch(amino_pattern) and main_mol.HasSubstructMatch(carboxyl_pattern)):
        return False, "Missing amino acid backbone structure"

    # Check for halogens in the main molecule
    halogens = ['F', 'Cl', 'Br', 'I']
    found_halogens = []
    
    for atom in main_mol.GetAtoms():
        if atom.GetSymbol() in halogens and atom.GetIsotope() == 0:  # Exclude isotopes
            found_halogens.append(atom.GetSymbol())
            
    if not found_halogens:
        return False, "No halogen atoms found"

    # Check if it's connected to the main structure (not just a salt)
    for halogen in found_halogens:
        halogen_pattern = Chem.MolFromSmarts(f'[{halogen}]-[!Cl&!Br&!F&!I]')
        if main_mol.HasSubstructMatch(halogen_pattern):
            return True, f"Non-proteinogenic amino acid with halogen(s): {', '.join(set(found_halogens))}"
    
    return False, "Halogen present only as counterion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24470',
                          'name': 'haloamino acid',
                          'definition': 'Any non-proteinogenic amino acid '
                                        'carrying at least one halo group.',
                          'parents': ['CHEBI:83820']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.0396039603960396 is too low.\n'
               "True positives: [('N[C@@H](CC1=CC=C(F)C=C1)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): F'), "
               "('N[C@@H](Cc1ccc(O)c(Br)c1)C(O)=O', 'Non-proteinogenic amino "
               "acid with halogen(s): Br')]\n"
               "False positives: [('NC(Cc1c[nH]c2c(Cl)cccc12)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('Cl.NC(CC1C(=O)NC2=CC=CC=C12)C(O)=O', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('N[C@H](Cc1ccc(O)c(F)c1)C(O)=O', 'Non-proteinogenic amino "
               "acid with halogen(s): F'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSC1C=CC(Br)=CC1O)C(=O)NCC(O)=O)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Br'), "
               "('N[C@@H](CS\\\\C(Cl)=C\\\\Cl)C(O)=O', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('C1=C(C=C(C(=C1O)O)Cl)CC(C(=O)O)N', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl'), "
               "('ClC1=CC=2NC=C(C2C=C1)C[C@@H]3NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C[C@H](N)C(=O)O)C(O)C4=CC=C(O)C=C4)CO)CCC(=O)O)C(O)C)COC(=O)[C@H]5N(C([C@@H](NC([C@H](NC3=O)C(C)C)=O)CC6=CC=CC=C6)=O)CC(C)C5O)C(C(=O)N)C', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('IC=1C=C(C[C@@H](N)C(O)=O)C=CC1OC2=CC=C(O)C=C2', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('Cl.NCCCC[C@H](N)C(O)=O', 'Non-proteinogenic amino acid with "
               "halogen(s): Cl'), ('[I-].[S+](CC[C@H](N)C(O)=O)(C)C', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('N[C@@H](CN1C=C(F)C(=O)NC1O)C(O)=O', 'Non-proteinogenic amino "
               "acid with halogen(s): F'), "
               "('N[C@@H](Cc1cc(O)c(O)cc1[18F])C(O)=O', 'Non-proteinogenic "
               "amino acid with halogen(s): F'), "
               "('FC1=CC=2NC=C(CC(N)C(O)=O)C2C=C1', 'Non-proteinogenic amino "
               "acid with halogen(s): F'), "
               "('ClCCSC[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('FC=1C(C(N)C(O)=O)=CC=CC1', 'Non-proteinogenic amino acid "
               "with halogen(s): F'), "
               "('C1(=CNC2=C1C=C(C=C2)Cl)C[C@@H](C(=O)O)N', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('C1=CC(=CC=C1CC(C(=O)O)N)Cl', 'Non-proteinogenic amino acid "
               "with halogen(s): Cl'), "
               "('C1=CC(=CC=C1NC(=O)CC(C(=O)O)N)OC2=CC(=C(C=C2Br)F)F', "
               "'Non-proteinogenic amino acid with halogen(s): F, Br'), "
               "('IC1=C(O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)C=CC(OC3=C(I)C=C(C[C@H](N)C(O)=O)C=C3I)=C1', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('C1(=CNC2=C1C=CC(=C2)Cl)CC(C(=O)O)N', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('ClC=1C=2C(CC(N)C(O)=O)=CNC2C=CC1', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl'), "
               "('N[C@@H](CS\\\\C(Cl)=C/Cl)C(O)=O', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl'), "
               "('N[C@@H](Cc1cc(I)c(Oc2ccc(OS(O)(=O)=O)c(I)c2)c(I)c1)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('Cl.Cl.CC(=N)NCCCC[C@H](N)C(O)=O', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl'), ('ClC(Cl)C[C@H](N)C(=O)O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('N[C@H](C(O)=O)CC1=CC(Cl)=C(C(Cl)=C1)OCC2=C3OC(C4=CC=CC=C4)=NC3=CC(N)=C2.Cl.Cl', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('N[C@@H](Cc1ccc(cc1)N(CCCl)CCCl)C(O)=O', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('P(N(CCCl)CCCl)(N(CCCl)CCCl)(OCCS(C[C@@H](C(N[C@@H](C(O)=O)C1=CC=CC=C1)=O)NC(CC[C@@H](C(O)=O)N)=O)(=O)=O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('Cl.NCCC[C@@H](N)C(O)=O', 'Non-proteinogenic amino acid with "
               "halogen(s): Cl'), "
               "('N[C@@H](CCCNC(N)=N)C(O)=O.OC(=O)C[C@H]1CCC2=C1NC1=C2C=C(OCC2=CC(=C(C=C2)C2CCCC2)C(F)(F)F)C=C1', "
               "'Non-proteinogenic amino acid with halogen(s): F'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSC(O)C(Cl)Cl)C(=O)NCC(O)=O)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSCCl)C(=O)NCC(=O)O)C(=O)O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSC1C(O)C=CC=C1Br)C(=O)NCC(O)=O)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Br'), "
               "('C1(=CNC2=C1C=CC(=C2Cl)Cl)C[C@@H](C(=O)O)N', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('N[C@@H](Cn1cc(F)c(=O)[nH]c1=O)C(O)=O', 'Non-proteinogenic "
               "amino acid with halogen(s): F'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSCCN(CCCl)c1ccc(CC(N)C(O)=O)cc1)C(=O)NCC(O)=O)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('NC(Cc1ccc(O)c(Br)c1)C(O)=O', 'Non-proteinogenic amino acid "
               "with halogen(s): Br'), ('Cl.OC(=O)[C@@H](N)CCCN', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('ClC(=C)CC[C@H](N)C(=O)O', 'Non-proteinogenic amino acid with "
               "halogen(s): Cl'), ('C(C(C(O)=O)N)C1=CC=CC=C1F', "
               "'Non-proteinogenic amino acid with halogen(s): F'), "
               "('C([C@@H](C(O)=O)N)C1=CC=CC=C1F', 'Non-proteinogenic amino "
               "acid with halogen(s): F'), "
               "('IC=1C=C(OC2=CC=C(C[C@@H](N)C(O)=O)C=C2)C=CC1OS(O)(=O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('N[C@@H](Cc1c[nH]c2c(Cl)cccc12)C(O)=O', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('C1=CC(=CC=C1O)OC2=C(C=C(C=C2I)C[C@@H](C(=O)O)N)I', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('C([C@H](CS)N)(=O)O.Cl', 'Non-proteinogenic amino acid with "
               "halogen(s): Cl'), ('[H][C@]1(CC(Cl)=NO1)[C@H](N)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('ClC1=NO[C@@H]([C@@H]1O)C(N)C(=O)O', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSC(=O)CCl)C(=O)NCC(O)=O)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('CC(CC(N)C(O)=O)C(F)(F)F', 'Non-proteinogenic amino acid with "
               "halogen(s): F'), "
               "('IC1=C(OC2OC(C(O)C(O)C2O)C(O)=O)C(I)=CC(OC3=C(I)C=C(CC(N)C(O)=O)C=C3I)=C1', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('IC=1C=CC(C[C@H](C(O)=O)N)=CC1', 'Non-proteinogenic amino "
               "acid with halogen(s): I'), ('[Cl-].C[S+](C)CC[C@H](N)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('IC1=CC(CC(N)C(O)=O)=CC(I)=C1OC2=CC=C(O)C=C2', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('ClC1=C(O)C(Cl)=CC(=C1)C(=O)NC(C(=O)O)CC2NC(C(=O)O)(C(O)C(N)C(=O)O)CC2', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('C1(=CNC2=C1C=CC(=C2)Cl)C[C@H](C(=O)O)N', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('NC(NCCC[C@@H](C(O)=O)N)=N.Cl', 'Non-proteinogenic amino acid "
               "with halogen(s): Cl'), "
               "('C1=CC(=C(C=C1OC2=C(C=C(C=C2I)CC(C(=O)O)N)I)I)O', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('IC1=C(O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@@H]2O)C(O)=O)C(I)=CC(OC3=CC=C(C[C@@H](N)C(O)=O)C=C3)=C1', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('C(=O)([C@@H](N)CC(CCN)Cl)O', 'Non-proteinogenic amino acid "
               "with halogen(s): Cl'), ('N[C@@H](Cc1cccc(F)c1)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): F'), "
               "('ClC1=CC(N2N=C(C=C2)C)=C([C@@H](OC3=NC(=NC(C4=CC=C(C[C@H](N)C(O)=O)C=C4)=C3)N)C(F)(F)F)C=C1', "
               "'Non-proteinogenic amino acid with halogen(s): F, Cl'), "
               "('NCCCC[C@H](N)C(O)=O.Cc1c(Cl)cccc1Nc1ncccc1C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('IC=1C=CC(C[C@@H](C(O)=O)N)=CC1', 'Non-proteinogenic amino "
               "acid with halogen(s): I'), "
               "('N(C(=O)C=1C(=NOC1C)C2=C(C=CC=C2F)Cl)[C@@H]([C@@]3(N[C@H](C(S3)(C)C)C(O)=O)[H])C(=O)NCCCC[C@@H](C(=O)O)N', "
               "'Non-proteinogenic amino acid with halogen(s): F, Cl'), "
               "('N[C@@H](CCSC(F)(F)F)C(O)=O', 'Non-proteinogenic amino acid "
               "with halogen(s): F'), ('Cl.NCCCC[C@@H](N)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('N[C@@H](Cc1ccc(OC(=O)c2c[nH]c3cc(Br)c(O)cc23)cc1)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Br'), "
               "('N[C@@H](CCC(=O)N[C@@H](CS\\\\C(Cl)=C/Cl)C(=O)NCC(O)=O)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('NC(Cc1c[nH]c2ccc(F)cc12)C(O)=O', 'Non-proteinogenic amino "
               "acid with halogen(s): F'), ('N[C@@H](Cc1cc(O)c(O)cc1F)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): F'), "
               "('NC(Cc1cc(Br)c(O)c(Br)c1)C(O)=O', 'Non-proteinogenic amino "
               "acid with halogen(s): Br'), ('NC(CF)CCC(N)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): F'), "
               "('NC(Cc1ccc(cc1)N(CCCl)CCCl)C(O)=O', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl'), ('C([C@H](CS)N)(=O)O.Cl.O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSCC(Cl)=O)C(=O)NCC(O)=O)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('Cl/C=C\\\\C[C@H](N)C(=O)O', 'Non-proteinogenic amino acid "
               "with halogen(s): Cl'), "
               "('IC1=C(OC2OC(C(O)C(O)C2O)C(O)=O)C=CC(OC3=C(I)C=C(CC(N)C(O)=O)C=C3I)=C1', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('ClC=1C(C[C@H](N)C(O)=O)=CC=CC1', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl'), ('C([C@H](C(O)=O)N)C1=CC=CC=C1F', "
               "'Non-proteinogenic amino acid with halogen(s): F'), "
               "('C1=C(C(=CC(=C1O)O)Cl)CC(C(=O)O)N', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl'), ('N[C@@H](CC(Cl)=C)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('IC=1C=CC(CC(C(O)=O)N)=CC1', 'Non-proteinogenic amino acid "
               "with halogen(s): I'), ('N[C@@H](CCCCNC(=O)C(F)(F)F)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): F'), "
               "('ClCCN(C1=CC=C(C[C@H](N)C(O)=O)C=C1)CCO', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('C1(=CNC2=C1C=CC(=C2)Cl)C[C@@H](C(=O)O)N', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('Cl.O=C(O)[C@@H](N)C1(CC1)C', 'Non-proteinogenic amino acid "
               "with halogen(s): Cl'), ('BrC1=CC=C(CC(N)C(O)=O)C=C1', "
               "'Non-proteinogenic amino acid with halogen(s): Br'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSC(C(=O)[O-])Cl)C(=O)NCC(O)=O)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('ClC1=C(O)C=CC(=C1)[C@@H](N2C(=O)[C@@H](NC(=O)/C(=N/O)/C3=CC=C(OCC[C@@H](N)C(=O)O)C=C3)C2)C(=O)O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('N[C@@H](Cc1ccc(Oc2ccc(OS(O)(=O)=O)c(I)c2)c(I)c1)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('N[C@H](Cc1c[nH]c2c(Cl)cccc12)C(O)=O', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('IC1=C(OC2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)C(I)=CC(OC3=C(I)C=C(C[C@H](N)C(O)=O)C=C3I)=C1', "
               "'Non-proteinogenic amino acid with halogen(s): I'), "
               "('[H]C(Cl)=C(Cl)SC[C@H](N)C(O)=O', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl'), "
               "('NC(CCC(=O)NC(CSC1CCOP(=O)(N1)N(CCCl)CCCl)C(=O)NCC(O)=O)C(O)=O', "
               "'Non-proteinogenic amino acid with halogen(s): Cl'), "
               "('Cl.Cl.S(/C(=N\\\\CCC[C@H](N)C(O)=O)/N)C', 'Non-proteinogenic "
               "amino acid with halogen(s): Cl'), "
               "('C1=CC(=C(C(=C1CC(C(=O)O)N)Cl)O)O', 'Non-proteinogenic amino "
               "acid with halogen(s): Cl')]\n"
               "False negatives: [('N[14C@]1(C[C@H](F)C1)C(O)=O', 'Missing "
               "amino acid backbone structure')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 72971,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9986315242083368}