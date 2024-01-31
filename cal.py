#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional
import sys

test_str_all_day = "First Day of Black History Month | Feb 1, 2024 |"
test_str_time = "Coaching | Feb 1, 2024 at 8:00 AM - 9:00 AM |"

@dataclass
class Event:
    title: str
    date: str
    start_time: Optional[str]
    end_time: Optional[str]

def to_front_matter(event: Event):
    lines: list[str] = list()
    lines.append('---')
    lines.append(f"title: {event.title}")
    lines.append(f"date: {event.date}")
    if event.start_time and event.end_time:
        lines.append(f"startTme: {event.start_time}")
        lines.append(f"endTime: {event.end_time}")
        lines.append(f"allDay: false")
    else:
        lines.append(f"allDay: true")
    lines.append("---")
    return '\n'.join(lines)


def main():
    for line in sys.stdin:
        event = process_line(line)
        print(to_front_matter(event))


def process_line(line: str) -> Event:
    pieces = line.split('|')
    title = pieces[0].strip()
    date_and_time = pieces[1].strip()
    if "at" in date_and_time:
        split = date_and_time.split(" at ")
        date = split[0].strip()
        start_time = split[1].split(' - ')[0].strip()
        end_time = split[1].split(' - ')[1].strip()
        return Event(title, date, start_time, end_time,)
    else:
        date = date_and_time
        return Event(title, date, None, None)


if __name__ == "__main__":
    main()