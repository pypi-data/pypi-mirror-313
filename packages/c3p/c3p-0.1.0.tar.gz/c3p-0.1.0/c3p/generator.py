import json
import logging
import random
from copy import copy, deepcopy
from pathlib import Path
from typing import Tuple, Optional
from typing import List
import sys
import io
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from llm import get_key, get_model
from typing import Iterator
from pathlib import Path

test_dir = Path("tmp")

logger = logging.getLogger(__name__)

from c3p.datamodel import ChemicalStructure, Result, ChemicalClass, Config, ResultSet, EvaluationResult, Dataset

example_dir = Path(__file__).parent.parent / "inputs"
validated_examples = ["benzenoid"]


BASE_SYSTEM_PROMPT = """
Write a program to classify chemical entities of a given class based on their SMILES string.

The program should consist of import statements (from rdkit) as well as a single function, named
is_<<chemical_class>> that takes a SMILES string as input and returns a boolean value plus a reason for the classification.

If the task is too hard or cannot be done, the program MAY return None, None.

You should ONLY include python code in your response. Do not include any markdown or other text, or
non-code separators.
If you wish to include explanatory information, then you can include them as code comments.

"""

def safe_name(name: str) -> str:
    """
    Convert a name to a safe format for use in python functions.

    Example:

        >>> safe_name("foo' 3<->x bar")
        'foo__3___x_bar'

    """
    return "".join([c if c.isalnum() else "_" for c in name])

def generate_system_prompt(examples: List[str] = None):
    """
    Generate a system prompt for classifying chemical entities based on SMILES strings.

    Args:
        examples:

    Returns:
    """
    if examples is None:
        examples = validated_examples
    for example in examples:
        system_prompt = BASE_SYSTEM_PROMPT
        system_prompt += f"Here is an example for the chemical class {example}:\n{example}.py\n---\n"
        with open(f"{example_dir}/{example}.py", "r") as f:
            system_prompt += f.read()
    return system_prompt


def generate_main_prompt(chemical_class: str, definition: str, instances: List[ChemicalStructure], err=None, prog=None):
    # replace all non-alphanumeric characters with underscores
    chemical_class_safe = safe_name(chemical_class)
    prompt = f"""
    Now create a program that classifies chemical entities of the class {chemical_class},
    defined as '{definition}'. The name of the function should be `is_{chemical_class_safe}`.
    Examples of structures that belong to this class are:
    """
    for instance in instances:
        prompt += f" - {instance.name}: SMILES: {instance.smiles}\n"
    if err:
        prompt += f"\nYour last attempt failed with the following error: {err}\n"
        if prog:
            prompt += f"\nYour last attempt was:\n{prog}\n"
    return prompt





def run_code(code_str: str, function_name: str, args: List[str], neg_args: List[str], max_false=100) -> List[Tuple[str, bool, str, dict]]:
    """
    Run the generated code and return the results.

    This expects the code to define a function with the name `function_name` that takes a single argument
    (SMILES) and returns a tuple of (arg, boolean, reason).

    Example:

        >>> code = "def is_foo(x): return x == 'foo', 'it is foo'"
        >>> run_code(code, 'is_foo', ['foo', 'bar'], [])
        [('foo', True, 'it is foo', {}), ('bar', False, 'it is foo', {})]

    Args:
        code_str:
        function_name:
        args:
        neg_args:

    Returns:

    """
    # suppress rdkit logging
    #log_stream = io.StringIO()
    #handler = logging.StreamHandler(log_stream)
    #tmp_logger = logging.getLogger()
    #tmp_logger.addHandler(handler)
    #tmp_logger.setLevel(logging.FATAL)
    # suppress at C++ level
    # https://github.com/rdkit/rdkit/issues/2683
    from rdkit import RDLogger
    RDLogger.DisableLog('rdApp.*')

    __metadata__ = {}
    # redirect stdout to a StringIO object
    f = io.StringIO()
    with redirect_stdout(f), redirect_stderr(f):
        exec(code_str, globals())
    logger.info(f"Output: {f.getvalue()}")

    f = io.StringIO()
    with redirect_stdout(f), redirect_stderr(f):
        metadata = globals().get('__metadata__', {})
        vals = []
        num_false_positives = 0
        num_false_negatives = 0
        for i, arg in enumerate(args + neg_args):
            # use json.dumps to make sure that the argument is safely encoded
            # e.g. SMILES may use backslashes
            arg_encoded = json.dumps(arg)
            func_exec_str = f"{function_name}({arg_encoded})"
            # logger.debug(f"Executing: {func_exec_str}")
            is_cls, reason = eval(func_exec_str)
            if is_cls and i >= len(args):
                num_false_positives += 1
                if num_false_positives > max_false:
                    break
            if not is_cls and i < len(args):
                num_false_negatives += 1
                if num_false_negatives > max_false:
                    break
            vals.append((arg, is_cls, reason, metadata))
    logger.info(f"Output: {f.getvalue()}")
    #tmp_logger.removeHandler(handler)
    return vals


