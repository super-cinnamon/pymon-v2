"""
the main chatbot (gemini api) processing file
will contain the helper functions in the gemini api notebook
"""
import dotenv
import os
import json
from copy import deepcopy
from datetime import datetime

import google.generativeai as genai

from src.pymon_assistant.utils import check_query_validity, check_history_validity
from src.pymon_assistant.tasks.web_search import get_context as web_context
from src.pymon_assistant.tasks.vdb_search import get_context as vdb_context


# load the dotenv file
dotenv.load_dotenv()

# get the Google AI Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# get the configuration settings
CONFIG_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "..", "config")

# get the chatbot configuration
with open(os.path.join(CONFIG_FOLDER_PATH, "gemini_config.json"), "r") as gemini_config:
    CHATBOT_CONFIG = json.load(gemini_config)

llm_config = CHATBOT_CONFIG["google_config"]
safety_config = CHATBOT_CONFIG["safety_settings"]

# get the prompt
with open(os.path.join(CONFIG_FOLDER_PATH, "prompt.md"), "r") as prompt_file:
    PROMPT = prompt_file.read()

# initialize the Gemini model
gemini = genai.GenerativeModel(model_name=llm_config["model_name"],
                               generation_config=llm_config["generation_config"],
                               safety_settings=safety_config)


def prompt_input(query, search_base="web"):
    """
    gets the LLM input with the prompt and context from web search
    and compiles it into a single string

    Parameters
    ----------
    query: str
        the user's input query to the LLM.
    context: list, optional
        the list of search results from the web search

    Returns
    -------
    str
        the compiled input for the LLM
    """
    pymon_input = ""

    # add the system prompt
    pymon_input += PROMPT.format(datetime.now())

    # add the context/search results
    if search_base == "web":
        pymon_input += web_context(query)
    elif search_base == "vdb":
        pymon_input += vdb_context(query)

    # add the user query
    pymon_input += "\n\n## User question:\n"
    pymon_input += query

    return pymon_input


def manage_history(history, convo, max_chat_size=5):
    """
    converts history from google content type to list of dict

    Parameters
    ----------
    history: list
        the list of previous conversations (google content type)
    convo: google.generativeai.generative_models.ChatSession
        the chat session containing all the messages
    max_chat_size: int, optional
        the maximum number of messages to keep in the history.
        Default is 5.

    Returns
    -------
    list
        the list of previous conversations (list of dict)

    """
    gemini_history = deepcopy(history)

    gemini_history.append({"role": convo.history[-2].role, "parts": convo.history[-2].parts[0].text})
    gemini_history.append({"role": convo.history[-1].role, "parts": convo.history[-1].parts[0].text})

    if len(gemini_history) > max_chat_size*2:
        gemini_history = gemini_history[-max_chat_size*2:]
    return gemini_history


def chat(instruction, history=[], search_base="vdb"):
    """
    the main chatbot function that processes the user input
    and returns the chatbot response and history.

    Parameters
    ----------
    instruction: str
        the user input query to the chatbot
    history: list, optional
        the list of previous conversations (list of dict)

    Returns
    -------
    str
        the chatbot response
    list
        the chat history (list of dict)

    Raises
    ------
    ValueError
        if the history or instruction is invalid
    """
    # get the llm input
    try:
        pymon_input = prompt_input(instruction, search_base=search_base)
    except Exception as e:
        print("switching to web search because of the following exception:")
        print(e)
        pymon_input = prompt_input(instruction, search_base="web")

    # init conversation
    if check_history_validity(history) and check_query_validity(instruction):
        convo = gemini.start_chat(history=history)
        response = convo.send_message(pymon_input)

        # get the response
        chat_response = response.text

        # get the correct conversation format
        messages = manage_history(history, convo)

    else:
        raise ValueError("Invalid history or instruction.")

    return chat_response, messages
