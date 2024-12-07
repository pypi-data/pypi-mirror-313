from copy import copy
import random
from typing import List, Tuple

from c3p.datamodel import ChemicalClass


def split_to_training_test(classes: List[ChemicalClass], proportion_test=0.2, n: int = 9999, start: int = 0) -> Tuple[List[ChemicalClass], List[ChemicalClass]]:
    """
    Generate a training and test set from a list of chemical classes.

    Note that we treat each chemical class as its own independent label; for each ChemicalClass,
    we generate two new ChemicalClass objects
    """
    test_set = []
    training_set = []
    for c in classes[start:n+start]:
        test_c = copy(c)
        train_c = copy(c)
        positive_examples = copy(c.instances)
        negative_examples = copy(c.negative_instances)
        random.shuffle(positive_examples)
        random.shuffle(negative_examples)
        i_positive = int(len(positive_examples) * proportion_test)
        i_negative = int(len(negative_examples) * proportion_test)
        test_c.instances = positive_examples[:i_positive]
        test_c.negative_instances = negative_examples[:i_negative]
        train_c.instances = positive_examples[i_positive:]
        train_c.negative_instances = negative_examples[i_negative:]
        test_set.append(test_c)
        training_set.append(train_c)
    return training_set, test_set