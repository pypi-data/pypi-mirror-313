from typing import Dict, Any
from langgraph.graph import StateGraph


def run_multiple_iterations(
        graph: StateGraph,
        starting_thread_id: int,
        num_repetitions: int,
        user_input_template: Dict[str, Any],
        recursion_limit: int = 100
) -> None:
    """
    Run the provided graph `num_repetitions` times, incrementing the thread_id each time.

    :param graph: The compiled StateGraph to run.
    :type graph: StateGraph
    :param starting_thread_id: The starting thread_id for the graph.
    :type starting_thread_id: int
    :param num_repetitions: Number of times to run the graph.
    :type num_repetitions: int
    :param user_input_template: The template for user input, which may vary by iteration.
    :type user_input_template: Dict[str, Any]
    :param recursion_limit: Maximum recursion depth allowed for each graph run.
    :type recursion_limit: int

    **Example**:

    .. code-block:: python

        # .compile method from official langgraph package
        graph = graph_builder.compile(checkpointer=memory)

        # Run the graph for 3 iterations, starting from thread ID 1
        run_multiple_iterations(graph, 1, 3, {"messages": [("user", "Tell me a joke")]})

        # Output:
        # Iteration: 1, Thread_ID 1
        # {'messages': [AIMessage(content='Why did the scarecrow win an award? Because he was outstanding in his field!',
        # additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 18,
        # 'prompt_tokens': 11, 'total_tokens': 29, ...})]}
        # ---
        # Iteration: 2, Thread_ID 2
        # {'messages': [AIMessage(content='Why did the scarecrow win an award? Because he was outstanding in his field!',
        # additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 17,
        # 'prompt_tokens': 11, 'total_tokens': 28, ...})]}
        # ---
        # Iteration: 3, Thread_ID 3
        # {'messages': [AIMessage(content='Why did the scarecrow win an award? Because he was outstanding in his field!',
        # additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 18,
        # 'prompt_tokens': 11, 'total_tokens': 29, ...})]}
        # ---
    """
    for i in range(num_repetitions):
        # Wygeneruj dla aktualnego thread ID i dostosuj user input w ramach potrzeby
        current_thread_id = str(starting_thread_id + i)
        config = {
            "configurable": {"thread_id": current_thread_id},
            "recursion_limit": recursion_limit
        }

        # Użyj całego user_input_template jako user input
        user_input = user_input_template.copy()

        print(f"Iteration: {i + 1}, Thread_ID {current_thread_id}")
        for event in graph.stream(user_input, config):
            for value in event.values():
                if "__end__" not in value:
                    print(value)
                    print("---")
