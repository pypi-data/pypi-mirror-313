"""
Classifies: CHEBI:139575 monounsaturated fatty acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_monounsaturated_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a monounsaturated fatty acyl-CoA.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a monounsaturated fatty acyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for CoA structure
    # Look for key substructures in CoA
    coA_substructures = [
        "COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12", # Adenosine diphosphate
        "SCCNC(=O)CCNC(=O)", # Pantetheine
        "C(C)(C)[C@@H](O)C(=O)" # Pantoic acid
    ]
    
    has_coA = all(mol.HasSubstructMatch(Chem.MolFromSmiles(substr)) for substr in coA_substructures)
    if not has_coA:
        return False, "Missing characteristic CoA substructure"

    # Check for thioester (C(=O)S) linkage
    thioester_pattern = Chem.MolFromSmarts("C(=O)S")
    if not mol.HasSubstructMatch(thioester_pattern):
        return False, "Missing thioester linkage"

    # Count number of double bonds in fatty acyl chain
    double_bond_pattern = Chem.MolFromSmarts("C=C")
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))

    if double_bonds == 0:
        return False, "No carbon-carbon double bonds found"
    elif double_bonds > 1:
        return False, f"Found {double_bonds} double bonds, expected 1"
    
    # Check if double bond is in fatty acyl chain by ensuring it's connected to carbons
    double_bond_atoms = mol.GetSubstructMatches(double_bond_pattern)
    for bond in double_bond_atoms:
        atom1 = mol.GetAtomWithIdx(bond[0])
        atom2 = mol.GetAtomWithIdx(bond[1])
        if atom1.GetSymbol() != 'C' or atom2.GetSymbol() != 'C':
            return False, "Double bond not between carbons"

    return True, "Monounsaturated fatty acyl-CoA with one carbon-carbon double bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139575',
                          'name': 'monounsaturated fatty acyl-CoA',
                          'definition': 'Any unsaturated fatty acyl-CoA in '
                                        'which the fatty acyl chain contains '
                                        'one carbon-carbon double bond.',
                          'parents': ['CHEBI:51006']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 10,
    'num_false_positives': 100,
    'num_true_negatives': 57399,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 1.0,
    'f1': 0.16666666666666669,
    'accuracy': 0.9982611417343372}