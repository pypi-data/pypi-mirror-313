from typing import Union

import pandas as pd
import numpy as np

def calculate_classification_metrics(tp, tn, fp, fn):
    """
    Calculate classification metrics from confusion matrix values.

    Parameters:
    tp (int/float): True positives
    tn (int/float): True negatives
    fp (int/float): False positives
    fn (int/float): False negatives

    Returns:
    dict: Dictionary containing various classification metrics
    """
    # Prevent division by zero by adding small epsilon
    eps = 1e-7

    # Basic counts
    total = tp + tn + fp + fn
    positives = tp + fp
    negatives = tn + fn
    actual_positives = tp + fn
    actual_negatives = tn + fp

    # Core metrics
    accuracy = (tp + tn) / (total + eps)
    precision = tp / (tp + fp + eps)
    recall = tp / (tp + fn + eps)
    specificity = tn / (tn + fp + eps)
    f1_score = 2 * (precision * recall) / (precision + recall + eps)

    # Additional metrics
    false_positive_rate = fp / (fp + tn + eps)
    false_negative_rate = fn / (fn + tp + eps)
    negative_predictive_value = tn / (tn + fn + eps)
    matthews_correlation_coef = ((tp * tn) - (fp * fn)) / np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn) + eps)
    balanced_accuracy = (recall + specificity) / 2

    return {
        # Counts
        'total_samples': total,
        'true_positives': tp,
        'true_negatives': tn,
        'false_positives': fp,
        'false_negatives': fn,

        # Core metrics
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'specificity': specificity,

        # Additional metrics
        'false_positive_rate': false_positive_rate,
        'false_negative_rate': false_negative_rate,
        'negative_predictive_value': negative_predictive_value,
        'matthews_correlation_coef': matthews_correlation_coef,
        'balanced_accuracy': balanced_accuracy
    }


def calculate_metrics_pandas(data: Union[pd.Series, pd.DataFrame]) -> pd.Series:
    return calculate_macro_stats(data)


def calculate_macro_stats(data: Union[pd.Series, pd.DataFrame]) -> pd.Series:
    """
    Calculate classification metrics using pandas operations.
    Works with both Series and DataFrame inputs containing:
    num_true_positives, num_true_negatives, num_false_positives, num_false_negatives
    """
    # If input is a Series, use the values directly
    if isinstance(data, pd.Series):
        tp = data['num_true_positives']
        tn = data['num_true_negatives']
        fp = data['num_false_positives']
        fn = data['num_false_negatives']
    else:
        # If input is a DataFrame, sum all rows to get totals
        tp = data['num_true_positives'].sum()
        tn = data['num_true_negatives'].sum()
        fp = data['num_false_positives'].sum()
        fn = data['num_false_negatives'].sum()

    metrics = pd.Series({
        # Basic counts
        'total': tp + tn + fp + fn,
        'positives': tp + fp,
        'negatives': tn + fn,
        'actual_positives': tp + fn,
        'actual_negatives': tn + fp,

        # Core metrics
        'accuracy': (tp + tn) / (tp + tn + fp + fn),
        'precision': tp / (tp + fp) if tp + fp > 0 else 0,
        'recall': tp / (tp + fn) if tp + fn > 0 else 0,
        'specificity': tn / (tn + fp) if tn + fp > 0 else 0,

        # Additional metrics
        'f1_score': 2 * tp / (2 * tp + fp + fn),
        'false_positive_rate': fp / (tn + fp) if tn + fp > 0 else 0,
        'negative_predictive_value': tn / (tn + fn) if tn + fn > 0 else 0,
    })

    metrics['balanced_accuracy'] = (metrics['recall'] + metrics['specificity']) / 2

    return metrics.round(4)