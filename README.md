Here's a complete `README.md` file you can copy and use for your Telegram bot project:

```markdown
# Telegram Support Bot

This is a Telegram bot built using the `pyTelegramBotAPI` library, designed to provide a platform for users to submit questions and suggestions to the support team of an educational institution.

## Features

- **User Registration**: Logs each user's ID and username upon their first interaction with the bot.
- **Question Submission**: Users can submit questions, which are logged and forwarded to the support team.
- **Suggestion Submission**: Users can provide feedback or suggestions, which are also logged and sent to support.
- **Support Interaction**: Support staff can reply to user inquiries directly through the bot.
- **Log Retrieval**: Admin commands to retrieve logs of questions and suggestions submitted by users.

## Requirements

- Python 3.x
- `pyTelegramBotAPI` library
- A Telegram Bot API token (can be created via [BotFather](https://core.telegram.org/bots#botfather))

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required libraries**:

   ```bash
   pip install pyTelegramBotAPI
   ```

3. **Update the `TOKEN` and `SUPPORT_ID` variables** in the code:
   - Replace `NONE` in `TOKEN = 'NONE'` with your Telegram bot token.
   - Replace `NONE` in `SUPPORT_ID = 'NONE'` with the Telegram chat ID of the support staff.

4. **Run the bot**:

   ```bash
   python bot.py
   ```

## Usage

1. **Start the bot**:
   - Open your Telegram app and search for your bot.
   - Start the bot using the command `/start`.

2. **Choose an option** from the displayed menu:
   - **❓ Задать вопрос ССУ**: Submit a question to the support team.
   - **💡 Предложение/Замечание**: Provide feedback or suggestions.
   - **👥 Авторы**: Learn about the bot's authors.

## Code Overview

### Initialization

- The bot is initialized with a `TOKEN` for communication with the Telegram API.
- Paths for log files (`users_log.txt`, `questions_log.txt`, and `ideas_log.txt`) are set.

### User and Log Management

- **Log User**: Each user is logged with their ID and username upon interaction.
- **Log Questions and Ideas**: Functions are provided to log questions and suggestions into separate files.

### Command Handlers

- **/start Command**: Displays a welcome message and presents a menu of options.

- **Message Handlers**:
  - Users can select options to submit questions or suggestions. 
  - The bot collects necessary information like full name and group number before submitting the question or idea.

### Support Interaction

- **Sending to Support**: When a user submits a question or suggestion, it is sent to the support staff along with a reply button for the staff to respond directly.

- **Reply Handling**: The support staff can reply to users via the bot, ensuring a seamless communication channel.

### Admin Commands

- Admins can retrieve logs of questions and suggestions through designated commands (currently placeholders).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, please open an issue or submit a pull request.

```

Make sure to replace `<repository-url>` and `<repository-directory>` with the actual URL of your repository and its directory name. Adjust any sections as necessary to better fit your project! Let me know if you need any further modifications.
