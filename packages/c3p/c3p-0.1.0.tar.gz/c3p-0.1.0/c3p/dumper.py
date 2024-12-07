import pprint
from distutils.command.config import config
from pathlib import Path
from typing import Union, List, Optional

import pandas as pd
import yaml
from pydantic import BaseModel

from c3p.datamodel import Config, Result, EvaluationResult, EvaluationExperiment
from c3p.generator import safe_name
from c3p.stats import calculate_metrics_pandas


def object_to_header(obj: Union[BaseModel, dict]):
    obj_yaml = yaml.dump(obj.model_dump() if isinstance(obj, BaseModel) else obj)
    obj_yaml = "\n".join([f"# {line}" for line in obj_yaml.split("\n")])
    return obj_yaml


def result_prog_path(r: Result, results_dir: Path):
    cn = safe_name(r.chemical_class.name)
    prog_dir = results_dir / "programs"
    prog_dir.mkdir(exist_ok=True, parents=True)
    return f"{prog_dir / cn}.py"

def write_program(result: Union[Result, EvaluationResult], result_dir: Path, config_yaml: Union[str, Config]):
    """
    Write a program to disk.

    Args:
        r:
        result_dir:
        config_yaml:

    Returns:
    """
    #if isinstance(config_yaml, Config):
    #    config_yaml = object_to_header(config_yaml)
    if isinstance(result, EvaluationResult):
        r = result.train_results.best_result
    prog_path = result_prog_path(r, result_dir)
    with open(prog_path, "w") as f:
        f.write(f'"""\nClassifies: {r.chemical_class.id} {r.chemical_class.name}\n"""')
        f.write("\n")
        f.write(r.code)
        f.write("\n\n\n__metadata__ = ")
        #f.write("\n\n# Classifier Metadata\n# ---\n")
        r_obj = r.model_dump()
        del r_obj["code"]
        cc = r_obj["chemical_class"]
        del cc["instances"]
        del cc["negative_instances"]
        del r_obj["true_positives"]
        del r_obj["false_positives"]
        del r_obj["true_negatives"]
        del r_obj["false_negatives"]
        pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)
        f.write(pp.pformat(r_obj))
        #block = object_to_header(r_obj)
        #f.write(block)

        # f.write(f"\n# Attempt={r.attempt}")
        # f.write(f"\n# Pr={r.precision}")
        # f.write(f"\n# Recall={r.recall}")
        # f.write(f"\n# F1={r.f1}")
        # if isinstance(result, EvaluationResult):
        #     f.write(f"\n# Eval Pr={result.test_result.precision}")
        #     f.write(f"\n# Eval Recall={result.test_result.recall}")
        #     f.write(f"\n# Eval F1={result.test_result.f1}")

def write_programs(results: List[Union[Result, EvaluationResult]], result_dir: Path, config_yaml: Union[str, Config]):
    for r in results:
        write_program(r, result_dir, config_yaml)

def result_as_dict(r: Result, e: EvaluationResult) -> dict:
    d = r.model_dump()
    del d["code"]
    d["chemical_class"] = r.chemical_class.name
    del d["config"]
    #d["attempt"] = e.train_results.best_result.attempt
    d["num_instances"] = len(r.chemical_class.instances)
    for k in ["f1", "precision", "accuracy", "attempt"]:
        d[f"train_{k}"] = getattr(e.train_results.best_result, k)
    return d

def write_eval_results(expt: EvaluationExperiment, results_dir: Path, f1_threshold: Optional[float]=None) -> pd.DataFrame:
    """
    Write the results of an evaluation experiment to disk.

    Args:
        expt:
        results_dir:

    Returns: dataframe of filtered results

    """
    if f1_threshold is None:
        f1_threshold = expt.config.f1_threshold
    expt_path = results_dir / "experiment.yaml"
    with open(expt_path, "w") as f:
        f.write(yaml.dump(expt.model_dump()))
    expt_path_json = results_dir / "experiment.json"
    with open(expt_path_json, "w") as f:
        f.write(expt.model_dump_json(indent=2))
    eval_results = expt.evaluation_results
    for r in eval_results:
        write_program(r, results_dir, expt.config)
    config = expt.config

    df_filtered = pd.DataFrame(
        [result_as_dict(r.test_result, r) for r in eval_results if r.train_results.best_result.f1 > f1_threshold])
    df_filtered["num_test_instances"] = df_filtered["num_true_positives"] + df_filtered["num_false_negatives"]
    df_filtered = df_filtered[df_filtered["num_test_instances"] > 0]
    df_filtered.to_csv(results_dir / "filtered_results.csv", index=False)
    summary_stats = calculate_metrics_pandas(df_filtered)
    summary_stats.to_csv(results_dir / "outcomes_macro.csv", header=False)
    summary_stats = df_filtered.select_dtypes(include=['int64', 'float64']).mean()
    summary_stats.to_csv(results_dir / "outcomes_micro.csv", header=False)
    desc = df_filtered.describe().transpose()
    desc.to_csv(results_dir / "summary_stats_desc.csv")
    return df_filtered


