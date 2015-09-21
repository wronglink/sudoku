import pytest


def pytest_addoption(parser):
    parser.addoption("--runbenchmark", action="store_true",
        help="run runbenchmarking tests")


def pytest_runtest_setup(item):
    if 'benchmark' in item.keywords and not item.config.getoption("--runbenchmark"):
        pytest.skip("need --runbenchmark option to run")
