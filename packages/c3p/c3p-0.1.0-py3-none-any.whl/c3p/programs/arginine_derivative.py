"""
Classifies: CHEBI:22617 arginine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_arginine_derivative(smiles: str):
    """
    Determines if a molecule is an arginine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an arginine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for basic arginine scaffold
    # Look for C-C-C-N-C(=N)-N substructure
    arg_scaffold = Chem.MolFromSmarts("[CH2][CH2][CH2]NC(=N)N")
    if not mol.HasSubstructMatch(arg_scaffold):
        return False, "Missing basic arginine side chain scaffold"

    # Must have at least one carboxyl group
    carboxyl = Chem.MolFromSmarts("C(=O)[OH]")
    if not mol.HasSubstructMatch(carboxyl):
        return False, "Missing carboxyl group"

    # Must have alpha carbon with amine group (can be substituted)
    alpha_c = Chem.MolFromSmarts("[CH,CH2]([NH,NH2])C(=O)[OH]")
    if not mol.HasSubstructMatch(alpha_c):
        return False, "Missing alpha carbon with amine"

    # Check for modifications
    modifications = []
    
    # Check for N-substitution on alpha amine
    n_subst = Chem.MolFromSmarts("[CH]([NH][#6,#7,#8,#9,#15,#16,#17,#35,#53])C(=O)[OH]")
    if mol.HasSubstructMatch(n_subst):
        modifications.append("N-substituted")
        
    # Check for modifications on guanidyl group
    guanidyl_mod = Chem.MolFromSmarts("NC(=[NH,NX])N[#6,#7,#8,#9,#15,#16,#17,#35,#53]")
    if mol.HasSubstructMatch(guanidyl_mod):
        modifications.append("guanidyl-modified")

    # Check for O-substitution on carboxyl
    carboxyl_mod = Chem.MolFromSmarts("C(=O)O[#6,#7,#8,#9,#15,#16,#17,#35,#53]")
    if mol.HasSubstructMatch(carboxyl_mod):
        modifications.append("carboxyl-modified")
        
    # Check for hydroxylation on carbon chain
    hydroxy = Chem.MolFromSmarts("CC(O)C")
    if mol.HasSubstructMatch(hydroxy):
        modifications.append("hydroxylated")

    if len(modifications) > 0:
        return True, f"Arginine derivative with modifications: {', '.join(modifications)}"
    else:
        return False, "Unmodified arginine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22617',
                          'name': 'arginine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of arginine at the '
                                        'amino group, the carboxy group, or '
                                        'the guanidyl group, or from the '
                                        'replacement of any hydrogen of '
                                        'arginine by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing arginine residues.',
                          'parents': ['CHEBI:83821']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 92320,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 0.42857142857142855,
    'f1': 0.05454545454545455,
    'accuracy': 0.9988747876702695}