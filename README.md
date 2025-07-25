# RemindMe Bot

**Your own reminder agent so that you don't miss anything while hanging out on your favorite platform!**

A Discord bot that helps you set reminders using natural language processing. Simply mention the bot and tell it what you want to be reminded about and when!

## Features

- 🤖 Natural language processing for intuitive reminder creation
- ⏰ Multiple time formats supported (seconds, minutes, hours, AM/PM)
- 💾 SQLite database for persistent reminder storage
- 🔄 Automatic reminder checking and notifications
- 📱 Direct message notifications when reminders are due

## Prerequisites

- Python 3.13 or higher
- Discord Bot Token
- Discord server with appropriate permissions

## Setup Instructions

### Method 1: Python Runtime

#### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd remindme_bot
```

#### 2. Create Virtual Environment

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
# Download spaCy language model
python -m spacy download en_core_web_sm
```

#### 4. Environment Configuration

Create a `.env` file in the project root:

```env
TOKEN=your_discord_bot_token_here
```

#### 5. Run the Bot

```bash
python -m remindme_bot
```

### Method 2: Docker Compose

#### 1. Environment Setup

Create a `.env` file in the project root:

```env
TOKEN=your_discord_bot_token_here
```

#### 2. Create Docker Volume

```bash
docker volume create remindme_bot_vol
```

#### 3. Run with Docker Compose

```bash
docker-compose -f remindme_bot_compose.yml up -d
```

#### 4. Check Logs

```bash
docker-compose -f remindme_bot_compose.yml logs -f
```

#### 5. Stop the Bot

```bash
docker-compose -f remindme_bot_compose.yml down
```

## Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Create a bot and copy the token
5. Enable "Message Content Intent" in Bot settings
6. Invite the bot to your server with appropriate permissions:
   - Send Messages
   - Read Message History
   - Use Slash Commands
   - Send Messages in Threads

## Usage

### Basic Commands

- **Get Help**: `@remindme_bot coms` - Shows supported time formats and examples
- **Set Reminder**: `@remindme_bot remind me to [task] in [time]`
- **Set Reminder at Specific Time**: `@remindme_bot remind me to [task] at [time]`

### Supported Time Formats

- **Seconds**: `s`, `sec`, `second`, `seconds`
- **Minutes**: `m`, `min`, `minute`, `minutes`
- **Hours**: `h`, `hr`, `hrs`, `hour`, `hours`
- **12-hour Format**: `am`, `pm` (e.g., `2pm`, `10:30am`)

## Example Use Cases

### 1. Quick Reminders
```
@remindme_bot remind me to check emails in 30min
@remindme_bot remind me to take a break in 1hr
@remindme_bot remind me to call mom in 2hrs
```

### 2. Specific Time Reminders
```
@remindme_bot remind me to attend meeting at 2pm
@remindme_bot remind me to submit report at 10:30am
@remindme_bot remind me to lunch break at 12pm
```

### 3. Short-term Reminders
```
@remindme_bot remind me to check the code in 45sec
@remindme_bot remind me to restart server in 5min
@remindme_bot remind me to save work in 10min
```

### 4. Work-related Reminders
```
@remindme_bot remind me to push code to repository in 1hr
@remindme_bot remind me to review pull requests at 3pm
@remindme_bot remind me to update documentation in 30min
@remindme_bot remind me to backup database at 11pm
```

### 5. Personal Reminders
```
@remindme_bot remind me to drink water in 1hr
@remindme_bot remind me to exercise at 6pm
@remindme_bot remind me to call dentist in 2hrs
@remindme_bot remind me to take medication at 8am
```

### 6. Study/Learning Reminders
```
@remindme_bot remind me to review notes in 45min
@remindme_bot remind me to practice coding at 7pm
@remindme_bot remind me to read chapter 5 in 2hrs
```

## How It Works

1. **Natural Language Processing**: The bot uses spaCy to parse your reminder message and extract the task and time
2. **Time Calculation**: Converts relative time (like "30min") or absolute time (like "2pm") into a target datetime
3. **Database Storage**: Stores the reminder in SQLite database with user ID, task, and target time
4. **Background Checking**: Runs a background task every 30 seconds to check for due reminders
5. **Notification**: Sends a direct message to the user when the reminder time is reached

## Database Structure

The bot uses SQLite with two main tables:
- `reminder_table`: Stores user reminders with task details and timing
- `rm_check_table`: Tracks the last check time for the reminder system

## Troubleshooting

### Common Issues

1. **Bot not responding**: Check if the bot has proper permissions in your Discord server
2. **Token errors**: Ensure your Discord bot token is correctly set in the `.env` file
3. **Time parsing issues**: Use supported time formats (check with `@remindme_bot coms`)
4. **Database errors**: Ensure the bot has write permissions in the directory

### Logs

- Check `remindme_bot.log` for detailed error logs
- For Docker: Use `docker-compose logs` to view container logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

If you encounter any issues or have questions, please create an issue in the repository or contact the maintainers.