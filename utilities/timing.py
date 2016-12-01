"""
Context Manager used with the statement 'with' to time some execution.

Example:
    with TimingManager() as t:
       # code to time
       process(its_complicated)
       # print measured time, e.g.:
       logger.info('Elapsed time {}'.format(time.end_log()))

TODO:
- improve docstring

Based on: http://stackoverflow.com/a/28218696
"""
import datetime as dt
import timeit


class TimingManager(object):
    """TimingManager class"""

    start = 0
    clock = timeit.default_timer

    def __enter__(self):
        self.start = self.clock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_log()
        return False

    def log(self, sec, elapsed=None):
        """Log current time and elapsed time if present.
        :param sec: Text to display, use '{}' to format the text with
            the current time.
        :param elapsed: Elapsed time to display. Default: None, no display.
        """
        print(sec.format(self._seconds_to_str(self.clock())))
        if elapsed is not None:
            print('Elapsed time: {}\n'.format(elapsed))

    def end_log(self):
        """Log time for the end of execution with elapsed time.
        """
        return self.now()

    def now(self):
        """Return current elapsed time as hh:mm:ss string.
        :return: String.
        """
        return str(dt.timedelta(seconds=self.clock() - self.start))

    @classmethod
    def _seconds_to_str(cls, sec):
        """Convert timestamp to h:mm:ss string.
        :param sec: Timestamp.
        """
        return str(dt.datetime.fromtimestamp(sec))
