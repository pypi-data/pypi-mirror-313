import pandas as pd
import pm4py
import numpy as np
from collections import defaultdict

pd.set_option('display.max_columns', None)


#2
def get_starts(event_log: pd.DataFrame) -> dict[str, int]:
    """
    Get the start activities of the event log.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :return: Start activities and their counts.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_starts(event_log))
    Event log loaded and formated from file: files/examples.csv
    {'__start__': 3}
    """
    start_activities = pm4py.get_start_activities(event_log)
    return start_activities


#3
def print_starts(event_log: pd.DataFrame) -> None:
    """
    Print the start activities of the event log.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_starts(event_log)
    Event log loaded and formated from file: files/examples.csv
    Start activities: {'__start__': 3}
    """
    start_activities = get_starts(event_log)
    print("Start activities:", start_activities)


#4
def get_ends(event_log: pd.DataFrame) -> dict[str, int]:
    """
    Get the end activities of the event log.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :return: End activities and their counts.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_ends(event_log))
    Event log loaded and formated from file: files/examples.csv
    {'test_supervisor': 3}
    """
    end_activities = pm4py.get_end_activities(event_log)
    return end_activities


#5
def print_ends(event_log: pd.DataFrame) -> None:
    """
    Print the end activities of the event log.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_ends(event_log)
    Event log loaded and formated from file: files/examples.csv
    End activities: {'test_supervisor': 3}
    """
    end_activities = get_ends(event_log)
    print("End activities:", end_activities)


#6
def get_act_counts(event_log: pd.DataFrame) -> dict[str, int]:
    """
    Get the counts of every activity in the event log.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :return: Activity counts.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_act_counts(event_log))
    Event log loaded and formated from file: files/examples.csv
    {'__start__': 27, 'ag_supervisor': 27, 'test_supervisor': 27, 'rg_supervisor': 22, 'DocWriter': 8, 'Search': 5, 'WebScraper': 5, 'ChartGenerator': 3, 'NoteTaker': 3}
    """
    activities = pm4py.get_event_attribute_values(event_log, 'concept:name')
    return activities


#7
def print_act_counts(event_log: pd.DataFrame) -> None:
    """
    Print the counts of every activity in the event log.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_act_counts(event_log)
    Event log loaded and formated from file: files/examples.csv
    Count of each activity: {'__start__': 27, 'ag_supervisor': 27, 'test_supervisor': 27, 'rg_supervisor': 22, 'DocWriter': 8, 'Search': 5, 'WebScraper': 5, 'ChartGenerator': 3, 'NoteTaker': 3}
    """
    activities = get_act_counts(event_log)
    print("Count of each activity:", activities)


#8
def get_sequences(event_log: pd.DataFrame) -> dict[int, list[str]]:
    """
    Return activity sequences for every case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :return: Mapping of case IDs to their activity sequences.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_sequences(event_log))
    Event log loaded and formated from file: files/examples.csv
    {18: ['__start__', 'ag_supervisor', 'test_supervisor'], 19: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor'], 20: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']}
    """
    # Tworzymy słownik, który będzie przechowywał sekwencje aktywności dla każdego case_id
    sequences_by_case = defaultdict(list)

    # Budujemy sekwencje dla każdego case_id
    for _, row in event_log.iterrows():
        # Upewnienie, że case_id jest int'em
        case_id = int(row['case_id'])
        activity = row['activity']
        sequences_by_case[case_id].append(activity)

        # Sortowanie po id
        sorted_sequences = dict(sorted(sequences_by_case.items()))
    return sorted_sequences


#9
def print_sequences(event_log: pd.DataFrame) -> None:
    """
    Print sequences for every case ID in the event log, sorted numerically by case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_sequences(event_log)
    Event log loaded and formated from file: files/examples.csv
    All sequences:
    Case ID 18: ['__start__', 'ag_supervisor', 'test_supervisor']
    Case ID 19: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']
    Case ID 20: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']
    """
    # Sekwencja dla każdego case_id
    sequences_by_case = get_sequences(event_log)

    print("All sequences:")

    # Sortowanie po case_id
    for case_id in sorted(sequences_by_case.keys(), key=lambda x: int(x)):
        sequence = sequences_by_case[case_id]
        print(f"Case ID {case_id}: {sequence}")


