# Telegram Bot

This is a simple Telegram bot built using the `pyTelegramBotAPI` library. The bot allows users to interact with various functionalities, such as checking a schedule, submitting questions, and providing suggestions. It logs user messages and keeps track of unique users.

## Features

- **User Registration**: Automatically registers unique users upon their first interaction with the bot.
- **Message Logging**: Logs all messages sent by users in individual text files for tracking purposes.
- **Interactive Menu**: Presents users with a menu of options to choose from.
- **Notification System**: Allows for sending notifications to all registered users.
- **Personal Messaging**: Supports sending direct messages to specific users by their user ID.

## Requirements

- Python 3.x
- `pyTelegramBotAPI` library
- Telegram Bot API token (you can create a bot using [BotFather](https://core.telegram.org/bots#botfather))

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   
2. Install the required libraries:
   
   ```bash
   pip install pyTelegramBotAPI

3. Update the token variable in the code with your Telegram bot token.
4. Replace the NONE placeholders in the code with appropriate URLs or messages.

##Usage
1. Run the bot:

   ```bash
   python bot.py
2. Interact with the bot via Telegram:

- **Start the bot using the command /start.
- **Choose an option from the menu.
- **Use the appropriate commands for notifications or personal messages.

