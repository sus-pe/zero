import logging

import __main__

logger = logging.getLogger(__name__)


def test_import_main() -> None:
    """
    Tests that imporing main is not broken.
    Do not remove this test otherwise coverage will not be 100%
    """
    logger.debug(__main__.__doc__)
