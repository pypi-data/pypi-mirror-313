import json
from langgraph_log_parser.analyze import *
from langgraph_log_parser.analyze_case_id import *
import pandas as pd
from typing import Optional
import os

def _convert_keys_to_serializable(data):
    """Recursively convert all keys in dictionaries to serializable types."""
    if isinstance(data, dict):
        return {str(k) if not isinstance(k, (str, int, float, bool, type(None))) else k: _convert_keys_to_serializable(
            v)
                for k, v in data.items()}
    elif isinstance(data, list):
        return [_convert_keys_to_serializable(item) for item in data]
    else:
        return data


def write_report(event_log: pd.DataFrame, output_file: Optional[str] = None) -> None:
    """
    Generate and save a comprehensive analysis report of the entire event log in JSON format.

    The generated JSON report includes:
        - Start and end activities
        - Activity frequencies
        - Activity sequences and their probabilities
        - Minimum self-distances between activities
        - Self-distance witnesses
        - Rework counts
        - Mean service times per activity
        - Case durations

    :param event_log: Event log data containing process execution information
    :type event_log: pd.DataFrame
    :param output_file: Path to save the JSON report, defaults to './report.json'
    :type output_file: Optional[str]

    **Example:**

    >>> csv_output = "files/process_log.csv"
    >>> event_log = pd.read_csv(csv_output)
    >>> write_report(event_log)  # Will use default './report.json'
    >>> write_report(event_log,"analysis/custom_report.json")  # Custom path
    Report successfully generated at: ./report.json
    Report successfully generated at: analysis/report.json
    """
    event_log = event_log.copy()

    structured_data = {
        "start_activities": get_starts(event_log),
        "end_activities": get_ends(event_log),
        "activities_count": get_act_counts(event_log),
        "sequences": get_sequences(event_log),
        "sequences_with_probabilities": get_sequence_probs(event_log),
        "minimum_self_distances": get_min_self_dists(event_log),
        "self_distance_witnesses": get_self_dist_witnesses(event_log),
        "rework_counts": get_act_reworks(event_log),
        "activities_mean_service_time": get_mean_act_times(event_log),
        "cases_durations": get_durations(event_log),
    }

    if output_file is None or os.path.isdir(output_file):
        base_path = output_file or "."
        output_file = os.path.join(base_path, "report.json")

    # Convert all keys to serializable types
    structured_data = _convert_keys_to_serializable(structured_data)

    # Write the structured JSON to the output file
    with open(output_file, "w") as file:
        json.dump(structured_data, file, indent=4)

    print(f"Report successfully generated at: {output_file}")

def write_case_report(event_log: pd.DataFrame, case_id: int, output_file: Optional[str] = None) -> None:
    """
    Generate and save a detailed analysis report for a specific case ID in JSON format.

    The generated JSON report includes:
        - Case ID
        - Start and end activity
        - Activity frequencies within the case
        - Activity sequence and its probability
        - Minimum self-distances between activities
        - Self-distance witnesses
        - Rework counts
        - Sum of service times per activity
        - Total case duration

    :param event_log: Event log data containing process execution information
    :type event_log: pd.DataFrame
    :param case_id: Identifier of the specific case to analyze
    :type case_id: int
    :param output_file: Path to save the JSON report, defaults to './{case_id}_report.json'
    :type output_file: Optional[str]

    **Example:**

    >>> csv_output = "files/process_log.csv"
    >>> event_log = pd.read_csv(csv_output)
    >>> write_case_report(event_log,12345)  # Will use default './12345_report.json'
    >>> write_case_report(event_log,12345,"analysis/case_report.json")  # Custom path
    Case 12345 report successfully generated at: ./12345_report.json
    Case 12345 report successfully generated at: analysis/12345_report.json
    """
    event_log = event_log.copy()

    structured_data = {
        "case_id": case_id,
        "start_activity": get_case_start(event_log, case_id),
        "end_activity": get_case_end(event_log, case_id),
        "activities_count": get_case_act_counts(event_log, case_id),
        "sequence_with_probability": get_case_sequence_prob(event_log, case_id),
        "minimum_self_distances": get_case_min_self_dists(event_log, case_id),
        "self_distance_witnesses": get_case_self_dist_witnesses(event_log, case_id),
        "rework_counts": get_case_act_reworks(event_log, case_id),
        "activities_sum_service_time": get_case_sum_act_times(event_log, case_id),
        "case_duration": get_case_duration(event_log, case_id),
    }

    if output_file is None or os.path.isdir(output_file):
        base_path = output_file or "."
        output_file = os.path.join(base_path, f"{case_id}_report.json")

    # Convert all keys to serializable types
    structured_data = _convert_keys_to_serializable(structured_data)

    # Write the structured JSON to the output file
    with open(output_file, "w") as file:
        json.dump(structured_data, file, indent=4)

    print(f"Case {case_id} report successfully generated at: {output_file}")