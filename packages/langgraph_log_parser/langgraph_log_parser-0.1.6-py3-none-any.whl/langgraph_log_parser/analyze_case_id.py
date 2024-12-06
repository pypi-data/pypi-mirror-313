import pandas as pd
import pm4py
from collections import defaultdict
from collections import Counter

pd.set_option('display.max_columns', None)

# 12
def get_case_sequence(event_log: pd.DataFrame, case_id: int) -> list[str]:
    """
    Return the activity sequence for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve the sequence for.
    :type case_id: int
    :return: The activity sequence for the specified case ID.
    :rtype: list
    :raises ValueError: If the case ID does not exist in the event log.

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_sequence(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']
    """
    # Sprawdź, czy case_id istnieje
    if case_id not in event_log['case_id'].unique():
        raise ValueError(f"Case ID {case_id} does not exist in the event log.")

    # Filtrowanie event log'u pod dane case_id
    case_log = event_log[event_log['case_id'] == case_id]

    # Wyciągnięcie sekwencji
    sequence = case_log['activity'].tolist()

    return sequence

#13
def print_case_sequence(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the activity sequence for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve the sequence for.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_case_sequence(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    Activity sequence for case ID 19: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']
    """
    sequence = get_case_sequence(event_log, case_id)
    print(f"Activity sequence for case ID {case_id}: {sequence}")

#14
def get_case_sequence_prob(event_log: pd.DataFrame, case_id: int) -> tuple[list[str], float]:
    """
    Return the activity sequence with its probability for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve the sequence and probability for.
    :type case_id: int
    :return: A tuple containing (sequence, probability) for the specified case ID.
    :rtype: tuple
    :raises ValueError: If the case ID does not exist in the event log.

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_sequence_prob(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    (['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor'], 0.3333333333333333)
    """
    # Sprawdź, czy case_id istnieje
    if case_id not in event_log['case_id'].unique():
        raise ValueError(f"Case ID {case_id} does not exist in the event log.")

    # Pobierz sekwencje o specyficznym case_id
    sequence = get_case_sequence(event_log, case_id)

    # Generujemy probabilistyczny język
    language = pm4py.get_stochastic_language(event_log)

    probability = language.get(tuple(sequence), 0)

    return sequence, probability

#15
def print_case_sequence_prob(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the activity sequence with its probability for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve and print the sequence and probability for.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_case_sequence_prob(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    Activity sequence with probability for case ID 19: Sequence: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']; Probability: 0.3333333333333333
    """
    sequence, probability = get_case_sequence_prob(event_log, case_id)
    print(f"Activity sequence with probability for case ID {case_id}: Sequence: {sequence}; Probability: {probability}")

#18
def get_case_min_self_dists(event_log: pd.DataFrame, case_id: int) -> dict[str, int]:
    """
    Return the minimum self-distances for all activities for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve the minimum self-distances for.
    :type case_id: int
    :return: A dictionary of activities with their minimum self-distances for the specified case ID.
    :rtype: dict
    :raises ValueError: If the case ID does not exist in the event log.

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_min_self_dists(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    {'DocWriter': 1, 'Search': 6, 'WebScraper': 4, '__start__': 1, 'ag_supervisor': 1, 'rg_supervisor': 1, 'test_supervisor': 2}
    """
    # Sprawdź, czy case_id istnieje w event logu
    if case_id not in event_log['case_id'].unique():
        raise ValueError(f"Case ID {case_id} does not exist in the event log.")

    # Filtrowanie event logu do specyficznego case id
    filtered_event_log = event_log[event_log['case_id'] == case_id]

    # Obliczanie minimalnych odległości własnych dla wybranego case_id
    msd = pm4py.get_minimum_self_distances(
        filtered_event_log,
        activity_key='concept:name',
        case_id_key='case:concept:name',
        timestamp_key='time:timestamp'
    )
    return msd

#19
def print_case_min_self_dists(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the minimum self-distances for all activities for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve and print the minimum self-distances for.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_case_min_self_dists(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    Minimum self distances for case ID 19: {'DocWriter': 1, 'Search': 6, 'WebScraper': 4, '__start__': 1, 'ag_supervisor': 1, 'rg_supervisor': 1, 'test_supervisor': 2}
    """

    min_self_distances = get_case_min_self_dists(event_log, case_id)
    print(f"Minimum self distances for case ID {case_id}: {min_self_distances}")

#26
def get_case_act_reworks(event_log: pd.DataFrame, case_id: int) -> dict[str, int]:
    """
    Return the rework counts for each activity for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve the rework counts for.
    :type case_id: int
    :return: A dictionary of activities with their rework counts for the specified case ID.
    :rtype: dict
    :raises ValueError: If the case ID does not exist in the event log.

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_act_reworks(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    {'__start__': 18, 'test_supervisor': 18, 'rg_supervisor': 15, 'Search': 3, 'WebScraper': 4, 'ag_supervisor': 14, 'DocWriter': 4}
    """
    # Sprawdź, czy case_id istnieje w event_log'u
    if case_id not in event_log['case_id'].unique():
        raise ValueError(f"Case ID {case_id} does not exist in the event log.")

    # Filtrowanie dla specyficznego case_id
    filtered_event_log = event_log[event_log['case_id'] == case_id]

    # Inicjalizacja liczenia aktywności
    activity_counts = defaultdict(int)

    # Tworzenie listy aktywności
    activities = filtered_event_log['concept:name'].tolist()

    # Policz wystąpienia każdej aktywności
    for activity in activities:
        activity_counts[activity] += 1

    # Jeżeli zaistniało raz — usuń bo nie rework
    rework_counts = {activity: count for activity, count in activity_counts.items() if count > 1}

    return rework_counts

#27
def print_case_act_reworks(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the rework counts for each activity for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve and print the rework counts for.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_case_act_reworks(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    Rework counts for case ID 19: {'__start__': 18, 'test_supervisor': 18, 'rg_supervisor': 15, 'Search': 3, 'WebScraper': 4, 'ag_supervisor': 14, 'DocWriter': 4}
    """
    rework_counts = get_case_act_reworks(event_log, case_id)
    print(f"Rework counts for case ID {case_id}: {rework_counts}")

#32
def get_case_duration(event_log: pd.DataFrame, case_id: int) -> float:
    """
    Calculate the duration time for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve the duration time for.
    :type case_id: int
    :return: The duration time for the specified case ID.
    :rtype: float
    :raises ValueError: If the case ID does not exist in the event log.

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_duration(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    120.730501
    """
    # Konwersja na string'a - bo get_case_duration przyjmuje tylko stringi
    case_id_str = str(case_id)

    # Sprawdź, czy case_id istnieje w event_log'u
    if case_id_str not in event_log['case_id'].astype(str).unique():
        raise ValueError(f"Case ID {case_id} does not exist in the event log.")

    # Wylicz czas trwania dla danego case_id
    duration = pm4py.get_case_duration(event_log, case_id_str)
    return duration

#33
def print_case_duration(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the duration time for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve and print the duration time for.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_case_duration(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    Duration for case ID 19: 120.730501 s
    """
    duration = get_case_duration(event_log, case_id)
    print(f"Duration for case ID {case_id}: {duration} s")

#34
def get_case_start(event_log: pd.DataFrame, case_id: int) -> str:
    """
    Retrieve the first activity for the specified case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve the start activity for.
    :type case_id: int
    :return: The first activity in the sequence.
    :rtype: str

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_start(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    __start__
    """
    sequence = get_case_sequence(event_log, case_id)
    return sequence[0]

#35
def print_case_start(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the first activity for the specified case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve and print the start activity for.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_case_start(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    Start activity for case ID 19: __start__
    """
    start_activity = get_case_start(event_log, case_id)
    print(f"Start activity for case ID {case_id}: {start_activity}")

#36
def get_case_end(event_log: pd.DataFrame, case_id: int) -> str:
    """
    Retrieve the last activity for the specified case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve the end activity for.
    :type case_id: int
    :return: The last activity in the sequence.
    :rtype: str

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_end(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    test_supervisor
    """
    sequence = get_case_sequence(event_log, case_id)
    return sequence[-1]

#37
def print_case_end(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the last activity for the specified case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve and print the end activity for.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_case_end(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    End activity for case ID 19: test_supervisor
    """
    end_activity = get_case_end(event_log, case_id)
    print(f"End activity for case ID {case_id}: {end_activity}")

#38
def get_case_act_counts(event_log: pd.DataFrame, case_id: int) -> dict[str, int]:
    """
    Count how many times each activity occurred for the specified case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to count activities for.
    :type case_id: int
    :return: A dictionary with activities as keys and their counts as values.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_act_counts(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    {'__start__': 18, 'test_supervisor': 18, 'rg_supervisor': 15, 'Search': 3, 'WebScraper': 4, 'ag_supervisor': 14, 'ChartGenerator': 1, 'DocWriter': 4}
    """
    sequence = get_case_sequence(event_log, case_id)
    return dict(Counter(sequence))

#39
def print_case_act_counts(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the count of each activity for the specified case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to count and print activities for.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_case_act_counts(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    Count of each activity for case ID 19: {'__start__': 18, 'test_supervisor': 18, 'rg_supervisor': 15, 'Search': 3, 'WebScraper': 4, 'ag_supervisor': 14, 'ChartGenerator': 1, 'DocWriter': 4}
    """
    activities_count = get_case_act_counts(event_log, case_id)
    print(f"Count of each activity for case ID {case_id}: {activities_count}")

#40
def get_case_sum_act_times(event_log: pd.DataFrame, case_id: int) -> dict[str, float]:
    """
    Calculate the sum service time in seconds for each activity for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID for which to calculate service times.
    :type case_id: int
    :return: Sum service times for each activity in the specified case.
    :rtype: dict

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_sum_act_times(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    {'ChartGenerator': 0.608224, 'DocWriter': 2.0285469999999997, 'Search': 1.7249849999999998, 'WebScraper': 2.4464859999999997, '__start__': 0.603216, 'ag_supervisor': 0.10220199999999999, 'rg_supervisor': 23.0226, 'test_supervisor': 0.747701}
    """

    # Konwersja na string'a - bo get_service_time przyjmuje tylko stringi
    case_id_str = str(case_id)

    # Usuń potencjalne spacje z case_id w logu
    event_log["case_id"] = event_log["case_id"].astype(str).str.strip()

    # Sprawdź, czy case_id istnieje w event_log'u
    if case_id_str not in event_log['case_id'].astype(str).unique():
        raise ValueError(f"Case ID {case_id} does not exist in the event log.")

    # Filtrowanie
    filtered_log = event_log[event_log["case_id"] == case_id_str].copy()

    # Wyliczenie średnich czasów wykonania aktywności w danym przypadku
    sum_serv_time = pm4py.get_service_time(
        filtered_log,
        start_timestamp_key="timestamp",
        timestamp_key="end_timestamp",
        aggregation_measure="sum"
    )

    return sum_serv_time

#41
def print_case_sum_act_times(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the sum service time in seconds for each activity for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID for which to calculate service times.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_sum_service_time_by_case_id(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    Sum service time of each activity for case ID 19 (in sec): {'ChartGenerator': 0.608224, 'DocWriter': 2.0285469999999997, 'Search': 1.7249849999999998, 'WebScraper': 2.4464859999999997, '__start__': 0.603216, 'ag_supervisor': 0.10220199999999999, 'rg_supervisor': 23.0226, 'test_supervisor': 0.747701}
    """
    sum_time = get_case_sum_act_times(event_log, case_id)
    print(f"Sum service time of each activity for case ID {case_id} (in sec): {sum_time}")


def get_case_self_dist_witnesses(event_log: pd.DataFrame, case_id: int) -> dict[str, list[list[str]]]:
    """
    Return the minimum self-distance witnesses for all activities for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve the witnesses for.
    :type case_id: int
    :return: A dictionary of activities with their for the specified case ID.
    :rtype: dict
    :raises ValueError: If the case ID does not exist in the event log.

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print(get_case_self_dist_witnesses(event_log,19))
    Event log loaded and formated from file: files/examples.csv
    {'__start__': [['test_supervisor']], 'test_supervisor': [['__start__', 'ag_supervisor'], ['__start__', 'rg_supervisor']], 'rg_supervisor': [['Search'], ['WebScraper']], 'Search': [['rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'WebScraper': [['rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'ag_supervisor': [['DocWriter'], ['ChartGenerator']], 'DocWriter': [['ag_supervisor']]}
    """
    # Konwersja case_id do int dla spójności
    event_log['case_id'] = event_log['case_id'].astype(int)
    case_id = int(case_id)

    # Sprawdź, czy case_id istnieje w dzienniku zdarzeń
    if case_id not in event_log['case_id'].unique():
        raise ValueError(f"Case ID {case_id} nie istnieje w dzienniku zdarzeń.")

    # Filtrowanie dziennika zdarzeń dla określonego case_id
    filtered_event_log = event_log[event_log['case_id'] == case_id].copy()

    # Sprawdzenie, czy po filtrowaniu dziennik zdarzeń nie jest pusty
    if filtered_event_log.empty:
        return {}

    # Resetowanie indeksu, aby zapewnić, że indeksy zaczynają się od 0
    filtered_event_log.reset_index(drop=True, inplace=True)

    # Grupowanie zdarzeń według aktywności i obliczanie indeksów
    activity_indices = {}
    for activity in filtered_event_log['concept:name'].unique():
        activity_indices[activity] = filtered_event_log[filtered_event_log['concept:name'] == activity].index.tolist()

    # Obliczanie minimalnych odległości własnych i świadków
    corrected_witnesses = {}
    for activity, indices in activity_indices.items():
        if len(indices) < 2:
            continue

        # Obliczanie przerw i znajdowanie minimalnej odległości własnej
        gaps = [indices[i + 1] - indices[i] - 1 for i in range(len(indices) - 1)]
        min_distance = min(gaps)

        # Identyfikacja świadków dla minimalnej odległości własnej
        witness_sequences = []
        for i in range(len(indices) - 1):
            gap_size = indices[i + 1] - indices[i] - 1
            if gap_size == min_distance:
                gap_events = filtered_event_log.iloc[indices[i] + 1:indices[i + 1]]['concept:name'].tolist()
                # Wykluczanie samej aktywności z listy zdarzeń w przerwie
                gap_events = [event for event in gap_events if event != activity]
                if gap_events:  # Dodaj tylko niepuste przerwy
                    witness_sequences.append(gap_events)

        # Deduplikacja sekwencji z zachowaniem ich kolejności
        unique_sequences = list(map(list, {tuple(seq) for seq in witness_sequences}))
        corrected_witnesses[activity] = unique_sequences

    return corrected_witnesses

def print_case_self_dist_witnesses(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Print the minimum self-distance witnesses for all activities for a specific case ID.

    :param event_log: Event log data.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve and print the witnesses for.
    :type case_id: int

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    >>> print_case_self_dist_witnesses(event_log,19)
    Event log loaded and formated from file: files/examples.csv
    Minimum self distance witnesses for case ID 19: {'__start__': [['test_supervisor']], 'test_supervisor': [['__start__', 'ag_supervisor'], ['__start__', 'rg_supervisor']], 'rg_supervisor': [['Search'], ['WebScraper']], 'Search': [['rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'WebScraper': [['rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'ag_supervisor': [['DocWriter'], ['ChartGenerator']], 'DocWriter': [['ag_supervisor']]}
    """
    witnesses = get_case_self_dist_witnesses(event_log, case_id)
    print(f"Minimum self distance witnesses for case ID {case_id}: {witnesses}")

#43
def print_case_analysis(event_log: pd.DataFrame, case_id: int) -> None:
    """
    Run multiple analyses on single case_id and print the results.

    :param event_log: The event log data to analyze.
    :type event_log: pd.DataFrame
    :param case_id: The case ID to retrieve and analyze.
    :type case_id: int

    **Example:**

    .. code-block:: python

        csv_output = "files/examples.csv"
        event_log = load_event_log(csv_output)
        print_full_analysis_by_id(event_log,19)
        # Event log loaded and formated from file: files/examples.csv
        #
        # ####################START###########################
        #
        # Start activity for case ID 19: __start__
        #
        # End activity for case ID 19: test_supervisor
        #
        # Count of each activity for case ID 19: {'__start__': 18, 'test_supervisor': 18, 'rg_supervisor': 15, 'Search': 3, 'WebScraper': 4, 'ag_supervisor': 14, 'ChartGenerator': 1, 'DocWriter': 4}
        #
        # Activity sequence for case ID 19: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']
        #
        # Activity sequence with probability for case ID 19: Sequence: ['__start__', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'ChartGenerator', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'Search', 'rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'DocWriter', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'ag_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor', 'test_supervisor']; Probability: 0.3333333333333333
        #
        # Minimum self distances for case ID 19: {'DocWriter': 1, 'Search': 6, 'WebScraper': 4, '__start__': 1, 'ag_supervisor': 1, 'rg_supervisor': 1, 'test_supervisor': 2}
        #
        # Minimum self distance witnesses for case ID 19: {'__start__': [['test_supervisor']], 'test_supervisor': [['__start__', 'rg_supervisor'], ['__start__', 'ag_supervisor']], 'rg_supervisor': [['WebScraper'], ['Search']], 'Search': [['rg_supervisor', 'WebScraper', 'rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'WebScraper': [['rg_supervisor', 'test_supervisor', '__start__', 'rg_supervisor']], 'ag_supervisor': [['DocWriter'], ['ChartGenerator']], 'DocWriter': [['ag_supervisor']]}
        #
        # Rework counts for case ID 19: {'__start__': 18, 'test_supervisor': 18, 'rg_supervisor': 15, 'Search': 3, 'WebScraper': 4, 'ag_supervisor': 14, 'DocWriter': 4}
        #
        # Sum service time of each activity for case ID 19 (in sec): {'ChartGenerator': 0.608224, 'DocWriter': 2.0285469999999997, 'Search': 1.7249849999999998, 'WebScraper': 2.4464859999999997, '__start__': 0.603216, 'ag_supervisor': 0.10220199999999999, 'rg_supervisor': 23.0226, 'test_supervisor': 0.747701}
        #
        # Duration for case ID 19: 120.730501 s
        #
        # ######################END###########################
    """

    print("\n####################START###########################\n")

    print_case_start(event_log, case_id)
    print()

    print_case_end(event_log, case_id)
    print()

    print_case_act_counts(event_log, case_id)
    print()

    print_case_sequence_prob(event_log, case_id)
    print()

    print_case_min_self_dists(event_log, case_id)
    print()

    print_case_self_dist_witnesses(event_log, case_id)
    print()

    print_case_act_reworks(event_log, case_id)
    print()

    print_case_sum_act_times(event_log, case_id)
    print()

    print_case_duration(event_log, case_id)

    print("\n######################END###########################")