"""
Classifies: CHEBI:24654 hydroxy fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

def is_hydroxy_fatty_acid(smiles: str):
    """
    Determines if a molecule is a hydroxy fatty acid, defined as a fatty acid carrying one or more hydroxy substituents.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxy fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    carboxylic_pattern_ionic = Chem.MolFromSmarts('C(=O)[O-]')
    if not (mol.HasSubstructMatch(carboxylic_pattern) or mol.HasSubstructMatch(carboxylic_pattern_ionic)):
        return False, "No carboxylic acid group found"

    # Check for hydroxy groups
    hydroxy_pattern = Chem.MolFromSmarts('[OH]')
    hydroxy_matches = mol.GetSubstructMatches(hydroxy_pattern)
    
    # Get carboxylic acid OH indices
    carboxylic_matches = mol.GetSubstructMatches(carboxylic_pattern)
    carboxylic_o_indices = [match[1] for match in carboxylic_matches]
    
    # Count hydroxy groups that are not part of carboxylic acid
    hydroxy_count = 0
    for match in hydroxy_matches:
        if match[0] not in carboxylic_o_indices:
            hydroxy_count += 1
            
    if hydroxy_count == 0:
        return False, "No hydroxy substituents found"

    # Check for too many rings (fatty acids typically have few or no rings)
    ring_info = mol.GetRingInfo()
    ring_count = ring_info.NumRings()
    if ring_count > 3:  # Increased tolerance for rings
        return False, "Too many rings for a fatty acid"

    # Calculate carbon chain characteristics
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 3:  # Reduced minimum carbon requirement
        return False, "Carbon chain too short for a fatty acid"

    # Check for aromatic systems (fatty acids shouldn't be aromatic)
    aromatic_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetIsAromatic())
    if aromatic_atoms > 2:  # Allow some aromatic atoms
        return False, "Contains too many aromatic atoms"

    # Check for peptide bonds
    peptide_pattern = Chem.MolFromSmarts('[NX3][CX3](=[OX1])[#6]')
    if mol.HasSubstructMatch(peptide_pattern):
        return False, "Contains peptide bond"

    # Calculate ratio of carbons to other heavy atoms (excluding H)
    other_heavy_atoms = sum(1 for atom in mol.GetAtoms() 
                           if atom.GetSymbol() not in ['C', 'H'])
    if other_heavy_atoms > carbon_count * 0.75:  # Increased tolerance for heteroatoms
        return False, "Too many heteroatoms for a fatty acid"

    return True, f"Hydroxy fatty acid with {hydroxy_count} hydroxy group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24654',
                          'name': 'hydroxy fatty acid',
                          'definition': 'Any fatty acid carrying one or more '
                                        'hydroxy substituents.',
                          'parents': ['CHEBI:35366', 'CHEBI:35868']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.5172413793103448 is too low.\n'
               "True positives: [('CCCCCCCCCCCCCCC(O)C(O)=O', 'Hydroxy fatty "
               "acid with 2 hydroxy group(s)'), "
               "('OCCCCCCCCCCCCCCCCCC[C@@H](O)CC(O)=O', 'Hydroxy fatty acid "
               "with 3 hydroxy group(s)'), ('C[C@@H](O)CC\\\\C=C\\\\C(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('CC(C)CCCC(C)CCCC(C)CCCC(C)C(O)C(O)=O', 'Hydroxy fatty acid "
               "with 2 hydroxy group(s)'), "
               "('OCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O', 'Hydroxy fatty "
               "acid with 2 hydroxy group(s)'), "
               "('CCCCCCC(O)C\\\\C=C/CCCCCCCC(O)=O', 'Hydroxy fatty acid with "
               "2 hydroxy group(s)'), ('C[C@@H](O)CCCCCCC[C@@H](O)CC(O)=O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('C(CCCCCCCC)CCCCCCC[C@@H](C(O)=O)O', 'Hydroxy fatty acid with "
               "2 hydroxy group(s)'), ('C[C@@H](O)CC[C@H](CC(O)=O)C(C)=C', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('[H][C@@]1(C\\\\C=C/CCCCC)O[C@@]1([H])\\\\C=C\\\\C(O)C\\\\C=C/CCCC(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C[C@H](O)C#CC#CC#CC#CCCCCCCCC(O)=O', 'Hydroxy fatty acid "
               "with 2 hydroxy group(s)'), "
               "('CCCCC\\\\C=C/C=C/[C@H](O)CCCCCCCC(O)=O', 'Hydroxy fatty acid "
               "with 2 hydroxy group(s)'), "
               "('O=C(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\[C@H](CCCC)O)O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('O[C@H](CCCC(O)=O)CC\\\\C=C\\\\C=C\\\\[C@H](O)C/C=C\\\\CCCCC', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('CCCCC(O)CCCCCCCCC(O)=O', 'Hydroxy fatty acid with 2 hydroxy "
               "group(s)'), "
               "('OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\C(C/C=C\\\\CC)O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C(=C\\\\C/C=C\\\\CCCC(C)O)\\\\CCCCCCCC(=O)O', 'Hydroxy fatty "
               "acid with 2 hydroxy group(s)'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCC[C@@H](O)C(O)=O', 'Hydroxy "
               "fatty acid with 2 hydroxy group(s)'), "
               "('C(/C=C/C=C/[C@H]([C@@H](O)C/C=C\\\\C/C=C\\\\CC)O)=C/C/C=C\\\\CCC(O)=O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('O[C@@H](CCCCC)/C=C/C=C\\\\C/C=C\\\\C=C\\\\C(=O)CCCC(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('CCCCCCC(O)C(O)\\\\C=C\\\\C(O)CCCCCCC(O)=O', 'Hydroxy fatty "
               "acid with 4 hydroxy group(s)'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C[C@H](O)\\\\C=C\\\\C=C/CCCC(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('O[C@@H]([C@@H](O)C(O)/C=C\\\\C/C=C\\\\CCCC(O)=O)C/C=C\\\\CCCCC', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('OCCCCCCCCCCCCCCCCCCCCCCCC(O)=O', 'Hydroxy fatty acid with 2 "
               "hydroxy group(s)'), "
               "('OC(CCCC(O)=O)\\\\C=C\\\\C=C\\\\C=C\\\\C(O)C\\\\C=C/C=C\\\\C(O)CC', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('C(CCCCCCC/C=C\\\\C=C\\\\[C@H](CCCCC)O)(=O)O', 'Hydroxy fatty "
               "acid with 2 hydroxy group(s)'), "
               "('C(CCCCCCCC(=O)OC(CCCCCCCCCCC(=O)O)CCCCCC)CCCCCCCCC', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('C(\\\\C([C@H]1[C@H](C/C=C\\\\CCCCC)O1)O)=C\\\\C/C=C\\\\CCCC(=O)O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C([C@H](/C=C/C=C/C=C\\\\[C@H](CCCC(O)=O)O)O)/C=C\\\\CCCC(C)O', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('CCCCC\\\\C=C\\\\C=C\\\\C(O)C\\\\C=C\\\\C=C\\\\C(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C[C@@H](O)CCCCCCCCCCCCC(O)=O', 'Hydroxy fatty acid with 2 "
               "hydroxy group(s)'), "
               "('OC(CC/C=C\\\\C/C=C\\\\C[C@H](\\\\C=C\\\\C=C\\\\C=C/[C@H](C/C=C\\\\CCO)O)O)=O', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('C(CC(CCCCCCCCCCC(=O)O)O)(=O)O', 'Hydroxy fatty acid with 3 "
               "hydroxy group(s)'), "
               "('OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\[C@H](C/C=C\\\\CCCCC)O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('OCCCCCCCCCC(O)CC(O)=O', 'Hydroxy fatty acid with 3 hydroxy "
               "group(s)'), "
               "('OC(C(O)C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)C/C=C\\\\CCCC(O)=O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('C(\\\\CC)=C\\\\C/C=C\\\\CC(/C=C/C=C\\\\C/C=C\\\\CCCC(=O)O)O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C(\\\\C=C/C=C/C=C/[C@H]([C@H](CCCCCO)O)O)=C/[C@H](CCCC(O)=O)O', "
               "'Hydroxy fatty acid with 5 hydroxy group(s)'), "
               "('O[C@@H](CCCC(O)=O)/C=C\\\\C=C\\\\CCC(=O)C/C=C\\\\C=C\\\\[C@@H](O)CC', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('C(CCC(O)=O)/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCCO', 'Hydroxy "
               "fatty acid with 2 hydroxy group(s)'), "
               "('[H]C(CCCC(O)=O)=CCC([H])=CC([H])=CC(O)CC([H])=CCCCCC', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('CCCCCCCCCCCC(O)CC(O)=O', 'Hydroxy fatty acid with 2 hydroxy "
               "group(s)'), "
               "('C(C(/C=C/C=C/C=C\\\\[C@H](CCCC(O)=O)O)=O)/C=C\\\\CCCCCO', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('O[C@H](CCCCCCCC)C=CC=CC=C[C@@H](O)CCCC(O)=O', 'Hydroxy fatty "
               "acid with 3 hydroxy group(s)'), "
               "('O=C(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C(C(C(CCCCC)O)O)O)O', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCCCC[C@H]1C[C@H]1CCCCCCCCCCCCCCCC[C@H](OC)[C@@H](C)CCCCCCCCCCCCCCCCCC)C(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C(C=CC=C/C=C/[C@H](C/C=C\\\\CC)O)=CC([C@H](CCCCCC(O)=O)O)O', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('O=C(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C(/C=C\\\\CCCCC)O)O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('OCCCCCCCCC[C@@H](O)CC(O)=O', 'Hydroxy fatty acid with 3 "
               "hydroxy group(s)'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C=C/C(O)CCCC(O)=O', 'Hydroxy "
               "fatty acid with 2 hydroxy group(s)'), "
               "('C(CCC)C/C=C\\\\C/C=C\\\\C[C@@H]([C@H](C/C=C\\\\CCCC(O)=O)O)O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('CCCCC\\\\C=C/C=C/C(O)C\\\\C=C/C\\\\C=C/CCCC(O)=O', 'Hydroxy "
               "fatty acid with 2 hydroxy group(s)'), "
               "('C(C(/C=C/C=C/C=C\\\\[C@H](CCCC(O)=O)O)=O)/C=C\\\\CCCCC=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('O[C@H](CCCC(O)=O)/C=C/C=C\\\\C=C\\\\[C@@H](O)C/C=C\\\\C=C\\\\[C@H](O)CC', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('C[C@@H](O)CCC\\\\C=C\\\\C=C\\\\C(O)=O', 'Hydroxy fatty acid "
               "with 2 hydroxy group(s)'), ('OC(CCCCCCCCCCC(CCCCCC)O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C(C(C(CCCCCCCCO)O)O)CCCCCCC(=O)O', 'Hydroxy fatty acid with "
               "4 hydroxy group(s)'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCCC[C@@H]1C[C@@H]1[C@H](C)CCCCCCCCCCCCCCCCCCC(=O)C(C)CCCCCCCCCCCCCCCCCC)C(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C(\\\\CC)=C\\\\C/C=C\\\\C/C=C\\\\CC(/C=C/C=C\\\\CCCC(=O)O)O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('OCCCCCCCCCCCCC\\\\C=C\\\\C(O)=O', 'Hydroxy fatty acid with 2 "
               "hydroxy group(s)')]\n"
               'False positives: '
               "[('[C@@]12([C@H](CCC=C1C=C[C@@H]([C@@H]2CC[C@H](C[C@H](CC(=O)O)O)O)C)OC([C@H](CC)C)=O)[H]', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('C1=CC(/C(/[C@H]1C/C=C\\\\CCCC([O-])=O)=C/C[C@H](CCCCC)O)=O', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('O[C@H]1[C@@H]([C@@H](CCCCCCCCC(O)=O)C(=O)C1)/C=C/[C@@H](O)CCCCC', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('OC(C(O)CCCCCCCC(O)=O)CCC(O)CCCCC', 'Hydroxy fatty acid with "
               "4 hydroxy group(s)'), "
               "('OC(=O)\\\\C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('[H]C(CCCC(O)=O)=CCCC([H])=CC([H])=CCC([H])=CCCCCC', 'Hydroxy "
               "fatty acid with 1 hydroxy group(s)'), "
               "('OC1(C2(C(C(CCC2)(C)C)C(O)C=C1CO)C)C(O)=O', 'Hydroxy fatty "
               "acid with 4 hydroxy group(s)'), ('C1=CC(C=C(C1=O)CC(O)=O)=O', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('P(OC[C@H](OC(=O)CCC(O)/C=C/C(O)=O)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('O=C(CCCC(O)=O)CC', 'Hydroxy fatty acid with 1 hydroxy "
               "group(s)'), "
               "('[C@H]1([C@@H]([C@H](CO[C@H]1C/C(=C/C(OCCCCCCCC([O-])=O)=O)/C)C/C=C/[C@H]([C@H](C)O)C)O)O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('CCCCCCC[C@@H](C\\\\C=C\\\\CCC(O)=O)OC', 'Hydroxy fatty acid "
               "with 1 hydroxy group(s)'), "
               "('[O-]C(CCCCCCC/C=C\\\\CCCCCCCCO[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)=O', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('O[C@@H](CCCCCCCC)C(O)=O', 'Hydroxy fatty acid with 2 hydroxy "
               "group(s)'), "
               "('OCC=1C(C2(C(C(CCC2)(C)C)CC1)C)CCC(COC(=O)C)=CC(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('O=C1O[C@@H](CCCCCCCCCCCCC[C@@H](O)C)[C@@H](C1=C)C(=O)O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C(\\\\C=C/CCCCCCCC(=O)[O-])=C/C(C/C=C\\\\CC)OO', 'Hydroxy "
               "fatty acid with 1 hydroxy group(s)'), "
               "('O[C@@H](CCCCCC)CC#CCCCCCCCC(O)=O', 'Hydroxy fatty acid with "
               "2 hydroxy group(s)'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCCCCCC\\\\C=C/CCCCCC', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C[C@@H]1O[C@@H](OCCCCCC\\\\C=C\\\\C(O)=O)[C@H](O)C[C@H]1O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('O=C(O)CCCCCCCC(O)C(O)CC(O)C(O)CC(O)C(O)C/C=C/CCCCCCC', "
               "'Hydroxy fatty acid with 7 hydroxy group(s)'), "
               "('OC(=O)CCCCCCCCC/C=C\\\\CCCCC', 'Hydroxy fatty acid with 1 "
               "hydroxy group(s)'), ('OC(=O)CCCCCC/C=C\\\\C/C=C\\\\CCCCCC', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('OC(=O)CCCC/C=C\\\\C/C=C\\\\CCCCCC(C)C', 'Hydroxy fatty acid "
               "with 1 hydroxy group(s)'), ('OC(=O)CCCCCCCCCC/C=C\\\\CO', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C(/C=C\\\\CCCCC=O)\\\\C=C/C=C/C=C/[C@H]([C@@H](O)CCCC(=O)[O-])SC[C@H]([NH3+])C(=O)[O-]', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('C[C@@H]1O[C@@H](OCCCCC[C@@H](O)CC(O)=O)[C@H](O)C[C@H]1O', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('O([C@@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCCCCCCCCCCCCC(O)=O', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('C(\\\\[C@H](CCCC([O-])=O)O)=C\\\\C=C\\\\C=C\\\\[C@@H](C\\\\C=C/C=C/C(CC)=O)O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C[C@H](CCCCC(=O)CC(O)=O)O[C@@H]1O[C@@H](C)[C@H](O)C[C@H]1O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('OC(=O)CCC/C=C\\\\C/C=C\\\\C=C\\\\C=O', 'Hydroxy fatty acid "
               "with 1 hydroxy group(s)'), "
               "('O=C1C[C@@](C2=CC=C(C(=O)OCC[C@@](O)(CC(=O)O)C)CC2)(C)C(C1)(C)C', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('O=C(O)C(=CCCCCC)[C@@H](C(=O)O)C', 'Hydroxy fatty acid with 2 "
               "hydroxy group(s)'), ('S1C(N[C@@H](C1)C(O)=O)CCCCCCCCCCC', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('C(=O)(OC[C@H](COP(OC[C@@H](C(=O)[O-])[NH3+])(=O)[O-])OC(=O)CCCCCCCCC(CCCCCCCC)O)CCCCCCCCCCCCCCC', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('CCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('O[C@@H]1C[C@H](O)[C@H](C\\\\C=C/CCCC(O)=O)[C@H]1CCC(=O)CCCCC(O)=O', "
               "'Hydroxy fatty acid with 4 hydroxy group(s)'), "
               "('OC(=O)CCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC', 'Hydroxy fatty acid "
               "with 1 hydroxy group(s)'), "
               "('O[C@@H]1[C@@H]([C@H](C(C1)=C)/C=C/C(=O)CCCCC)C/C=C\\\\CCCC(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('CC(C(CC)C(O)=O)O', 'Hydroxy fatty acid with 2 hydroxy "
               "group(s)'), ('OC(=O)C(CCCCCCCCCC)C', 'Hydroxy fatty acid with "
               "1 hydroxy group(s)'), "
               "('C(CCCCCC1C(C1)CCCCCCCCCCCCC[C@@H](O)[C@H](C([O-])=O)CCCCCCCCCCCCCCCCCCCCCCCC)CCCCCCCCC2C(C2)CCCCCCCCCCCCCCCCCCCC', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('[H][C@]1(\\\\C=C\\\\[C@@H](O)C(C)CC#CC)[C@H](O)C[C@@H]2C\\\\C(C[C@H]12)=C/CCCC(O)=O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('OC(=O)C/C(=C/CCC)/C', 'Hydroxy fatty acid with 1 hydroxy "
               "group(s)'), ('OC(=O)CC(CCCCCC)(C)C', 'Hydroxy fatty acid with "
               "1 hydroxy group(s)'), "
               "('O=C(O)C1[C@@]2(C(C)=C([C@H]1[C@@H](C(C)C)CC2)C=O)C', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('CCCCC\\\\C=C/CCC\\\\C=C\\\\CC\\\\C=C/CCCC(O)=O', 'Hydroxy "
               "fatty acid with 1 hydroxy group(s)'), "
               "('OC(=O)CCC/C=C/C\\\\C=C\\\\C\\\\C=C\\\\CCCCCC', 'Hydroxy "
               "fatty acid with 1 hydroxy group(s)'), "
               "('ClC[C@@]1(O)[C@H]2C(=O)OCC(=C[C@@H]2[C@@H](C(C)C)CC1)C(=O)O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('O=C(O)/C(=C/[C@@H](CCCCC)C)/C', 'Hydroxy fatty acid with 1 "
               "hydroxy group(s)'), ('OC(=O)CCCC#CCC#CCC#CCC#CCCCCCCC', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('O=C(O)/C=C(/C=C/[C@@H]1O[C@]2(O[C@@H]([C@@H](C)CC2)C/C=C(/C=C/[C@H](O)[C@H](/C=C/C(=O)O)C)\\\\C)CC[C@]1(OC(=O)CCC(=O)OC)CCCC)\\\\C', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('C(=C/C=C/[C@H](CCCCC)OO)/C=C/[C@H](C/C=C\\\\CCCC([O-])=O)OO', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('CCC=CCC=CCC=CCCCCCCCC(=O)O', 'Hydroxy fatty acid with 1 "
               "hydroxy group(s)'), ('OC(=O)C(CCCC(C)C)C', 'Hydroxy fatty acid "
               "with 1 hydroxy group(s)'), ('OC(CCCCCCC)/C=C/CCCCCCCC(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('O(C1C(C(CC1)CC(O)=O)C/C=C/CC)C2OC(C(O)C(O)C2O)CO', 'Hydroxy "
               "fatty acid with 5 hydroxy group(s)'), "
               "('OC(=O)\\\\C=C\\\\CC\\\\C=C\\\\CCC', 'Hydroxy fatty acid with "
               "1 hydroxy group(s)'), "
               "('OC(=O)C1N(CCC1)/C=C/C=C(\\\\O)/C=[N+]\\\\2/C(CCC2)C([O-])=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('CC\\\\C=C/C=C/C=C/CCCCCCCCCC(O)=O', 'Hydroxy fatty acid with "
               "1 hydroxy group(s)'), ('OC(=O)CC(N)CC(C)C', 'Hydroxy fatty "
               "acid with 1 hydroxy group(s)'), ('CCCCCCCC\\\\C=C\\\\CC(O)=O', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('CCCCCCCCCCCCCCCCCCC(C)CC(C)\\\\C=C(/C)C(O)=O', 'Hydroxy "
               "fatty acid with 1 hydroxy group(s)'), "
               "('OC(=O)CCC/C=C\\\\CCCCC', 'Hydroxy fatty acid with 1 hydroxy "
               "group(s)'), "
               "('C(C([O-])=O)C/C=C\\\\CC(/C=C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)OO', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('OC(C1CCC(=CC1)C(O)=O)(C)C', 'Hydroxy fatty acid with 2 "
               "hydroxy group(s)'), ('OC(=O)[C@]1(C([C@H](CC1)C(O)=O)(C)C)C', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CC', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('C(=O)([O-])CC1C(C(CC1)=O)C/C=C\\\\CCO', 'Hydroxy fatty acid "
               "with 1 hydroxy group(s)'), "
               "('OC(=O)CCCCCC#CCC#CCC#CCC#CCC#CCC', 'Hydroxy fatty acid with "
               "1 hydroxy group(s)'), "
               "('[H][C@](COP(OC[C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCC)=O)[H])(=O)O)(C(O)=O)N', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('OC(=O)C(C(C)C)CCCC', 'Hydroxy fatty acid with 1 hydroxy "
               "group(s)'), "
               "('[H][C@](COP(OC[C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])(=O)O)(C(O)=O)N', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('[C@@H]1([C@@H](C[C@H]([C@@H](O1)C)O)O)OCCCCCCCCCCC/C=C/C([O-])=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('OC(=O)CCCCCC/C=C/C=C/C=C/CCCCC', 'Hydroxy fatty acid with 1 "
               "hydroxy group(s)'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('O=C1[C@@H](CCCCC)/C(/C=C1)=C\\\\C=C\\\\C/C=C\\\\CCCC(O)=O', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('O=C1OC(=O)C(=C1CCCCCCCCCCCCCCCC/C=C(\\\\C(=O)O)/CC(=O)O)C', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('CC(C)(C)[C@@H](C(=O)O)NC(=O)OC(C)(C)C', 'Hydroxy fatty acid "
               "with 1 hydroxy group(s)'), ('O=C(O)C[C@H](O)C[C@H](O)CCCCC', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('C(C(O)=O)C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C[C@@H]1[C@H](CC)O1', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('C([C@H](/C=C/C=C/C=C\\\\[C@H](CCCC([O-])=O)O)O)/C=C\\\\CCCCC([O-])=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('OC1(C(CC(=O)C=C1CO)(C)C)/C=C/C(/C)=C/C(O)=O', 'Hydroxy fatty "
               "acid with 3 hydroxy group(s)'), ('OC(=O)CCCCCCCCCCC(N)CCCCCC', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('OC(=O)\\\\C=C\\\\C=C\\\\CCCCCCCCCCC', 'Hydroxy fatty acid "
               "with 1 hydroxy group(s)'), ('O=C(CCCCCCCCCCCC(O)=O)CCCCC', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('CCCCCCCCCCCCCCSCC(=O)O', 'Hydroxy fatty acid with 1 hydroxy "
               "group(s)'), "
               "('CCCCCC(=O)\\\\C=C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(O)=O', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)'), "
               "('O=C(CCCCCCCCCCCCCCC)C(O)=O', 'Hydroxy fatty acid with 1 "
               "hydroxy group(s)'), "
               "('P(OC[C@H](OC(=O)CCC(=O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)(O)=O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('C[C@@H]1OC=C2C(O)=C(C(O)=O)C(=O)C(C)=C2[C@H]1C', 'Hydroxy "
               "fatty acid with 2 hydroxy group(s)'), "
               "('O[C@H]1[C@@H]([C@@H](C(=O)C1)CC)/C=C/[C@@H](O)C/C=C\\\\C/C=C\\\\C/C=C\\\\CCC(O)=O', "
               "'Hydroxy fatty acid with 3 hydroxy group(s)'), "
               "('O=C(O)C(O)CCCCCCCCCCCCCCO[C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](OC(=O)C)[C@@H]([C@H]2OC(=O)C)OC(=O)C)CO)[C@@H]([C@H]1O)O)COC(=O)C', "
               "'Hydroxy fatty acid with 5 hydroxy group(s)'), "
               "('O[C@@H](CCCCCC)C/C=C\\\\CCCCCCCC(O)=O', 'Hydroxy fatty acid "
               "with 2 hydroxy group(s)'), ('OC(=O)C(CCCC(CCCCCC)C)C', "
               "'Hydroxy fatty acid with 1 hydroxy group(s)'), "
               "('OC(=O)C1=CCNCC1', 'Hydroxy fatty acid with 1 hydroxy "
               "group(s)'), ('OC(=O)CC/C=C\\\\CC=C', 'Hydroxy fatty acid with "
               "1 hydroxy group(s)'), "
               "('C(CCC)C/C=C\\\\C/C=C\\\\C[C@H]([C@@H](C/C=C\\\\CCCC([O-])=O)O)O', "
               "'Hydroxy fatty acid with 2 hydroxy group(s)')]\n"
               "False negatives: [('CC[C@H](O)CC(=O)C(O)=O', 'Too many "
               "heteroatoms for a fatty acid'), ('CC[C@](O)(C(C)=O)C(O)=O', "
               "'Too many heteroatoms for a fatty acid'), "
               "('C[N+](C)(C)C[C@H](O)[C@@H](O)C([O-])=O', 'Too many "
               "heteroatoms for a fatty acid'), ('O=C(O)/C=C(/OC)\\\\CCO', 'No "
               "significant aliphatic chain found'), ('CCC(C)(O)C(O)=O', 'Too "
               "many heteroatoms for a fatty acid'), "
               "('CC[C@](C)(O)C(=O)C(O)=O', 'Too many heteroatoms for a fatty "
               "acid'), "
               "('O=C1C(=O)[C@@H]2[C@@](O)([C@]3(CC[C@@H]4[C@@]([C@H]3C2)(CCCC4(C)C)C)C)C=C1COC(=O)CC(O)(CC(=O)O)C', "
               "'Too many rings for a fatty acid'), ('CC[C@H](O)C(O)=O', 'Too "
               "many heteroatoms for a fatty acid'), ('OC/C(=C/C)/C(O)=O', 'No "
               "significant aliphatic chain found'), "
               "('OC[C@H](O)[C@H](O)C(O)=O', 'Too many heteroatoms for a fatty "
               "acid'), ('OC(CC)C(O)C(O)=O', 'Too many heteroatoms for a fatty "
               "acid'), "
               "('O=C(O)[C@@](O)(CC(=O)NCCCN(O)C(=O)CCCCCCC)CC(=O)NCCCN(O)C(=O)C', "
               "'Contains peptide bond')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 68,
    'num_false_positives': 100,
    'num_true_negatives': 2018,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.40476190476190477,
    'recall': 0.9444444444444444,
    'f1': 0.5666666666666667,
    'accuracy': 0.9525114155251142}