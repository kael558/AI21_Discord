DISCORD_BOT_SCRIPT=main.py

# Stop the Discord bot
pkill -f "python3 $DISCORD_BOT_SCRIPT"

# Delete the data files
rm data/*

# Activate the virtual env
source venv/bin/activate

# Re-scrape the file
scrapy crawl ai21_spider -O data/AI21.csv

# Setup the index
python3 bot.py

# Restart the Discord bot
python3 "$DISCORD_BOT_SCRIPT" &