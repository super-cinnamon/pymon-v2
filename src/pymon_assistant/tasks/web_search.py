"""
the main web search processing file
will contain the helper functions in the search api notebook
"""
from duckduckgo_search import DDGS

from src.pymon_assistant.utils import check_context_validity


def search_DDG(query):
    """
    searches the web using DuckDuckGo

    Parameters
    ----------
    query: str
        the user's input query to the search engine

    Returns
    -------
    list
        the list of search results from the search engine
    """
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=10)]
        return results


def rag_input(search_results):
    """
    compiles the search results into a single string

    Parameters
    ----------
    search_results: list
        the list of search results from the search engine

    Returns
    -------
    str
        the compiled input for the LLM
    """

    rag_string = "\n\n## Search results:\n"

    # check context shape validity
    if not check_context_validity(search_results):
        rag_string += "No search results available.\n"

    else:
        for res in search_results:
            rag_string += res['title']+": "+res['body']+"\n"+"link: "+res['href']+"\n\n"

    return rag_string


def get_context(query):
    """
    searches the web, and returns a markdown formatted string of the search results

    Parameters
    ----------
    query: str
        the user's input query to the search engine

    Returns
    -------
    str
        the markdown formatted string of the search results
    """
    search_results = search_DDG(query)
    text_input = rag_input(search_results)
    return text_input
