"""
Classifies: CHEBI:22715 benzimidazoles
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_benzimidazoles(smiles: str):
    """
    Determines if a molecule is a benzimidazole (benzene ring fused to an imidazole ring).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a benzimidazole, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define SMARTS pattern for benzimidazole core structure
    # [nH]1cnc2ccccc12 or n1c[nH]c2ccccc12
    benzimidazole_pattern = Chem.MolFromSmarts('[nH]1cnc2ccccc12')
    benzimidazole_pattern2 = Chem.MolFromSmarts('n1c[nH]c2ccccc12')
    
    # Also check for N-substituted variants
    n_subst_pattern = Chem.MolFromSmarts('n1cnc2ccccc12')

    matches = mol.GetSubstructMatches(benzimidazole_pattern)
    matches2 = mol.GetSubstructMatches(benzimidazole_pattern2)
    n_subst_matches = mol.GetSubstructMatches(n_subst_pattern)

    if matches or matches2 or n_subst_matches:
        # Find substituents
        substituents = []
        if matches or matches2:
            core_atoms = set(matches[0] if matches else matches2[0])
        else:
            core_atoms = set(n_subst_matches[0])
            
        for atom_idx in core_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in core_atoms:
                    substituents.append(neighbor.GetSymbol())

        if len(substituents) > 0:
            return True, f"Substituted benzimidazole with substituents at: {', '.join(set(substituents))}"
        else:
            return True, "Unsubstituted benzimidazole"
            
    return False, "No benzimidazole core structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22715',
                          'name': 'benzimidazoles',
                          'definition': 'An organic heterocyclic compound '
                                        'containing a benzene ring fused to an '
                                        'imidazole ring.',
                          'parents': ['CHEBI:27171', 'CHEBI:38101']},
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
    'num_true_positives': 39,
    'num_false_positives': 100,
    'num_true_negatives': 73271,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.2805755395683453,
    'recall': 0.975,
    'f1': 0.43575418994413406,
    'accuracy': 0.9986241843865361}