@contextmanager
def capture_output():
    """
    Capture stdout and stderr using a context manager.

    Example:

        >>> with capture_output() as (out, err):
        ...     print("Hello, World!")
        ...
        >>> print(out.getvalue())
        Hello, World!

    """
    # Create StringIO objects to capture output
    stdout, stderr = io.StringIO(), io.StringIO()

    # Save the current stdout/stderr
    old_stdout, old_stderr = sys.stdout, sys.stderr

    try:
        # Replace stdout/stderr with our StringIO objects
        sys.stdout, sys.stderr = stdout, stderr
        yield stdout, stderr
    finally:
        # Restore the original stdout/stderr
        sys.stdout, sys.stderr = old_stdout, old_stderr



def generate_and_test_classifier(
        cls: ChemicalClass,
        attempt=0,
        err=None,
        prog=None,
        config=None,
        suppress_llm=False
) -> Iterator[Result]:
    """
    Main workflow

    The main workflow is a cycle between

    1. Generating code
    2. Running the code on positive and negative examples
    3. Go to 1 until `N` iterations or sufficient accuracy is received

    Each cycle will result a result. The final one is typically the best, but this
    is not guaranteed.

    :param cls: target chemical class for which is write a program
    :param attempt: counts which attempt this is
    :param err: error from previous iteration
    :param prog: program from previous iteration
    :param config: setup
    :return: iterator of results
    """
    logger.info(f"Test: {cls.name} attempt={attempt} err={err} suppress_llm={suppress_llm} prog={prog}")
    if config is None:
        config = Config()
    cls_lite = deepcopy(cls)
    cls_lite.instances = []
    cls_lite.negative_instances = []
    next_attempt = attempt + 1
    if next_attempt > config.max_attempts:
        print(f"FAILED: {cls.name} err={err[0:40]}")
        return
    safe = safe_name(cls.name)
    func_name = f"is_{safe}"
    if suppress_llm:
        code_str = prog
    else:
        system_prompt = generate_system_prompt(validated_examples)
        main_prompt = generate_main_prompt(cls.name, cls.definition, cls.instances, err=err, prog=prog)
        logger.info(f"System Prompt: {system_prompt}")
        logger.info(f"Main Prompt: {main_prompt}")
        model = get_model(config.llm_model_name)
        if model.needs_key:
            model.key = get_key(None, model.needs_key, model.key_env_var)
        if "o1" in config.llm_model_name:
            response = model.prompt(f"SYSTEM PROMPT: {system_prompt} MAIN PROMPT: {main_prompt}", stream=False)
        else:
            response = model.prompt(main_prompt, system=system_prompt)
        code_str = response.text()
        if not code_str:
            print(f"No code returned for {cls.name} // {response}")
        if "```" in code_str:  # Remove code block markdown
            code_str = code_str.split("```")[1].strip()
            if code_str.startswith("python"):
                code_str = code_str[6:]
            code_str = code_str.strip()
        # print(code_str)

    positive_instances = cls.instances
    negative_instances = cls.negative_instances
    if config.max_negative_to_test is not None:
        random.shuffle(negative_instances)
        negative_instances = negative_instances[:config.max_negative_to_test]
    if not positive_instances:
        raise ValueError(f"No positive instances for {cls.name}")
    if not negative_instances:
        raise ValueError(f"No negative instances for {cls.name}")
    logger.info(f"Testing {cls.name} with {len(positive_instances)} positive instances and {len(negative_instances)} negative instances")
    # negative_instances = []
    smiles_to_cls = {instance.smiles: True for instance in positive_instances}
    # for s in structures.values():
    #    if s.smiles not in smiles_to_cls:
    #        negative_instances.append(s)
    #    if len(negative_instances) >= len(positive_instances):
    #        break
    for instance in negative_instances:
        smiles_to_cls[instance.smiles] = False
    try:
        logger.info(f"Running code {len(code_str)} on {len(positive_instances)} + {len(negative_instances)} instances")
        with capture_output() as (stdout, stderr):
            #inputs = [instance.smiles for instance in positive_instances + negative_instances]
            results = run_code(code_str, func_name,
                               [instance.smiles for instance in positive_instances],
                               [instance.smiles for instance in negative_instances])
    except Exception as e:
        logger.info(f"Attempt {attempt} failed: {e}")
        # problem executing; we still yield a result, as this
        # may be useful for post-processing all results;
        # we also try again with a new attempt, unless we are suppressing LLM
        yield Result(
            chemical_class=cls_lite,
            config=config,
            code=code_str,
            message=err,
            attempt=attempt,
            success=False,
            error=str(e) + stderr.getvalue(),
            stdout=stdout.getvalue(),
        )
        msg = "Attempt failed: " + str(e)
        if not suppress_llm:
            yield from generate_and_test_classifier(cls, attempt=next_attempt, config=config, err=msg, prog=code_str)
        return
    true_positives = [(smiles, reason) for smiles, is_cls, reason, _ in results if is_cls and smiles_to_cls[smiles]]
    true_negatives = [(smiles, reason) for smiles, is_cls, reason, _ in results if
                      not is_cls and not smiles_to_cls[smiles]]
    false_positives = [(smiles, reason) for smiles, is_cls, reason, _ in results if is_cls and not smiles_to_cls[smiles]]
    false_negatives = [(smiles, reason) for smiles, is_cls, reason, _ in results if not is_cls and smiles_to_cls[smiles]]
    # We avoid placing all negatives in the payload as these can be large
    result = Result(
        chemical_class=cls_lite,
        config=config,
        code=code_str,
        message=err,
        true_positives=true_positives,
        false_positives=false_positives,
        num_true_negatives=len(true_negatives),
        num_false_negatives=len(false_negatives),
        attempt=attempt,
        #stdout=stdout.getvalue(),
        error=stderr.getvalue(),
        success=True,
    )
    result.calculate()
    logger.info(f"Attempt {attempt} for {cls.name} F1={result.f1}")
    yield result
    if suppress_llm:
        logger.info(f"No LLM - only executing")
        return
    if result.f1 is None or result.f1 < config.f1_threshold and not suppress_llm:
        max_examples = config.max_instances_in_prompt
        # try again, feeding in the results of the current attempt
        msg = f"\nAttempt failed: F1 score of {result.f1} is too low."
        msg += "\nTrue positives: " + str(true_positives[:max_examples])
        msg += "\nFalse positives: " + str(false_positives[:max_examples])
        msg += "\nFalse negatives: " + str(false_negatives[:max_examples])
        logger.info(f"Retrying {cls.name} with new prompt")
        yield from generate_and_test_classifier(cls, config=config, attempt=next_attempt, err=msg, prog=code_str)


