# AI21 Labs Discord Bot

<a name="readme-top"></a>

[![MIT License][license-shield]][license-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#-what-is-this">What is this?</a></li>
    <li>
      <a href="#-getting-started">Getting Started</a>
      <ul>
        <li><a href="#-quick-install">Quick Install</a></li>
        <li><a href="#-running-the-discord-bot">Running the Discord Bot</a></li>
        <li><a href="#-running-the-scraper">Running the Scraper</a></li>
        <li><a href="#-setting-up-the-vector-database">Setting up the Vector Database</a></li>
        <li><a href="#-putting-it-all-together">Putting it all Together</a></li>
      </ul>
    </li>
    <li><a href="#-logging">Logging</a></li>
    <li><a href="#-testing">Testing</a></li>
    <li><a href="#-roadmap">Roadmap</a></li>
    <li><a href="#-contributing">Contributing</a></li>
    <li><a href="#-license">License</a></li>
  </ol>
</details>



## 🤔 What is this?
A Discord Bot that responds to user's with the power of AI21 Labs' large language models. 

A User can directly message (DM) the Bot or place a "❓" reaction on their message in a text channel to ask the Bot to respond. 

The Bot will read the past 5 messages in an attempt to maintain conversation history. It will solely consist of messages exchanged between the User and the Bot.

The Bot chooses a language model and parameters most suited to respond to the user input. In addition, it may use indexed information (available from AI21 Labs' website) to provide links and up to date information regarding AI21 Labs.

Command options are available to the user:
 - `--no-history` or `-nh` : Bot will ignore all previous messages
 - `--verbose` or `-v` : Bot will output preset used to generate response

The user may append these options to their Discord message in the following format: 
 - `Write a poem about Europe -nh --verbose`
 - `What is AI21 Labs --no-history -v`

Both examples will make the Bot ignore previous messages and output the model parameters used for generation. 

A scraper is provided that will read and extract information from both the documentation and the home page of AI21 Labs. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📖 Getting Started 
### ⚡️ Quick Install
Navigate to the folder you want to put the project in and run the following commands.

`git clone https://github.com/kael558/AI21_Discord.git`

`pip install -r requirements.txt`

Make sure you have environment variables with the following values:
```
AI21_API_KEY=<API KEY FOR AI21 LABS>
DISCORD_TOKEN=<DISCORD TOKEN FOR APPLICATION FROM DEVELOPER SITE>
```

One way to do that is to create a .env file in the top level directory and put these variables in because python-dotenv is installed.

### 🤖 Running the Discord Bot
`python main.py`

This will setup and start the Discord Bot for it to respond to messages. 

### 🕷️ Running the Scraper
Navigate to the top level directory and run the following command:

`scrapy crawl ai21_spider -O data/AI21.csv`

This will start the scraper and output the data into the AI21.csv file in the data folder. 

There are two versions of the scraper:
1. The title spider will scrape the title, contents and link of every page
2. The text spider will scrape the individual text elements - assign a depth to them - and the link of every page. 

### 📁 Setting up the Vector Database
Once the raw data has been collected via the scraper, it must be indexed into a vector database. Running the following will do so:

`python index.py`

This will index all the data from AI21.csv into a vector database which can be queried when the Bot needs it. 

### ⚙️ Putting it all Together with a Shell Script
A restart_client.sh script is provided for Linux. It does the following:
1. Stops the Discord Bot if it is running 
2. Moves the existing data into a temporary folder
3. Runs the scraper to collect the updated data
4. Sets up the vector database
5. If step 3 or 4 fail, then re-use the old data. Else delete the old data.
6. Restarts the Discord Bot

This script can be run like so:
`./restart_client.sh`

You can see the Discord Bot running as "python3 main.py" with:

`ps -ef | grep python`

And to kill the process:

`pkill -f "python3 main.py"`


### 💧 Droplet Setup From Scratch
This section covers all steps from a-z to set up the project on a fresh Digital Ocean droplet. Run the following on your terminal:
```
# Clone the repo
git clone https://github.com/kael558/AI21_Discord.git
cd AI21_Discord/

# Updates the package lists.
sudo apt update

# Upgrades the packages
sudo apt -y upgrade

# Install pip
sudo apt install -y python3-pip

# Installs the necessary development libraries and tools for building and compiling software
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

# Install python venv
sudo apt install -y python3-venv

# Create and activate a new virtual env
python3 -m venv venv
source venv/bin/activate

# Install wheel 
pip install wheel==0.40.0
pip install annoy==1.17.2

# Install the project dependencies
pip install -r requirements.txt --no-cache-dir

# Make a .env file and populate it with AI21_API_KEY and DISCORD_TOKEN
vi .env

# Add execution permissions to .sh file
chmod +x restart_client.sh

# Run the .sh file
./restart_client.sh
```

A CRON job can be setup with the following schedule:
```
# Opens the crontab configuration file
crontab -e

# Sets the script to run on the first of every month
0 0 1 * * /path/to/restart_client.sh
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## ⚠️ Logging
Logging is provided and all logs are saved in the logs folder with the following files:
 - bot.log: errors with the Discord Bot while it is running
 - scraper.log: errors with the Scraper
 - index.log: errors with the indexing 

## 🔧 Testing
A short manual testing suite (*tests.py*) is provided to assess the quality of the context retrieved and the responses. Run the following:

`python -m unittest`


## 📅 Roadmap
- [x] Default bot
- [x] Variable Preset
- [x] AI21 Indexed information
- [x] Improving scraper (including any text node elements, by adding depth to elements and including hierarchical elements for context)
- [x] Test hierarchical context retrieval to get context
- [x] Finishing touches (like README, discord icon, discord name, transfer hosting)

## 🤝 Contributing
All rights belong to AI21 Labs. 

You may fork the project and work in your own repository.

## ⚖️ License
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[license-shield]: https://img.shields.io/github/license/kael558/AI21_Discord.svg?style=for-the-badge
[license-url]: https://github.com/kael558/AI21_Discord/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[rahel-linkedin-url]: https://www.linkedin.com/in/rahelgunaratne/
