from sanic import Sanic
from sanic.response import json
from sanic.response import text
from sanic_cors import CORS, cross_origin

from prompt import Prompt
from query_type import QueryType
from query_openai import run_query


import selenium_util as sel_util
import constants as cts

import os
import time

app = Sanic(__name__)
CORS(app)


@app.route("/", methods=["GET"])
async def home(request):
    return text("Hello World!")


@app.route("/chat", methods=["POST"])
async def chat(request):
    """
    request: the request body of the POST request
    request['message']: the message the user is attempting to send the chatbot

    returns: The chatbot's reply, which the frontend can then parse
    """
    request_json = request.json
    user_message = request_json["message"]
    print("User Message: ", user_message)

    # Build Prompt object
    cur_prompt = Prompt(
        prompt_text=user_message,
        is_searchable=False,
        searchable_text="",
        is_user_prompt=True,
        in_scope=False,
        contains_context=False,
    )

    # Prompt in scope
    in_scope = await run_query(query_text=user_message, qt=QueryType.IN_SCOPE)
    print("IN SCOPE: ", in_scope)
    if in_scope.content == "TRUE":
        cur_prompt.in_scope = True

    # Prompt has searchable text
    has_searchable_text = await run_query(
        query_text=user_message, qt=QueryType.IS_SEARCHABLE
    )
    if has_searchable_text.content == "TRUE":
        cur_prompt.is_searchable = True

    # Task 2: Isolate searchable text
    is_searchable = cur_prompt.is_searchable
    search_queries = []
    if is_searchable:
        print("Generating search queries")
        searchable_text = await run_query(
            query_text=user_message, qt=QueryType.SEARCHABLE_TEXT
        )
        print("Generated Search queries: ", searchable_text)
        searchable_text = searchable_text.content
        cur_prompt.searchable_text = searchable_text
        queries = searchable_text.split(",")
        search_queries = [q.replace('"', "") for q in queries]

    if not cur_prompt.in_scope:
        return json({"result": "Your question is out of scope. Please try again"})
    # Task 3: Run search and retrieve context information (Selenium)
    print("Creating Driver...")
    driver = sel_util.get_driver()
    print("Driver Created")
    sel_util.navigate_to_url(driver=driver, url=cts.PART_SELECT_URL)
    print("Navigated to URL")
    search_results = []
    for query in search_queries:
        print("Searching for term: ", query)
        sel_util.perform_search(driver=driver, search_term=query)
        page_type = sel_util.determine_page_type(driver=driver)
        if page_type == sel_util.PageType.PRODUCT:
            res_txt = sel_util.extract_data_from_product_page(driver=driver)
            search_results.append(res_txt)
            continue

        # Page type is RESULTS
        urls_to_query = sel_util.extract_links_from_results(driver=driver)
        for url in urls_to_query:
            res_txt = sel_util.extract_data_from_product_page(driver=driver, url=url)
            search_results.append(res_txt)
            time.sleep(3)
    driver.quit()

    # Task 4: Integrate into context prompt
    answer_prompt_text = ""
    for res in search_results:
        answer_prompt_text += res
        answer_prompt_text += "\n\n"

    answer_prompt_text += "\n ** USER QUERY BELOW ** "
    answer_prompt_text += user_message

    print("Querying for answer")
    chat_response = await run_query(query_text=answer_prompt_text, qt=QueryType.MAIN)
    result = chat_response.content
    print("Final Result: ", result)

    return json({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), auto_reload=True)
