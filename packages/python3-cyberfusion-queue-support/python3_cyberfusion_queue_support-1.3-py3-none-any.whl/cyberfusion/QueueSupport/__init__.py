"""Classes for queue."""

import logging
from typing import List

from cyberfusion.QueueSupport.exceptions import QueueFulfillFailed
from cyberfusion.QueueSupport.interfaces import OutcomeInterface
from cyberfusion.QueueSupport.items import _Item

logger = logging.getLogger(__name__)


class Queue:
    """Represents queue."""

    def __init__(self) -> None:
        """Set attributes."""
        self.items: List[_Item] = []

    def add(self, item: _Item, *, move_duplicate_last: bool = True) -> None:
        """Add item to queue."""
        if item not in self.items:
            self.items.append(item)

            logger.info("Added item to queue (reference: '%s')", item.reference)
        else:
            # If item already in queue, move to last place

            if move_duplicate_last:
                self.items.append(self.items.pop(self.items.index(item)))

                logger.info(
                    "Added item to queue (reference: '%s') (moving duplicate last)",
                    item.reference,
                )
            else:
                logger.info(
                    "Didn't add item to queue (reference: '%s') (already present)",
                    item.reference,
                )

    def process(self, preview: bool) -> List[OutcomeInterface]:
        """Process items."""
        logger.info("Processing items")

        results = []

        for item in self.items:
            logger.info("Processing item '%s'", item.reference)

            if not item.hide_outcomes:
                results.extend(item.outcomes)

            if not preview:
                try:
                    logger.info("Fulfilling item '%s'", item.reference)

                    item.fulfill()

                    logger.info("Fulfilled item '%s'", item.reference)
                except QueueFulfillFailed:
                    raise
                except Exception as e:
                    raise QueueFulfillFailed(
                        item,
                    ) from e

            logger.info("Processed item '%s'", item.reference)

        logger.info("Processed items")

        return results
