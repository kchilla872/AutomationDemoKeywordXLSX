# conftest.py
from pathlib import Path
import pytest
from utils.excel_reader import load_test_cases
from utils.log_manager import LogManager


def pytest_addoption(parser):
    """Add CLI options for execution control."""
    parser.addoption("--execute", action="store", default="N", help="Execute test cases based on flag (Y/N)")
    parser.addoption("--priority", action="store", default="All", help="Run test cases based on priority")


@pytest.fixture(scope="session")
def app_url():
    """Load application URL from file."""
    with open('configuration/resources/url.txt') as f:
        return f.read().strip()


@pytest.fixture(scope="session", autouse=True)
def logger():
    """Session-wide logger setup (works on local and Jenkins)."""
    LogManager.cleanup_old_logs()
    logger = LogManager.setup_logger(name="keyword_framework")
    logger.info("===== Test Session Started =====")
    return logger


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override browser context arguments if needed."""
    return {**browser_context_args}


def pytest_generate_tests(metafunc):
    """Dynamically parameterize tests from Excel based on Execute and Priority flags."""
    if "test_case_id" in metafunc.fixturenames:
        execute_flag = metafunc.config.getoption("--execute")
        priority = metafunc.config.getoption("--priority")

        test_data = load_test_cases("test_suites/hiresense_keywords.xlsx")

        if test_data:
            # Filter by Execute flag
            if execute_flag.upper() == "Y":
                test_data = [row for row in test_data if str(row.get("Execute", "")).strip().upper() == "Y"]

            # Filter by Priority
            if priority.lower() != "all":
                test_data = [row for row in test_data if str(row.get("Priority", "")).strip().lower() == priority.lower()]

            # Collect unique TestCase IDs
            unique_ids = sorted({
                row.get("TestCaseId") or row.get("TestCaseID")
                for row in test_data if row.get("TestCaseId") or row.get("TestCaseID")
            })

            if not unique_ids:
                pytest.exit(f"No test cases found matching Execute={execute_flag}, Priority={priority}")

            metafunc.parametrize("test_case_id", unique_ids)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to attach log file content to the HTML report.
    Works seamlessly in Jenkins and local HTML output.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    log_dir = Path("logs")
    if log_dir.exists():
        log_files = sorted(log_dir.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)
        if log_files:
            latest_log = log_files[0]
            try:
                log_content = latest_log.read_text(encoding="utf-8")
                if pytest_html:
                    extra.append(pytest_html.extras.text(log_content, name="Execution Log"))
            except Exception:
                pass
    report.extra = extra


@pytest.fixture(scope="session")
def execute_flag(request):
    """Return execute flag."""
    return request.config.getoption("--execute")


@pytest.fixture(scope="session")
def test_priority(request):
    """Return priority value."""
    return request.config.getoption("--priority")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """Log session completion."""
    logger = LogManager.get_logger("keyword_framework")
    logger.info("===== Test Session Completed =====")
    logger.info(f"Session exit status: {exitstatus}")
