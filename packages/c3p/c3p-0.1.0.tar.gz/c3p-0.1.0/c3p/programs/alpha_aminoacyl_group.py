"""
Classifies: CHEBI:22487 alpha-aminoacyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_alpha_aminoacyl_group(smiles: str):
    """
    Determines if a molecule is an alpha-aminoacyl group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an alpha-aminoacyl group, False otherwise
        str: Reason for classification
    """
    # Replace * with dummy atom [X] for RDKit compatibility
    smiles = smiles.replace('*', '[X]')
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for dummy atom (attachment point)
    dummy_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 0]
    if len(dummy_atoms) != 1:
        return False, "Must have exactly one attachment point (*)"
        
    dummy_atom = dummy_atoms[0]
    
    # Check for C(=O)- group attached to dummy atom
    for neighbor in dummy_atom.GetNeighbors():
        if neighbor.GetSymbol() != 'C':
            continue
            
        carbonyl = False
        alpha_carbon = None
        
        for carbonyl_neighbor in neighbor.GetNeighbors():
            if carbonyl_neighbor.GetSymbol() == 'O' and carbonyl_neighbor.GetTotalNumHs() == 0:
                # Found C=O
                carbonyl = True
            elif carbonyl_neighbor.GetSymbol() == 'C':
                # Found potential alpha carbon
                alpha_carbon = carbonyl_neighbor
                
        if not carbonyl or alpha_carbon is None:
            continue
            
        # Check alpha carbon has NH2 group
        amine_found = False
        for alpha_neighbor in alpha_carbon.GetNeighbors():
            if alpha_neighbor.GetSymbol() == 'N' and alpha_neighbor.GetTotalNumHs() >= 1:
                amine_found = True
                break
                
        if amine_found:
            # Check stereochemistry if present
            stereo = ""
            if alpha_carbon.GetChiralTag() == Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
                stereo = "L-"
            elif alpha_carbon.GetChiralTag() == Chem.ChiralType.CHI_TETRAHEDRAL_CW:
                stereo = "D-"
                
            # Determine side chain
            side_chain = []
            for alpha_neighbor in alpha_carbon.GetNeighbors():
                if alpha_neighbor.GetSymbol() not in ['N', 'C'] or \
                   (alpha_neighbor.GetSymbol() == 'C' and alpha_neighbor != neighbor):
                    side_chain.append(alpha_neighbor.GetSymbol())
                    
            return True, f"{stereo}alpha-aminoacyl group with side chain containing {', '.join(side_chain)}"
            
    return False, "No alpha-aminoacyl group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22487',
                          'name': 'alpha-aminoacyl group',
                          'definition': 'A univalent carboacyl group formed by '
                                        'loss of OH from the carboxy group of '
                                        'an alpha-amino acid.',
                          'parents': ['CHEBI:27207']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183868,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999673689591786}