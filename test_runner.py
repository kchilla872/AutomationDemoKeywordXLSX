import pytest
from utils.excel_reader import load_test_cases
from utils.keywords import KEYWORD_MAP


@pytest.mark.usefixtures("app_url")
def test_keyword_driven(page, app_url, test_case_id):
    steps = load_test_cases("test_suites/hiresense_keywords.xlsx")
    steps_to_run = [step for step in steps if step['TestCaseID'] == test_case_id]

    # Navigate to base URL first
    page.goto(app_url)

    for step in steps_to_run:
        key = step['Keyword'].strip()  # Strip spaces here
        func = KEYWORD_MAP.get(key)
        if not func:
            pytest.fail(f"Keyword '{step['Keyword']}' not implemented")
        func(page, step['Locator'], step['InputData'])

