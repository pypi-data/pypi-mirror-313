import os
import json
import csv
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from glob import glob


@dataclass
class SupervisorConfig:
    """
    Configuration for a supervisor node.

    :param name: Name of the supervisor.
    :type name: str
    :param supervisor_type: Type of the supervisor ('graph' or 'subgraph').
    :type supervisor_type: str
    """
    name: str
    supervisor_type: str


@dataclass
class SubgraphConfig:
    """
    Configuration for a subgraph and its components.

    :param name: Name of the subgraph.
    :type name: str
    :param nodes: List of nodes within the subgraph.
    :type nodes: List[str]
    :param supervisor: Configuration of the subgraph's supervisor.
    :type supervisor: SupervisorConfig
    """
    name: str
    nodes: List[str]
    supervisor: SupervisorConfig  # Subgraph's supervisor


@dataclass
class GraphConfig:
    """
    Overall graph configuration.

    :param supervisors: Optional list of graph-level supervisors.
    :type supervisors: Optional[List[SupervisorConfig]]
    :param subgraphs: Optional list of subgraphs.
    :type subgraphs: Optional[List[SubgraphConfig]]
    :param nodes: Optional list of nodes for non-subgraph mode.
    :type nodes: Optional[List[str]]
    """
    # Optional graph-level supervisors
    supervisors: Optional[List[SupervisorConfig]] = None
    # Optional subgraphs
    subgraphs: Optional[List[SubgraphConfig]] = None
    # Optional nodes list for non-subgraph mode
    nodes: Optional[List[str]] = None


def _build_config_mappings(graph_config: GraphConfig) -> Dict[str, Any]:
    """
    Build lookup structures from graph configuration.

    :param graph_config: The graph configuration object.
    :type graph_config: GraphConfig

    :return: A dictionary with mappings for supervisors, subgraphs, and nodes.
    :rtype: Dict
    """
    # Initialize all mappings
    graph_supervisors = set()
    subgraph_map = {}
    subgraph_supervisors = {}
    node_to_subgraph = {}
    valid_nodes = set()

    # Handle supervisors if present
    if graph_config.supervisors:
        graph_supervisors = {sup.name for sup in graph_config.supervisors}

    # Handle subgraphs if present
    if graph_config.subgraphs:
        subgraph_map = {sg.name: sg for sg in graph_config.subgraphs}
        subgraph_supervisors = {sg.supervisor.name: sg.name for sg in graph_config.subgraphs}

        # Collect nodes from subgraphs
        for sg in graph_config.subgraphs:
            for node in sg.nodes:
                node_to_subgraph[node] = sg.name
                valid_nodes.add(node)
    # Handle non-subgraph case
    elif graph_config.nodes:
        valid_nodes.update(graph_config.nodes)
    else:
        raise ValueError("Either subgraphs or nodes must be provided in the configuration")

    return {
        'graph_supervisors': graph_supervisors,
        'subgraph_map': subgraph_map,
        'subgraph_supervisors': subgraph_supervisors,
        'node_to_subgraph': node_to_subgraph,
        'valid_nodes': valid_nodes
    }


