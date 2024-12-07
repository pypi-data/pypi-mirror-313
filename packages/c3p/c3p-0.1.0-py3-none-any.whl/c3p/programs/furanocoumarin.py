"""
Classifies: CHEBI:24128 furanocoumarin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetSymmSSSR

def is_furanocoumarin(smiles: str):
    """
    Determines if a molecule is a furanocoumarin based on presence of fused furan and coumarin rings.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a furanocoumarin, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Get ring systems
    rings = list(GetSymmSSSR(mol))
    if len(rings) < 3:
        return False, "Too few rings - needs fused furan and coumarin"
        
    # Look for furan ring (5-membered with O)
    furan_rings = []
    for ring in rings:
        if len(ring) == 5:
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if any(atom.GetSymbol() == 'O' for atom in ring_atoms):
                if all(atom.GetIsAromatic() for atom in ring_atoms):
                    furan_rings.append(ring)
                    
    if not furan_rings:
        return False, "No furan ring found"
        
    # Look for pyrone ring (6-membered with O and C=O)
    pyrone_rings = []
    for ring in rings:
        if len(ring) == 6:
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check for O in ring
            has_o = False
            for atom in ring_atoms:
                if atom.GetSymbol() == 'O':
                    has_o = True
                    break
            if not has_o:
                continue
                
            # Check for carbonyl group
            has_carbonyl = False
            for atom_idx in ring:
                atom = mol.GetAtomWithIdx(atom_idx)
                if atom.GetSymbol() == 'C':
                    for bond in atom.GetBonds():
                        other_idx = bond.GetOtherAtomIdx(atom_idx)
                        other = mol.GetAtomWithIdx(other_idx)
                        if other.GetSymbol() == 'O' and bond.GetBondType() == Chem.BondType.DOUBLE:
                            has_carbonyl = True
                            break
                            
            if has_carbonyl:
                pyrone_rings.append(ring)
                
    if not pyrone_rings:
        return False, "No pyrone ring found"
        
    # Check if rings are fused (share atoms)
    benzene_rings = []
    for ring in rings:
        if len(ring) == 6:
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in ring_atoms):
                if all(atom.GetSymbol() == 'C' for atom in ring_atoms):
                    benzene_rings.append(ring)
                    
    if not benzene_rings:
        return False, "No benzene ring found"
        
    # Check fusion between rings
    for furan in furan_rings:
        for benzene in benzene_rings:
            shared = set(furan).intersection(set(benzene))
            if len(shared) == 2:  # Fused rings share 2 atoms
                for pyrone in pyrone_rings:
                    shared2 = set(benzene).intersection(set(pyrone))
                    if len(shared2) == 2:
                        return True, "Found fused furan-benzene-pyrone ring system"
                        
    return False, "Rings not properly fused"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24128',
                          'name': 'furanocoumarin',
                          'definition': 'Any furochromene that consists of a '
                                        'furan ring fused with a coumarin. The '
                                        'fusion may occur in different ways in '
                                        'give several isomers.',
                          'parents': ['CHEBI:39432']},
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
    'num_true_positives': 10,
    'num_false_positives': 64,
    'num_true_negatives': 183662,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.13513513513513514,
    'recall': 0.5,
    'f1': 0.21276595744680854,
    'accuracy': 0.9995972701446562}