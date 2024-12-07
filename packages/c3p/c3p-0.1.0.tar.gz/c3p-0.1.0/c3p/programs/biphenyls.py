"""
Classifies: CHEBI:22888 biphenyls
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_biphenyls(smiles: str):
    """
    Determines if a molecule is a biphenyl compound (two phenyl/substituted phenyl rings joined by single bond).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a biphenyl, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Get all aromatic rings
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)
                
    if len(aromatic_rings) < 2:
        return False, "Fewer than 2 aromatic rings found"
        
    # Check for direct single bond connection between any two aromatic rings
    for ring1 in aromatic_rings:
        ring1_atoms = set(ring1)
        for ring2 in aromatic_rings:
            if ring1 == ring2:
                continue
            ring2_atoms = set(ring2)
            
            # Check for single bond between rings
            for atom1_idx in ring1:
                atom1 = mol.GetAtomWithIdx(atom1_idx)
                for bond in atom1.GetBonds():
                    atom2_idx = bond.GetOtherAtomIdx(atom1_idx)
                    if (atom2_idx in ring2_atoms and 
                        bond.GetBondType() == Chem.BondType.SINGLE):
                        
                        # Check if both rings are phenyl or substituted phenyl
                        ring1_atoms_list = [mol.GetAtomWithIdx(i) for i in ring1]
                        ring2_atoms_list = [mol.GetAtomWithIdx(i) for i in ring2]
                        
                        if all(atom.GetSymbol() == 'C' for atom in ring1_atoms_list) and \
                           all(atom.GetSymbol() == 'C' for atom in ring2_atoms_list):
                            
                            # Get substituents
                            substituents = []
                            for ring_atoms in [ring1_atoms, ring2_atoms]:
                                for atom_idx in ring_atoms:
                                    atom = mol.GetAtomWithIdx(atom_idx)
                                    for neighbor in atom.GetNeighbors():
                                        if neighbor.GetIdx() not in ring1_atoms and \
                                           neighbor.GetIdx() not in ring2_atoms:
                                            substituents.append(neighbor.GetSymbol())
                                            
                            if len(substituents) > 0:
                                return True, f"Substituted biphenyl with substituents: {', '.join(set(substituents))}"
                            else:
                                return True, "Unsubstituted biphenyl"
                            
    return False, "No direct single bond connection between phenyl rings found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22888',
                          'name': 'biphenyls',
                          'definition': 'Benzenoid aromatic compounds '
                                        'containing two phenyl or '
                                        'substituted-phenyl groups which are '
                                        'joined together by a single bond.',
                          'parents': [   'CHEBI:33836',
                                         'CHEBI:36820',
                                         'CHEBI:64459']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 124,
    'num_false_positives': 100,
    'num_true_negatives': 7020,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.5535714285714286,
    'recall': 1.0,
    'f1': 0.7126436781609196,
    'accuracy': 0.9861954721148537}