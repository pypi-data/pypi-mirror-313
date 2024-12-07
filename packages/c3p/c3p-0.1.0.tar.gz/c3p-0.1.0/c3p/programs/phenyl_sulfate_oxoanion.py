"""
Classifies: CHEBI:140317 phenyl sulfate oxoanion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phenyl_sulfate_oxoanion(smiles: str):
    """
    Determines if a molecule is a phenyl sulfate oxoanion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phenyl sulfate oxoanion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of aromatic ring
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)
    
    if not aromatic_rings:
        return False, "No aromatic ring found"

    # Check for phenyl group (all carbons in aromatic ring)
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if all(atom.GetSymbol() == 'C' for atom in atoms):
            phenyl_ring = ring
            break
    else:
        return False, "No phenyl ring found"

    # Look for sulfate oxoanion group (-OS([O-])(=O)=O) attached to phenyl
    found_sulfate = False
    for atom_idx in phenyl_ring:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'O':  # Check for O attached to phenyl
                for next_neighbor in neighbor.GetNeighbors():
                    if next_neighbor.GetSymbol() == 'S':  # Check for S attached to O
                        s_atom = next_neighbor
                        s_neighbors = list(s_atom.GetNeighbors())
                        
                        # Check for sulfate pattern: 4 oxygens (including the phenyl-O),
                        # with at least one negative charge and two double bonds
                        if len(s_neighbors) == 4 and \
                           all(n.GetSymbol() == 'O' for n in s_neighbors) and \
                           sum(n.GetFormalCharge() for n in s_neighbors) <= -1 and \
                           len([b for b in mol.GetBonds() if b.GetBeginAtomIdx() == s_atom.GetIdx() 
                               and b.GetBondType() == Chem.BondType.DOUBLE]) == 2:
                            found_sulfate = True
                            break
                            
    if found_sulfate:
        return True, "Contains phenyl ring with sulfate oxoanion group"
    else:
        return False, "No sulfate oxoanion group found attached to phenyl ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140317',
                          'name': 'phenyl sulfate oxoanion',
                          'definition': 'An aryl sulfate oxoanion obtained by '
                                        'deprotonation of the sulfo group of '
                                        'any phenyl sulfate; major species at '
                                        'pH 7.3.',
                          'parents': ['CHEBI:139371']},
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
    'num_true_positives': 2,
    'num_false_positives': 42,
    'num_true_negatives': 183866,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.045454545454545456,
    'recall': 1.0,
    'f1': 0.08695652173913045,
    'accuracy': 0.9997716274264586}