# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import argparse
import ast
import re
from multiprocessing import Pool

from cosmic_toolbox.logger import get_logger

LOGGER = get_logger(__file__)


def arg_str_to_dict(arg_str):
    """
    Converts a string in the format "{arg:value}" or "{arg1:value1,arg2:value2,...}"
    to a dictionary with keys and values.
    Note: strings should not contain ' or ".

    :param arg_str: A string in the format "{arg:value}" or
        "{arg1:value1, arg2:value2,...}".
    :return arg_dict: dictionary with keys and values corresponding to the input string.
    """
    arg_dict = {}
    # Use regular expression to extract argument pairs
    arg_pairs = re.findall(r"(\w+?):((\d+\.\d+)|(\d+)|([-\w.\[\],()]+))", arg_str)
    # Loop over argument pairs and add to dictionary
    for pair in arg_pairs:
        arg_name, arg_value = pair[0], pair[1]
        # If the value is a tuple, convert it to a tuple
        if "(" in arg_value and ")" in arg_value:
            arg_value = ast.literal_eval(arg_value)
        # If the value is a list, convert it to a list
        elif "[" in arg_value and "]" in arg_value:
            arg_value = ast.literal_eval(arg_value)
        else:
            # If the value is an integer, convert it to an integer
            try:
                arg_value = int(arg_value)
            # If the value is a float, convert it to a float
            except ValueError:
                try:
                    arg_value = float(arg_value)
                except ValueError:
                    # If the value is a string, strip the quotes
                    arg_value = arg_value.strip("'\"")
        arg_dict[arg_name] = arg_value
    return arg_dict


def parse_sequence(s):
    """
    Parses a string to a list/tuple for argparse. Can be used as type for argparse.

    :param s: String to parse.
    :return: tuple or list.
    :raises argparse.ArgumentTypeError: If the string cannot be parsed to a tuple.
    """
    try:
        # Using ast.literal_eval to safely evaluate the string as a Python literal
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        raise argparse.ArgumentTypeError(f"Invalid list value: {s}")


def parse_list(s):
    """
    Parses a string to a list for argparse. Can be used as type for argparse.

    :param s: String to parse.
    :return: list.
    """
    return list(parse_sequence(s))


def is_between(x, min, max):
    """
    Checks if x is between min and max.

    :param x: Value to check.
    :param min: Minimum value.
    :param max: Maximum value.
    :return: True if x is between min and max, False otherwise.
    """

    return (x > min) & (x < max)


def run_imap_multiprocessing(func, argument_list, num_processes, verb=True):
    """
    Runs a function with a list of arguments in parallel using multiprocessing.

    :param func: Function to run.
    :param argument_list: List of arguments to run the function with.
    :param num_processes: Number of processes to use.
    :param verb: If True, show progress bar.
    :return: List of results from the function.
    """

    pool = Pool(processes=num_processes)

    result_list = []
    if verb:
        for result in LOGGER.progressbar(
            pool.imap(func=func, iterable=argument_list),
            total=len(argument_list),
            at_level="info",
        ):
            result_list.append(result)
    else:
        for result in pool.imap(func=func, iterable=argument_list):
            result_list.append(result)

    return result_list
