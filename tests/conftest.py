import pytest
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,
        "slow_mo": 500
    }


@pytest.fixture(scope="session")
def report_dir():
    """Create and return reports directory"""
    report_path = Path("reports")
    report_path.mkdir(exist_ok=True)
    return report_path


def pytest_configure(config):
    """Configure pytest and initialize result file"""
    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Create/clear result.txt file
    result_file = reports_dir / "result.txt"
    with open(result_file, "w") as f:
        f.write(f"Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        item.rep_call = rep


@pytest.fixture(scope="function", autouse=True)
def write_test_result(request, report_dir):
    """Automatically write test result to result.txt"""
    yield
    
    # Get test result
    test_name = request.node.name
    if hasattr(request.node, 'rep_call'):
        outcome = "PASSED" if request.node.rep_call.passed else "FAILED"
    else:
        outcome = "UNKNOWN"
    
    # Write to result.txt
    result_file = report_dir / "result.txt"
    with open(result_file, "a") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {test_name} ... {outcome}\n")


@pytest.fixture(scope="session", autouse=True)
def finalize_results(request, report_dir):
    """Finalize test results at end of session"""
    yield
    
    result_file = report_dir / "result.txt"
    if result_file.exists():
        with open(result_file, "a") as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Tests finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
