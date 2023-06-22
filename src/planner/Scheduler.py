from typing import Dict, Set


class Scheduler:
    def __init__(self) -> None:
        self.schedule: Dict[str, Set[int]] = {
            "Monday": set(),
            "Tuesday": set(),
            "Wednesday": set(),
            "Thursday": set(),
            "Friday": set(),
            "Saturday": set(),
            "Sunday": set(),
        }

    def time_to_blocks(self, time: str) -> int:
        """Convert a time string to a 15-minute block."""
        time_int = int(time)
        block = 4 * (time_int // 100) + (time_int % 100) // 15
        return block

    def block_to_time(self, block: int) -> str:
        """Convert a block back to a time string."""
        hour = block // 4
        minute = (block % 4) * 15
        return f"{hour:02d}{minute:02d}"

    def range_to_blocks(self, start: str, end: str) -> range:
        """Convert a time range to a range of 15-minute blocks."""
        return range(self.time_to_blocks(start), self.time_to_blocks(end))

    def add(self, day: str, start: str, end: str) -> bool:
        """Add a time range to a day.
        Return False if the range conflicts with the existing schedule."""
        if (start == end):
            # If the start and end are equal, no need to clear anything
            return True

        new_blocks = set(self.range_to_blocks(start, end))
        if new_blocks.intersection(self.schedule[day]):
            return False  # If a conflict is found, it could not be added.

        self.schedule[day].update(new_blocks)
        return True

    def clear(self, day: str, start: str, end: str) -> None:
        """Remove a time range from a day."""
        if (start == end):
            # If the start and end are equal, no need to clear anything
            pass

        blocks_to_remove = set(self.range_to_blocks(start, end))
        self.schedule[day].difference_update(blocks_to_remove)
