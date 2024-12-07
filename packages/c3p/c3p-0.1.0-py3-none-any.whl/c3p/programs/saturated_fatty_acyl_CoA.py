"""
Classifies: CHEBI:231546 saturated fatty acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_saturated_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a saturated fatty acyl-CoA.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a saturated fatty acyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of CoA substructure
    coA_pattern = Chem.MolFromSmarts('[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12')
    if not mol.HasSubstructMatch(coA_pattern):
        return False, "Missing CoA substructure"
        
    # Check for thioester linkage
    thioester_pattern = Chem.MolFromSmarts('C(=O)SCC')
    if not mol.HasSubstructMatch(thioester_pattern):
        return False, "Missing thioester linkage"
        
    # Get the fatty acid chain by finding the carbon connected to the thioester
    matches = mol.GetSubstructMatches(thioester_pattern)
    if not matches:
        return False, "Could not identify fatty acid chain"
        
    # Get the first carbon of fatty acid chain
    fatty_acid_start = matches[0][0]
    
    # Check if fatty acid chain has any double or triple bonds
    unsaturated_pattern = Chem.MolFromSmarts('[#6]=[#6,#7,#8]')
    triple_bond_pattern = Chem.MolFromSmarts('[#6]#[#6,#7]')
    
    # Get all atoms in the fatty acid chain
    fatty_acid_atoms = set()
    visited = set()
    stack = [fatty_acid_start]
    
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        fatty_acid_atoms.add(current)
        atom = mol.GetAtomWithIdx(current)
        
        # Only follow carbon-carbon single bonds
        for neighbor in atom.GetNeighbors():
            neighbor_idx = neighbor.GetIdx()
            if neighbor.GetSymbol() == 'C' and mol.GetBondBetweenAtoms(current, neighbor_idx).GetBondType() == Chem.rdchem.BondType.SINGLE:
                stack.append(neighbor_idx)
    
    # Create a substructure of just the fatty acid chain
    fatty_acid_mol = Chem.PathToSubmol(mol, list(fatty_acid_atoms))
    
    # Check for unsaturation in fatty acid chain
    if fatty_acid_mol.HasSubstructMatch(unsaturated_pattern) or fatty_acid_mol.HasSubstructMatch(triple_bond_pattern):
        return False, "Fatty acid chain contains unsaturated bonds"
        
    # Count carbons in fatty acid chain
    carbon_count = len([atom for atom in fatty_acid_mol.GetAtoms() if atom.GetSymbol() == 'C'])
    
    return True, f"Saturated fatty acyl-CoA with {carbon_count} carbons in fatty acid chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:231546',
                          'name': 'saturated fatty acyl-CoA',
                          'definition': 'A fatty acyl-CoA that results from '
                                        'the formal condensation of the thiol '
                                        'group of coenzyme A with the carboxy '
                                        'group of any saturated fatty acid.',
                          'parents': ['CHEBI:37554']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 170132,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 0.3333333333333333,
    'f1': 0.019230769230769232,
    'accuracy': 0.9994008282668077}