#10
def get_sequence_probs(event_log: pd.DataFrame) -> list[tuple[int, tuple[str, ...], float]]:
    """
    Return sequences with probabilities for each case ID.
    If sequence already occurred it only lists the ID of the latest occurrence.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :return: List of tuples containing (case ID, sequence, probability).
    :rtype: list

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_sequence_probs(event_log))
    Event log loaded and formated from file: files/examples.csv
    [(18, ('__start__', 'ag_supervisor', 'test_supervisor'), 0.3333333333333333), (19, ('__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor'), 0.3333333333333333), (20, ('__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor'), 0.3333333333333333)]
    """
    sequences_by_case = get_sequences(event_log)

    # Generujemy probabilistyczny język
    language = pm4py.get_stochastic_language(event_log)

    # Tworzymy odwrotny słownik dla łatwego porównania
    case_by_sequence = {tuple(seq): case_id for case_id, seq in sequences_by_case.items()}

    # Sortujemy sequences_by_case według numerycznych wartości case_id
    sorted_sequences = sorted(case_by_sequence.items(), key=lambda x: int(x[1]))

    # Generowanie listy rezultatów
    result = [(case_id, sequence, language.get(sequence, 0)) for sequence, case_id in sorted_sequences]
    return result


#11
def print_sequence_probs(event_log: pd.DataFrame) -> None:
    """
    Print sequences with probabilities for each case ID.
    If sequence already occurred it only prints the ID of the latest occurrence.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_sequence_probs(event_log)
    Event log loaded and formated from file: files/examples.csv
    ID of last sequence occurrence with probability of occurrence:
    Case ID 18: ('__start__', 'ag_supervisor', 'test_supervisor'), 0.3333333333333333
    Case ID 19: ('__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor'), 0.3333333333333333
    Case ID 20: ('__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor'), 0.3333333333333333
    """
    sequences_with_probabilities = get_sequence_probs(event_log)

    print("ID of last sequence occurrence with probability of occurrence:")
    for case_id, sequence, probability in sequences_with_probabilities:
        print(f"Case ID {case_id}: {sequence}, {probability}")


# 16
def get_min_self_dists(event_log: pd.DataFrame) -> dict[int, dict[str, int]]:
    """
    Calculate the minimum self-distances for each activity in each case.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :return: Dictionary where keys are case IDs and values are dictionaries of activities with their minimum self-distances.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_min_self_dists(event_log))
    Event log loaded and formated from file: files/examples.csv
    {18: {}, 19: {'DocWriter': 1, 'Search': 6, 'WebScraper': 4, '__start__': 1, 'ag_supervisor': 1, 'rg_supervisor': 1, 'test_supervisor': 2}, 20: {'ChartGenerator': 1, 'DocWriter': 3, 'NoteTaker': 3, 'Search': 36, '__start__': 1, 'ag_supervisor': 1, 'rg_supervisor': 1, 'test_supervisor': 2}}
    """
    unique_case_ids = event_log['case:concept:name'].unique()
    sorted_case_ids = np.sort(unique_case_ids.astype(int))

    # Słownik do przechowywania minimalnych odległości własnych dla każdego Case ID
    min_self_distances = {}

    # Iterujemy po każdym case_id i obliczamy minimalne odległości własne dla jego aktywności
    for case_id in sorted_case_ids:
        # Filtrowanie event logu dla danego case_id
        filtered_event_log = event_log[event_log['case:concept:name'] == str(case_id)]

        # Kalkulowanie minimalnych odległości własnych dla danego case_id
        msd = pm4py.get_minimum_self_distances(
            filtered_event_log,
            activity_key='concept:name',
            case_id_key='case:concept:name',
            timestamp_key='time:timestamp'
        )
        min_self_distances[int(case_id)] = msd

    return min_self_distances


