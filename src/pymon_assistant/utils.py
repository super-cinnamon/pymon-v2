"""
helper functions for the pymon assistant
will contain all the files for processing and checking data validity
"""
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def check_query_validity(query):
    """
    checks if the query is valid for the pymon assistant
    the query must be a string, not empty

    Parameters
    ----------
    query: str
        the user's input query

    Returns
    -------
    bool
        True if the query is valid, False otherwise
    """
    if isinstance(query, str) and query:
        return True
    else:
        return False


def check_history_validity(history):
    """
    checks if the history is valid for the pymon assistant
    the history must be a list of dicts, with the keys 'role' and 'text'

    Parameters
    ----------
    history: list
        the list of previous user inputs

    Returns
    -------
    bool
        True if the history is valid, False otherwise
    """
    if isinstance(history, list):
        for item in history:
            if not isinstance(item, dict) or 'role' not in item or 'parts' not in item:
                return False

            # the role must be either 'user' or 'model'
            elif item['role'] not in ['user', 'model']:
                return False

        return True


def check_context_validity(context, search_type="web"):
    """
    checks if the context is valid for the pymon assistant
    the context must be a list of strings, not empty

    Parameters
    ----------
    context: list
        the list of search results from the web search

    Returns
    -------
    bool
        True if the context is valid, False otherwise
    """
    if isinstance(context, list) and context:
        # title href and body
        if search_type == "web":
            if all(isinstance(result, dict) for result in context):
                return True
        elif search_type == "vdb":
            if all(isinstance(result, str) for result in context):
                return True
    else:
        return False
