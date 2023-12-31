# will contain any extra function that checks query validity and trigger validity
import re


def format_history(previous_messages):
    formatted_history = []
    formatted_history.append({"role": "user", "parts": previous_messages[0]})
    formatted_history.append({"role": "model", "parts": previous_messages[1]})
    return formatted_history


async def fetch_message(message):
    result = await message.channel.fetch_message(message.reference.resolved.reference.message_id)
    return result


def clean_message(text):
    search_results = re.search(r"\<\@\d+\>", text)
    if search_results:
        cleaned_text = text[search_results.end():]
        return cleaned_text
    else:
        return text
