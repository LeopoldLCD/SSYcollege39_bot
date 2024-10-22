Here’s a detailed `README.md` file for your Telegram bot code. You can copy and paste it directly:

```markdown
# Telegram Support Bot

This project is a Telegram bot built using the `pyTelegramBotAPI` library. The bot serves as a support system for users to ask questions and submit suggestions to a support team in an educational context.

## Features

- **User Registration**: Automatically logs user ID and username upon first interaction.
- **Question Submission**: Users can submit questions to the support team.
- **Suggestion Submission**: Users can provide suggestions or feedback.
- **Broadcast Messaging**: The support team can send messages to all registered users.
- **Log Retrieval**: The bot can retrieve logs of questions and suggestions.

## Requirements

- Python 3.x
- `pyTelegramBotAPI` library

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required libraries**:

   ```bash
   pip install pyTelegramBotAPI
   ```

3. **Update the `TOKEN` and `SUPPORT_ID` variables** in the code:
   - Replace `NONE` in `TOKEN = 'NONE'` with your Telegram bot token.
   - Replace `NONE` in `SUPPORT_ID = 'NONE'` with the Telegram chat ID of the support staff.

4. **Create log files**:
   - Ensure that the following log files exist in the same directory as the script:
     - `users_log.txt`
     - `questions_log.txt`
     - `ideas_log.txt`

5. **Run the bot**:

   ```bash
   python bot.py
   ```

## Usage

1. **Start the bot**:
   - Open Telegram and find your bot.
   - Start the bot by sending the command `/start`.

2. **Interact with the bot**:
   - Choose one of the options:
     - **❓ Задать вопрос ССУ**: Submit a question to the support team.
     - **💡 Предложение/Замечание**: Provide feedback or suggestions.
     - **👥 Авторы**: View information about the bot's authors.

3. **Broadcast Messages**:
   - Support staff can send messages to all users using the command `/all`. This command is restricted to the support staff only.

## Code Overview

### Initialization

- The bot is initialized with a `TOKEN` for Telegram API communication.
- User IDs are loaded from `users_log.txt` at startup.

### User and Log Management

- **User ID Loading**: Loads user IDs from the `users_log.txt` file.
- **Logging Functions**:
  - `log_user`: Records user ID and username when they interact with the bot.
  - `log_question`: Logs submitted questions.
  - `log_idea`: Logs submitted suggestions.

### Command Handlers

- **/start Command**: Displays a welcome message and presents options to the user.
- **/all Command**: Sends a message to all users. Only accessible to support staff.

### User Interaction

- Users can ask questions or submit suggestions through inline keyboard options.
- The bot collects necessary information (full name and group number) before submitting the question or suggestion.

### Support Interaction

- Questions and suggestions are forwarded to the support team along with a reply button for the support team to respond directly to the user.

### Admin Commands

- Admin commands are implemented for log retrieval, currently set up as placeholders. You can expand these functionalities as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, please open an issue or submit a pull request.

```

Make sure to replace `<repository-url>` and `<repository-directory>` with the actual URL of your repository and its directory name. Adjust any sections as necessary to better fit your project! Let me know if you need any further modifications.
