"""
Classifies: CHEBI:26776 stilbenoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import FindMolChiralCenters

def is_stilbenoid(smiles: str):
    """
    Determines if a molecule is a stilbenoid (contains 1,2-diphenylethylene backbone).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a stilbenoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find double bonds
    double_bonds = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
            double_bonds.append(bond)
    
    if not double_bonds:
        return False, "No double bonds found"

    # For each double bond, check if it connects two carbons with phenyl groups
    for bond in double_bonds:
        start_atom = bond.GetBeginAtom()
        end_atom = bond.GetEndAtom()
        
        # Check if both atoms are carbons
        if start_atom.GetSymbol() != 'C' or end_atom.GetSymbol() != 'C':
            continue
            
        # Get neighboring atoms excluding the double bond
        start_neighbors = [n for n in start_atom.GetNeighbors() if n.GetIdx() != end_atom.GetIdx()]
        end_neighbors = [n for n in end_atom.GetNeighbors() if n.GetIdx() != start_atom.GetIdx()]

        # Check for phenyl groups on both sides
        start_phenyl = False
        end_phenyl = False
        
        # Helper function to find 6-membered aromatic rings
        def find_aromatic_ring(start_atom, center_atom):
            visited = set()
            ring = set()
            
            def dfs(atom, prev_atom, depth):
                if depth > 6:
                    return False
                visited.add(atom.GetIdx())
                ring.add(atom.GetIdx())
                
                if depth == 6:
                    # Check if we can get back to start
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetIdx() == start_atom.GetIdx():
                            # Verify all atoms are aromatic
                            for idx in ring:
                                if not mol.GetAtomWithIdx(idx).GetIsAromatic():
                                    return False
                            return True
                    return False
                
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetIdx() == prev_atom.GetIdx():
                        continue
                    if neighbor.GetIdx() not in visited:
                        if dfs(neighbor, atom, depth + 1):
                            return True
                ring.remove(atom.GetIdx())
                return False
                
            return dfs(start_atom, center_atom, 1)

        # Check each neighbor for phenyl groups
        for neighbor in start_neighbors:
            if neighbor.GetIsAromatic():
                if find_aromatic_ring(neighbor, start_atom):
                    start_phenyl = True
                    break
                    
        for neighbor in end_neighbors:
            if neighbor.GetIsAromatic():
                if find_aromatic_ring(neighbor, end_atom):
                    end_phenyl = True
                    break

        if start_phenyl and end_phenyl:
            return True, "Contains 1,2-diphenylethylene backbone"
            
    return False, "No 1,2-diphenylethylene backbone found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26776',
                          'name': 'stilbenoid',
                          'definition': 'Any olefinic compound characterised '
                                        'by a 1,2-diphenylethylene backbone.',
                          'parents': ['CHEBI:33659', 'CHEBI:78840']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot access local variable 'find_ring' where "
               'it is not associated with a value',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 82003,
    'num_false_negatives': 51,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 0.08928571428571429,
    'f1': 0.06211180124223601,
    'accuracy': 0.9981621003176767}