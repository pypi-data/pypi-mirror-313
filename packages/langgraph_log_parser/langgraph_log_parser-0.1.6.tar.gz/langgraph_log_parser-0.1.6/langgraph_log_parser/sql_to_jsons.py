import os
import sqlite3
import json
from typing import Dict, Any

import msgpack

def _convert(obj):
    """
    Convert bytes, dicts, lists, and tuples to strings recursively.

    :param obj: The object to convert (bytes, dict, list, or tuple).
    :type obj: Any
    :return: The converted object with strings instead of bytes.
    :rtype: Any
    """
    # Konwersja byte'ów do string'ów
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="ignore")
    # Konwersja słowników do string'ów
    elif isinstance(obj, dict):
        # Konwersja elementów słownika rekursywnie
        return {key: _convert(value) for key, value in obj.items()}
    # Konwersja listy do string'ów
    elif isinstance(obj, list):
        # Konwersja elementów listy rekursywnie
        return [_convert(element) for element in obj]
    # Konwersja tupli do string'ów
    elif isinstance(obj, tuple):
        # Konwersja elementów tupli rekursywnie
        return tuple(_convert(element) for element in obj)
    else:
        return obj


def export_sqlite_to_jsons(db_path: str = "checkpoints.sqlite", output_folder: str ="files/json") -> None:
    """
    Fetch data from the SQLite database and export it as JSON files.

    :param db_path: Path to the SQLite database file.
    :type db_path: str
    :param output_folder: Path to the folder where output JSON files will be saved.
    :type output_folder: str

    **Example:**

    >>> database = "test.sqlite"
    >>> output = "files"
    >>> export_sqlite_to_jsons(database,output)
    JSON file created: files/thread_1.json
    JSON file created: files/thread_2.json
    JSON file created: files/thread_3.json
    """

    # Upewnij się, że folder istnieje
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Połączenie do bazy danych
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()

    try:
        # Pobieramy dane z tabeli "checkpoints"
        cursor.execute("SELECT * FROM checkpoints")
        rows = cursor.fetchall()

        # Słownik do przechowywania danych pogrupowanych według thread_ID
        data_by_thread: Dict[int, list] = {}

        for row in rows:
            thread_id = row[0]

            try:
                # Deserializacja z użyciem msgpack
                checkpoint = msgpack.loads(row[5])
                # Konwersja byte'ów do string'ów
                checkpoint = _convert(checkpoint)
            except Exception as e:
                print(f"Error deserializing checkpoint in row with thread_ID {thread_id}: {e}")
                checkpoint = None

            try:
                # Deserializacja metadanych z użyciem JSON
                metadata = json.loads(row[6])
                # To samo dla metadata (na MacOS z jakiegoś powodu też w postaci byte'ów)
                metadata = _convert(metadata)
            except Exception as e:
                print(f"Error deserializing metadata in row with thread_ID {thread_id}: {e}")
                metadata = None

            # Przygotowanie obiektu JSON
            json_object: Dict[str, Any] = {
                "thread_ID": thread_id,
                "checkpoint": checkpoint,
                "metadata": metadata
            }

            # Grupowanie danych według thread_ID
            if thread_id not in data_by_thread:
                data_by_thread[thread_id] = []
            data_by_thread[thread_id].append(json_object)

        # Zapisz dane dla każdego thread_ID w osobnym pliku JSON
        for thread_id, jsons in data_by_thread.items():
            output_path = os.path.join(output_folder, f"thread_{thread_id}.json")
            try:
                with open(output_path, 'w') as json_file:
                    # Zapisz dane jako JSON
                    json.dump(jsons, json_file, indent=4)
                print(f"JSON file created: {output_path}")
            except Exception as e:
                print(f"Error writing JSON file for thread_ID {thread_id}: {e}")

    finally:
        conn.close()