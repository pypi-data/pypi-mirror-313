"""
Classifies: CHEBI:140326 tertiary carboxamide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_tertiary_carboxamide(smiles: str):
    """
    Determines if a molecule contains a tertiary carboxamide group (RC(=O)NR1R2).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains a tertiary carboxamide, False otherwise
        str: Reason for classification
    """
    # Convert SMILES to RDKit mol object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Standardize the molecule
    uncharger = rdMolStandardize.Uncharger()
    mol = uncharger.uncharge(mol)
    
    # SMARTS pattern for tertiary carboxamide: RC(=O)NR1R2 
    # where R, R1, R2 are not hydrogen
    pattern = Chem.MolFromSmarts('[C;!$(C([#1])[#1])](=[O;!$(O[#1])])([!$([OH1])])[N;!$(N[#1])]([#6;!$([#6][#1])])([#6;!$([#6][#1])])')
    
    if mol.HasSubstructMatch(pattern):
        matches = mol.GetSubstructMatches(pattern)
        
        # Get atoms involved in the match
        for match in matches:
            c_atom = mol.GetAtomWithIdx(match[0])  # Carbon
            o_atom = mol.GetAtomWithIdx(match[1])  # Oxygen
            n_atom = mol.GetAtomWithIdx(match[3])  # Nitrogen
            r1_atom = mol.GetAtomWithIdx(match[4]) # R1 substituent
            r2_atom = mol.GetAtomWithIdx(match[5]) # R2 substituent
            
            # Verify it's a tertiary carboxamide
            if (c_atom.GetSymbol() == 'C' and 
                o_atom.GetSymbol() == 'O' and
                n_atom.GetSymbol() == 'N' and
                n_atom.GetTotalNumHs() == 0):  # No hydrogens on N
                
                return True, f"Contains tertiary carboxamide group with substituents {r1_atom.GetSymbol()} and {r2_atom.GetSymbol()} on nitrogen"
                
    return False, "No tertiary carboxamide group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140326',
                          'name': 'tertiary carboxamide',
                          'definition': 'A carboxamide resulting from the '
                                        'formal condensation of a carboxylic '
                                        'acid with a secondary amine; formula '
                                        'RC(=O)NHR(1)R(2).',
                          'parents': ['CHEBI:37622']},
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
    'num_true_positives': 22,
    'num_false_positives': 100,
    'num_true_negatives': 504,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.18032786885245902,
    'recall': 1.0,
    'f1': 0.3055555555555556,
    'accuracy': 0.8402555910543131}