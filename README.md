# Smart Screenshot Renamer 📸🤖

An intelligent Python application that automatically monitors your Screenshots folder and renames screenshot files using AI to generate descriptive, meaningful filenames based on the image content. Includes automatic startup functionality for seamless integration into your workflow.

## ✨ Features

- **🔍 Automatic Monitoring**: Watches your Screenshots folder for new PNG files in real-time
- **🤖 AI-Powered Naming**: Uses OpenAI GPT-4 to analyze screenshot content and generate descriptive filenames
- **📝 Smart Naming Convention**: Converts descriptions into clean, hyphen-separated filenames (e.g., `meeting-summary-zoom.png`)
- **🔄 Duplicate Handling**: Automatically handles filename conflicts by adding numbers
- **⚡ Real-time Processing**: Processes screenshots immediately when they're created
- **🚀 Auto-Start**: Set up automatic startup on login using macOS Launch Agents
- **📊 Logging**: Comprehensive logging for monitoring and debugging
- **🛡️ Error Handling**: Robust error handling for various file system edge cases

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenAI API key
- macOS (for screenshot directory setup and auto-start functionality)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd screen_shots_filenaming
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   Or add it to your shell profile (`.zshrc` or `.bash_profile`):
   ```bash
   echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

### Setup Screenshots Directory

First, configure macOS to save screenshots to a dedicated folder:

```bash
# Create the Screenshots directory
mkdir -p ~/Desktop/Screenshots

# Set macOS to save screenshots to this directory
defaults write com.apple.screencapture location ~/Desktop/Screenshots

# Restart the system UI server to apply changes
killall SystemUIServer
```

### Running the Application

#### Manual Mode

Start the screenshot monitor manually:

```bash
python app.py
```

You should see:
```
👀 Watching for screenshots in: /Users/your-username/Desktop/Screenshots
Press Ctrl+C to stop...
```

#### Auto-Start Mode (Recommended)

Set up automatic startup so the app runs whenever you log in:

```bash
# Make the setup script executable
chmod +x setup_autostart.sh

