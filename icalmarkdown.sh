#!/bin/bash

cal=$(icalbuddy -nrd --noCalendarNames  -ss '' --excludeEventProps location,notes,attendees -ps ', | ,' -b '| '  eventsToday+3)

echo "| Event | Time |"
echo "|-------|------|"
while IFS='\n' read -r line; do
	echo "$line"' |'
done <<< "$cal"


