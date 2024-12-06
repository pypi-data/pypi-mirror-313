import logging

from fiddler.utils.logger import _attach_handler, set_logging


def test_attach_handler() -> None:
    """
    Assume: other parts of this test suite do not call set_logging() /
    _attach_handler() before that.
    """
    flog = logging.getLogger('fiddler')

    # You can see this next message emitted when invoking pytest with
    #
    #   pytest -vv -s --log-cli-level=INFO -k test_logger
    #
    # because then this message reaches the pytest-configured root logger and
    # gets emitted to stderr.
    flog.info('msg expected to propagate to the root logger')

    # Confirm that the 'fiddler' logger does not have emission handlers
    # attached itself, and that is configured to propagate messages up the
    # hierarchy (towards the root logger).
    assert len(flog.handlers) == 0
    assert flog.propagate

    # Call that legacy method: it emits a warning and calls _attach_handler()
    # under the hood. It is expected to indeed not skip the setup, as can be
    # checked by the returned boolean.
    attached = set_logging()
    assert attached

    # This next message can be seen by running
    #
    #  pytest -s -k test_logger
    #
    # because it bypasses the root logger installed by pytest. The
    # now-installed handler attached to the 'fiddler' logger emits to stderr
    # directly, and because of the `-s` any stderr emitted during test
    # execution goes straight to the terminal.
    flog.info('msg expected to not propagate to root (but emitted by stream handler)')
    flog.warning('testmsg')
    flog.error('testmsg')
    flog.critical('testmsg')

    # Confirm that the 'fiddler' logger is now not configured anymore to bubble
    # up log msgs.
    assert not flog.propagate

    # Confirm that a second execution does not attach another handler.
    attached = _attach_handler()
    assert not attached

    # This should not be set in stone. It's not all too common for a library to
    # attach a handler to a logger (is typically left to the calling program).
    assert len(flog.handlers) == 1

    # Cleanup (make subsequent tests have log msgs emitted by this library flow
    # into the root logger).
    flog.propagate = True
    flog.handlers = []
