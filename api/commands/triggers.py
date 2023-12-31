from src.pymon_assistant.tasks.chat import chat
from api.utils import (
    format_history, 
    fetch_message, 
    clean_message,
)

QUESTION_STARTER = "tell me pymon, "


def get_llm_response(message, history=[]):
    # placeholder for the LLM response
    response, updated_history = chat(message, history=history)
    return response


def qna_trigger(message):
    """
    boolean method that checks if the message is a question to Pymon

    Parameters
    ----------
    message : str
        the message that triggered the action

    Returns
    -------
    bool:
        True if the message is a question to Pymon, False otherwise
    """
    if message.content.startswith(QUESTION_STARTER):
        return True


def qna_action(message, client=None, history=[]):
    """
    is triggered when the LLM is needed to reply to a question

    Parameters
    ----------
    message : str
        the message from the user on discord

    Returns
    -------
    str:
        Pymon LLM response through discord API
    """
    query = message.content.replace(QUESTION_STARTER, '')
    if client:
        query = message.content.replace(client.user.mention, '')

    # get the LLM response
    response = get_llm_response(query, history=history)
    return response


def mention_trigger(client, message):
    if client.user.mentioned_in(message):
        return True
    else:
        return False


async def reply_trigger(message, client):
    # if message is a reply to client user id, then return true
    if message.reference and message.reference.resolved.author.id == client.user.id:
        pymon_message = message.reference.resolved.content
        user_message = await fetch_message(message)
        user_message = clean_message(user_message.content)

        history = format_history([user_message, pymon_message])
        return True, history
    else:
        return False
