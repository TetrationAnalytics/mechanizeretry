import signal


class TimeoutException(Exception):
    pass


class Timeout(object):
    """Timeout class using ALARM signal

    This can be used as a context manager to raise an ALARM signal at a
    specified time in the future, that alarm is then used to raise a
    TimeoutException

    """
    def __init__(self, sec):
        self.sec = int(sec)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)  # disable alarm

    def raise_timeout(self, *args):
        raise TimeoutException()