"""
Classifies: CHEBI:134091 perfluorinated compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_perfluorinated_compound(smiles: str):
    """
    Determines if a molecule is a perfluorinated compound.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a perfluorinated compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of carbon
    has_carbon = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            has_carbon = True
            break
    if not has_carbon:
        return False, "No carbon atoms found"
        
    # Check for C-H bonds - should have none
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            if atom.GetTotalNumHs() > 0:
                return False, "Contains C-H bonds"

    # Check for aromatic carbons - should have none
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetIsAromatic():
            return False, "Contains aromatic carbons"
                
    # Check for C-F bonds - must have at least one
    has_cf_bond = False
    for bond in mol.GetBonds():
        atoms = [bond.GetBeginAtom(), bond.GetEndAtom()]
        if 'C' in [atom.GetSymbol() for atom in atoms] and 'F' in [atom.GetSymbol() for atom in atoms]:
            has_cf_bond = True
            break
    if not has_cf_bond:
        return False, "No C-F bonds found"
        
    # Check for presence of allowed heteroatoms
    allowed_heteroatoms = {'O', 'S'}
    heteroatoms = set()
    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        if symbol not in ['C', 'F']:
            if symbol not in allowed_heteroatoms:
                return False, f"Contains disallowed heteroatom: {symbol}"
            heteroatoms.add(symbol)
            
    if not heteroatoms:
        return False, "No heteroatoms besides fluorine found - this is a fluorocarbon, not a perfluorinated compound"

    # Check that all carbons are fully fluorinated (except those bonded to heteroatoms)
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            f_count = 0
            c_count = 0
            hetero_count = 0
            double_bond_count = 0
            
            for bond in atom.GetBonds():
                other = bond.GetOtherAtom(atom)
                if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                    double_bond_count += 1
                if other.GetSymbol() == 'F':
                    f_count += 1
                elif other.GetSymbol() == 'C':
                    c_count += 1
                elif other.GetSymbol() in allowed_heteroatoms:
                    hetero_count += 1
                else:
                    return False, f"Carbon bonded to disallowed atom: {other.GetSymbol()}"
                    
            expected_f = 4 - c_count - hetero_count - double_bond_count
            if f_count < expected_f:
                return False, "Carbon atom not fully fluorinated"
                
    return True, f"Perfluorinated compound with heteroatoms: {', '.join(heteroatoms)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134091',
                          'name': 'perfluorinated compound',
                          'definition': 'An organofluorine compound containing '
                                        'only C-F bonds (no C-H bonds) and C-C '
                                        'bonds but also other heteroatoms '
                                        '(particularly other halogens, oxygen, '
                                        'and sulfur). Their properties '
                                        'represent a blend of fluorocarbons '
                                        '(containing only C-F and C-C bonds) '
                                        'and the parent functionalised organic '
                                        'species.',
                          'parents': ['CHEBI:37143']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.14285714285714288 is too low.\n'
               'True positives: '
               "[('OC(=O)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F', "
               "'Perfluorinated compound with heteroatoms: O'), "
               "('C(C(C(S(O)(=O)=O)(F)F)(F)F)(C(F)(F)F)(F)F', 'Perfluorinated "
               "compound with heteroatoms: S, O')]\n"
               "False positives: [('[O-]C(=O)C(F)(F)F', 'Perfluorinated "
               "compound with heteroatoms: O'), "
               "('FC(F)(F)C(F)(F)N1C(F)(F)C(F)(F)C(F)(F)C(F)(F)C1(F)F', "
               "'Perfluorinated compound with heteroatoms: N'), "
               "('FC(F)(Cl)Br', 'Perfluorinated compound with heteroatoms: Br, "
               "Cl'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)S(F)(=O)=O', "
               "'Perfluorinated compound with heteroatoms: S, O'), "
               "('FC(F)(F)C(F)(F)C(F)(F)N(C(F)(F)C(F)(F)C(F)(F)F)C(F)(F)C(F)(F)C(F)(F)F', "
               "'Perfluorinated compound with heteroatoms: N'), "
               "('FC(S(OS(C(F)(F)F)(=O)=O)(=O)=O)(F)F', 'Perfluorinated "
               "compound with heteroatoms: S, O'), "
               "('C(C(C(F)(F)OC(F)(F)F)(F)F)(=O)O', 'Perfluorinated compound "
               "with heteroatoms: O'), "
               "('OC(=O)C(F)(OC(F)(F)C(F)(OC(F)(F)C(F)(F)C(F)(F)F)C(F)(F)F)C(F)(F)F', "
               "'Perfluorinated compound with heteroatoms: O'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(F)(F)N(C(F)(F)C(F)(F)C(F)(F)C(F)(F)F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F', "
               "'Perfluorinated compound with heteroatoms: N'), "
               "('FC(F)(F)C1(F)C(F)(F)C(F)(F)C(F)(N2C(F)(F)C(F)(F)C(F)(F)C(F)(F)C2(F)F)C(F)(F)C1(F)F', "
               "'Perfluorinated compound with heteroatoms: N'), "
               "('FC(S([O-])(=O)=O)(F)F', 'Perfluorinated compound with "
               "heteroatoms: S, O'), ('FC(Cl)(Cl)Cl', 'Perfluorinated compound "
               "with heteroatoms: Cl'), ('FC(F)(F)C(Cl)=O', 'Perfluorinated "
               "compound with heteroatoms: O, Cl'), ('ClC(Cl)(F)F', "
               "'Perfluorinated compound with heteroatoms: Cl'), "
               "('FC(F)(Cl)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)Cl', "
               "'Perfluorinated compound with heteroatoms: Cl'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(=O)OC(=O)C(F)(F)C(F)(F)C(F)(F)F', "
               "'Perfluorinated compound with heteroatoms: O'), "
               "('ClC(F)(F)C(F)(F)F', 'Perfluorinated compound with "
               "heteroatoms: Cl'), ('FC(F)(F)S(=O)(=O)[N-]S(=O)(=O)C(F)(F)F', "
               "'Perfluorinated compound with heteroatoms: S, O, N'), "
               "('S=C(F)N', 'Perfluorinated compound with heteroatoms: S, N'), "
               "('FC(F)(F)N1C(F)(F)C(F)(F)C2(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C2(F)C1(F)F', "
               "'Perfluorinated compound with heteroatoms: N'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C1(F)OC(F)(F)C(F)(F)C1(F)F', "
               "'Perfluorinated compound with heteroatoms: O'), "
               "('C(C(Cl)(F)F)(F)(Cl)Cl', 'Perfluorinated compound with "
               "heteroatoms: Cl'), "
               "('FC(F)(F)C1(F)N2C(F)(F)C(F)(F)C(F)(F)C(F)(F)C2(F)C(F)(F)C(F)(F)C1(F)F', "
               "'Perfluorinated compound with heteroatoms: N'), "
               "('FC1(F)N(C(F)(F)C(F)(F)C1(F)F)C1(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C1(F)F', "
               "'Perfluorinated compound with heteroatoms: N')]\n"
               'False negatives: []',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 9,
    'num_true_negatives': 183905,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.18181818181818182,
    'recall': 1.0,
    'f1': 0.3076923076923077,
    'accuracy': 0.9999510646164553}