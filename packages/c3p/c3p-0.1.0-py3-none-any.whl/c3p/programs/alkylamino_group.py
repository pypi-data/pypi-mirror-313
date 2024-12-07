"""
Classifies: CHEBI:22332 alkylamino group
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alkylamino_group(smiles: str):
    """
    Determines if a molecule contains an alkylamino group (alkyl substituents attached via nitrogen).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains alkylamino group, False otherwise
        str: Reason for classification
    """
    # Replace wildcard atom (*) with carbon to allow RDKit processing
    smiles = smiles.replace('*', 'C')
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Find nitrogen atoms
    n_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'N']
    if not n_atoms:
        return False, "No nitrogen atoms found"
        
    for n_atom in n_atoms:
        # Get neighbors of nitrogen
        neighbors = n_atom.GetNeighbors()
        
        # Check if nitrogen is bonded to at least one carbon
        carbon_neighbors = [neigh for neigh in neighbors if neigh.GetSymbol() == 'C']
        if not carbon_neighbors:
            continue
            
        # Check if at least one carbon neighbor is sp3 (alkyl)
        for c_atom in carbon_neighbors:
            if c_atom.GetHybridization() == Chem.HybridizationType.SP3:
                # Check if this carbon is part of an alkyl chain
                is_alkyl = True
                for next_neigh in c_atom.GetNeighbors():
                    if next_neigh.GetSymbol() not in ['C', 'H', 'N']:
                        if not (next_neigh.GetSymbol() == 'O' and len([b for b in next_neigh.GetBonds() if b.GetBondType() == Chem.BondType.DOUBLE]) > 0):
                            is_alkyl = False
                            break
                
                if is_alkyl:
                    return True, "Contains alkylamino group - nitrogen bonded to sp3 carbon"
                    
    return False, "No alkylamino groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22332',
                          'name': 'alkylamino group',
                          'definition': 'Alkyl substituents attached to the '
                                        'remainder of a molecule via nitrogen.',
                          'parents': ['CHEBI:33456']},
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
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 68,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.42528735632183906}