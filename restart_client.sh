#!/bin/bash
DISCORD_BOT_SCRIPT=main.py

# Stop the Discord bot
pkill -f "python3 $DISCORD_BOT_SCRIPT"

# Reset the log files
rm logs/*

# Move all files in data folder to temp_data folder
directory="temp_data/"
mkdir -p "$directory"
mv data/* "$directory"

# Activate the virtual env
source venv/bin/activate

# Re-scrape the file
scrapy crawl ai21_spider -O data/AI21.csv

# Setup the index
python3 index.py

# Delete the /temp_data folder
rm -rf "$directory"

# Restart the Discord bot as a background process
python3 "$DISCORD_BOT_SCRIPT" &

# Exit the script
exit 0