# Discord Athan Bot

### General Goal
The purpose of this bot is to fetch athan timings from a specific location and play the athan in the most recently used voice channel.

### Modules Used
**discord.py** - Library used for aplication creation to utilize discord API 
**aladhan-api** - API used for getting Islamic Athan timings for any part of the world
**FFmpeg** - Framework used for playing Athan files through discord voice channels

### How To Setup
1. The user must firstly install the required modules. The instuctions can be found from the module developers' respective pages.
2. In the `keys.py` file, there are 3 values the user must fill in:
  - The *TOKEN* is the bot token retrieved from the Discord Developer Portal in the format of a string.
  - The *blacklisted_channel* is the channel that the bot will not join, in the format of the integer of the channel id. For example, this can be your afk channel.
  - The *default_channel* is the channel that the bot will naturally join if there has been no recent voice chat activity, in the format of the integer of the channel id.

3. In the `main.py`, the user must set their location to obtain the Athan timings for their country. A docmentation for the city and countries are found on the developers page. By default, the location is set to Calgary, Canada
