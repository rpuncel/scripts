#!/bin/bash

cal=$(icalbuddy --dateFormat %Y-%m-%d --timeFormat %H:%M -nrd --noCalendarNames  -ss '' --excludeEventProps location,notes,attendees -ps ', | ,' -b ''  eventsToday+3)

echo "| Event | Time |"
echo "|-------|------|"
while IFS='\n' read -r line; do
	echo "$line"' |'
done <<< "$cal"


