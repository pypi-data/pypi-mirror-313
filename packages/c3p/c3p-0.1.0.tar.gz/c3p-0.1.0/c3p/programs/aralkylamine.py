"""
Classifies: CHEBI:18000 aralkylamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aralkylamine(smiles: str):
    """
    Determines if a molecule is an aralkylamine (alkylamine with aromatic substituent).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aralkylamine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for amine groups (-NH2, -NHR, -NR2) not part of amides/sulfonamides/aromatic rings
    pattern_amine = Chem.MolFromSmarts('[NX3;H2,H1,H0;!$(NC=O);!$(NS=O);!$(N=*);!$(n)]')
    if pattern_amine is None:
        return None, "Invalid amine SMARTS pattern"
    amine_matches = mol.GetSubstructMatches(pattern_amine)
    
    if not amine_matches:
        return False, "No aliphatic amine groups found"

    # Look for aromatic rings
    aromatic_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetIsAromatic()]
    if not aromatic_atoms:
        return False, "No aromatic rings found"
    
    # For each amine, check if it's connected to an aromatic ring through a carbon chain
    for amine_match in amine_matches:
        amine_idx = amine_match[0]
        amine_atom = mol.GetAtomWithIdx(amine_idx)
        
        # Get neighboring carbon atoms of the amine
        carbon_neighbors = [neighbor for neighbor in amine_atom.GetNeighbors() 
                          if neighbor.GetSymbol() == 'C' and not neighbor.GetIsAromatic()]
        
        for carbon in carbon_neighbors:
            # Check if this carbon is part of a path to an aromatic ring
            visited = set()
            stack = [(carbon, [carbon.GetIdx()])]
            
            while stack:
                current_atom, path = stack.pop()
                
                if current_atom.GetIdx() in visited:
                    continue
                    
                visited.add(current_atom.GetIdx())
                
                if current_atom.GetIsAromatic():
                    chain_length = len(path) - 1  # Exclude the aromatic atom
                    ring_type = "aromatic ring"
                    if current_atom.GetSymbol() == 'C':
                        ring_type = "benzene ring"
                    elif current_atom.GetSymbol() == 'N':
                        ring_type = "pyridine ring"
                    elif current_atom.GetSymbol() == 'O':
                        ring_type = "furan ring"
                    elif current_atom.GetSymbol() == 'S':
                        ring_type = "thiophene ring"
                    return True, f"Found aralkylamine with {chain_length}-carbon chain connecting {ring_type} to amine"
                
                for neighbor in current_atom.GetNeighbors():
                    if (neighbor.GetSymbol() == 'C' and neighbor.GetIdx() not in path) or neighbor.GetIsAromatic():
                        new_path = path + [neighbor.GetIdx()]
                        stack.append((neighbor, new_path))
                        
    return False, "No alkyl chain connecting aromatic ring to amine found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18000',
                          'name': 'aralkylamine',
                          'definition': 'An alkylamine in which the alkyl '
                                        'group is substituted by an aromatic '
                                        'group.',
                          'parents': ['CHEBI:22331', 'CHEBI:64365']},
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
               "False negatives: [('O1C(C=2C(CNCC1)=CC=CC2)C3=CC=CC=C3', "
               "'Invalid aralkyl SMARTS pattern'), "
               "('C1NC(=NCN1CC2=CC=CC=C2)NC#N', 'Invalid aralkyl SMARTS "
               "pattern'), ('C1=CC=C(C=C1)CNC2=NC(=O)C(=CC3=CC=C(C=C3)O)S2', "
               "'Invalid aralkyl SMARTS pattern'), "
               "('CC1=C(C(=NC1=C2CSC(=NN2)NCC3=CC=CC=C3)C)C(=O)C', 'Invalid "
               "aralkyl SMARTS pattern'), ('O1C(C2NCCCC2)=CC=C1C', 'No "
               "aromatic rings found'), "
               "('C1=CC=C(C=C1)CNC2=NC(=O)C(=CC3=CC=CC=C3)S2', 'Invalid "
               "aralkyl SMARTS pattern'), "
               "('O(C(=O)[C@@H]([C@@]1(NCCCC1)[H])C2=CC=CC=C2)CC', 'Invalid "
               "aralkyl SMARTS pattern'), "
               "('CC1=CC=C(O1)C(=O)CCNC2=CC(=CC=C2)Br', 'Invalid aralkyl "
               "SMARTS pattern'), "
               "('C[C@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@@H]1CN(C)CC4=CN=CC=C4)[C@@H](C)CO', "
               "'Invalid aralkyl SMARTS pattern'), "
               "('CCNC(=O)C[C@H]1CC[C@@H]2[C@@H](O1)COC[C@@H](CN2CC3=CC=NC=C3)O', "
               "'Invalid aralkyl SMARTS pattern'), "
               "('O[C@H]1[C@H](NCC(C)C)[C@H](C[C@H]1O)C=2C=CC=NC2', 'Invalid "
               "aralkyl SMARTS pattern'), ('S1C(CNC)=CC=C1C2=CC=NC=C2', "
               "'Invalid aralkyl SMARTS pattern'), "
               "('C1=COC(=C1)C2=CC(=NC(=N2)NCC3=CC=C(C=C3)Cl)C(F)(F)F', "
               "'Invalid aralkyl SMARTS pattern')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 13,
    'num_false_positives': 100,
    'num_true_negatives': 1019,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.11504424778761062,
    'recall': 1.0,
    'f1': 0.20634920634920637,
    'accuracy': 0.911660777385159}