"""Configuration file for pytest."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def pytest_addoption(parser: "argparse.ArgumentParser") -> None:
    """Add a command line option to disable tkinter for the test function."""
    parser.addoption(
        "--tk-disable",
        action="store_true",
        help="Disable tkinter for the test function.",
    )
