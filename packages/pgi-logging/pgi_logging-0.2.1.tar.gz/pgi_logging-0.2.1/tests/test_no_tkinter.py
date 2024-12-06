"""Test the functionality of tkinter not being available."""

import sys
from unittest import mock

import pytest

from tests import logger

# Global variable to hold the test parameters
test_params = []

# TKINTER_EXISTS = None
try:
    import tkinter  # noqa

    SYSTEM_NO_TKINTER = False
    logger.info("System can load tkinter!")
except ImportError:
    SYSTEM_NO_TKINTER = True
    logger.error("System cannot load tkinter!")


# if the argparse option is passed to disable tkinter, then set the SYSTEM_NO_TKINTER flag to True
if "--tk-disable" in sys.argv:
    SYSTEM_NO_TKINTER = True


@pytest.mark.skipif(
    SYSTEM_NO_TKINTER, reason="System DOES NOT have tkinter available."
)
@pytest.mark.parametrize(
    "no_tkinter, skip_tkinter_check, mock_no_tkinter_import",
    [
        pytest.param(
            False,
            True,
            False,
            id="TKINTER_EXISTS=True, NO_TKINTER=False, SKIP_TKINTER_CHECK=True",
        ),
        pytest.param(
            None,
            False,
            False,
            id="TKINTER_EXISTS=True, NO_TKINTER=None, SKIP_TKINTER_CHECK=False",
        ),
        pytest.param(
            True,
            True,
            False,
            marks=[pytest.mark.xfail(exception=AssertionError)],
            id="TKINTER_EXISTS=True, NO_TKINTER=True, SKIP_TKINTER_CHECK=True",
        ),
        pytest.param(
            False,
            True,
            True,
            marks=[pytest.mark.xfail(exception=ImportError)],
            id="TKINTER_EXISTS=False, NO_TKINTER=False, SKIP_TKINTER_CHECK=True",
        ),
        pytest.param(
            None,
            False,
            True,
            marks=[pytest.mark.xfail(exception=ImportError)],
            id="TKINTER_EXISTS=False, NO_TKINTER=None, SKIP_TKINTER_CHECK=False",
        ),
        pytest.param(
            True,
            True,
            True,
            marks=[pytest.mark.xfail(exception=AssertionError)],
            id="TKINTER_EXISTS=False, NO_TKINTER=True, SKIP_TKINTER_CHECK=True",
        ),
    ],
)
def test_no_tkinter(
    no_tkinter: bool,
    skip_tkinter_check: bool,
    mock_no_tkinter_import: bool,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """Test the tkinter availability with the given flags."""
    # Mock the tkinter import if tkinter is not available
    with monkeypatch.context() as mp:
        if mock_no_tkinter_import:
            # logger.warning("Disabling tkinter module import for the test function.")
            # Force the tkinter module to be unavailable and set the environment variable to False
            mp.setitem(
                sys.modules,
                "tkinter",
                mock.Mock(side_effect=ImportError("No module named 'tkinter'")),
            )

        if no_tkinter:
            # logger.warning("Disabling tkinter successful import flag for the test function.")
            # Force the tkinter module to be unavailable and set the environment variable to False
            mp.setenv("TKINTER_EXISTS", "False")
        else:
            mp.setenv("TKINTER_EXISTS", "True")

        if skip_tkinter_check:
            # logger.warning("Skipping the tkinter check for the test function.")
            # Set the environment variable to True
            mp.setenv("SKIP_TKINTER_CHECK", "True")
        else:
            mp.setenv("SKIP_TKINTER_CHECK", "False")

        # Import the module to reload the flags
        from pgi_logging import pgi_handlers

        # Check if tkinter handler is available
        assert hasattr(pgi_handlers, "TkinterTextHandler")


if __name__ == "__main__":
    pytest.main()


"""
poetry run pytest tests/test_no_tkinter.py

poetry run pytest tests/test_no_tkinter.py --tk-disable
"""
