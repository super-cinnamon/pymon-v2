QUESTION_STARTER = "tell me pymon, "


def get_llm_response(message, history=[]):
    # placeholder for the LLM response
    response = f'your question was: {message}, I will be able to answer very soon.'
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


def qna_action(message, client=None):
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
    response = get_llm_response(query)
    return response


def mention_trigger(client, message):
    if client.user.mentioned_in(message):
        return True
    else:
        return False
