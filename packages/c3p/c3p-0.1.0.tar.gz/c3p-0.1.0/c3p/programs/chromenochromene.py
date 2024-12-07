"""
Classifies: CHEBI:133135 chromenochromene
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_chromenochromene(smiles: str):
    """
    Determines if a molecule is a chromenochromene (contains two ortho-fused chromene rings).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a chromenochromene, False otherwise
        str: Reason for classification
    """
    
    # Create RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Generate the ring information
    rings = mol.GetRingInfo()
    
    # SMARTS pattern for chromene ring
    chromene_pattern = Chem.MolFromSmarts("[#6]1[#6][#6][#6]2[#8][#6][#6][#6][#6]2[#6]1")
    
    # Find all matches of chromene pattern
    matches = mol.GetSubstructMatches(chromene_pattern)
    
    if len(matches) < 2:
        return False, "Does not contain at least two chromene rings"
        
    # Check if any two chromene rings are ortho-fused
    found_ortho_fusion = False
    for i in range(len(matches)):
        for j in range(i+1, len(matches)):
            ring1_atoms = set(matches[i])
            ring2_atoms = set(matches[j])
            
            # Check for shared atoms (fusion)
            shared_atoms = ring1_atoms.intersection(ring2_atoms)
            
            if len(shared_atoms) >= 2:  # At least 2 atoms shared for ortho fusion
                # Get the bonds between shared atoms to confirm ortho fusion
                shared_atoms_list = list(shared_atoms)
                bond_count = 0
                for idx1 in range(len(shared_atoms_list)):
                    for idx2 in range(idx1+1, len(shared_atoms_list)):
                        bond = mol.GetBondBetweenAtoms(shared_atoms_list[idx1], 
                                                      shared_atoms_list[idx2])
                        if bond is not None:
                            bond_count += 1
                            
                if bond_count >= 1:  # Confirms ortho fusion
                    found_ortho_fusion = True
                    break
                    
        if found_ortho_fusion:
            break
            
    if not found_ortho_fusion:
        return False, "Chromene rings are not ortho-fused"
        
    # Count number of substituents
    substituent_count = 0
    for atom in mol.GetAtoms():
        if atom.GetDegree() > 2 and atom.IsInRing():
            for neighbor in atom.GetNeighbors():
                if not neighbor.IsInRing():
                    substituent_count += 1
                    
    if substituent_count > 0:
        return True, f"Chromenochromene with {substituent_count} substituents"
    else:
        return True, "Unsubstituted chromenochromene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133135',
                          'name': 'chromenochromene',
                          'definition': 'Any organic heteroolycyclic compound '
                                        'whose skeleton two ortho-fused '
                                        'chromene rings, and their '
                                        'derivatives.',
                          'parents': ['CHEBI:38166']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 17261,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.994241289951051}