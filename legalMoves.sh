#! /bin/bash

if ! command -v inotifywait &> /dev/null; then
	echo "Error: please install inotifywait before proceeding."
	exit 1
fi

file_to_monitor="/home/jason/python/stockfish_project/piece.csv"

while true; do
	clear
	printf " Legal Moves:\n\n"
	cat "$file_to_monitor"
	inotifywait -q -e modify "$file_to_monitor" > /dev/null 2>&1

done