#17
def print_min_self_dists(event_log: pd.DataFrame) -> None:
    """
    Calculate and print the minimum self-distances for each activity in each case.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_min_self_dists(event_log)
    Event log loaded and formated from file: files/examples.csv
    Minimal self-distances for every activity:
    Case ID 18: {}
    Case ID 19: {'DocWriter': 1, 'Search': 6, 'WebScraper': 4, '__start__': 1, 'ag_supervisor': 1, 'rg_supervisor': 1, 'test_supervisor': 2}
    Case ID 20: {'ChartGenerator': 1, 'DocWriter': 3, 'NoteTaker': 3, 'Search': 36, '__start__': 1, 'ag_supervisor': 1, 'rg_supervisor': 1, 'test_supervisor': 2}
    """
    min_self_distances = get_min_self_dists(event_log)

    print("Minimal self-distances for every activity:")
    for case_id, distances in min_self_distances.items():
        print(f"Case ID {case_id}: {distances}")


#24
def get_act_reworks(event_log: pd.DataFrame) -> dict[int, dict[str, int]]:
    """
    Return the rework counts for each activity in each case.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :return: Rework counts for each case ID.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_act_reworks(event_log))
    Event log loaded and formated from file: files/examples.csv
    {18: {}, 19: {'__start__': 18, 'test_supervisor': 18, 'rg_supervisor': 15, 'Search': 3, 'WebScraper': 4, 'ag_supervisor': 14, 'DocWriter': 4}, 20: {'__start__': 8, 'test_supervisor': 8, 'rg_supervisor': 7, 'Search': 2, 'ag_supervisor': 12, 'ChartGenerator': 2, 'DocWriter': 4, 'NoteTaker': 3}}
    """
    rework_counts_by_case = {}
    unique_case_ids = event_log['case:concept:name'].unique()
    sorted_case_ids = np.sort(unique_case_ids.astype(int))

    for case_id in sorted_case_ids:
        # Filtrowanie logu dla bieżącego case_id
        filtered_event_log = event_log[event_log['case:concept:name'] == str(case_id)]

        # Inicjalizacja licznika powtórzeń
        activity_counts = defaultdict(int)

        # Tworzymy listę aktywności w bieżącej ścieżce
        activities = filtered_event_log['concept:name'].tolist()

        # Zliczanie wystąpień każdej aktywności
        for activity in activities:
            activity_counts[activity] += 1

        # Usunięcie aktywności, które wystąpiły tylko raz (bo nie są "rework")
        rework_counts = {activity: count for activity, count in activity_counts.items() if count > 1}
        rework_counts_by_case[int(case_id)] = rework_counts
    return rework_counts_by_case


#25
def print_act_reworks(event_log: pd.DataFrame) -> None:
    """
    Print the rework counts for each activity in each case.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_act_reworks(event_log)
    Event log loaded and formated from file: files/examples.csv
    Count of activity rework:
    Case ID 18: {}
    Case ID 19: {'__start__': 18, 'test_supervisor': 18, 'rg_supervisor': 15, 'Search': 3, 'WebScraper': 4, 'ag_supervisor': 14, 'DocWriter': 4}
    Case ID 20: {'__start__': 8, 'test_supervisor': 8, 'rg_supervisor': 7, 'Search': 2, 'ag_supervisor': 12, 'ChartGenerator': 2, 'DocWriter': 4, 'NoteTaker': 3}
    """
    rework_counts_by_case = get_act_reworks(event_log)

    print("Count of activity rework:")
    for case_id, rework_counts in rework_counts_by_case.items():
        print(f"Case ID {case_id}: {rework_counts}")


#28
def get_mean_act_times(event_log: pd.DataFrame) -> dict[str, float]:
    """
    Calculate the mean service time for each activity.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :return: Mean service times for each activity.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_mean_act_times(event_log))
    Event log loaded and formated from file: files/examples.csv
    {'ChartGenerator': 0.587241, 'DocWriter': 1.0209089999999998, 'NoteTaker': 0.5753873333333334, 'Search': 0.580575, 'WebScraper': 0.6020846, '__start__': 0.0411957037037037, 'ag_supervisor': 0.007210296296296296, 'rg_supervisor': 1.8212668636363636, 'test_supervisor': 0.04827048148148148}
    """
    mean_serv_time = pm4py.get_service_time(
        event_log, start_timestamp_key='timestamp', timestamp_key='end_timestamp', aggregation_measure='mean'
    )
    return mean_serv_time


