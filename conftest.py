# conftest.py
from pathlib import Path
import pytest
from utils.excel_reader import load_test_cases
from utils.screenshot import save_page_screenshot


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
        test_data = load_test_cases("test_suites/hiresense_keywords.xlsx")
        unique_ids = sorted({step['TestCaseID'] for step in test_data if step['TestCaseID'] is not None})
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