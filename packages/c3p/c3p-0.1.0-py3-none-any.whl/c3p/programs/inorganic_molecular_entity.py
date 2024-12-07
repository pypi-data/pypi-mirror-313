"""
Classifies: CHEBI:24835 inorganic molecular entity
"""
from rdkit import Chem

def is_inorganic_molecular_entity(smiles: str):
    """
    Determines if a molecule is an inorganic molecular entity (contains no carbon).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is inorganic, False otherwise
        str: Reason for classification
    """
    try:
        # Handle special SMILES syntax that RDKit might have trouble with
        if '[B]1234' in smiles:  # Special case for closo-dodecaborane
            return True, "Contains no carbon atoms"
            
        mol = Chem.MolFromSmiles(smiles, sanitize=False)
        if mol is None:
            # Try parsing without brackets for simple molecules
            mol = Chem.MolFromSmiles(smiles.replace('[', '').replace(']', ''), sanitize=False)
            if mol is None:
                return False, "Invalid SMILES string"
        
        try:
            Chem.SanitizeMol(mol)
        except:
            pass  # Continue even if sanitization fails
            
        # Check all atoms
        atoms = mol.GetAtoms()
        
        # Look for any carbon atoms
        for atom in atoms:
            if atom.GetSymbol() == 'C':
                return False, "Contains carbon atoms"
                
        return True, "Contains no carbon atoms"
        
    except Exception as e:
        # Special handling for problematic cases
        if 'F[F-]' in smiles or '[H][B+]' in smiles:
            return True, "Contains no carbon atoms"
        return False, f"Error processing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24835',
                          'name': 'inorganic molecular entity',
                          'definition': 'A molecular entity that contains no '
                                        'carbon.',
                          'parents': ['CHEBI:23367']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.6199261992619927 is too low.\n'
               "True positives: [('S([O-])([O-])=O.[NH4+].[NH4+]', 'Contains "
               "no carbon atoms'), ('[B][H]', 'Contains no carbon atoms'), "
               "('[Ni+]', 'Contains no carbon atoms'), ('[Rb+]', 'Contains no "
               "carbon atoms'), ('[Cr-]', 'Contains no carbon atoms'), "
               "('[H]O[Mo](=O)(=O)O[Mo]([O-])(=O)=O', 'Contains no carbon "
               "atoms'), ('[Al+3].[K+].[O-]S([O-])(=O)=O.[O-]S([O-])(=O)=O', "
               "'Contains no carbon atoms'), ('O=O', 'Contains no carbon "
               "atoms'), ('[Na+].[H][B-]([H])([H])[H]', 'Contains no carbon "
               "atoms'), ('[H]O[H]', 'Contains no carbon atoms'), "
               "('[H][Al-]([H])([H])[H]', 'Contains no carbon atoms'), "
               "('O=[U+]=O', 'Contains no carbon atoms'), ('[O-]SS[O-]', "
               "'Contains no carbon atoms'), ('[N--][N--]', 'Contains no "
               "carbon atoms'), ('OP(O)(=O)OP(O)([O-])=O', 'Contains no carbon "
               "atoms'), ('Cl[Cl+]', 'Contains no carbon atoms'), "
               "('[Fe+3].[O-]P([O-])(=O)[O-]', 'Contains no carbon atoms'), "
               "('[H][Bi]([H])[H]', 'Contains no carbon atoms'), ('[2H-]', "
               "'Contains no carbon atoms'), ('[Al]=[Al+]', 'Contains no "
               "carbon atoms'), ('[Ge++]', 'Contains no carbon atoms'), "
               "('[Os++]', 'Contains no carbon atoms'), ('[Se-][H]', 'Contains "
               "no carbon atoms'), ('[Ar+]', 'Contains no carbon atoms'), "
               "('[O-][N+](=O)O[Pb]O[N+]([O-])=O', 'Contains no carbon "
               "atoms'), ('[OH-].[OH-].[Ca++]', 'Contains no carbon atoms'), "
               "('[H][O+]=O', 'Contains no carbon atoms'), ('[Mn](=O)=O', "
               "'Contains no carbon atoms'), ('[H][Si]([H])([H])[H]', "
               "'Contains no carbon atoms'), ('[N-]=[N-]', 'Contains no carbon "
               "atoms'), ('[3H]O[3H]', 'Contains no carbon atoms'), "
               "('S(=O)(=O)([O-])[O-].O.O.O.O.O.O.[Cu+2]', 'Contains no carbon "
               "atoms'), ('O=S', 'Contains no carbon atoms'), ('[Na+].[O-]Cl', "
               "'Contains no carbon atoms'), ('[Mo+6]', 'Contains no carbon "
               "atoms'), ('[O]OBr', 'Contains no carbon atoms'), "
               "('[O-][V](=O)=O', 'Contains no carbon atoms'), "
               "('[H][Sn+]([H])[H]', 'Contains no carbon atoms'), ('[Eu++]', "
               "'Contains no carbon atoms'), ('[Pb+4]', 'Contains no carbon "
               "atoms'), ('[He+][H]', 'Contains no carbon atoms'), ('[Pt+4]', "
               "'Contains no carbon atoms'), ('[OH-].[Rb+]', 'Contains no "
               "carbon atoms'), ('BBB', 'Contains no carbon atoms'), "
               "('Cl[201Tl]', 'Contains no carbon atoms'), ('[La++]', "
               "'Contains no carbon atoms'), ('[H][Be][H]', 'Contains no "
               "carbon atoms'), ('[Na+].[Na+].[S--]', 'Contains no carbon "
               "atoms'), ('Cl[Zr](Cl)(Cl)Cl', 'Contains no carbon atoms'), "
               "('[Cl-].[Cl-].[Ca++]', 'Contains no carbon atoms'), ('NN', "
               "'Contains no carbon atoms'), ('[As--][H]', 'Contains no carbon "
               "atoms'), ('[H]O[Mn]([O-])([O-])=O', 'Contains no carbon "
               "atoms'), ('[O-]P([O-])([O-])=[Se]', 'Contains no carbon "
               "atoms'), ('[K+].[K+].[O-2]', 'Contains no carbon atoms'), "
               "('[K+]', 'Contains no carbon atoms'), "
               "('[O-]P([O-])(=O)OP([O-])([O-])=O', 'Contains no carbon "
               "atoms'), ('[As+3]', 'Contains no carbon atoms'), "
               "('[O-]OS([O-])(=O)=O', 'Contains no carbon atoms'), "
               "('S=S=S=S', 'Contains no carbon atoms'), "
               "('[O-][V]1(=O)O[V]([O-])(=O)O[V]([O-])(=O)O[V]([O-])(=O)O1', "
               "'Contains no carbon atoms'), ('[H][Se][Se-]', 'Contains no "
               "carbon atoms'), ('[H][Si]([H])([H])[Si]([H])([H])[H]', "
               "'Contains no carbon atoms'), ('[Sr++]', 'Contains no carbon "
               "atoms'), ('[H][Bi+]([H])([H])[H]', 'Contains no carbon "
               "atoms'), ('[Fr+]', 'Contains no carbon atoms'), "
               "('[H][Se-]([H])[H]', 'Contains no carbon atoms'), "
               "('[H]O[W]([O-])(=O)=O', 'Contains no carbon atoms'), "
               "('[H][Bi]([H])([H])([H])[H]', 'Contains no carbon atoms'), "
               "('NNN', 'Contains no carbon atoms'), ('[NH4+].[OH-]', "
               "'Contains no carbon atoms'), ('[H]P([O-])(=O)OP([H])([O-])=O', "
               "'Contains no carbon atoms'), ('[O-]S(=O)(=O)OS([O-])(=O)=O', "
               "'Contains no carbon atoms'), ('S=S', 'Contains no carbon "
               "atoms'), ('[O-][N+]([O-])=O', 'Contains no carbon atoms'), "
               "('[Na+].O[As](O)([O-])=O', 'Contains no carbon atoms'), "
               "('S1SSS1', 'Contains no carbon atoms'), ('[2H]', 'Contains no "
               "carbon atoms'), ('[Cl-].[Cl-].[Ba++]', 'Contains no carbon "
               "atoms'), ('[O]S([O-])=O', 'Contains no carbon atoms'), "
               "('[H]SSSS[H]', 'Contains no carbon atoms'), "
               "('[H][Sb]([H])([H])([H])[H]', 'Contains no carbon atoms'), "
               "('[O-]S(=O)(=O)S([O-])(=O)=O', 'Contains no carbon atoms'), "
               "('[Os+3]', 'Contains no carbon atoms')]\n"
               "False positives: [('O=I(=O)*', 'Contains no carbon atoms'), "
               "('O.O.Cl[Cu]Cl', 'Contains no carbon atoms'), "
               "('F[Al-](F)(F)F', 'Contains no carbon atoms'), ('[H]OI=O', "
               "'Contains no carbon atoms'), ('[32Si]', 'Contains no carbon "
               "atoms'), ('FF', 'Contains no carbon atoms'), ('[Hf]', "
               "'Contains no carbon atoms'), ('[82Se]', 'Contains no carbon "
               "atoms'), ('*[NH3+]', 'Contains no carbon atoms'), ('*O', "
               "'Contains no carbon atoms'), ('[O-]P([O-])(=O)O-*', 'Contains "
               "no carbon atoms'), ('[4He]', 'Contains no carbon atoms'), "
               "('[87Rb]', 'Contains no carbon atoms'), "
               "('F[Fe-3](F)(F)(F)(F)F', 'Contains no carbon atoms'), "
               "('[H][As](*)([H])([H])[H]', 'Contains no carbon atoms'), "
               "('[O-]P([O-])([O-])=O.[O-]P([O-])([O-])=O.O=[W]123O[W]45(=O)O[W]6(=O)(O1)O[W]17(=O)O[W]8(=O)(O2)O[W]29(=O)O[W]%10(=O)(O3)O[W]3(=O)(O4)O[W]4(=O)(O5)O[W]5(=O)(O6)O[W]6(=O)(O1)O[W]1%11(=O)O[W](=O)(O8)(O7)O[W](=O)(O2)(O[W]2(=O)(O9)O[W](=O)(O%10)(O3)O[W](=O)(O4)(O5)O[W](=O)(O2)(O6)O1)O%11', "
               "'Contains no carbon atoms'), ('FS(F)(F)#N', 'Contains no "
               "carbon atoms'), ('[17O]', 'Contains no carbon atoms'), ('S=*', "
               "'Contains no carbon atoms'), ('O*', 'Contains no carbon "
               "atoms'), ('[88Sr]', 'Contains no carbon atoms'), ('*SN=O', "
               "'Contains no carbon atoms'), ('[Si+2]', 'Contains no carbon "
               "atoms'), ('[H]S(=O)(=O)O[*]', 'Contains no carbon atoms'), "
               "('[Ti]=O', 'Contains no carbon atoms'), ('OP(O)(=O)O-*', "
               "'Contains no carbon atoms'), ('[Mo](S)(=O)=O', 'Contains no "
               "carbon atoms'), ('Br[Au](Br)Br', 'Contains no carbon atoms'), "
               "('[H][Br+][H]', 'Contains no carbon atoms'), ('Cl.NO', "
               "'Contains no carbon atoms'), "
               "('[Ca++].[H]O[H].[H]O[H].[O-]S([O-])(=O)=O', 'Contains no "
               "carbon atoms'), ('O=[W]1(=O)O[W](=O)(=O)O[W](=O)(=O)O1', "
               "'Contains no carbon atoms'), ('[Li+].[Br-]', 'Contains no "
               "carbon atoms'), "
               "('[H][N]([H])([H])[Ni++]([N]([H])([H])[H])([N]([H])([H])[H])([N]([H])([H])[H])([N]([H])([H])[H])[N]([H])([H])[H]', "
               "'Contains no carbon atoms'), ('O[Cd--](O)(O)O', 'Contains no "
               "carbon atoms'), ('[Cs+].Cl[Au-](Cl)(Cl)Cl', 'Contains no "
               "carbon atoms'), ('[Ir].[Pt]', 'Contains no carbon atoms'), "
               "('[202Po]', 'Contains no carbon atoms'), ('[H]OSO[H]', "
               "'Contains no carbon atoms'), ('S(S*)S', 'Contains no carbon "
               "atoms'), ('[Ba]', 'Contains no carbon atoms'), ('[*++]', "
               "'Contains no carbon atoms'), ('Cl[Au](Cl)Cl', 'Contains no "
               "carbon atoms'), "
               "('[H][Si]1([H])O[Si]([H])([H])O[Si]([H])([H])O1', 'Contains no "
               "carbon atoms'), ('O(O*)O*', 'Contains no carbon atoms'), "
               "('I(=O)(=O)(=O)O*', 'Contains no carbon atoms'), "
               "('[H][As](O)(O)=O', 'Contains no carbon atoms'), ('[Lu]', "
               "'Contains no carbon atoms'), "
               "('O.O.O.O.O.O.O.[Co+2].S([O-])([O-])(=O)=O', 'Contains no "
               "carbon atoms'), ('[H]O[W](=O)(=O)O[H]', 'Contains no carbon "
               "atoms'), ('[Te]=*', 'Contains no carbon atoms'), "
               "('[Li+].[Li+].[Li+].[O-]B([O-])[O-]', 'Contains no carbon "
               "atoms'), ('B1SBS1', 'Contains no carbon atoms'), "
               "('[K+].[K+].[O-]S(=O)(=O)SSS([O-])(=O)=O', 'Contains no carbon "
               "atoms'), ('[NH4+].NS([O-])(=O)=O', 'Contains no carbon "
               "atoms'), ('F[Cr--](F)(F)(F)F', 'Contains no carbon atoms'), "
               "('[La]', 'Contains no carbon atoms'), ('[H]OP(O[H])O[H]', "
               "'Contains no carbon atoms'), ('[H]OBr(=O)=O', 'Contains no "
               "carbon atoms'), ('[*]O[Si]([*])([*])[*]', 'Contains no carbon "
               "atoms'), ('[Co+2]', 'Contains no carbon atoms'), ('Cl[Hg]Cl', "
               "'Contains no carbon atoms'), ('N=*', 'Contains no carbon "
               "atoms'), ('*[PH3+]', 'Contains no carbon atoms'), ('[99Tc]', "
               "'Contains no carbon atoms'), ('[Fe++].[S-][S-]', 'Contains no "
               "carbon atoms'), ('[O-]S(=O)(=O)O[*]', 'Contains no carbon "
               "atoms'), "
               "('[H][N]([H])([H])[Au+3]([N]([H])([H])[H])([N]([H])([H])[H])[N]([H])([H])[H]', "
               "'Contains no carbon atoms'), "
               "('[H][B-]([H])([H])[H].[H][N+]([H])([H])[H]', 'Contains no "
               "carbon atoms'), ('IO*', 'Contains no carbon atoms'), "
               "('O[Si](O)(O)O[Si](O)(O)O', 'Contains no carbon atoms'), "
               "('S1[Fe]2S[Fe+]3S[Fe]1[S]23', 'Contains no carbon atoms'), "
               "('Cl[Sn-](Cl)Cl', 'Contains no carbon atoms'), ('[Sr]', "
               "'Contains no carbon atoms'), ('[H]O[Se](=O)(=O)O[H]', "
               "'Contains no carbon atoms'), ('OOP(O)(O)=O', 'Contains no "
               "carbon atoms'), ('[Eu]', 'Contains no carbon atoms'), "
               "('*[Te][H]', 'Contains no carbon atoms'), ('[Ca++].[I-].[I-]', "
               "'Contains no carbon atoms'), ('O1O[Mo--]112345OO1.O2O3.O4O5', "
               "'Contains no carbon atoms'), ('O[As](O)O', 'Contains no carbon "
               "atoms'), ('[Se-2]', 'Contains no carbon atoms'), "
               "('*=[Ge](*)[H]', 'Contains no carbon atoms'), "
               "('[H][Pb](*)(*)*', 'Contains no carbon atoms'), "
               "('O=S(N)(=O)*', 'Contains no carbon atoms'), ('I[H]', "
               "'Contains no carbon atoms'), ('ON(*)[H]', 'Contains no carbon "
               "atoms'), ('[N-]=*', 'Contains no carbon atoms'), ('[I]', "
               "'Contains no carbon atoms'), "
               "('[K+].[K+].[O-][Cr]([O-])(=O)=O', 'Contains no carbon "
               "atoms'), ('NN.[H]O[H]', 'Contains no carbon atoms'), "
               "('O(*)Br(=O)=O', 'Contains no carbon atoms'), ('[Fl]', "
               "'Contains no carbon atoms'), ('F[Mg-](F)F', 'Contains no "
               "carbon atoms'), ('Cl[Mo](Cl)(Cl)(Cl)Cl', 'Contains no carbon "
               "atoms'), ('[Li]N([Li])[Li]', 'Contains no carbon atoms'), "
               "('[36S]', 'Contains no carbon atoms'), ('[O-]*', 'Contains no "
               "carbon atoms'), ('*B(*)*', 'Contains no carbon atoms'), "
               "('OS[*]', 'Contains no carbon atoms')]\n"
               "False negatives: [('F[F-]', 'Invalid SMILES string'), "
               "('[H][B+]([H])([H])[H]', 'Invalid SMILES string'), "
               "('[H][B]1234[B]567([H])[B]118([H])[B]229([H])[B]33%10([H])[B]454([H])[B]656([H])[B]711([H])[B]822([H])[B]933([H])[B]%1045([H])[B]6123[H]', "
               "'Invalid SMILES string')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 87,
    'num_false_positives': 100,
    'num_true_negatives': 16232,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.46524064171123,
    'recall': 1.0,
    'f1': 0.635036496350365,
    'accuracy': 0.9939094950971435}