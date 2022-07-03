# Chuck-Bot: A NAFF powered discord bot

![GitHub repo size](https://img.shields.io/github/repo-size/ThePieroCV/ChuckBot?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/ThePieroCV/ChuckBot?style=for-the-badge)
![License](https://img.shields.io/github/license/ThePieroCV/ChuckBot?style=for-the-badge)
![Github open issues](https://img.shields.io/github/issues-raw/ThePieroCV/ChuckBot?style=for-the-badge)
![Tag Latest Release](https://img.shields.io/github/v/tag/ThePieroCV/ChuckBot?style=for-the-badge)

![ChuckBot](./assets/lr.gif)

> ChuckBot is a discord bot that brings you different kind of options to make your life easier. Powered by NAFF, this bot is the real naff shady!

___
### Adjustments and Improvements

Goals to reach on next updates:

- [x] Genius Integration - Lyrics
- [ ] Unified YoutubeDLP interaction to speed up
- [ ] Pomodoro Tool

___

## 💻 Pre-requirements

Before getting up this bot, be aware of the next :

* NAFF uses Python 3.10.x, it is recommended to use virtual environments.
* You need FFMPEG installed (On Path, or then pasted on local cloned repo).
* Read and internalize how NAFF works on [NAFF documentation](https://dis-snek.readthedocs.io).

___
## 🚀 Installing Chuck-Bot

In order to install ChuckBot, follow the next steps:

Clone the repo:
```console
git clone https://github.com/ThePieroCV/ChuckBot.git
```

Go into Chuck-Bot folder:
```console
cd ChuckBot
```

Install pip requirements:
```console
pip install -r requirements.txt
```

Create **.env** file with content:
```
DISCORD_TOKEN = '#YOUR_TOKEN_HERE'
ENV_SCOPE = 'A_SCOPE ANOTHER_SCOPE ...'
SPOTIFY_CLIENT = 'CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'CLIENT_SECRET'
GENIUS_TOKEN = 'GENIUS_TOKEN'
```

Finally, run the bot:
```console
python bot.py
```

___
## ☕ Using ChuckBot

Chuckbot now supports:
- [X] Scales (Cogs) manager.
- [X] Music player (Youtube).
- [X] Music player (Spotify playlists)
- [X] Genius lyrics


To customize ChuckBot, you can add new extensions that will be recognized automatically. You can review other premade *.py* Extensions to customize it.

___

## 🐞 Known Bugs
- [X] **Solved**. Can't regrow Scales with **_regrow_scales** command due to *two-in-one* music scale. **Removed two-in-one scales**.
- [ ] Genius lyrics search system is not totally accurate, but it works on most of the songs tested.

___

## 📝 License

This project has **GPL-3.0** license. See [License](LICENSE) for more details.
