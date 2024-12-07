"""Items."""

import logging
from typing import Optional

from cyberfusion.QueueSupport.interfaces import ItemInterface

logger = logging.getLogger(__name__)


class _Item(ItemInterface):
    """Represents base item."""

    @property
    def hide_outcomes(self) -> bool:
        """Get if outcomes should be hidden."""
        return self._hide_outcomes

    @property
    def reference(self) -> Optional[str]:
        """Get free-form reference, for users' own administrations."""
        return self._reference
