# Discord Athan Bot

### General Goal
The purpose of this bot is to fetch athan timings from a specific location and play the athan in the most recently used voice channel.

### Modules Used
**discord.py** - Library used for aplication creation to utilize discord API 
**aladhan-api** - API used for getting Islamic Adhan timings for any part of the world
**FFmpeg** - Framework used for playing Adhan files through discord voice channels

### How To Setup
1. In the `keys.py` file, there are 3 values the user must fill in.
  a) The * *TOKEN* * is the bot token retrieved from the Discord Developer Portal in the format of a string.
  b) The * *blacklisted_channel* *
