"""
This module describes how we handle manual cost tracking in Sieve.
"""
bill_handler = None
internal_bill_handler = None


def get_bill_handler():
    global bill_handler
    if bill_handler is None:
        bill_handler = CostHandler()
    return bill_handler


def get_internal_bill_handler():
    global internal_bill_handler
    if internal_bill_handler is None:
        internal_bill_handler = CostHandler()
    return internal_bill_handler


import threading


class CostHandler:
    """
    This class handles billing interaction for approved organizations in Sieve.

    It is responsible for tracking and updating the cost of a prediction as manually tracked
    by the function owner. It is useful for approved organizations to manually bill users
    at predict time.
    """

    def __init__(self):
        self._current_cost_dollars = 0
        self._lock = threading.Lock()

    def get_dollars(self):
        with self._lock:
            return self._current_cost_dollars

    def set_dollars(self, cost_dollars):
        with self._lock:
            self._current_cost_dollars = cost_dollars

    def add_dollars(self, cost_dollars):
        with self._lock:
            self._current_cost_dollars += cost_dollars

    def reset(self):
        with self._lock:
            current_cost_dollars = self._current_cost_dollars
            self._current_cost_dollars = 0
            return current_cost_dollars


def bill(cost_dollars):
    """
    This function is used to manually bill a user for a prediction.

    :param cost_dollars: The cost in dollars to bill the user
    :type cost_dollars: float
    """
    get_bill_handler().add_dollars(cost_dollars)


def view_bill():
    """
    This function is used to view the current cost of a prediction.

    :return: The current cost in dollars
    :rtype: float
    """
    return get_bill_handler().get_dollars()


def internal_bill(cost_dollars):
    """
    This function is used to track the at-cost spend for LLMs, APIs, etc..

    :param cost_dollars: The cost in dollars to track
    :type cost_dollars: float
    """
    get_internal_bill_handler().add_dollars(cost_dollars)


def view_internal_bill():
    """
    This function is used to view the current cost of a prediction.

    :return: The current internal cost in dollars
    :rtype: float
    """
    return get_internal_bill_handler().get_dollars()
