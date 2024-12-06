import os
import pandas as pd
import pm4py
from typing import Optional


def generate_prefix_tree(event_log: pd.DataFrame, output_path: Optional[str] = None) -> None:
    """
    Generate and save a prefix tree visualization.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param output_path: Path to save the prefix tree visualization, defaults to 'tree.png'
    :type output_path: Optional[str]

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> generate_prefix_tree(event_log)  # Will use default 'tree.png'
    Event log loaded and formated from file: files/examples.csv
    Prefix Tree saved as: prefix_tree.png
    """

    # Use the provided path or construct default
    if output_path is None or os.path.isdir(output_path):
        base_path = output_path or '.'
        output_path = os.path.join(base_path, 'prefix_tree.png')

    # Jeżeli użytkownik nie podał ścieżki
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Wygeneruj prefix tree
    prefix_tree = pm4py.discover_prefix_tree(
        event_log, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp'
    )

    # Zapisz wizualizacje prefix tree
    pm4py.save_vis_prefix_tree(prefix_tree, output_path)
    print("Prefix Tree saved as:", output_path)


def generate_performance_dfg(event_log: pd.DataFrame, output_path: Optional[str] = None) -> None:
    """
    Generate and save a visualization of directly-follows graph annotated with performance.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param output_path: Path to save the visualization of dfg with performance.
    :type output_path: str

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> generate_performance_dfg(event_log)  # Will use default 'dfg_performance.png'
    Event log loaded and formated from file: files/examples.csv
    Performance DFG saved as: dfg_performance.png
    """

    if output_path is None or os.path.isdir(output_path):
        base_path = output_path or '.'
        output_path = os.path.join(base_path, 'dfg_performance.png')

    # Jeżeli użytkownik nie podał ścieżki
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log)

    pm4py.save_vis_performance_dfg(dfg,start_activities, end_activities, output_path)
    print("Performance DFG saved as:", output_path)


def generate_visualizations(
        event_log: pd.DataFrame,
        output_dir: Optional[str] = None
) -> None:
    """
    Generate and save all process mining visualizations.

    :param event_log: Event log data
    :type event_log: pd.DataFrame
    :param output_dir: Directory to save the visualizations
    :type output_dir: Optional[str]

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> generate_visualizations(event_log, "output/visualizations")
    Generating all process mining visualizations...
    Prefix Tree saved as: output/visualizations/prefix_tree.png
    Performance DFG saved as: output/visualizations/dfg_performance.png
    All visualizations generated successfully!
    """

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Generating all process mining visualizations...")

    # Generate prefix tree
    tree_path = os.path.join(output_dir, 'prefix_tree.png')
    generate_prefix_tree(event_log, tree_path)

    # Generate performance DFG
    dfg_path = os.path.join(output_dir, 'dfg_performance.png')
    generate_performance_dfg(event_log, dfg_path)

    print("All visualizations generated successfully!")