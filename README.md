# Smart Screenshot Renamer 📸🤖

An intelligent Python application that automatically monitors your Screenshots folder and renames screenshot files using AI to generate descriptive, meaningful filenames based on the image content.

## ✨ Features

- **🔍 Automatic Monitoring**: Watches your Screenshots folder for new PNG files in real-time
- **🤖 AI-Powered Naming**: Uses OpenAI GPT-4 to analyze screenshot content and generate descriptive filenames
- **📝 Smart Naming Convention**: Converts descriptions into clean, hyphen-separated filenames (e.g., `meeting-summary-zoom.png`)
- **🔄 Duplicate Handling**: Automatically handles filename conflicts by adding numbers
- **⚡ Real-time Processing**: Processes screenshots immediately when they're created
- **🛡️ Error Handling**: Robust error handling for various file system edge cases

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenAI API key
- macOS (for screenshot directory setup)

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
   
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
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

Start the screenshot monitor:

```bash
python app.py
```

You should see:
```
👀 Watching for screenshots in: /Users/your-username/Desktop/Screenshots
Press Ctrl+C to stop...
```

## 💡 How It Works

1. **Monitor**: The app continuously watches the `~/Desktop/Screenshots` directory
2. **Detect**: When a new PNG file is created (screenshot taken), it's detected immediately
3. **Analyze**: The screenshot is sent to OpenAI GPT-4 for content analysis
4. **Rename**: A descriptive filename is generated and the file is automatically renamed

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

The app uses GPT-4 for image analysis. You can modify the prompt or model in the `generate_filename()` function:

```python
response = client.responses.create(
    model="gpt-4.1",  # Change model here
    input = [
        {
            "role": "user",
            "content": [
                { 
                    "type": "input_text", 
                    "text": "Your custom prompt here..."  # Modify prompt
                },
                # ... rest of the configuration
            ]
        }
    ]
)
```

## 🔧 Troubleshooting

### Common Issues

**1. "Watch directory does not exist" error**
- Make sure you've created the Screenshots directory: `mkdir -p ~/Desktop/Screenshots`

**2. OpenAI API errors**
- Verify your API key is set correctly
- Check your OpenAI account has sufficient credits
- Ensure you have access to GPT-4 API

**3. Screenshots not being processed**
- Verify screenshots are being saved as PNG files
- Check that the screenshot directory path is correct
- Make sure the filename contains "screenshot" (case-insensitive)

**4. Permission errors**
- Ensure the app has read/write permissions to the Screenshots directory
- On macOS, you might need to grant terminal/Python accessibility permissions

### Debug Mode

The app includes detailed debugging output. Look for messages starting with:
- `🐛 DEBUG` - Path resolution debugging
- `✅` - Successful operations
- `❌` - Errors
- `🔍` - File processing status

## 📁 Project Structure

```
screen_shots_filenaming/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🛠️ Development

### Key Components

- **`ScreenshotHandler`**: File system event handler class
- **`generate_filename()`**: AI-powered filename generation
- **`clean_file_path()`**: Path normalization utilities
- **`encode_image()`**: Base64 encoding for API requests

### Adding Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📋 Requirements

```
watchdog    # File system monitoring
openai      # AI integration
pillow      # Image processing
```

## 📝 License

This project is open source. Please check the license file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 💬 Support

If you encounter any issues or have questions, please open an issue on the repository.

---

**Happy screenshotting with smart naming! 📸✨**