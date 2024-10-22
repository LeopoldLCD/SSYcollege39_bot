
```markdown
# Telegram Support Bot

This is a Telegram bot developed using the `pyTelegramBotAPI` library, designed to facilitate user support and feedback for a college. Users can submit questions, provide suggestions, and view information about the bot's authors.

## Features

- **User Logging**: Logs each user's ID and username upon their first interaction.
- **Question Submission**: Allows users to submit questions that are logged and forwarded to support staff.
- **Suggestion Submission**: Users can provide feedback or suggestions, which are also logged and sent to support.
- **Support Interaction**: Support staff can reply to user inquiries directly through the bot.
- **Log Retrieval**: Admin commands to retrieve logs of questions and suggestions submitted by users.

## Requirements

- Python 3.x
- `pyTelegramBotAPI` library
- A Telegram Bot API token (can be created via [BotFather](https://core.telegram.org/bots#botfather))

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required libraries:

   ```bash
   pip install pyTelegramBotAPI
   ```

3. Update the `TOKEN` variable in the code with your Telegram bot token and set the `SUPPORT_ID` variable.

4. Replace any `NONE` placeholders in the code with appropriate values (like the support chat ID).

## Usage

1. Run the bot:

   ```bash
   python bot.py
   ```

2. Interact with the bot via Telegram:
   - Start the bot using the command `/start`.
   - Choose an option from the displayed menu:
     - **Задать вопрос ССУ**: Submit a question to the support team.
     - **Предложение/Замечание**: Provide feedback or suggestions.
     - **Авторы**: Learn about the bot's authors.

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

### Running the Bot

The bot operates continuously using `bot.polling(none_stop=True)` to listen for incoming messages and respond accordingly.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```

Make sure to replace `<repository-url>` and `<repository-directory>` with the actual URL of your repository and its directory name. You can also modify or expand any sections to better fit your needs! Let me know if you need any changes or additional information.
