from httplib import BadStatusLine
import logging
import mechanize
import socket
import time
from urllib2 import HTTPError, URLError

from timeout import Timeout, TimeoutException

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
    logging.NullHandler = NullHandler


logger = logging.getLogger("mechanizeretry")
logger.addHandler(logging.NullHandler())


class RetryBrowser(mechanize.Browser):
    """ A sublcass of the mechanize.Browser class that adds retries if an
        HTTPError, URLError or BadStatusLine occurs to the following methods:

        * open
        * submit

        If the methods are called without retries specified, they default to
        the standard mechanize.Browser methods.  If retries are specified,
        the method standard calls are wrapped in a loop
    """
    def __init__(self, global_timeout=None, **kwargs):
        """

        :param global_timeout: int, defaults to 300 if not set.
        :param kwargs:
        """
        self._global_timeout = global_timeout if global_timeout is not None else 300
        mechanize._sockettimeout._GLOBAL_DEFAULT_TIMEOUT = self.global_timeout
        mechanize.Browser.__init__(self, **kwargs)

    @property
    def global_timeout(self):
        return self._global_timeout

    def _open(self, url, data=None, headers=None,
              timeout=None):
        timeout = self.global_timeout if timeout is None else timeout
        # mechanize calls open internally with request objects, just pass them through if this is
        # the case.
        if isinstance(url, mechanize.Request):
            request = url
        else:
            headers = dict() if headers is None else headers
            request = mechanize.Request(url, data=data, headers=headers, timeout=timeout)
        with Timeout(timeout):
            return mechanize.Browser.open(self, request)

    def open(self, url, data=None, headers=None, retries=None, delay=None, backoff=None,
             timeout=None):
        timeout = self.global_timeout if timeout is None else timeout
        # Reset to sane values if needed.
        retries = 1 if retries is None or retries == 0 else retries
        delay = 0 if delay is None else delay
        backoff = 1 if backoff is None or backoff == 0 else backoff
        # Retry with sleep on certain errors
        for atry in range(1, retries + 1):
            try:
                return self._open(url, data=data, headers=headers, timeout=timeout)
            except (HTTPError, URLError, BadStatusLine, socket.timeout, socket.error), e:
                logger.error("Open of '{0}' failed - Error: {1}".format(url, e))
                try:
                    logger.error("Response:\n{0}".format(e.read()))
                except AttributeError:
                    pass
                if atry == retries:
                    raise
            except TimeoutException:
                logger.error("Open request to {0} timed out".format(url))
                if atry == retries:
                    raise TimeoutException("Open request to {0} timed out".format(url))
            delay = delay * backoff
            if backoff != 1:
                logger.info("Backed delay off by a factor of {0} to {1}".format(backoff, delay))
            time.sleep(delay)

    def _submit(self, timeout=None, *args, **kwargs):
        timeout = self.global_timeout if timeout is None else timeout
        with Timeout(timeout):
            return mechanize.Browser.submit(self, *args, **kwargs)

    def submit(self, retries=None, delay=None, backoff=None, timeout=None, *args, **kwargs):
        timeout = self.global_timeout if timeout is None else timeout
        # Reset for sane values
        retries = 1 if retries is None or retries == 0 else retries
        delay = 0 if delay is None else delay
        backoff = 1 if backoff is None or backoff == 0 else backoff
        # Retry with sleep on HTTPError, URLError and BadStatusLine
        for atry in range(1, retries + 1):
            try:
                return self._submit(timeout=timeout, *args, **kwargs)
            except (HTTPError, URLError, BadStatusLine), e:
                logger.error("Submit failed - Error: {0}".format(e))
                try:
                    logger.error("Response:\n{0}".format(e.read()))
                except AttributeError:
                    pass
                if atry == retries:
                    raise
            except TimeoutException:
                logger.error("Submit request timed out")
                if atry == retries:
                    raise TimeoutException("Submit request timed out")
            delay = delay * backoff
            if backoff != 1:
                logger.info("Backed delay off by a factor of {0} to {1}".format(backoff, delay))
            time.sleep(delay)

    def _select_form(self, timeout=None, *args, **kwargs):
        timeout = self.global_timeout if timeout is None else timeout
        with Timeout(timeout):
            return mechanize.Browser.select_form(self, *args, **kwargs)

    def select_form(self, retries=None, delay=None, backoff=None, timeout=None, *args, **kwargs):
        timeout = self.global_timeout if timeout is None else timeout
        # Reset for sane values
        retries = 1 if retries is None or retries == 0 else retries
        delay = 0 if delay is None else delay
        backoff = 1 if backoff is None or backoff == 0 else backoff
        for atry in range(1, retries + 1):
            try:
                return self._select_form(timeout, *args, **kwargs)
            except TimeoutException:
                logger.error("select_form request timed out")
                if atry == retries:
                    raise TimeoutException("select_form request timed out")
            delay = delay * backoff
            if backoff != 1:
                logger.info("Backed delay off by a factor of {0} to {1}".format(backoff, delay))
            time.sleep(delay)