# Run the setup script
./setup_autostart.sh
```

The setup script will:
- Create a Launch Agent configuration
- Set up logging directories
- Start the service automatically
- Configure it to restart if it crashes

## 💡 How It Works

1. **Monitor**: The app continuously watches the `~/Desktop/Screenshots` directory
2. **Detect**: When a new PNG file is created (screenshot taken), it's detected immediately
3. **Analyze**: The screenshot is sent to OpenAI GPT-4 for content analysis
4. **Rename**: A descriptive filename is generated and the file is automatically renamed
5. **Log**: All operations are logged for monitoring and debugging

### Example Transformations

| Original Filename | AI-Generated Filename |
|-------------------|----------------------|
| Screenshot 2025-01-06 at 4.25.00 PM.png | meeting-summary-zoom.png |
| Screenshot 2025-01-06 at 5.30.15 PM.png | code-editor-python-function.png |
| Screenshot 2025-01-06 at 6.45.22 PM.png | website-login-form.png |

## ⚙️ Configuration

### Monitoring Directory

By default, the app monitors `~/Desktop/Screenshots`. To change this, modify the `watch_dir` variable in `app.py`:

```python
watch_dir = os.path.expanduser("~/your/custom/path")
```

### AI Model Settings

The app uses OpenAI's API for image analysis. The current implementation uses:

```python
def generate_filename(image_path):
    try:
        base64_image = encode_image(image_path)
        response = client.responses.create(
            model="gpt-4.1",
            input = [
                {
                    "role": "user",
                    "content": [
                        { 
                            "type": "input_text", 
                            "text": "You are a great file name generator. Please analyze the image and return the name of the image in English, and use a hyphen to separate words, for example: meeting-summary-zoom. Don't include any other text in your response, just the name of the image." 
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ]
        )
        return response.output_text
    except Exception as e:
        print(f"❌ GPT API Error: {e}")
        return None
```

You can modify the prompt or model as needed for your use case.

## 🚀 Auto-Start Management

### Setup Auto-Start

```bash
./setup_autostart.sh
```

### Management Commands

```bash
# Stop the service
launchctl unload ~/Library/LaunchAgents/com.user.screenshot-renamer.plist

# Start the service
launchctl load ~/Library/LaunchAgents/com.user.screenshot-renamer.plist

# Check if service is running
launchctl list | grep screenshot-renamer

# View logs
tail -f logs/screenshot-renamer.log

# View error logs
tail -f logs/screenshot-renamer-error.log
```

### Uninstall Auto-Start

```bash
# Make the uninstall script executable
chmod +x uninstall_autostart.sh

# Run the uninstall script
./uninstall_autostart.sh
```

## 🔧 Troubleshooting

### Common Issues

**1. "Watch directory does not exist" error**
- Make sure you've created the Screenshots directory: `mkdir -p ~/Desktop/Screenshots`
- Verify the path in your configuration matches where screenshots are saved

**2. OpenAI API errors**
- Verify your API key is set correctly: `echo $OPENAI_API_KEY`
- Check your OpenAI account has sufficient credits
- Ensure you have access to GPT-4 API
- Try testing the API key with a simple API call

**3. Screenshots not being processed**
- Verify screenshots are being saved as PNG files
- Check that the screenshot directory path is correct
- Make sure the filename contains "screenshot" (case-insensitive)
- Check the logs for any error messages

**4. Permission errors**
- Ensure the app has read/write permissions to the Screenshots directory
- On macOS, you might need to grant terminal/Python accessibility permissions
- Check that Python has Full Disk Access in System Preferences > Security & Privacy

**5. Auto-start not working**
- Check if the Launch Agent is loaded: `launchctl list | grep screenshot-renamer`
- Verify the API key is properly set in the plist file
- Check the error logs: `tail -f logs/screenshot-renamer-error.log`

### Debug Mode

The app includes detailed debugging output. Look for messages starting with:
- `🐛 DEBUG` - Path resolution debugging
- `✅` - Successful operations
- `❌` - Errors
- `🔍` - File processing status
- `📸` - Screenshot processing events

## 📁 Project Structure

```
screen_shots_filenaming/
├── app.py                              # Main application file
├── requirements.txt                    # Python dependencies
├── setup_autostart.sh                 # Auto-start setup script
├── uninstall_autostart.sh             # Auto-start removal script
├── com.user.screenshot-renamer.plist   # Launch Agent configuration
├── logs/                               # Log files directory
│   ├── screenshot-renamer.log          # Application logs
│   └── screenshot-renamer-error.log    # Error logs
└── README.md                           # This file
```

## 🛠️ Development

### Key Components

- **`ScreenshotHandler`**: File system event handler class that monitors for file changes
- **`generate_filename()`**: AI-powered filename generation using OpenAI API
- **`clean_file_path()`**: Path normalization utilities for handling special characters
- **`encode_image()`**: Base64 encoding for API requests
- **`process_screenshot()`**: Core logic for processing screenshot files

### Code Structure

The application is built with:
- **Watchdog**: For monitoring file system events
- **OpenAI API**: For AI-powered image analysis
- **Pillow**: For image processing support
- **Launch Agents**: For automatic startup on macOS

### Adding Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (especially the file monitoring logic)
5. Update the README if needed
6. Submit a pull request

## 📋 Requirements

```
watchdog>=2.1.0     # File system monitoring
openai>=1.0.0       # AI integration
pillow>=8.0.0       # Image processing
```

## 📝 License

This project is open source. Please check the license file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

When contributing:
- Test the auto-start functionality
- Ensure logging works correctly
- Test with various screenshot formats
- Update documentation as needed

## 💬 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the log files in the `logs/` directory
3. Open an issue on the repository with:
   - Your operating system version
   - Python version
   - Error messages from logs
   - Steps to reproduce the issue

## 🎯 Tips for Best Results

1. **Clear Screenshots**: The AI works best with clear, readable screenshots
2. **Consistent Naming**: The AI learns from patterns, so consistent screenshot types help
3. **Monitor Logs**: Keep an eye on the logs to ensure everything is working smoothly
4. **API Usage**: Be mindful of your OpenAI API usage and costs

---

**Happy screenshotting with smart naming! 📸✨**