def learn_program(cls: ChemicalClass, config: Config) -> ResultSet:
    # print(f"## {test_cls.name} POS={len(test_cls.instances)} NEG={len(test_cls.negatives)}")
    results = []
    for result in generate_and_test_classifier(cls, config=config):
        # print(f"attempt={result.attempt} compiled={result.success} tp={result.num_true_positives} tn={result.num_true_negatives} fp={result.num_false_positives} f1={result.f1}, len=={len(result.code)}")
        results.append(result)
        result.calculate()
    return ResultSet.from_results(results)

def randomize_and_split_list(l: List, proportion: float) -> Tuple[List, List]:
    l = copy(l)
    random.shuffle(l)
    n = int(len(l) * proportion)
    return l[:n], l[n:]

def evaluate_for_class(cls: ChemicalClass, config: Config, dataset: Dataset) -> Optional[EvaluationResult]:
    """
    Evaluate a classifier for a single class.

    Args:
        cls:
        config:

    Returns:

    """
    pos_train, pos_test = randomize_and_split_list(cls.instances, config.test_proportion)
    if len(pos_test) < 1:
        return
    negative_instances = get_negative_examples(dataset, cls)
    # neg_train, neg_test = randomize_and_split_list(negative_instances, config.test_proportion)
    train_cls = copy(cls)
    train_cls.instances = pos_train
    train_cls.negative_instances = negative_instances
    test_cls = copy(cls)
    test_cls.instances = pos_test
    test_cls.negative_instances = negative_instances
    train_result_set = learn_program(train_cls, config)
    if not train_result_set.results:
        return
    prog = train_result_set.best_result.code
    test_results = list(generate_and_test_classifier(test_cls, config=config, prog=prog, suppress_llm=True))
    if not test_results:
        return
    test_result = test_results[-1]
    test_result.calculate()
    return EvaluationResult(train_results=train_result_set, test_result=test_result)

def get_negative_examples(dataset: Dataset, cc: ChemicalClass) -> List[ChemicalStructure]:
    """
    Get negative examples for a chemical class.

    Args:
        dataset:
        cc:

    Returns:

    """
    negative_examples = set(dataset.structures)
    negative_examples = negative_examples.difference(cc.instances)
    return list(negative_examples)