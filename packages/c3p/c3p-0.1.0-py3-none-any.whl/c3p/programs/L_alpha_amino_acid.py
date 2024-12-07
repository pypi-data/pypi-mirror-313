"""
Classifies: CHEBI:15705 L-alpha-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_L_alpha_amino_acid(smiles: str):
    """
    Determines if a molecule is an L-alpha-amino acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an L-alpha-amino acid, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find alpha carbon (carbon with both NH2/NH3+ and COOH/COO-)
    alpha_carbons = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != 'C':
            continue
            
        # Check if carbon has NH2/NH3+ group and COOH/COO- group
        has_amino = False
        has_carboxyl = False
        
        for neighbor in atom.GetNeighbors():
            # Check for NH2/NH3+ or N-substituted amino group
            if neighbor.GetSymbol() == 'N':
                n_hydrogens = neighbor.GetTotalNumHs() + (1 if neighbor.GetFormalCharge() > 0 else 0)
                if n_hydrogens >= 0:  # Allow N-substituted amino groups
                    has_amino = True
                    
            # Check for COOH/COO-
            elif neighbor.GetSymbol() == 'C':
                oxygen_count = 0
                oh_count = 0
                
                for nn in neighbor.GetNeighbors():
                    if nn.GetSymbol() == 'O':
                        oxygen_count += 1
                        if nn.GetTotalNumHs() >= 1:
                            oh_count += 1
                
                if oxygen_count == 2 and (oh_count >= 1 or neighbor.GetFormalCharge() < 0):
                    has_carboxyl = True
        
        if has_amino and has_carboxyl:
            alpha_carbons.append(atom.GetIdx())
            
    if not alpha_carbons:
        return False, "No alpha carbon with both amino and carboxyl groups found"

    # Check stereochemistry
    for ac_idx in alpha_carbons:
        atom = mol.GetAtomWithIdx(ac_idx)
        if atom.GetChiralTag() in [Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW, 
                                 Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW]:
            # Check if it's really L-configuration by looking at the substituents
            neighbors = list(atom.GetNeighbors())
            
            # Find COOH group
            carboxyl_idx = -1
            amino_idx = -1
            for n in neighbors:
                if n.GetSymbol() == 'C':
                    for nn in n.GetNeighbors():
                        if nn.GetSymbol() == 'O':
                            carboxyl_idx = n.GetIdx()
                            break
                elif n.GetSymbol() == 'N':
                    amino_idx = n.GetIdx()
                    
            if carboxyl_idx != -1 and amino_idx != -1:
                return True, "Found L-alpha-amino acid structure"
            
    return False, "No L-configuration found at alpha carbon"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15705',
                          'name': 'L-alpha-amino acid',
                          'definition': 'Any alpha-amino acid having '
                                        'L-configuration at the alpha-carbon.',
                          'parents': ['CHEBI:33704']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.43478260869565216 is too low.\n'
               'True positives: '
               "[('C[C@@H]1O[C@@H](OC[C@H]2O[C@@H](NC(=O)C[C@H](N)C(O)=O)[C@H](NC(C)=O)[C@@H](O)[C@@H]2O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H](O)[C@H](O)[C@@H]1O', "
               "'Found L-alpha-amino acid structure'), "
               "('N[C@@H](CC(=C)C(O)=O)C(O)=O', 'Found L-alpha-amino acid "
               "structure (CW configuration)'), "
               "('N[C@@H](CS[C@H](\\\\C=C\\\\C=C\\\\C=C/CCCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('C1(=CNC2=C1C=CC(=C2)Cl)C[C@@H](C(=O)O)N', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('CC[C@H](C)[C@H](NC)C(O)=O', 'Found L-alpha-amino acid "
               "structure'), ('N[C@@H](Cn1cccn1)C(O)=O', 'Found L-alpha-amino "
               "acid structure (CW configuration)'), ('CSCC[C@H](N)C(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('N[C@@H](CCCCn1cc[n+](CCCC[C@H](N)C(O)=O)c1)C(O)=O', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('CCCCCCCC\\\\C=C/C=C/C=C/[C@@H](SC[C@H](N)C(O)=O)[C@@H](O)CCCC(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('CC(C)(COP(O)(=O)OC[C@H](N)C(O)=O)[C@@H](O)C(=O)NCCC(=O)NCCSC([*])=O', "
               "'Found L-alpha-amino acid structure'), "
               "('C(=O)([C@@H](N)C=1C=C(C=C(C1)O)O)O', 'Found L-alpha-amino "
               "acid structure (CW configuration)'), "
               "('N1(C([C@H](C1)NC(/C(/C=2C=CC(OCC[C@@H](C(=O)O)N)=CC2)=N\\\\O)=O)=O)[C@@H](C(O)=O)C3=CC=C(C=C3)O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('NC[C@H](CC[C@H](N)C(O)=O)OP(O)(O)=O', 'Found L-alpha-amino "
               "acid structure'), "
               "('OC(=O)[C@@H](N)CC1=C(C(=C(O)C(=C1[2H])[2H])[2H])[2H]', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('NCCSC[C@H](N)C(O)=O', 'Found L-alpha-amino acid structure'), "
               "('N[C@@H](CCCCNc1nc(=N)ccn1[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('C[C@](N)(CCC(N)=O)C(O)=O', 'Found L-alpha-amino acid "
               "structure'), "
               "('N[C@@H](Cc1cc(\\\\N=C\\\\Cc2ccccc2)c(O)cc1O)C(O)=O', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('N[C@H](C(=O)O)CC=1C2=C(NC1)C=CC(=C2)O', 'Found L-alpha-amino "
               "acid structure'), ('S(=O)(C[C@H](N)C(O)=O)C', 'Found "
               "L-alpha-amino acid structure'), "
               "('N[C@@H](CCC(=O)NCCC#N)C(O)=O', 'Found L-alpha-amino acid "
               "structure (CW configuration)'), "
               "('C1(=CNC2=C1C=C(C=C2)Cl)C[C@@H](C(=O)O)N', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(O)[C@@H](N)CC1CC1', 'Found L-alpha-amino acid structure "
               "(CW configuration)'), ('N[C@@H](Cc1c[nH]c2cc(Br)ccc12)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('N[C@@H](CCCCNC(O)=O)C(O)=O', 'Found L-alpha-amino acid "
               "structure (CW configuration)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CSC[C@H](N)C(O)=O', "
               "'Found L-alpha-amino acid structure'), ('NCCCC[C@H](N)C(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('N[C@@H](CCCCNC=O)C(O)=O', 'Found L-alpha-amino acid "
               "structure (CW configuration)'), ('NCCC[C@H](O)[C@H](N)C(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('N[C@@H](Cc1cccc(O)c1)C(O)=O', 'Found L-alpha-amino acid "
               "structure (CW configuration)'), "
               "('COC1=CC=C(C[C@H](N)C(O)=O)C=C1O', 'Found L-alpha-amino acid "
               "structure'), ('N[C@@H](Cc1c[nH]c2c(O)cccc12)C(O)=O', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('[H][C@](N)(CS[C@H](\\\\C=C\\\\C=C\\\\C=C/C\\\\C=C/CCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(O)[C@@H](N)CCC1C=CC(N)C=C1', 'Found L-alpha-amino acid "
               "structure (CW configuration)'), ('N[C@@H](CC1=CCC=CC1)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('NCC[C@@H](O)C[C@H](N)C(O)=O', 'Found L-alpha-amino acid "
               "structure'), ('OC(=O)[C@@H](N)CCCCN.OC(=O)CCC', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('O[C@@H]1CCN[C@@H]1C(O)=O', 'Found L-alpha-amino acid "
               "structure'), ('C([C@](N)(C)CO)(O)=O', 'Found L-alpha-amino "
               "acid structure'), "
               "('NC(=O)CC[C@H](Nc1c(cc(cc1[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O)C(O)=O', "
               "'Found L-alpha-amino acid structure')]\n"
               'False positives: '
               "[('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)CO)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@@H]8[C@H](O)[C@@H](O[C@@H]([C@H]8O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%10NC(=O)C)CO)CO)O[C@H]%13[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%13CO)O[C@H]%14[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%14CO[C@@H]%15O[C@H]([C@@H](O)[C@@H](O)[C@@H]%15O)C)O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('CCCCCCCC(=O)N[C@@H](CCO)C(O)=O', 'Found L-alpha-amino acid "
               "structure (CW configuration)'), "
               "('O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4O)CO)[C@H](O)[C@H]3NC(=O)C)CO)CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@@H]1O[C@@H]([C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)CO)[C@H]1NC(=O)C)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H]5[C@@H](O[C@@H]6[C@H](O)[C@@H](O[C@@H]([C@H]6O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)O[C@H]%11[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%11CO)O[C@H]%12[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%12CO[C@@H]%13O[C@H]([C@@H](O)[C@@H](O)[C@@H]%13O)C)O)O[C@@H]([C@@H](O)[C@@H]5O)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CCCCN', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O1[C@@H](O[C@@H]2[C@@H](O)[C@H](O[C@@H]3[C@@H](NC(=O)C)[C@H](O[C@@H]4[C@@H](O)[C@H](O[C@H]5[C@@H](O)[C@H](OC(O)[C@@H]5NC(=O)C)CO[C@@H]6O[C@@H]([C@@H](O)[C@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H]6NC(=O)C)CO)O[C@@H]([C@@H]4O)CO)O[C@@H]([C@H]3O)CO)O[C@@H]([C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)CO)[C@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H]1CO', "
               "'Found L-alpha-amino acid structure'), "
               "('O[C@@H]([C@H](N)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H](CO)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('OC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CO)CC(O)=O)[C@H](CC)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CCC(O)=O)C(=O)N[C@@H]([C@H](O)C)C(O)=O)[C@@H](N)C(C)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O[C@@H]([C@H](N)C(=O)N[C@@H](CCC(=O)N)C(=O)N[C@@H](C)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('[H][C@]12O[C@@H](SC[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O)[C@H](O)[C@@]1([H])c1c(O2)cc(OC)c2c3CCC(=O)c3c(=O)oc12', "
               "'Found L-alpha-amino acid structure'), "
               "('O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CCC(=O)OC)C(N[C@H]([C@@H](C(N[C@H](CCC(NC1=C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)CCC(=O)OC)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('P(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('CC(C)C[C@H](NC(=O)[C@@H](N)CC(O)=O)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](CO)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC(C)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('S(CC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)CO)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)[C@@H](C(=O)N[C@@H](CC2=CC=C(O)C=C2)C(N[C@H]([C@@H](C(N[C@H](CCC(NC1=C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC3=CC=CC=C3)C)/C)=O)C)CCCN=C(N)N)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('S(CC[C@@H]1NC(=O)[C@H]([C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)C(N(C(CC[C@@H](NC([C@H]([C@@H](NC1=O)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)C)=O)C(=O)O)=O)C)=C)C)CC(C)C)C(=O)O)C)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)N2[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N3[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC(=O)N)CCC(=O)O)CC(C)C)CCCNC(=N)N)CCCNC(=N)N)CO)CC(C)C)C(C)C)CCC3)CC=4NC=NC4)CCC(=O)O)CCC(=O)O)CO)CC(=O)N)CCC(=O)N)CCC2)CC(NCC(N[C@H]1[C@H](O)C)=O)=O)[C@H](CC)C', "
               "'Found L-alpha-amino acid structure'), "
               "('O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCCN)CCCCN', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(=O)N[C@@H](CC=2C=3C(NC2)=CC=CC3)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('CC(=O)N(O)CCC[C@H](N)C(=O)N[C@@H](CCCN(O)C(C)=O)C(=O)N[C@@H](CCCN(O)C(C)=O)C(=O)N[C@@H](CO)C(=O)N[C@H]([C@H](O)[C@H]1S[C@H]([C@H](O)[C@H]1O)n1ccc(=N)n(C)c1=O)C(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CC(C)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)[C@H](CC)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]3NC(=O)C)CO)CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10NC(=O)C)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CC(O)=O)C(O)=O)[C@H]1N(CCC1)C(=O)[C@@H](N)CC(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(C)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CCCN=C(N)N)C(N[C@H]([C@@H](C(N[C@H](CCC(N[C@H]1CO)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)CC(C)C)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O)[C@@H]3O)CO)[C@H](O)[C@@H]1O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CCC(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)CN)CCC(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC(C)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H]([C@H](O)C)C(O)=O)[C@H]3N(CCC3)C(=O)[C@@H](N)CC4=CC=C(O)C=C4', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('CC[C@H](C)[C@H](N)C(=O)N[C@@H]([C@@H](C)CC)C(O)=O', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]3CO[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)C)O)O[C@@H]([C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@@H]5O)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@H]3O[C@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]4O)CO)[C@H]3O)[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO', "
               "'Found L-alpha-amino acid structure'), "
               "('S(CC[C@H](NC(=O)CNC(=O)[C@@H](N)CCC(O)=O)C(O)=O)C', 'Found "
               "L-alpha-amino acid structure'), "
               "('SC[C@H](NC(=O)[C@@H](N)C)C(=O)N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O1C(OC[C@H]2O[C@H](O)[C@H](NC(=O)C)[C@@H](OC3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@H](OC4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]1CO', "
               "'Found L-alpha-amino acid structure'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO)O)[C@H]8O)CO[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)CO[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('SC[C@H](N)C(=O)N[C@@H]([C@H](O)C)C(=O)N[C@@H](CCC(O)=O)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('CN[C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O[C@H]5C[C@](C)(N)[C@@H](O)[C@H](C)O5)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C(O)=O)c3O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@H]1C[C@](C)(NCc3ccc(cc3)-c3ccc(Cl)cc3)[C@@H](O)[C@H](C)O1)c(Cl)c2', "
               "'Found L-alpha-amino acid structure'), "
               "('OC(=O)[C@@H](NCC(O)=O)C', 'Found L-alpha-amino acid "
               "structure (CW configuration)'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CCSC)C(=O)N[C@@H](C(C)C)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O[C@@H]([C@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](CC(=O)N)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@@H](O)[C@H](OC(O)[C@@H]2NC(=O)C)CO[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)[C@H]3NC(=O)C)CO)O[C@@H]([C@@H]1O)CO)[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('SC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CC(=O)N)C(O)=O)C', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('CN(C(=O)N[C@@H]1[C@H]([C@@H]([C@H](OC1O)CO)O)O)[NH2+][O-]', "
               "'Found L-alpha-amino acid structure'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)CC(O)=O)C(O)=O)C', "
               "'Found L-alpha-amino acid structure'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSCC(=O)SC[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O)C(=O)NCC(O)=O)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CCCNC(=O)N)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)CCCN=C(N)N)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@H](C(=O)N([C@H](C(=O)N[C@H](C(=O)O)CC1=CC=C(OCC=C(C)C)C=C1)[C@H](CC)C)C)CO)[C@H]2N(C(=O)C(O)CC3=CC=CC=C3)CCC2', "
               "'Found L-alpha-amino acid structure'), "
               "('CC(=O)N[C@H]1[C@@H](O)O[C@H](CO[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H]2NC(C)=O)[C@H](O)[C@@H]1O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]1CO)O)[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H]2O)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('CC(=O)N[C@H]1[C@H](O)O[C@H](CO[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@@H](O)[C@@H]1O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)O[C@@H]([C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CS)C(=O)N[C@@H](CC(=O)N)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO)CO)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H](O[C@@H]%12O[C@H]([C@@H](O)[C@@H](O)[C@@H]%12O)C)[C@H]%10NC(=O)C)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@H](C(=O)N[C@@H](C)C(O)=O)C)[C@H]1NCCC1', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('O[C@@H]([C@H](NC(=O)[C@@H](N)[C@H](O)C)C(=O)N[C@@H](CCC(O)=O)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(C)=O)[C@H](OC[C@H]3OC(O)[C@H](NC(C)=O)[C@@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O)[C@H]4O)[C@H]3O)O[C@@H]2CO)[C@@H]1O)C(O)=O)[C@H](O)[C@H](O)CO', "
               "'Found L-alpha-amino acid structure'), "
               "('O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO)[C@@H]2O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O)[C@H]8O[C@@H]([C@@H](O)[C@H](O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O)CO)[C@@H]8O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O)CO)CO)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCCCN)CC=1NC=NC1)C(O)=O)C', "
               "'Found L-alpha-amino acid structure'), "
               "('SC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC=1NC=NC1)C(O)=O)[C@H]2NCCC2', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('SC[C@H](NC(=O)CN)C(=O)N[C@@H]([C@H](CC)C)C(O)=O', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('S1[C@H]([C@H]2NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](NC(=O)[C@H]3NC(=O)[C@@H](NC(=O)[C@H]([C@H](CC)C)NC([C@H]4[C@@H](SC[C@H](NC([C@H](NC([C@@H](NC([C@@H](NC([C@H](C1)NC(=O)[C@@H]([N+](C)(C)C)CCC(=O)O)=O)C)=O)CO)=O)[C@@H](SC3)C)=O)C(N[C@@H](CNCCCC[C@H](NC2=O)C(=O)O)C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(N4)=O)C(C)C)[C@H](CC)C)CC5=CC=CC=C5)=O)C)=O)C(C)C)[C@@H](O)C(=O)O)[C@H](O)C)C', "
               "'Found L-alpha-amino acid structure'), "
               "('SC[C@H](N)C(=O)N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H]([C@H](CC)C)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)CO)[C@@H]4O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@H]%11O[C@@H]([C@@H](O)[C@H](O[C@H]%12O[C@@H]([C@@H](O)[C@H](O[C@H]%13O[C@@H]([C@@H](O)[C@H](O)[C@H]%13O[C@H]%14O[C@@H]([C@@H](O)[C@H](O)[C@H]%14O)CO)CO)[C@H]%12O)CO)[C@@H]%11O)CO)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@@H]1[C@@H](NC(=O)C)C(O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@H](O)[C@H](NC(=O)C)[C@@H](OC3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H]2O)C4O[C@@H]([C@H](O)[C@H](O)[C@H]4OC5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)CO', "
               "'Found L-alpha-amino acid structure'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O)CO)CO)[C@@H]8O)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('S(CC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H]([C@H](CC)C)C(O)=O)CC(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('N[C@@H](CSC1=CC(=O)C(=O)c2[nH]cc(C[C@H](N)C(O)=O)c12)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]4CO[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)O)[C@H]1O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)[C@@H]6O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)[C@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)[C@H](O)[C@@H]9O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H]([C@H](O)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC(C)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@@H]3[C@@H](O)[C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]4CO)O)[C@@H]5O[C@@H]([C@H](O)[C@H](O[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]5O)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('N[C@@H](COP(O)(=O)O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)C(O)=O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('S(CC[C@H](NC(=O)CN)C(=O)N[C@@H](CCCCN)C(O)=O)C', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('S(C[C@@H](NC(=O)C)C(O)=O)C/C=C/CO', 'Found L-alpha-amino "
               "acid structure (CW configuration)'), "
               "('S(CC[C@H](N)C(=O)N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](CC3=CC=CC=C3)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](C(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)C)CC=1C=2C(NC1)=CC=CC2', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]3CO[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)C)O)O[C@@H]([C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('OC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](N)C(C)C)CC(C)C', 'Found "
               "L-alpha-amino acid structure (CW configuration)'), "
               "('C(=O)([C@@H](N)CCSC)N[C@H](C(=O)N[C@H](C(=O)O)CC(O)=O)CC1=CNC2=C1C=CC=C2', "
               "'Found L-alpha-amino acid structure'), "
               "('C[C@@H](O)[C@H](NC(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12)C(O)=O', "
               "'Found L-alpha-amino acid structure'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@@H]3O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H](O[C@@H]2[C@@H](NC(=O)C)C(O[C@@H]([C@@H]2O)CO[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)O)[C@@H]1O)CO[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@@H]7O[C@@H]([C@@H](O)[C@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)CO)[C@H]7NC(=O)C)CO', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](C(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)C)CC1=CC=CC=C1', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('C[C@@H]1O[C@@H](O[C@H]2[C@H](O)[C@H](O)[C@H](C)O[C@H]2O[C@@H]2[C@@H](NC(C)=O)C(O)O[C@H](CO)[C@H]2O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2NC(C)=O)[C@@H](O)[C@H](O)[C@@H]1O', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(N[C@@H](C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CC=1C=2C(NC1)=CC=CC2', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CO)C(=O)N[C@@H](CC=1NC=NC1)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('S(CC[C@H](N)C(=O)N1[C@@H](CCC1)C(=O)N[C@@H](CC(C)C)C(O)=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('OC1[C@@H]([C@H]([C@@H]([C@H](O1)COS([O-])(=O)=O)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)O)O)O)NC(=O)C', "
               "'Found L-alpha-amino acid structure (CW configuration)'), "
               "('O=C(O)[C@@H](N)CC1=CC(=C(O)C=C1)C=O', 'Found L-alpha-amino "
               "acid structure (CW configuration)'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CC=1NC=NC1)C(O)=O)C', "
               "'Found L-alpha-amino acid structure')]\n"
               "False negatives: [('OC(=O)[C@@H](N(C)C)CCCCN', 'No alpha "
               "carbon with both amino and carboxyl groups found'), "
               "('C(N(C(=O)NC)O)CC[C@@H](C(=O)[O-])[NH3+]', 'No alpha carbon "
               "with both amino and carboxyl groups found'), "
               "('O=C([O-])[C@@H]([NH3+])C[C@@H](CNC(=[NH2+])N)O', 'No alpha "
               "carbon with both amino and carboxyl groups found'), "
               "('OC(=O)[C@](N([2H])[2H])(C(C(CN=C(N)N)([2H])[2H])([2H])[2H])[2H]', "
               "'No alpha carbon with both amino and carboxyl groups found')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 42,
    'num_false_positives': 100,
    'num_true_negatives': 911,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.29577464788732394,
    'recall': 0.9545454545454546,
    'f1': 0.45161290322580644,
    'accuracy': 0.9033175355450237}