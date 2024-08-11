import unittest
from query_openai import run_query
from query_type import QueryType
from selenium_util import PageType
from selenium_util import (
    get_driver,
    navigate_to_url,
    perform_search,
    determine_page_type,
    extract_data_from_product_page,
    extract_links_from_results,
)
from config import get_config_env
import os


class TestRunQuery(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["OPENAI_API_KEY"] = get_config_env()['OPENAI_API_KEY']
    
    async def test_run_query_returns_true_scope(self):
        result = await run_query(
            "Are PartSelect dishwashers worth the money?", QueryType.IN_SCOPE
        )
        result_content = result.content
        self.assertEqual(result_content, "TRUE")

    async def test_run_query_returns_true_scope_two(self):
        result = await run_query(
            "Does the D678HY part work with most PartSelect dishwashers",
            QueryType.IN_SCOPE,
        )
        result_content = result.content
        self.assertEqual(result_content, "TRUE")

    async def test_run_query_returns_false_scope(self):
        result = await run_query(
            "What is the time complexity of quicksort?", QueryType.IN_SCOPE
        )
        result_content = result.content
        self.assertEqual(result_content, "FALSE")

    async def test_run_query_return_true_searchable(self):
        result = await run_query(
            "Is the P67YH65 part compatible with the R874 refrigerator?",
            QueryType.IN_SCOPE,
        )
        result_content = result.content
        self.assertEqual(result_content, "TRUE")

    async def test_run_query_return_false_searchable(self):
        result = await run_query(
            "Does PartSelect generally have good dishwashers?", QueryType.IS_SEARCHABLE
        )
        result_content = result.content
        self.assertEqual(result_content, "FALSE")

    async def test_run_query_return_false_searchable_two(self):
        result = await run_query(
            "Should I buy things from PartSelect?", QueryType.IS_SEARCHABLE
        )
        result_content = result.content
        self.assertEqual(result_content, "FALSE")

    async def test_run_query_return_true_searchable_identify_models(self):
        result = await run_query(
            "What are some large fridges from PartSelect that I can buy?",
            QueryType.IS_SEARCHABLE,
        )
        result_content = result.content
        self.assertEqual(result_content, "TRUE")

    async def test_run_query_return_true_searchable_identify_models_two(self):
        result = await run_query(
            "What is the best fridge and the best dishwasher from part select?",
            QueryType.IS_SEARCHABLE,
        )
        result_content = result.content
        self.assertEqual(result_content, "TRUE")

    async def test_get_search_queries(self):
        result = await run_query(
            "Which part is more expensive: P786HG or P897YT?", QueryType.SEARCHABLE_TEXT
        )
        result_content = result.content
        query_lst = result_content.split(",")
        self.assertEqual(['"P786HG"', '"P897YT"'], query_lst)

    async def test_get_search_queries(self):
        result = await run_query(
            "What is the best fridge on partselect?", QueryType.SEARCHABLE_TEXT
        )
        result_content = result.content
        query_lst = result_content.split(",")
        self.assertEqual(['"best fridge"'], query_lst)

    async def test_get_driver(self):
        driver = get_driver()
        driver.quit()

    async def test_navigate_to_main_page(self):
        driver = get_driver()
        success = navigate_to_url(driver=driver)
        driver.quit()
        self.assertEqual(success, True)

    async def test_perform_search_part_number(self, part_number="PS346995"):
        driver = get_driver()
        navigate_to_url(driver=driver)
        success = perform_search(driver=driver, search_term=part_number)
        driver.quit()
        self.assertEqual(success, True)

    async def test_perform_search_general_query(self, search_query="fridge parts"):
        driver = get_driver()
        navigate_to_url(driver=driver)
        success = perform_search(driver=driver, search_term=search_query)
        driver.quit()
        self.assertEqual(success, True)

    async def test_page_type_results(self):
        driver = get_driver()
        navigate_to_url(driver=driver)
        search_term = "fridge parts"
        perform_search(driver=driver, search_term=search_term)
        page_type = determine_page_type(driver=driver)
        self.assertEqual(page_type, PageType.RESULTS)
        driver.quit()

    async def test_page_type_product(self):
        driver = get_driver()
        navigate_to_url(driver=driver)
        search_term = "PS346995"
        perform_search(driver=driver, search_term=search_term)
        page_type = determine_page_type(driver=driver)
        self.assertEqual(page_type, PageType.PRODUCT)
        driver.quit()

    async def test_extract_links(self):
        driver = get_driver()
        navigate_to_url(driver=driver)
        search_term = "fridge parts"
        perform_search(driver=driver, search_term=search_term)
        urls = extract_links_from_results(driver=driver)
        EXPECTED = [
            "https://www.partselect.com/PS12364199-Frigidaire-242126602-Refrigerator-Door-Shelf-Bin.htm?SourceCode=18",
            "https://www.partselect.com/PS11701542-Whirlpool-EDR1RXD1-Refrigerator-Ice-and-Water-Filter.htm?SourceCode=18",
            "https://www.partselect.com/PS11752778-Whirlpool-WPW10321304-Refrigerator-Door-Shelf-Bin.htm?SourceCode=18",
        ]

        self.assertEqual(urls, EXPECTED)
        driver.quit()

    async def test_extract_data(self):
        driver = get_driver()
        test_url = "https://www.partselect.com/PS12364199-Frigidaire-242126602-Refrigerator-Door-Shelf-Bin.htm?SourceCode=18"
        result_text = extract_data_from_product_page(driver=driver, url=test_url)
        expected_first_part = "Refrigerator Door Shelf Bin 242126602"
        split_by_line = result_text.split("\n")
        self.assertEqual(expected_first_part, split_by_line[1])
        driver.quit()


if __name__ == "__main__":
    unittest.main()