#29
def print_mean_act_times(event_log: pd.DataFrame) -> None:
    """
    Print the mean service time for each activity.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_mean_act_times(event_log)
    Event log loaded and formated from file: files/examples.csv
    Mean duration of every activity (in sec): {'ChartGenerator': 0.587241, 'DocWriter': 1.0209089999999998, 'NoteTaker': 0.5753873333333334, 'Search': 0.580575, 'WebScraper': 0.6020846, '__start__': 0.0411957037037037, 'ag_supervisor': 0.007210296296296296, 'rg_supervisor': 1.8212668636363636, 'test_supervisor': 0.04827048148148148}
    """
    mean_serv_time = get_mean_act_times(event_log)
    print("Mean duration of every activity (in sec):", mean_serv_time)


#30
def get_durations(event_log: pd.DataFrame) -> dict[str, float]:
    """
    Calculate the duration of each case in seconds.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :return: Case durations.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_durations(event_log))
    Event log loaded and formated from file: files/examples.csv
    {'18': 4.580137, '19': 120.730501, '20': 74.653202}
    """
    # Pobranie unikalnych identyfikatorów przypadków (case_id)
    unique_case_ids = event_log['case:concept:name'].unique()
    sorted_array = np.sort(unique_case_ids.astype(int)).astype(str)

    # Iterowanie po każdym case_id i uzyskanie jego czasu trwania
    case_durations = {}
    for case_id in sorted_array:
        duration = pm4py.get_case_duration(event_log, case_id)
        case_durations[case_id] = duration
    return case_durations


#31
def print_durations(event_log: pd.DataFrame) -> None:
    """
    Print the duration of each case in seconds.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_durations(event_log)
    Event log loaded and formated from file: files/examples.csv
    Duration of the case:
    Case ID 18: 4.580137 s
    Case ID 19: 120.730501 s
    Case ID 20: 74.653202 s
    """
    case_durations = get_durations(event_log)
    print("Duration of the case:")

    for case_id, duration in case_durations.items():
        print(f"Case ID {case_id}: {duration} s")


