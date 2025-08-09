import logging

import zero

logger = logging.getLogger(__name__)


def test_sanity() -> None:
    logger.info(zero)
