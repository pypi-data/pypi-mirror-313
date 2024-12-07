"""
Classifies: CHEBI:24922 isoquinolines
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import HybridizationType

def is_isoquinolines(smiles: str):
    """
    Determines if a molecule is an isoquinoline or derivative.
    Isoquinolines contain a benzene ring fused to a pyridine ring.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an isoquinoline, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get ring information
    rings = mol.GetRingInfo()
    
    # Look for 6-membered rings
    ring_atoms_list = rings.AtomRings()
    
    for i in range(len(ring_atoms_list)):
        ring1 = ring_atoms_list[i]
        if len(ring1) != 6:
            continue
            
        # Check if ring1 has exactly one aromatic nitrogen
        ring1_atoms = [mol.GetAtomWithIdx(idx) for idx in ring1]
        ring1_ar_n = sum(1 for atom in ring1_atoms if atom.GetSymbol() == 'N' and atom.GetIsAromatic())
        
        if ring1_ar_n != 1:
            continue
            
        # Look for adjacent 6-membered ring
        for j in range(len(ring_atoms_list)):
            if i == j:
                continue
                
            ring2 = ring_atoms_list[j]
            if len(ring2) != 6:
                continue
                
            # Check if rings share exactly 2 atoms (fused)
            shared_atoms = set(ring1).intersection(set(ring2))
            if len(shared_atoms) != 2:
                continue
                
            # Check if ring2 is benzene (all carbons)
            ring2_atoms = [mol.GetAtomWithIdx(idx) for idx in ring2]
            if all(atom.GetSymbol() == 'C' and atom.GetIsAromatic() for atom in ring2_atoms):
                # Found isoquinoline core
                # Check for substituents
                all_ring_atoms = set(ring1).union(set(ring2))
                substituents = []
                for atom_idx in all_ring_atoms:
                    atom = mol.GetAtomWithIdx(atom_idx)
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetIdx() not in all_ring_atoms:
                            substituents.append(neighbor.GetSymbol())
                            
                if substituents:
                    return True, f"Substituted isoquinoline with substituents: {', '.join(set(substituents))}"
                else:
                    return True, "Unsubstituted isoquinoline"
                
    return False, "No isoquinoline core found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24922',
                          'name': 'isoquinolines',
                          'definition': 'A class of organic heteropolycyclic '
                                        'compound consisting of isoquinoline '
                                        'and its substitution derivatives.',
                          'parents': ['CHEBI:38101', 'CHEBI:38166']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_positives': 10,
    'num_false_positives': 100,
    'num_true_negatives': 8221,
    'num_false_negatives': 56,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 0.15151515151515152,
    'f1': 0.11363636363636363,
    'accuracy': 0.981399785382139}