def get_self_dist_witnesses(event_log: pd.DataFrame) -> dict[int, dict[str, list[list[str]]]]:
    """
    Compute the minimum self-distance witnesses for each activity in each case of the event log.

    :param event_log: Event log data containing events with case IDs and activity names.
    :type event_log: pd.DataFrame
    :return: A dictionary where each key is a case ID, and each value is another dictionary mapping
             activities to lists of witness sequences.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_all_self_distance_witnesses(event_log))
    Event log loaded and formated from file: files/examples.csv
    {18: {}, 19: {'__start__': [['test_supervisor']], 'test_supervisor': [['__start__', 'rg_supervisor'], ['__start__', 'ag_supervisor']], 'rg_supervisor': [['Search'], ['WebScraper']], 'Search': [['rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'WebScraper': [['rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'ag_supervisor': [['DocWriter'], ['ChartGenerator']], 'DocWriter': [['ag_supervisor']]}, 20: {'__start__': [['test_supervisor']], 'test_supervisor': [['__start__', 'rg_supervisor']], 'rg_supervisor': [['Search'], ['WebScraper']], 'Search': [['rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'ag_supervisor': [['DocWriter'], ['ChartGenerator'], ['NoteTaker']], 'ChartGenerator': [['ag_supervisor']], 'DocWriter': [['ag_supervisor', 'NoteTaker', 'ag_supervisor']], 'NoteTaker': [['ag_supervisor', 'DocWriter', 'ag_supervisor']]}}
    """
    # Konwersja case_id do int'a
    event_log['case_id'] = event_log['case_id'].astype(int)
    unique_case_ids = event_log['case_id'].unique()

    # Sortowanie case_id
    sorted_case_ids = sorted(unique_case_ids)

    all_msd_witnesses = {}

    for case_id in sorted_case_ids:
        # Filtrowanie event log'u dla aktualnego case_id
        filtered_event_log = event_log[event_log['case_id'] == case_id].copy()

        if filtered_event_log.empty:
            continue

        # Reset index'u by zapewnić, że index'y zaczynają się od 0
        filtered_event_log.reset_index(drop=True, inplace=True)

        # Grupowanie event'ów po aktywności i kalkulacja indeksów
        activity_indices = {}
        for activity in filtered_event_log['concept:name'].unique():
            activity_indices[activity] = filtered_event_log[
                filtered_event_log['concept:name'] == activity].index.tolist()

        # Wylicz minimalne odległości własne i świadków
        min_self_distances = {}
        corrected_witnesses = {}
        for activity, indices in activity_indices.items():
            # Nie ma odległości własnej jak nie występuje przynajmniej 2 razy
            if len(indices) < 2:
                continue

            # Wylicz przerwy i znajdź minimalne odległości własne
            gaps = [indices[i + 1] - indices[i] - 1 for i in range(len(indices) - 1)]
            min_distance = min(gaps)
            min_self_distances[activity] = min_distance

            # Zidentyfikuj świadków dla minimalnych odległości własnych
            witness_sequences = []
            for i in range(len(indices) - 1):
                gap_size = indices[i + 1] - indices[i] - 1
                if gap_size == min_distance:
                    gap_events = filtered_event_log.iloc[indices[i] + 1:indices[i + 1]]['concept:name'].tolist()
                    # Wyłącz aktywność z listy
                    gap_events = [event for event in gap_events if event != activity]
                    # Dodaj tylko nie pustę przerwy
                    if gap_events:
                        witness_sequences.append(gap_events)

            # De duplikacja sekwencji z zachowaniem ich kolejności
            unique_sequences = list(map(list, {tuple(seq) for seq in witness_sequences}))
            corrected_witnesses[activity] = unique_sequences

        all_msd_witnesses[case_id] = corrected_witnesses

    return all_msd_witnesses


def print_self_dist_witnesses(event_log: pd.DataFrame) -> None:
    """
    Print the minimum self-distance witnesses for each activity in each case.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_self_dist_witnesses(event_log)
    Event log loaded and formated from file: files/examples.csv
    Witnesses of minimum self-distances:
    Case ID 18: {}
    Case ID 19: {'__start__': [['test_supervisor']], 'test_supervisor': [['__start__', 'rg_supervisor'], ['__start__', 'ag_supervisor']], 'rg_supervisor': [['Search'], ['WebScraper']], 'Search': [['rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'WebScraper': [['rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'ag_supervisor': [['DocWriter'], ['ChartGenerator']], 'DocWriter': [['ag_supervisor']]}
    Case ID 20: {'__start__': [['test_supervisor']], 'test_supervisor': [['__start__', 'rg_supervisor']], 'rg_supervisor': [['Search'], ['WebScraper']], 'Search': [['rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'ag_supervisor': [['DocWriter'], ['ChartGenerator'], ['NoteTaker']], 'ChartGenerator': [['ag_supervisor']], 'DocWriter': [['ag_supervisor', 'NoteTaker', 'ag_supervisor']], 'NoteTaker': [['ag_supervisor', 'DocWriter', 'ag_supervisor']]}
    """
    all_msd_witnesses = get_self_dist_witnesses(event_log)

    print("Witnesses of minimum self-distances:")
    for case_id, witnesses in all_msd_witnesses.items():
        print(f"Case ID {case_id}: {witnesses}")


