# noinspection PyUnresolvedReferences
from .._core._c_uutils_base_time import _CTimeMonitor

__all__ = ['TimeMonitor']


class TimeMonitor:
    """
    Monitors time periods based on event counts.

    This class provides an efficient way to track events and rates over time,
    minimizing the number of system clock queries.
    """

    def __init__(self, period_in_seconds: float = 1.0):
        """
        Initialize the TimeMonitor.

        :param period_in_seconds: The period to monitor in seconds
        :type period_in_seconds: float
        """
        self._monitor = _CTimeMonitor(period_in_seconds)

    def get_events(self) -> int:
        """
        Get the number of events registered for the current period.

        :return: Number of events
        :rtype: int
        """
        return self._monitor.get_events()

    def event_rate(self) -> int:
        """
        Compute the number of events per second.

        :return: Event rate
        :rtype: int
        """
        return self._monitor.event_rate()

    def has_passed(self) -> bool:
        """
        Account for an event and check if the specified time period has passed.

        :return: True if the period has passed, False otherwise
        :rtype: bool
        """
        return self._monitor.has_passed()

    def next(self) -> None:
        """
        Prepare for the next period.
        """
        self._monitor.next()

    def reset(self) -> None:
        """
        Reset the monitor for another/unrelated performance measure.
        """
        self._monitor.reset()
