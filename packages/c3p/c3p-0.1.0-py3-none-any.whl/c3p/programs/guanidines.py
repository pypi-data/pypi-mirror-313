"""
Classifies: CHEBI:24436 guanidines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_guanidines(smiles: str):
    """
    Determines if a molecule contains a guanidino group with general structure (R(1)R(2)N)(R(3)R(4)N)C=N-R(5)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains guanidino group, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # SMARTS pattern for guanidino group: (R(1)R(2)N)(R(3)R(4)N)C=N-R(5)
    # Note: [#6] is carbon, [#7] is nitrogen
    guanidino_pattern = Chem.MolFromSmarts('[#7][#6](=[#7])[#7]')
    
    if mol.HasSubstructMatch(guanidino_pattern):
        matches = mol.GetSubstructMatches(guanidino_pattern)
        
        # Get atoms in the matched pattern
        for match in matches:
            n1, c, n2, n3 = match
            
            # Get the atoms
            n1_atom = mol.GetAtomWithIdx(n1)
            c_atom = mol.GetAtomWithIdx(c)
            n2_atom = mol.GetAtomWithIdx(n2)
            n3_atom = mol.GetAtomWithIdx(n3)
            
            # Verify carbon has double bond to one nitrogen
            double_bond_count = 0
            for bond in c_atom.GetBonds():
                if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE and \
                   bond.GetOtherAtom(c_atom).GetAtomicNum() == 7:
                    double_bond_count += 1
                    
            if double_bond_count == 1:
                # Count number of nitrogens connected to the central carbon
                n_count = 0
                for atom in c_atom.GetNeighbors():
                    if atom.GetAtomicNum() == 7:
                        n_count += 1
                        
                if n_count == 3:
                    return True, "Contains guanidino group (R(1)R(2)N)(R(3)R(4)N)C=N-R(5)"
                    
    return False, "Does not contain guanidino group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24436',
                          'name': 'guanidines',
                          'definition': 'Any organonitrogen compound '
                                        'containing a carbamimidamido '
                                        '(guanidino) group. Guanidines have '
                                        'the general structure '
                                        '(R(1)R(2)N)(R(3)R(4)N)C=N-R(5) and '
                                        'are related structurally to amidines '
                                        'and ureas.',
                          'parents': ['CHEBI:35352']},
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
    'num_true_positives': 19,
    'num_false_positives': 100,
    'num_true_negatives': 6139,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.15966386554621848,
    'recall': 1.0,
    'f1': 0.2753623188405797,
    'accuracy': 0.9840204538191115}