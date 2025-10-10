import time
import pytest
from utils.excel_reader import load_test_cases
from utils.keywords import KEYWORD_MAP
from utils.log_manager import LogManager


@pytest.mark.usefixtures("app_url")
def test_keyword_driven(page, app_url, test_case_id, logger):
    """
    Keyword-driven test executor.
    Dynamically runs all steps for a given TestCaseID.
    """
    all_steps = load_test_cases("test_suites/hiresense_keywords.xlsx")
    steps_to_run = [s for s in all_steps if str(s.get('TestCaseID') or s.get('TestCaseId')) == str(test_case_id)]

    if not steps_to_run:
        pytest.skip(f"No steps found for TestCaseID: {test_case_id}")

    LogManager.log_test_start(logger, test_case_id)

    start_time = time.time()
    page.goto(app_url)

    for step in steps_to_run:
        keyword = step.get("Keyword", "").strip()
        locator = step.get("Locator", "")
        input_data = step.get("InputData", "")
        step_no = step.get("StepNo", "")

        LogManager.log_step(logger, step_no, keyword, locator, input_data)

        func = KEYWORD_MAP.get(keyword)
        if not func:
            LogManager.log_step_result(logger, step_no, "FAIL", f"Keyword '{keyword}' not implemented")
            pytest.fail(f"Keyword '{keyword}' not implemented")

        try:
            func(page, locator, input_data)
            LogManager.log_step_result(logger, step_no, "PASS")
        except Exception as e:
            LogManager.log_exception(logger, e, context=f"Step {step_no} - {keyword}")
            LogManager.log_step_result(logger, step_no, "FAIL", str(e))
            pytest.fail(f"Step {step_no} failed - {e}")

    duration = time.time() - start_time
    LogManager.log_test_end(logger, test_case_id, status="PASS", duration=duration)
