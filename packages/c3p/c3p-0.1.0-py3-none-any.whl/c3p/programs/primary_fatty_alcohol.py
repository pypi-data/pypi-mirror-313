"""
Classifies: CHEBI:142622 primary fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_primary_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is a primary fatty alcohol - a fatty alcohol where the hydroxy group 
    is attached to a methylene (CH2) group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a primary fatty alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find terminal OH groups (primary alcohols)
    primary_oh_pattern = Chem.MolFromSmarts('[CH2][OH1]')
    matches = mol.GetSubstructMatches(primary_oh_pattern)
    
    if not matches:
        return False, "No primary hydroxyl group found"

    # For each OH group found, verify it's part of a fatty chain
    for match in matches:
        carbon_idx = match[0]  # Get the carbon atom index
        carbon = mol.GetAtomWithIdx(carbon_idx)
        
        # Start BFS from the carbon to find the longest chain
        visited = set()
        queue = [(carbon, 0)]
        chain_length = 0
        
        while queue:
            current_atom, depth = queue.pop(0)
            if current_atom.GetIdx() not in visited:
                visited.add(current_atom.GetIdx())
                chain_length = max(chain_length, depth)
                
                for neighbor in current_atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'C' and neighbor.GetIdx() not in visited:
                        queue.append((neighbor, depth + 1))
        
        # Check if we have a sufficiently long carbon chain (at least 3 additional carbons)
        if chain_length >= 3:
            # Check if the molecule is not too complex (avoid complex ring systems and heavily branched structures)
            ring_count = len(mol.GetRingInfo().AtomRings())
            if ring_count > 2:  # Allow maximum 2 rings
                continue
                
            # Count number of non-carbon/hydrogen atoms
            non_ch_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() not in ['C', 'H', 'O'])
            if non_ch_count > 2:  # Allow maximum 2 non-C/H atoms (excluding the OH)
                continue
                
            return True, "Primary fatty alcohol - hydroxyl group attached to CH2"
            
    return False, "Not a primary fatty alcohol - structure too complex or chain too short"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:142622',
                          'name': 'primary fatty alcohol',
                          'definition': 'Any fatty alcohol in which the '
                                        'hydroxy group is attached to a '
                                        'methylene (CH2) group.',
                          'parents': ['CHEBI:15734', 'CHEBI:24026']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.12173913043478259 is too low.\n'
               "True positives: [('CCC(C)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CCCCO', 'Primary fatty alcohol - hydroxyl group attached to "
               "CH2'), ('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCCO', 'Primary fatty "
               "alcohol - hydroxyl group attached to CH2'), "
               "('CC(C)CCCCCCCCCCCCCCCCCCCO', 'Primary fatty alcohol - "
               "hydroxyl group attached to CH2'), ('CCCCCO', 'Primary fatty "
               "alcohol - hydroxyl group attached to CH2'), "
               "('CC(C)CCCCCCCCCCCCCCCCCCCCCCCCCCCO', 'Primary fatty alcohol - "
               "hydroxyl group attached to CH2'), ('CC(C)CCCCCCCCCCCCCCO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2')]\n"
               'False positives: '
               "[('COC1=CC=C(C=C1)S(=O)(=O)N[C@H]2CC[C@@H](O[C@H]2CO)CC(=O)NCC3=CC=CC=C3F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CCCC#CC1=CC=C(C=C1)[C@H]2[C@@H]3CN(CC(=O)N3[C@H]2CO)C(=O)NC4=CC(=CC=C4)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC=CC1=CC=C2[C@H]3[C@@H](CN2C1=O)[C@@H]([C@H](N3CCC(F)(F)F)C(=O)N(C)C)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN1[C@H]([C@@H]2CCN([C@@H]2C3=C1C=CC(=C3)Br)S(=O)(=O)C4=CC=CC(=C4)F)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC1=CC=CC=C1S(=O)(=O)NCC[C@H]2CC[C@@H]([C@H](O2)CO)NS(=O)(=O)C3=CC=CC=C3C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)C(=O)CCC(F)(F)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN(C[C@@H]1[C@H]([C@@H](N1C(=O)CC2=CN=CC=C2)CO)C3=CC=CC=C3)C(=O)COC', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1C[C@H]([C@@H](O[C@H]1CCNC(=O)C2=CC=CC=C2F)CO)NC(=O)NC3=CC=C(C=C3)C(F)(F)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CCCNC(=O)N1C[C@@H]2[C@@H]([C@@H](N2C(=O)CN3CCOCC3)CO)C4=CC=CC=C41', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3=CC=NC=C3)[C@H](C)CO)C)CN(C)CC4CCCCC4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1[C@H]2[C@H]([C@@H](N2C(=O)CN1C(=O)NC3=C(C=CC(=C3)F)F)CO)C4=CC=C(C=C4)C=CC5=CC=CC=C5', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CCCNC(=O)C[C@H]1C[C@@H]2[C@H]([C@H](O1)CO)OC3=C2C=C(C=C3)NS(=O)(=O)C4=CC=C(C=C4)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1C[C@H]([C@@H](O[C@H]1CCN2C=C(N=N2)C3CC3)CO)NC(=O)C4=CN=CC=C4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('COCCNC(=O)C[C@H]1C[C@H]2[C@@H]([C@@H](O1)CO)OC3=C2C=C(C=C3)NS(=O)(=O)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1C[C@H]([C@H](O[C@H]1CC(=O)NCCC2=CC=NC=C2)CO)NS(=O)(=O)C3=CC=C(C=C3)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1[C@H](O[C@H]([C@@H]2[C@H]1C3=C(O2)C=CC(=C3)NC(=O)NC4=CC=C(C=C4)C(F)(F)F)CO)CC(=O)NCC5=CN=CC=C5', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CCNC(=O)[C@@H]1[C@H]([C@@H]2CN3C(=CC=C(C3=O)C4=CC=CC=C4)[C@H]1N2CCC(F)(F)F)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN(C)C(=O)C[C@H]1C[C@H]2[C@@H]([C@H](O1)CO)OC3=C2C=C(C=C3)NC(=O)C4=CN=CC=C4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN(C)CC(=O)N[C@@H]1C=C[C@H](O[C@@H]1CO)CC(=O)NCC2=CC=CC=C2OC', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3CCCCC3)[C@@H](C)CO)C)CN(C)CC4=CC=NC=C4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC1=CC=C(C=C1)S(=O)(=O)N[C@@H]2CC[C@@H](O[C@@H]2CO)CC(=O)NCCCN(C)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N)[C@@H](C)CO)C)CNC', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H](C1=CC=CC=C1)NC(=O)C[C@H]2C[C@H]3[C@@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)NC5CCCCC5', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC(C)NC(=O)N1CC2(C1)[C@H]([C@H](N2C(=O)C3CCCC3)CO)C4=CC=CC=C4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN(C)CC1=CN(N=N1)CC[C@H]2CC[C@@H]([C@@H](O2)CO)NC(=O)CC3=CN=CC=C3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)CC3=CC4=C(C=C3)OCO4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3=CC=NC=C3)[C@@H](C)CO)C)CN(C)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('O=C(NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(C)C)CC(C)C)CCC(=O)N)C)C)(C)C)CCC(=O)N)(C)C)CC(C)C)(C)C)C(NC(=O)C(NC(=O)C(NC(=O)C)CC=1C2=C(C=CC=C2)NC1)C)(C)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1C[C@@H]([C@@H](O[C@@H]1CC(=O)NCCC2=CC=NC=C2)CO)NC(=O)CC3=CC=CC=N3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CCC1=CN=C(S1)N2[C@@H]([C@H]([C@H]2C#N)C3=CC=C(C=C3)C#CC(C)C)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC1=C(C(=NO1)C)NC(=O)N[C@H]2CC[C@@H](O[C@H]2CO)CC(=O)N3CCN(CC3)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('[NH3+][C@@H](CCO)C([O-])=O', 'Primary fatty alcohol - "
               "hydroxyl group attached to CH2'), "
               "('C1CCC(CC1)C(=O)N[C@H]2CC[C@H](O[C@@H]2CO)CCNC(=O)C3=CC=C(C=C3)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC1C=NC(=N1)S(=O)(=O)N2CC[C@H]3[C@@H]2C4=C(C=CC(=C4)C5=CC=CC=C5F)N([C@@H]3CO)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)CCCN(C)C)[C@H](C)CO)C)CN(C)C(=O)C3=CC=CC=C3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1CCC(=CC1)C2=CC=C(C=C2)[C@@H]3[C@H](N([C@@H]3C#N)C(=O)CC4=CC=NC=C4)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('O1[C@H]2C(=CC[C@H]3[C@H]2[C@]4(OC(C)(C)O[C@H]4C[C@@H]3C)[C@@H](C1)CO)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN1C=C(N=C1)S(=O)(=O)N[C@@H]2C=C[C@@H](O[C@@H]2CO)CC(=O)NCC3CC3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN(C)CC1=CN(N=N1)CC[C@@H]2CC[C@H]([C@@H](O2)CO)NC(=O)NC3=CC4=C(C=C3)OCO4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)CCCN(C)C)[C@H](C)CO)C)CN(C)S(=O)(=O)C3=CC=CC=C3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3=CC=CC=C3)[C@H](C)CO)C)CN(C)C(=O)NC(C)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)C(=O)C3=CC=CC=C3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1CC1CC(=O)NC2=CC3=C(C=C2)O[C@@H]4[C@H]3C[C@@H](O[C@@H]4CO)CC(=O)NCC5=C(C=CC(=C5)F)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1COCCC1C(=O)NC2=CC3=C(C=C2)O[C@@H]4[C@H]3C[C@H](O[C@@H]4CO)CC(=O)NCC5=C(C=CC(=C5)F)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)S(=O)(=O)C3=CC=C(C=C3)OC', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1=CC=C(C=C1)C2C=C(N=C3N2NC(=N3)CCCO)C4=CC=C(C=C4)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CCO[C@@H]1[C@H]([C@@H](C=C(O1)C(=O)NCC#C)C2CC2)CCCO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CS(=O)(=O)NC1=CC2=C(C=C1)O[C@H]3[C@@H]2C[C@H](O[C@@H]3CO)CC(=O)NCC4=CC=C(C=C4)OC5=CC=CC=C5', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H](C1=CC=CC=C1)NC(=O)C[C@H]2C=C[C@H]([C@@H](O2)CO)NC(=O)NC3=CC4=C(C=C3)OCO4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN(C)CC(=O)NC1=CC2=C(C=C1)O[C@H]3[C@@H]2C[C@@H](O[C@H]3CO)CC(=O)NC4CCCCC4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1[C@H](O[C@H]([C@H]2[C@@H]1C3=C(O2)C=CC(=C3)NC(=O)NC4=CC=C(C=C4)C(F)(F)F)CO)CC(=O)NCC5=CC=CC=N5', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('COC(=O)C1CNC(CO)C1', 'Primary fatty alcohol - hydroxyl group "
               "attached to CH2'), "
               "('C1CCN(CC1)C(=O)C[C@@H]2C=C[C@@H]([C@H](O2)CO)NC(=O)C3=CC4=C(C=C3)OCO4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('COC1=CC=CC(=C1)CNC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=O)C=CC=C4[C@H]2N3C(=O)C5CCCCC5)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC1=CC=CC=C1S(=O)(=O)N2CC[C@H]3[C@@H]2C4=C(C=CC(=C4)C5=CC(=CC=C5)OC)N[C@@H]3CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CS(=O)(=O)N1C[C@H]2[C@@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)Br', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN(C[C@H]1[C@H]([C@H](N1CC2=CC=CC=N2)CO)C3=CC=CC=C3)S(=O)(=O)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NS(=O)(=O)C3=CC=C(C=C3)F)[C@H](C)CO)C)CNC', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('O=C(N)/C(=C/C(=O)CC12C3[C@@H](C(CO)(CC1C3)OC2)C)/C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1C[C@@H]([C@@H](O[C@@H]1CCNC(=O)C2CC2)CO)NC(=O)NC3=CC4=C(C=C3)OCO4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1C[C@@H]([C@H](O[C@@H]1CCN2C=C(N=N2)C3=CC=CC=N3)CO)NC(=O)C4=CC=C(C=C4)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1CC1CC(=O)NC2=CC3=C(C=C2)O[C@@H]4[C@H]3C[C@@H](O[C@H]4CO)CC(=O)NCC(F)(F)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('OCCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC([O-])=O', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC1=CC=C(C=C1)S(=O)(=O)N2CC[C@@H]3[C@H]2C4=C(C=CC(=C4)C5=CC(=CC=C5)C(=O)N(C)C)N[C@H]3CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('O(C[C@](CO)(OC(CCCCCCCCC/C=C\\\\CCCCCC)=O)[H])C(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('[H][C@]12CC[C@]([H])(C[C@@H](C1)OC(=O)C(CO)c1ccccc1)[N@+]2(C)C(C)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)CC3=CC=CC=C3)[C@H](C)CO)C)CN(C)C(=O)NC(C)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1C[C@@H]([C@H](O[C@H]1CCNS(=O)(=O)C2=CC=C(C=C2)Cl)CO)NC(=O)C3=CC=CC=N3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=CC=C3)[C@H](C)CO)C)CN(C)CC4CC4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1[C@H](O[C@@H]([C@@H]2[C@H]1C3=C(O2)C=CC(=C3)NC(=O)NC4=CC=CC=C4F)CO)CC(=O)NCC5=CC=C(C=C5)OC6=CC=CC=C6', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3=CC=CC=C3)[C@@H](C)CO)C)CN(C)CC4=CC=NC=C4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC1=CC=CC(=C1)C2=CC=C(C=C2)[C@H]3[C@@H]4CN(CCCCN4[C@@H]3CO)S(=O)(=O)C5=CC=CC=C5F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1[C@@H]2[C@@H]([C@H](N2C(=O)C3=CC=CC=N3)CO)C4=CC=CC=C4N1C(=O)C5=CC=NC=C5', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)C(=O)NC(C)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CS(=O)(=O)NC1=CC2=C(C=C1)O[C@@H]3[C@H]2C[C@H](O[C@@H]3CO)CC(=O)NCC4=C(C=CC(=C4)F)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NS(=O)(=O)C)[C@H](C)CO)C)CN(C)CC3=CC4=C(C=C3)OCO4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('COC1=CC=C(C=C1)NC(=O)N[C@@H]2CC[C@H](O[C@@H]2CO)CC(=O)NC3CCC3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CC=CC=C3OC)O[C@@H]1CN(C)CC4CCOCC4)[C@H](C)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H](C1=CC=CC=C1)NC(=O)C[C@@H]2CC[C@H]([C@H](O2)CO)NC(=O)NC3=CC4=C(C=C3)OCO4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NS(=O)(=O)C)[C@H](C)CO)C)CN(C)CC3=CC=C(C=C3)OC', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1C=2C=3C(NC2[C@]4(N5[C@@]1([C@]([C@](C4)(/C(/C5)=C(\\\\C)/[H])[H])(CO)C(OC)=O)[H])[H])=CC=CC3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1C[C@H]([C@H](O[C@@H]1CC(=O)NCCCN2CCOCC2)CO)NC(=O)NC3=CC4=C(C=C3)OCO4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C1=CC=C(C(=C1)C#CC2=CC=C(C=C2)[C@@H]3[C@H](N([C@@H]3C#N)C(=O)C4=CN=CC=C4)CO)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)C(=O)C5=CC=NC=C5)C(=O)C6CCOCC6)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC1=C(C(=NO1)C)NC(=O)N[C@@H]2CC[C@@H](O[C@H]2CO)CC(=O)NC3=CC=C(C=C3)C4=CC=CC=C4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('O(CC(C(CC1=CC=2OCOC2C=C1)CO)CC3=CC=4OCOC4C=C3)C(=O)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC(C)NC(=O)N1CC[C@@H]2[C@H]1C3=C(C=CC(=C3)Br)N([C@H]2CO)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CCC1=CN=C(S1)N2[C@H]([C@H]([C@@H]2C#N)C3=CC=C(C=C3)C4=CCCC4)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3CCCCC3)[C@H](C)CO)C)CN(C)CC4=CC=C(C=C4)OC', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('O=C1C(=C2[C@@](CC2)(C)[C@@H]3[C@H]1C[C@](CO)(C)C3)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN(C)C(=O)C[C@@H]1C[C@@H]2[C@H]([C@@H](O1)CO)OC3=C2C=C(C=C3)NS(=O)(=O)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN(C)CC1=CN(N=N1)CC[C@@H]2CC[C@@H]([C@@H](O2)CO)NC(=O)NC3=CC4=C(C=C3)OCO4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CC=CC=C3OC)O[C@@H]1CN(C)CC4CCOCC4)[C@@H](C)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CCNC(=O)C[C@@H]1C=C[C@@H]([C@H](O1)CO)NS(=O)(=O)C2=CC=C(C=C2)F', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3CCCCC3)[C@H](C)CO)C)CN(C)CC4=CC=NC=C4', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('COC1=CC=C(C=C1)S(=O)(=O)N[C@H]2CC[C@H](O[C@H]2CO)CCNC(=O)CC3=CC=CC=N3', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CC1=CC=CC=C1S(=O)(=O)NCC[C@@H]2CC[C@H]([C@H](O2)CO)NS(=O)(=O)C3=CC=CC=C3C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('CN1[C@H]2CN3C(=CC=C(C3=O)C4=CC=C(C=C4)F)[C@@H]1[C@@H]([C@H]2CO)C(=O)NC5CCC5', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('C[C@@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=CC=C3)[C@H](C)CO)C)CN(C)C', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2'), "
               "('COC(=O)\\\\C=C(/C)CC\\\\C=C(/C)CC[C@H]1O[C@]1(C)CO', "
               "'Primary fatty alcohol - hydroxyl group attached to CH2')]\n"
               "False negatives: [('CCCCCC(/C=C/CO)O', 'Multiple hydroxyl "
               "groups found - not a primary fatty alcohol')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 2411,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 1.0,
    'f1': 0.13793103448275862,
    'accuracy': 0.9603017070265979}