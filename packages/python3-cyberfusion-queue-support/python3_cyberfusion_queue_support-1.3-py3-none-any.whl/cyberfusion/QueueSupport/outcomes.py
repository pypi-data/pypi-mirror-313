"""Outcomes."""

from typing import List, Optional

from cyberfusion.QueueSupport.interfaces import OutcomeInterface
from cyberfusion.SystemdSupport.units import Unit


class CopyItemCopyOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, source: str, destination: str) -> None:
        """Set attributes."""
        self.source = source
        self.destination = destination

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Copy {self.source} to {self.destination}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, CopyItemCopyOutcome):
            return False

        return other.source == self.source and other.destination == self.destination


class MoveItemMoveOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, source: str, destination: str) -> None:
        """Set attributes."""
        self.source = source
        self.destination = destination

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Move {self.source} to {self.destination}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, MoveItemMoveOutcome):
            return False

        return other.source == self.source and other.destination == self.destination


class MkdirItemCreateOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, path: str) -> None:
        """Set attributes."""
        self.path = path

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Create {self.path}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, MkdirItemCreateOutcome):
            return False

        return other.path == self.path


class SystemdTmpFilesCreateItemCreateOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, path: str) -> None:
        """Set attributes."""
        self.path = path

    def __str__(self) -> str:
        """Get human-readable string."""
        return (
            f"Create tmp files according to tmp files configuration file at {self.path}"
        )

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, SystemdTmpFilesCreateItemCreateOutcome):
            return False

        return other.path == self.path


class UnlinkItemUnlinkOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, path: str) -> None:
        """Set attributes."""
        self.path = path

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Unlink {self.path}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, UnlinkItemUnlinkOutcome):
            return False

        return other.path == self.path


class RmTreeItemRemoveOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, path: str) -> None:
        """Set attributes."""
        self.path = path

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Remove directory tree {self.path}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, RmTreeItemRemoveOutcome):
            return False

        return other.path == self.path


class CommandItemRunOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, command: List[str]) -> None:
        """Set attributes."""
        self.command = command

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Run {self.command}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, CommandItemRunOutcome):
            return False

        return other.command == self.command


class ChmodItemModeChangeOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, path: str, old_mode: Optional[int], new_mode: int) -> None:
        """Set attributes."""
        self.path = path
        self.old_mode = old_mode
        self.new_mode = new_mode

    def __str__(self) -> str:
        """Get human-readable string."""
        old_mode: Optional[str]

        if self.old_mode is not None:
            old_mode = oct(self.old_mode)
        else:
            old_mode = None

        return f"Change mode of {self.path} from {old_mode} to {oct(self.new_mode)}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, ChmodItemModeChangeOutcome):
            return False

        return (
            other.path == self.path
            and other.old_mode == self.old_mode
            and other.new_mode == self.new_mode
        )


class ChownItemOwnerChangeOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(
        self, *, path: str, old_owner_name: Optional[str], new_owner_name: str
    ) -> None:
        """Set attributes."""
        self.path = path
        self.old_owner_name = old_owner_name
        self.new_owner_name = new_owner_name

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Change owner of {self.path} from {self.old_owner_name} to {self.new_owner_name}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, ChownItemOwnerChangeOutcome):
            return False

        return (
            other.path == self.path
            and other.old_owner_name == self.old_owner_name
            and other.new_owner_name == self.new_owner_name
        )


class ChownItemGroupChangeOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(
        self, *, path: str, old_group_name: Optional[str], new_group_name: str
    ) -> None:
        """Set attributes."""
        self.path = path
        self.old_group_name = old_group_name
        self.new_group_name = new_group_name

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Change group of {self.path} from {self.old_group_name} to {self.new_group_name}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, ChownItemGroupChangeOutcome):
            return False

        return (
            other.path == self.path
            and other.old_group_name == self.old_group_name
            and other.new_group_name == self.new_group_name
        )


class SystemdUnitEnableItemEnableOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, unit: Unit) -> None:
        """Set attributes."""
        self.unit = unit

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Enable {self.unit.name}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, SystemdUnitEnableItemEnableOutcome):
            return False

        return other.unit.name == self.unit.name


class SystemdUnitDisableItemDisableOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, unit: Unit) -> None:
        """Set attributes."""
        self.unit = unit

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Disable {self.unit.name}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, SystemdUnitDisableItemDisableOutcome):
            return False

        return other.unit.name == self.unit.name


class SystemdUnitRestartItemRestartOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, unit: Unit) -> None:
        """Set attributes."""
        self.unit = unit

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Restart {self.unit.name}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, SystemdUnitRestartItemRestartOutcome):
            return False

        return other.unit.name == self.unit.name


class SystemdUnitReloadItemReloadOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, unit: Unit) -> None:
        """Set attributes."""
        self.unit = unit

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Reload {self.unit.name}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, SystemdUnitReloadItemReloadOutcome):
            return False

        return other.unit.name == self.unit.name


class SystemdUnitStopItemStopOutcome(OutcomeInterface):
    """Represents outcome."""

    def __init__(self, *, unit: Unit) -> None:
        """Set attributes."""
        self.unit = unit

    def __str__(self) -> str:
        """Get human-readable string."""
        return f"Stop {self.unit.name}"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, SystemdUnitStopItemStopOutcome):
            return False

        return other.unit.name == self.unit.name