def _process_single_json(json_data: List[Dict], graph_config: GraphConfig, config: Dict) -> List[Dict[str, Any]]:
    """
    Process a single JSON and return entries to write.

    :param json_data: List of JSON entries.
    :type json_data: List[Dict]
    :param graph_config: The graph configuration object.
    :type graph_config: GraphConfig
    :param config: Precomputed configuration mappings.
    :type config: Dict

    :return: List of processed entries to write.
    :rtype: List[Dict]
    """
    has_subgraphs = bool(graph_config.subgraphs)
    has_supervisors = bool(graph_config.supervisors)
    visited_global_start = False
    entries_to_write = []

    def _get_subgraph_context(json_entry: Dict) -> Optional[str]:
        """
        Determine the current subgraph context from a JSON entry.

        :param json_entry: A single JSON entry to evaluate.
        :type json_entry: Dict

        :return: Name of the subgraph, if applicable.
        :rtype: Optional[str]
        """
        if not has_subgraphs:
            return None

        metadata = json_entry.get('metadata', {})

        if 'langgraph_checkpoint_ns' in metadata:
            checkpoint_ns = metadata['langgraph_checkpoint_ns']
            parts = checkpoint_ns.split('|')
            if parts:
                subgraph_name = parts[0].split(':')[0]
                if subgraph_name in config['subgraph_map']:
                    return subgraph_name

        node = metadata.get('langgraph_node')
        if node in config['node_to_subgraph']:
            return config['node_to_subgraph'][node]

        return None

    def _is_graph_supervisor(activity: str) -> bool:
        """
        Check if an activity is a graph-level supervisor.

        :param activity: Name of the activity.
        :type activity: str

        :return: True if the activity is a graph-level supervisor.
        :rtype: bool
        """
        return activity in config['graph_supervisors']

    for i, json_entry in enumerate(json_data):
        case_id = json_entry.get('thread_ID')
        timestamp = json_entry['checkpoint'].get('ts')

        metadata = json_entry.get('metadata', {})
        writes = metadata.get('writes', {})

        if not writes:
            continue

        activity = next((key for key in writes.keys() if key != 'messages'), None)
        if not activity:
            continue

        # Skip activities that aren't in our valid nodes list (unless they're supervisors or __start__)
        if (activity != '__start__' and
                not _is_graph_supervisor(activity) and
                activity not in config['subgraph_supervisors'] and
                activity not in config['valid_nodes']):
            continue

        context = _get_subgraph_context(json_entry)
        should_write = False
        org_resource = None

        if has_subgraphs:
            # === SUBGRAPH MODE ===
            if activity == '__start__' and not visited_global_start:
                should_write = True
                org_resource = '__start__'
                visited_global_start = True
            elif _is_graph_supervisor(activity):
                should_write = True
                org_resource = activity

                # Look ahead for next subgraph supervisor activity
                for j in range(i + 1, len(json_data)):
                    next_json = json_data[j]
                    if next_json.get('thread_ID') != case_id:
                        continue

                    next_metadata = next_json.get('metadata', {})
                    next_writes = next_metadata.get('writes', {})
                    if not next_writes:
                        continue

                    next_activity = next((key for key in next_writes.keys() if key != 'messages'), None)
                    if next_activity in config['subgraph_supervisors']:
                        next_context = config['subgraph_supervisors'][next_activity]
                        entries_to_write.append({
                            'case_id': case_id,
                            'timestamp': next_json['checkpoint'].get('ts'),
                            'end_timestamp': next_json['checkpoint'].get('ts'),
                            'cost': 0,
                            'activity': '__start__',
                            'org:resource': next_context
                        })
                        current_subgraph = next_context
                        break
            elif activity in config['subgraph_supervisors']:
                should_write = True
                org_resource = config['subgraph_supervisors'][activity]
                current_subgraph = org_resource
            elif activity in config['valid_nodes'] and context:
                should_write = True
                org_resource = config['node_to_subgraph'][activity]
        else:
            # === NON-SUBGRAPH MODE ===
            if activity == '__start__' and not visited_global_start:
                should_write = True
                org_resource = '__start__'
                visited_global_start = True
            elif has_supervisors and _is_graph_supervisor(activity):
                should_write = True
                org_resource = activity
            elif activity in config['valid_nodes']:  # Only process explicitly listed nodes
                should_write = True
                org_resource = activity

        if should_write:
            # Find end_timestamp
            end_timestamp = None
            for j in range(i + 1, len(json_data)):
                next_json = json_data[j]
                if next_json.get('thread_ID') == case_id and next_json.get('metadata', {}).get('writes'):
                    end_timestamp = next_json['checkpoint'].get('ts')
                    break

            if end_timestamp is None:
                end_timestamp = timestamp

            entries_to_write.append({
                'case_id': case_id,
                'timestamp': timestamp,
                'end_timestamp': end_timestamp,
                'cost': 0,
                'activity': activity,
                'org:resource': org_resource
            })

    return entries_to_write


def export_jsons_to_csv(
        input_folder: str,
        csv_path: str,
        graph_config: GraphConfig,
        csv_fields: Optional[List[str]] = None
) -> None:
    """
    Process all JSON files in the input folder and combine them into a single CSV file.

    :param input_folder: Path to the folder containing JSON files.
    :type input_folder: str
    :param csv_path: Path to save the output CSV file.
    :type csv_path: str
    :param graph_config: The graph configuration object.
    :type graph_config: GraphConfig
    :param csv_fields: Optional list of fields for the output CSV.
    :type csv_fields: List[str], optional

    **Example:**

    >>> output = "json"
    >>> csv_output = "csv_output.csv"
    >>> graph_config = GraphConfig(nodes=["chatbot_node"])
    >>> export_jsons_to_csv(output,csv_output,graph_config)
    Processed: json/thread_1.json
    Processed: json/thread_2.json
    Processed: json/thread_3.json
    Successfully exported combined data to: csv_output.csv
    """
    if csv_fields is None:
        csv_fields = ['case_id', 'timestamp', 'end_timestamp', 'cost', 'activity', 'org:resource']

    # Ensure output directory exists
    if os.path.dirname(csv_path):
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    # Build configuration mappings
    config = _build_config_mappings(graph_config)

    # Get all JSON files in the input folder
    json_files = glob(os.path.join(input_folder, '*.json'))

    if not json_files:
        raise ValueError(f"No JSON files found in {input_folder}")

    all_entries = []

    # Process each JSON file
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                jsons = json.load(f)

            # Process the current JSON file
            entries = _process_single_json(jsons, graph_config, config)
            all_entries.extend(entries)

            print(f"Processed: {json_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")

    # Sort all entries by timestamp
    all_entries.sort(key=lambda x: x['timestamp'])

    # Write combined results to CSV
    with open(csv_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(all_entries)

    print(f"Successfully exported combined data to: {csv_path}")