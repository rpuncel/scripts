#!/usr/bin/env python3
import os

from dataclasses import dataclass
from typing import Optional, Tuple
import sys
import pathlib
import re

'''
TODO

- [ ] read sys.argv[1] for a directory to use for events
- [ ] write a file per event using the frontmatter
- [ ] read file first and just update
'''
test_str_all_day = "First Day of Black History Month | Feb 1, 2024 |"
test_str_time = "Coaching | Feb 1, 2024 at 8:00 AM - 9:00 AM |"

@dataclass
class Event:
    title: str
    date: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class Store:
    
    dir: pathlib.Path
    
    def __init__(self, dir):
        self.dir = dir
        os.makedirs(dir, exist_ok=True)


    def upsert_event(self, event: Event):
        '''
        Checks for an existing markdown file corresponding to the event.
        If one exists, it is read in, and the details from the event as passed in
        are used to update the frontmatter of the file.

        If the file did not exist, a new one is created and frontmatter is inserted.
        '''

        file_path = self.dir / f"{event.date} {event.title}.md"

        if file_path.exists():
            # File exists, update frontmatter
            with open(file_path, 'r+') as file:
                lines = file.readlines()
                file.seek(0)

                found_section = False
                existing_frontmatter: dict[str, str] = {}
                for i, line in enumerate(lines):
                    if found_section:
                        file.write(line)
                    else: 
                        if i == 0 and not line.strip().startswith('---'):
                            file.write(to_front_matter(event, existing_frontmatter))
                            file.write(line)
                            found_section = True
                        elif i != 0 and line.strip().startswith('---'):
                            file.write(to_front_matter(event, existing_frontmatter))
                            found_section = True
                        elif not line.strip().startswith('---'):
                            key, value = extract_key_value(line)
                            if key not in ["title", "allDay", "startTime", "endTime", "date"]:
                                existing_frontmatter[key] = value

                file.truncate()
        else:
            # File does not exist, create new file with frontmatter
            with open(file_path, 'w') as file:
                file.write(to_front_matter(event))


def extract_key_value(line: str) -> Tuple[str, str]:
    pattern = r'^(\w+):(.*)$'
    match = re.match(pattern, line)
    if match:
        key = match.group(1)
        value = match.group(2)
        return key, value
    else:
        raise ValueError(f"line is not a key: value: {line}")


def to_front_matter(event: Event, existing_frontmatter: Optional[dict] = None):
    if existing_frontmatter is None:
        existing_frontmatter = {}
    lines: list[str] = list()
    lines.append('---')
    lines.append(f"title: {event.title}")
    if event.start_time and event.end_time:
        lines.append(f"allDay: false")
        lines.append(f"startTime: {event.start_time}")
        lines.append(f"endTime: {event.end_time}")
    else:
        lines.append(f"allDay: true")
    lines.append(f"date: {event.date}")
    for key in existing_frontmatter:
        lines.append(f'{key}:{existing_frontmatter[key]}')
    lines.append("---")
    lines.append("")
    return '\n'.join(lines)

def main():
    path = sys.argv[1]
    print(path)
    store = Store(path)
    for line in sys.stdin:
        event = process_line(line)
        store.upsert_event(event)


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