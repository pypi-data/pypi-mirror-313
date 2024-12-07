"""
Classifies: CHEBI:134361 allylic alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_allylic_alcohol(smiles: str):
    """
    Determines if a molecule contains an allylic alcohol group.
    An allylic alcohol has a hydroxy group attached to a saturated carbon atom 
    adjacent to a carbon-carbon double bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains allylic alcohol, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Pattern for allylic alcohol:
    # [C;!$(C=*);!$(C#*)][OH] adjacent to C=C
    # The central carbon must be sp3 hybridized (not part of double/triple bond)
    # and have a hydroxyl group and be next to a C=C double bond
    pattern = Chem.MolFromSmarts("[C;!$(C=*);!$(C#*);!$(C[O;!H])][OH]-[#6]=[#6]")
    
    if pattern is None:
        return None, "Invalid SMARTS pattern"
        
    # Find all double bonds in the molecule
    double_bonds = mol.GetSubstructMatches(Chem.MolFromSmarts("C=C"))
    if not double_bonds:
        return False, "No carbon-carbon double bonds found"

    # Find all hydroxyl groups attached to sp3 carbons
    hydroxy_groups = mol.GetSubstructMatches(Chem.MolFromSmarts("[C;!$(C=*);!$(C#*)][OH]"))
    if not hydroxy_groups:
        return False, "No hydroxyl groups found on sp3 carbons"

    # Check if any hydroxyl group is adjacent to a double bond
    allylic_alcohols = []
    for oh_match in hydroxy_groups:
        c_with_oh = mol.GetAtomWithIdx(oh_match[0])
        if c_with_oh.GetHybridization() != Chem.HybridizationType.SP3:
            continue
            
        # Check neighbors of the carbon with OH
        for neighbor in c_with_oh.GetNeighbors():
            if neighbor.GetSymbol() != 'C':
                continue
                
            # Check if this carbon is part of a double bond
            for bond in neighbor.GetBonds():
                if bond.GetBondType() == Chem.BondType.DOUBLE:
                    other_atom = bond.GetOtherAtom(neighbor)
                    if other_atom.GetSymbol() == 'C':
                        allylic_alcohols.append(oh_match)
                        break

    if allylic_alcohols:
        count = len(set(allylic_alcohols))  # Remove duplicates
        return True, f"Found {count} allylic alcohol group{'s' if count > 1 else ''}"

    return False, "No allylic alcohol groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134361',
                          'name': 'allylic alcohol',
                          'definition': 'An alcohol where the hydroxy group is '
                                        'attached to a saturated carbon atom '
                                        'adjacent to a double bond (R groups '
                                        'may be H, organyl, etc.).',
                          'parents': ['CHEBI:30879', 'CHEBI:78840']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               'False negatives: '
               "[('C(C(O)=O)C/C=C\\\\C[C@H](\\\\C=C\\\\C=C/C=C/C=C/[C@H]([C@@H](C/C=C\\\\CC)O)O)O', "
               "'No allylic alcohol groups found'), "
               "('C\\\\C(=C/CO)\\\\C=C\\\\C=C(/C)\\\\C=C\\\\C1=C(C)CCCC1(C)C', "
               "'No allylic alcohol groups found'), "
               "('C(C(O)=O)C/C=C\\\\C/C=C\\\\C\\\\C=C/C=C/[C@H](C/C=C\\\\C/C=C\\\\CC)O', "
               "'No allylic alcohol groups found'), "
               "('C(C(O)=O)C/C=C\\\\C/C=C\\\\C\\\\C=C/C=C/[C@@H](C/C=C\\\\C/C=C\\\\CC)O', "
               "'No allylic alcohol groups found'), "
               "('C1=2[C@@H](C(=C(OC1=CC(=CC2O)O)C3=CC=C(C(=C3)O)O)O)O', 'No "
               "allylic alcohol groups found'), "
               "('C(=C/[C@H](C/C=C\\\\C/C=C\\\\CC)O)/C=C/C=C/[C@@H](CCCCCC(O)=O)O', "
               "'No allylic alcohol groups found'), "
               "('CC1C(O)C=C2C1(C)C=CCC2(C)C', 'No allylic alcohol groups "
               "found'), ('CC1=CC(O)OC1=O', 'No allylic alcohol groups "
               "found'), "
               "('CC(\\\\C=C\\\\C1=C(C)C(O)CCC1(C)C)=C/C=C/C(C)=C/C(O)=O', 'No "
               "allylic alcohol groups found'), "
               "('[C@@]12([C@]3([C@](CC[C@@]1(C[C@@](CC2)(C)C4CO4)[H])(C([C@H](CC3)O)=C)C)[H])C', "
               "'No allylic alcohol groups found'), "
               "('CCC(C)[C@H]1O[C@@]2(C[C@@H]3C[C@@H](C\\\\C=C(C)\\\\[C@@H](O)[C@@H](C)\\\\C=C\\\\C=C4/CO[C@@H]5[C@H](O)C(C)=C[C@@H](C(=O)O3)[C@]45O)O2)C[C@H](O)[C@@H]1C', "
               "'No allylic alcohol groups found'), "
               "('O=C(CCC/C=C\\\\C/C=C\\\\CC(C(/C=C/C(CCCCC)O)O)O)O', 'No "
               "allylic alcohol groups found'), "
               "('C(\\\\[C@H](CCCC(O)=O)O)=C\\\\C=C\\\\C=C\\\\[C@@H](C\\\\C=C/C=C/[C@H](CC)O)O', "
               "'No allylic alcohol groups found'), "
               "('O=C(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\[C@H](/C=C\\\\CCCCC)O)O', "
               "'No allylic alcohol groups found'), "
               "('OC(CC/C=C\\\\C/C=C\\\\C[C@@H](/C=C/C=C\\\\C=C\\\\[C@H](C/C=C\\\\CC)O)O)=O', "
               "'No allylic alcohol groups found'), "
               "('C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC=C2C[C@H](C1)O)[H])(CC[C@@]4([C@H](C)CC/C=C(\\\\CO)/C)[H])[H])C)[H])C', "
               "'No allylic alcohol groups found'), "
               "('CC(\\\\C=C\\\\[C@@]1(O)C(C)=CC(=O)CC1(C)C)=C/C(O)=O', 'No "
               "allylic alcohol groups found'), "
               "('C\\\\C1=C/C[C@H](O)\\\\C(C)=C\\\\[C@H]2OC(=O)C(=C)[C@@H]2CC1', "
               "'No allylic alcohol groups found'), "
               "('C(\\\\[C@H]1[C@@H](CC([C@@H]1C/C=C\\\\CCCC(O)=O)=O)O)=C/[C@H](C(CCCC)(C)C)O', "
               "'No allylic alcohol groups found'), "
               "('C[C@@](O)(\\\\C=C\\\\[C@H]1CC=CC(=O)O1)[C@@H](C[C@@H](O)\\\\C=C/C=C\\\\C=C\\\\CO)OP(O)(O)=O', "
               "'No allylic alcohol groups found'), "
               "('C(C=C/C=C\\\\C=C\\\\[C@H](C/C=C\\\\CC)O)=C[C@@H]([C@@H](C/C=C\\\\CCC(O)=O)O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O', "
               "'No allylic alcohol groups found'), "
               "('C(CCC)C/C=C\\\\C/C=C\\\\C[C@@H]([C@H](C/C=C\\\\CCCC(O)=O)O)O', "
               "'No allylic alcohol groups found'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC[C@](C)(O)C=C', 'No allylic alcohol "
               "groups found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 22,
    'num_false_positives': 100,
    'num_true_negatives': 1507,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.18032786885245902,
    'recall': 0.9565217391304348,
    'f1': 0.30344827586206896,
    'accuracy': 0.938036809815951}