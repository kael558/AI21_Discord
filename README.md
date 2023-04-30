# AI21 Labs Discord Bot

<a name="readme-top"></a>

[![MIT License][license-shield]][license-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



## 🤔 What is this?
A Discord Bot that responds to user's with the power of AI21 Labs' large language models. 

A User can directly message (DM) or place a "❓" reaction on their message in a text channel to ask the Bot to respond. 

The Bot will read the past 5 messages in an attempt to maintain conversation history. It will solely consist of messages exchanged between the User and the Bot.

The Bot chooses a language model and parameters most suited to respond to the user input. In addition, it may use indexed information (available from AI21 Labs' website) to provide links and up to date information regarding AI21 Labs.

Command options are available to the user:
 - --no-history or -nh : Bot will ignore all previous messages
 - --verbose or -v : Bot will output preset used to generate response

The user may append these options to their Discord message in the following format: 
 - Write a poem about Europe -nh --verbose
 - What is AI21 Labs --no-history -v
Both examples will make the Bot ignore previous messages and output the model parameters used for generation. 

A scraper is provided that will read and extract information from both the documentation and the home page of AI21 Labs. 

## 📖 Getting Started 
### Quick Install
Navigate to the folder you want to put the project in and run the following commands.

`git clone `https://github.com/kael558/AI21_Discord.git`

`pip install -r requirements.txt`

Make sure you have environment variables with the following values:
AI21_API_KEY=<API KEY FOR AI21 LABS>
DISCORD_TOKEN=<DISCORD TOKEN FOR APPLICATION FROM DEVELOPER SITE>

One way to do that is to create a .env file in the top level directory and put these variables in.

### Running the Discord Bot
`python main.py`

This will start the Discord Bot and it will respond to messages. 

### Running the Scraper
Navigate to the top level directory and run the following command:
`scrapy crawl ai21_spider -O data/AI21.csv `

This will start the scraper and output the data into the AI21.csv file in the data folder. 

### Running the Index Setup
Once the raw data has been collected via the scraper. It must be indexed into a vector database. Running the following will do so:
`python bot.py`

This will index all the data from AI21.csv into a vector database which can be queried when the Bot needs it. 

### Running the .sh script
An restart_client.sh script is provided. It does the following:
 - Stops the Discord Bot if it is running
 - Deletes all the AI21 data
 - Runs the scraper to collect the data
 - Runs the index setup to index the data
 - Restarts the Discord Bot

This script can be run on Linux like so:
`./restart_client.sh`

Note: A CRON job is setup with the following schedule:
 - `crontab -e` # Opens the crontab configuration file
 - `0 0 1 * * /path/to/restart_client.sh` # Sets the script to run on the first of every month

## Roadmap
- [x] Default bot
- [x] Variable Preset
- [x] AI21 Indexed information
- [ ] Finishing touches (like README, discord icon, discord name, transfer hosting)

## Contributing
All rights belong to AI21 Labs. 

You may fork the project and work in your own repository.

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues

[license-shield]: https://img.shields.io/github/license/kael558/AI21_Discord.svg?style=for-the-badge
[license-url]: https://github.com/kael558/AI21_Discord/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[rahel-linkedin-url]: https://www.linkedin.com/in/rahelgunaratne/