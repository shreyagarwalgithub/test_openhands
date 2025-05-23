# ChatGPT Assistant

A system that provides daily updates on your ChatGPT chats, consolidates your searches, and notifies you about newer material on topics you've researched.

## Features

- Retrieve and analyze recent ChatGPT conversations
- Extract research topics from your chats
- Track research topics and check for new materials
- Generate daily updates with consolidated information
- Send email notifications with updates
- Web dashboard for viewing and managing updates

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Google API key and Custom Search Engine ID (for research updates)
- SMTP server access (for email notifications)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/chatgpt-assistant.git
   cd chatgpt-assistant
   ```

2. Install the package:
   ```
   pip install -e .
   ```

3. Create a `.env` file with your configuration:
   ```
   cp chatgpt_assistant/.env.example .env
   ```

4. Edit the `.env` file with your API keys and configuration.

## Usage

### Running the Web Interface

```
chatgpt-assistant --web --port 5000
```

Then open your browser to http://localhost:5000

### Running a One-time Update

```
chatgpt-assistant --update
```

### Scheduling Daily Updates

```
chatgpt-assistant --schedule
```

### Running Everything Together

```
chatgpt-assistant --web --schedule --port 5000
```

## Deployment Options

### Local Mac Deployment

1. Install the package as described above
2. Create a launch agent to run the assistant at login:
   ```
   mkdir -p ~/Library/LaunchAgents
   ```

3. Create a file `~/Library/LaunchAgents/com.user.chatgpt-assistant.plist`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.user.chatgpt-assistant</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/local/bin/python3</string>
           <string>-m</string>
           <string>chatgpt_assistant.main</string>
           <string>--web</string>
           <string>--schedule</string>
           <string>--port</string>
           <string>5000</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
       <key>StandardErrorPath</key>
       <string>/tmp/chatgpt-assistant.err</string>
       <key>StandardOutPath</key>
       <string>/tmp/chatgpt-assistant.out</string>
   </dict>
   </plist>
   ```

4. Load the launch agent:
   ```
   launchctl load ~/Library/LaunchAgents/com.user.chatgpt-assistant.plist
   ```

### Heroku Deployment

1. Create a `Procfile` in the project root:
   ```
   web: python -m chatgpt_assistant.main --web --schedule --port $PORT
   ```

2. Create a `runtime.txt` file:
   ```
   python-3.9.7
   ```

3. Deploy to Heroku:
   ```
   heroku create
   git push heroku main
   ```

4. Set environment variables in Heroku:
   ```
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set GOOGLE_API_KEY=your_google_api_key
   heroku config:set GOOGLE_CSE_ID=your_google_cse_id
   heroku config:set EMAIL_HOST=smtp.example.com
   heroku config:set EMAIL_PORT=587
   heroku config:set EMAIL_USER=your_email@example.com
   heroku config:set EMAIL_PASSWORD=your_email_password
   heroku config:set EMAIL_RECIPIENT=recipient@example.com
   heroku config:set UPDATE_TIME=08:00
   ```

## License

MIT
