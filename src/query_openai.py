from openai import OpenAI
from query_type import QueryType

import os
import constants as cts


def qt_to_filepath(qt: QueryType) -> str:
    folder = "./prompts/"
    filename = ""
    if qt == QueryType.MAIN:
        filename += cts.ANSWER_PROMPT_NAME
    elif qt == QueryType.IN_SCOPE:
        filename += cts.SCOPE_PROMPT_NAME
    elif qt == QueryType.IS_SEARCHABLE:
        filename += cts.SEARCHABILITY_NAME
    elif qt == QueryType.SEARCHABLE_TEXT:
        filename += cts.SEARCHABLE_TEXT_NAME

    rv = folder + filename
    if not os.path.exists(rv):
        raise FileNotFoundError("No file with name" + rv + "can be found")

    return rv


async def run_query(query_text: str, qt: QueryType, message_history=[]) -> str:
    prompt_filename = qt_to_filepath(qt=qt)
    with open(prompt_filename, "r") as prompt_file:
        prompt = prompt_file.read()

    prompt += query_text

    client = OpenAI()
    message_list = [{"role": "user", "content": prompt}]
    if len(message_history) > 0:
        messages_except_last = message_history[:-1]
        message_list = messages_except_last + message_list
        print("The Message List: ", message_list)
    completion = client.chat.completions.create(
        model=cts.GPT_MODEL, messages=message_list
    )

    return completion.choices[0].message
