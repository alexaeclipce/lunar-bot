# Lunar Bot

## Overview
A Telegram bot that provides daily lunar day information including moon phase, lunar day descriptions with health/love/work advice, and moon images.

## Recent Changes
- 2026-02-08: Imported from GitHub, upgraded to python-telegram-bot v20+ (async API) for Python 3.12 compatibility. Fixed hardcoded image paths to use relative paths.

## Project Architecture
- **Language**: Python 3.12
- **Framework**: python-telegram-bot v22 (async API)
- **Dependencies**: ephem (astronomical calculations), python-telegram-bot
- **Structure**:
  - `lunar-bot/bot.py` - Main bot logic
  - `lunar-bot/images/` - Moon phase images (1-30)
  - `lunar-bot/requirements.txt` - Python dependencies

## Configuration
- **BOT_TOKEN** (secret): Telegram Bot API token required to run the bot

## User Preferences
- Bot content is in Russian
- Coordinates default to Crimea (lat=45.0, lon=34.0)
