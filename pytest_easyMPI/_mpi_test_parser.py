import inspect
import os
import re


def strip_colour_codes(string):
    pattern = re.compile(r'\x1B\[\d+(;\d+){0,2}m')
    return pattern.sub('', string)


def get_pytest_input(func):
    """
    Convert function object to pytest input string.

    Pytest allows the user to pass the name of an individual
    test to run. This function takes a function object and converts
    it into a string that can be passed to pytest to run only that
    specific test function.

    Arguments
    ---------
    func : function
        The test function object for which to generate a string input

    Returns
    -------
    str
        Input string for pytest to run the given test function

    """
    module = inspect.getfile(func)
    module = os.path.relpath(module)

    func = "::".join(func.__qualname__.split("."))

    return f"{module}::{func}"


def temp_ouput_file(pytest_input):
    """
    Return the name of the temporary output file for a given test.

    Arguments
    ---------
    pytest_input : str
        The pytest input indicating for which test function to obtain
        the temporary output file name

    Returns
    -------
    str
        The temporary output file name for the given test function

    """
    return pytest_input.replace("/", ".").replace("::", ".")


def contains_failure(message):
    """
    Check if a given pytest contained a failure.

    Arguments
    ---------
    message : str
        The pytest output to check

    Returns
    -------
    bool
        True if the output contains failures; False otherwise

    """
    return "= FAILURES =" in message


def get_traceback(message):
    """
    Extract traceback from pytest output

    Parameters
    ----------
    message : str
        The pytest output

    Returns
    -------
    str
        The traceback found in the given pytest output

    Raises
    ------
    ValueError
        If message does not contain a traceback
    """
    try:
        index = message.index("= FAILURES ")
    except ValueError:
        raise ValueError("Given message does not contain a traceback")

    for _ in range(3):
        index = message.index("\n", index + 1)

    end_index = message.rindex("short test summary info")
    end_index = message.rindex("\n", 0, end_index)

    return message[index:end_index]


def get_summary(message):
    """
    Return summary statement from pytest output

    Parameters
    ----------
    message : message
        The pytest output

    Returns
    -------
    str
        The summary statement
    """
    groups = re.search(
        r"=* short test summary info =*\nFAILED .*?::.*? - (.*)", strip_colour_codes(message)
    ).groups()

    return groups[0]


END_OF_TEST = "%<<<<END_OF_TEST>>>>%"
"""
Placeholder at the end of an mpi output file.

Can be used to check if the entire test suite ran through.
"""
