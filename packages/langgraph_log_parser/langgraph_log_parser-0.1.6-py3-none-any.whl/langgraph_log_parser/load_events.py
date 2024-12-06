import pandas as pd
import pm4py

#1
def load_event_log(file_path: str) -> pd.DataFrame:
    """
    Load CSV data into a formatted PM4Py DataFrame.

    :param file_path: Path to the CSV file containing the event log.
    :type file_path: str
    :return: PM4Py formatted DataFrame.
    :rtype: pd.DataFrame

    **Example:**

    >>> csv_output = "files/examples.csv"
    >>> event_log = load_event_log(csv_output)
    Event log loaded and formated from file: files/examples.csv
    """
    # Ładowanie CSV do pandas DataFrame
    df = pd.read_csv(file_path)

    # Formatowanie DataFrame dla PM4Py
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    print(f"Event log loaded and formated from file: {file_path}")
    return pm4py.format_dataframe(df, case_id='case_id', activity_key='activity', timestamp_key='timestamp')