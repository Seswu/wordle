"""
Test module.

All *test* functions are executed automatically by pytest.
Any @pytest.fixture functions, when named as parameter, brings in the result
of the fixture function as parameter for the given test function.
"""
# pylint: disable=redefined-outer-name, no-name-in-module
#         ref-out-name:
#         Pytest does some automatic decoration for ease of use;
#         presumably this is what pylint catches on to and complains
#         about.
#         no-name-in:
#         Pylint is unable to locate perfectly normal members of perfectly
#         normal modules. Explanations for this remain elusive.

# Standard libraries
import faulthandler
import logging
import pytest

LOG = logging.getLogger("__name__")

# Internal code


@pytest.fixture(scope="function")
def setup():
    """
    Populates stack with initial data for later testing.
    """
    faulthandler.enable(open("core.dump", 'w'))
    testdata = "Something complicated"
    return testdata


def test_unit_one(setup):
    """
    Test One.
    """
    testdata = setup
    assert str(testdata)
    LOG.debug(testdata)
    LOG.info("Test One run")
