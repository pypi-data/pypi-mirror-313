"""
Classifies: CHEBI:140992 omega-hydroxy-long-chain fatty acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_omega_hydroxy_long_chain_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is an omega-hydroxy-long-chain fatty acid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an omega-hydroxy-long-chain fatty acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylate anion
    carboxylate = False
    carboxylate_carbon = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            neighbors = [n for n in atom.GetNeighbors()]
            if len(neighbors) == 1 and neighbors[0].GetSymbol() == 'C':
                carb_neighbor = neighbors[0]
                if len([n for n in carb_neighbor.GetNeighbors() if n.GetSymbol() == 'O']) == 2:
                    carboxylate = True
                    carboxylate_carbon = carb_neighbor.GetIdx()
                    break
    
    if not carboxylate:
        return False, "No carboxylate anion group found"

    # Check for terminal hydroxyl group and its carbon
    terminal_oh_carbons = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            oh_count = 0
            carbon_neighbors = 0
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                    oh_count += 1
                elif neighbor.GetSymbol() == 'C':
                    carbon_neighbors += 1
            if oh_count == 1 and carbon_neighbors == 1:
                terminal_oh_carbons.append(atom.GetIdx())

    if not terminal_oh_carbons:
        return False, "No terminal hydroxyl group found"

    # For each terminal OH carbon, check if it's connected to carboxylate through a chain
    valid_chain = False
    chain_length = 0
    for terminal_c in terminal_oh_carbons:
        # Get shortest path between terminal carbon and carboxylate carbon
        path = Chem.GetShortestPath(mol, terminal_c, carboxylate_carbon)
        if path:
            # Check if path consists mainly of carbons (allowing some C=C bonds)
            carbon_path = True
            path_atoms = [mol.GetAtomWithIdx(i) for i in path]
            
            # Count carbons in path that are part of rings
            ring_carbons = sum(1 for atom in path_atoms if atom.IsInRing())
            
            # Check if path has too many ring carbons
            if ring_carbons > 2:  # Allow maximum 2 ring carbons
                continue
                
            for atom in path_atoms:
                if atom.GetSymbol() not in ['C']:
                    carbon_path = False
                    break
            if carbon_path and 17 <= len(path) <= 21:  # Chain length between 17-21
                valid_chain = True
                chain_length = len(path)
                break

    if not valid_chain:
        return False, "No valid hydrocarbon chain found between carboxylate and terminal OH"

    # Additional checks for ring structures
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 1:  # Allow maximum 1 ring
        return False, "Structure contains too many rings"

    return True, f"Contains carboxylate anion, terminal hydroxyl group, and valid chain of length {chain_length}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140992',
                          'name': 'omega-hydroxy-long-chain fatty acid anion',
                          'definition': 'An omega-hydroxy fatty acid anion '
                                        'obtained by deprotonation of the '
                                        'carboxy group of any '
                                        'omega-hydroxy-long-chain fatty acid; '
                                        'major species at pH 7.3.',
                          'parents': ['CHEBI:57560', 'CHEBI:76307']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.19354838709677416 is too low.\n'
               'True positives: '
               "[('C(=C\\\\C(C/C=C\\\\CCCCCO)O)/C=C\\\\C/C=C\\\\CCCC(=O)[O-]', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 20'), "
               "('C(=C\\\\C/C=C\\\\CCCCCO)\\\\CCCCCCCC(=O)[O-]', 'Contains "
               'carboxylate anion, terminal hydroxyl group, and valid chain of '
               "length 18'), ('[O-]C(CCCCCCC/C=C\\\\C[C@@H](CCCCCCO)O)=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 18')]\n"
               'False positives: '
               "[('C1(C)(CO)CCC(C(=C1\\\\C=C\\\\C(=C\\\\C=C\\\\C(=C\\\\C(=O)[O-])\\\\C)\\\\C)C)=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 12'), "
               "('C1(C)(CO)CCC(C(=C1\\\\C=C\\\\C(=C\\\\C=C\\\\C(=C\\\\C(=O)[O-])\\\\C)\\\\C)C)O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 12'), ('OCCCCCCCCCC(O)CC([O-])=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 12'), "
               "('[NH3+][C@@H](CS[C@H](\\\\C=C\\\\C=C\\\\C=C/C\\\\C=C/CCCCCO)[C@@H](O)CCCC([O-])=O)C([O-])=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 20'), "
               "('C(CCCO)CC(/C=C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCC([O-])=O)O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 20'), "
               "('O[C@@](C[N+](C)(C)C)(CC([O-])=O)C=CC=CCCCCCCCCCCO', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 17'), "
               "('OCCCCCCCCCCCCCCCCCCCCCCCCCC([O-])=O', 'Contains carboxylate "
               'anion, terminal hydroxyl group, and valid chain of length '
               "26'), "
               "('[C@H]1([C@H]([C@H](O)CC1=O)/C=C/[C@H](CCCCCO)O)CCCCCCC([O-])=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 17'), "
               "('OCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC([O-])=O', 'Contains "
               'carboxylate anion, terminal hydroxyl group, and valid chain of '
               "length 30'), ('OCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC([O-])=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 32'), "
               "('[C@H]1([C@H](C=CC1=O)/C=C/[C@H](CCCCCO)O)CCCCCCC([O-])=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 17'), "
               "('[O-]C(CCC[C@@H](/C=C/C=C\\\\CCCCCCCCCO)O)=O', 'Contains "
               'carboxylate anion, terminal hydroxyl group, and valid chain of '
               "length 18'), "
               "('OCCCCC\\\\C=C/C[C@@H](O)\\\\C=C\\\\C=C\\\\C=C/[C@@H](O)CCCC([O-])=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 20'), "
               "('C1(C)(C)CCC(C(=C1/C=C/C(=C/C=C/C(=C/C(=O)[O-])/C)/C)CO)=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 12'), ('OCCCCCCCCCCCCCC(O)CC([O-])=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 16'), ('OCCCCCCCCCCCC([O-])=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 12'), "
               "('OC(C[N+](C)(C)C)(C(=O)CCCCCCCCCCCO)CC([O-])=O', 'Contains "
               'carboxylate anion, terminal hydroxyl group, and valid chain of '
               "length 15'), "
               "('C1(C)(CO)CCCC(=C1\\\\C=C\\\\C(=C\\\\C=C\\\\C(=C\\\\C(=O)[O-])\\\\C)\\\\C)C', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 12'), "
               "('[C@@]1(C)(CO)CC[C@@H](C(=C1\\\\C=C\\\\C(=C\\\\C=C\\\\C(=C\\\\C(=O)[O-])\\\\C)\\\\C)C)O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 12'), "
               "('C(\\\\[C@H]1[C@@H](CC([C@@H]1C/C=C\\\\CCCC([O-])=O)=O)O)=C/[C@H](CCCCCO)O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 17'), "
               "('[O-]C(CCCC(/C=C/C=C\\\\CCCCCCCCCO)=O)=O', 'Contains "
               'carboxylate anion, terminal hydroxyl group, and valid chain of '
               "length 18'), ('CC(CO)CCCC(C)CCCC(C)CCCC(C)CC([O-])=O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 16'), "
               "('C1(C)(C)CCCC(=C1\\\\C=C\\\\C(=C\\\\C=C\\\\C(=C\\\\C(=O)[O-])\\\\C)\\\\C)CO', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 12'), "
               "('C(C(/C=C/C=C/C=C\\\\[C@H](CCCC([O-])=O)O)=O)/C=C\\\\CCCCCO', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 20'), "
               "('C1(C)(C)CCC(C(=C1\\\\C=C\\\\C(=C\\\\C=C\\\\C(=C\\\\C(=O)[O-])\\\\C)\\\\C)CO)O', "
               "'Contains carboxylate anion, terminal hydroxyl group, and "
               "valid chain of length 12')]\n"
               'False negatives: []',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 10,
    'num_true_negatives': 183886,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.23076923076923078,
    'recall': 1.0,
    'f1': 0.375,
    'accuracy': 0.9999456223252982}