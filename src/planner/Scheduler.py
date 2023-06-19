class Scheduler:
    def __init__(self):
        self.schedule = {
            "Monday": set(),
            "Tuesday": set(),
            "Wednesday": set(),
            "Thursday": set(),
            "Friday": set(),
            "Saturday": set(),
            "Sunday": set(),
        }

    def time_to_blocks(self, time):
        """Convert a time string to a half-hour block."""
        time_int = int(time)
        block = 2 * (time_int // 100) + (time_int % 100) // 30
        return block

    def range_to_blocks(self, start, end):
        """Convert a time range to a range of half-hour blocks."""
        return range(self.time_to_blocks(start), self.time_to_blocks(end))

    def block_to_time(self, block):
        """Convert a block back to a time string."""
        hour = block // 2
        minute = (block % 2) * 30
        return f"{hour:02d}{minute:02d}"

    def add(self, day, start, end):
        """Add a time range to a day. Return False if the range conflicts with the existing schedule."""
        new_blocks = set(self.range_to_blocks(start, end))
        if new_blocks.intersection(self.schedule[day]):
            return False
        self.schedule[day].update(new_blocks)
        return True

    def clear(self, day, start, end):
        """Remove a time range from a day."""
        blocks_to_remove = set(self.range_to_blocks(start, end))
        self.schedule[day].difference_update(blocks_to_remove)

    def __str__(self):
        result = []
        for day, blocks in self.schedule.items():
            if blocks:
                time_ranges = []
                sorted_blocks = sorted(list(blocks))
                start_block = sorted_blocks[0]
                end_block = start_block
                for block in sorted_blocks[1:]:
                    if block == end_block + 1:
                        end_block = block
                    else:
                        time_ranges.append((self.block_to_time(start_block), self.block_to_time(end_block)))
                        start_block = block
                        end_block = block
                time_ranges.append((self.block_to_time(start_block), self.block_to_time(end_block)))
                result.append(f"{day}: {', '.join(f'{start}-{end}' for start, end in time_ranges)}")
        return "\n".join(result)


def main():
    scheduler = Scheduler()

    # Adding time slots
    print(scheduler.add("Monday", "0600", "0800"))  # Output: True
    print(scheduler.add("Monday", "0800", "1000"))  # Output: True
    print(scheduler.add("Monday", "0900", "1100"))  # Output: False

    # Trying to add a conflicting time slot
    print(scheduler.add("Tuesday", "0800", "1000"))  # Output: True
    print(scheduler.add("Tuesday", "0900", "1100"))  # Output: False

    # Clearing time slots
    scheduler.clear("Monday", "0630", "0800")
    print(scheduler.add("Monday", "0629", "0800"))  # Output: True

    # Clearing a non-existing time slot
    scheduler.clear("Wednesday", "0600", "0800")
    print(scheduler.add("Wednesday", "0600", "0800"))  # Output: True


if __name__ == "__main__":
    main()
