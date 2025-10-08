# conftest.py
from pathlib import Path
import pytest
from utils.excel_reader import load_test_cases
from utils.screenshot import save_page_screenshot


def pytest_addoption(parser):
    parser.addoption("--execute", action="store", default="N", help="Execute test cases based on flag (Y/N)")
    parser.addoption("--priority", action="store", default="All", help="Run test cases based on priority")


@pytest.fixture(scope="session")
def app_url():
    with open('configuration/resources/url.txt') as f:
        return f.read().strip()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override browser context arguments."""
    return {
        **browser_context_args,
    }


def pytest_generate_tests(metafunc):
    if "test_case_id" in metafunc.fixturenames:
        # Get command line options
        execute_flag = metafunc.config.getoption("--execute")
        priority = metafunc.config.getoption("--priority")

        # Load test data
        test_data = load_test_cases("test_suites/hiresense_keywords.xlsx")

        if test_data:
            print(f"\n[DEBUG] Sample row keys: {test_data[0].keys()}")
            print(f"[DEBUG] Sample row: {test_data[0]}")
            print(f"[DEBUG] Total rows loaded: {len(test_data)}")
            print(f"[DEBUG] Execute flag requested: '{execute_flag}'")
            print(f"[DEBUG] Priority requested: '{priority}'")

            # Filter based on Execute flag
            if execute_flag.upper() == "Y":
                filtered = []
                for step in test_data:
                    exec_val = step.get("Execute", "")
                    # Handle None values
                    if exec_val is None:
                        exec_val = ""
                    exec_val = str(exec_val).strip().upper()
                    if exec_val == "Y":
                        filtered.append(step)
                test_data = filtered
                print(f"[DEBUG] After Execute filter: {len(test_data)} rows")

            # Filter based on Priority
            if priority.lower() != "all":
                filtered = []
                for step in test_data:
                    pri_val = step.get("Priority", "")
                    # Handle None values
                    if pri_val is None:
                        pri_val = ""
                    pri_val = str(pri_val).strip().lower()
                    if pri_val == priority.lower():
                        filtered.append(step)
                test_data = filtered
                print(f"[DEBUG] After Priority filter: {len(test_data)} rows")

            # Get unique test case IDs (check both possible column names)
            unique_ids = sorted({
                step.get("TestCaseId") or step.get("TestCaseID")
                for step in test_data
                if step.get("TestCaseId") is not None or step.get("TestCaseID") is not None
            })

            print(f"[DEBUG] Unique Test Case IDs: {unique_ids}")

            if not unique_ids:
                print(f"\n[ERROR] No test cases found matching Execute={execute_flag}, Priority={priority}")
                pytest.exit(f"No test cases found matching Execute={execute_flag}, Priority={priority}")

            metafunc.parametrize("test_case_id", unique_ids)


def slugify(value):
    """
    Converts value to a string safe for filenames:
    - Replaces non-alphanumeric characters with underscores
    - Leaves hyphens and underscores
    """
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in str(value))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook: Called for each test run phase; attaches screenshot in HTML report.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    # Attach screenshot after call phase (after test execution)
    if report.when == 'call':
        page = item.funcargs.get("page")
        if page:
            # Slugify nodeid for safe screenshot file
            screen_file = f"screenshots/{slugify(item.nodeid)}.png"
            Path("screenshots").mkdir(exist_ok=True)
            page.screenshot(path=screen_file, full_page=True)
            # Attach to HTML report if plugin available
            if pytest_html:
                extra.append(pytest_html.extras.png(screen_file))
        report.extra = extra


@pytest.fixture(scope="session")
def execute_flag(request):
    return request.config.getoption("--execute")


@pytest.fixture(scope="session")
def test_priority(request):
    return request.config.getoption("--priority")