#42
def print_analysis(event_log: pd.DataFrame) -> None:
    """
    Run multiple analyses on the event log and print the results.

    :param event_log: The event log data to analyze.
    :type event_log: pd.DataFrame

    **Example**:

    .. code-block:: python

        csv_output = "files/examples.csv"
        event_log = load_event_log(csv_output)
        print_all_self_distance_witnesses(event_log)
        # Event log loaded and formated from file: files/examples.csv
        #
        # ###################START###########################
        #
        # Start activities: {'__start__': 3}
        #
        # End activities: {'test_supervisor': 3}
        #
        # Count of each activity: {'__start__': 27, 'ag_supervisor': 27, 'test_supervisor': 27, 'rg_supervisor': 22, 'DocWriter': 8, 'Search': 5, 'WebScraper': 5, 'ChartGenerator': 3, 'NoteTaker': 3}
        #
        # All sequences:
        # Case ID 18: ['__start__', 'ag_supervisor', 'test_supervisor']
        # Case ID 19: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']
        # Case ID 20: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']
        #
        # ID of last sequence occurrence with probability of occurrence:
        # Case ID 18: ('__start__', 'ag_supervisor', 'test_supervisor'), 0.3333333333333333
        # Case ID 19: ('__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor'), 0.3333333333333333
        # Case ID 20: ('__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor'), 0.3333333333333333
        #
        # Minimal self-distances for every activity:
        # Case ID 18: {}
        # Case ID 19: {'DocWriter': 1, 'Search': 6, 'WebScraper': 4, '__start__': 1, 'ag_supervisor': 1, 'rg_supervisor': 1, 'test_supervisor': 2}
        # Case ID 20: {'ChartGenerator': 1, 'DocWriter': 3, 'NoteTaker': 3, 'Search': 36, '__start__': 1, 'ag_supervisor': 1, 'rg_supervisor': 1, 'test_supervisor': 2}
        #
        # Witnesses of minimum self-distances:
        # Case ID 18: {}
        # Case ID 19: {'__start__': [['test_supervisor']], 'test_supervisor': [['__start__', 'ag_supervisor'], ['__start__', 'rg_supervisor']], 'rg_supervisor': [['Search'], ['WebScraper']], 'Search': [['rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'WebScraper': [['rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'ag_supervisor': [['DocWriter'], ['ChartGenerator']], 'DocWriter': [['ag_supervisor']]}
        # Case ID 20: {'__start__': [['test_supervisor']], 'test_supervisor': [['__start__', 'rg_supervisor']], 'rg_supervisor': [['Search'], ['WebScraper']], 'Search': [['rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'NoteTaker', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'ag_supervisor': [['DocWriter'], ['NoteTaker'], ['ChartGenerator']], 'ChartGenerator': [['ag_supervisor']], 'DocWriter': [['ag_supervisor', 'NoteTaker', 'ag_supervisor']], 'NoteTaker': [['ag_supervisor', 'DocWriter', 'ag_supervisor']]}
        #
        # Count of activity rework:
        # Case ID 18: {}
        # Case ID 19: {'__start__': 18, 'test_supervisor': 18, 'rg_supervisor': 15, 'Search': 3, 'WebScraper': 4, 'ag_supervisor': 14, 'DocWriter': 4}
        # Case ID 20: {'__start__': 8, 'test_supervisor': 8, 'rg_supervisor': 7, 'Search': 2, 'ag_supervisor': 12, 'ChartGenerator': 2, 'DocWriter': 4, 'NoteTaker': 3}
        #
        # Mean duration of every activity (in sec): {'ChartGenerator': 0.587241, 'DocWriter': 1.0209089999999998, 'NoteTaker': 0.5753873333333334, 'Search': 0.580575, 'WebScraper': 0.6020846, '__start__': 0.0411957037037037, 'ag_supervisor': 0.007210296296296296, 'rg_supervisor': 1.8212668636363636, 'test_supervisor': 0.04827048148148148}
        #
        # Duration of the case:
        # Case ID 18: 4.580137 s
        # Case ID 19: 120.730501 s
        # Case ID 20: 74.653202 s
        #
        # ######################END###########################
    """

    print("\n####################START###########################\n")

    print_starts(event_log)
    print()

    print_ends(event_log)
    print()

    print_act_counts(event_log)
    print()

    print_sequences(event_log)
    print()

    print_sequence_probs(event_log)
    print()

    print_min_self_dists(event_log)
    print()

    print_self_dist_witnesses(event_log)
    print()

    print_act_reworks(event_log)
    print()

    print_mean_act_times(event_log)
    print()

    print_durations(event_log)

    print("\n######################END###########################")
