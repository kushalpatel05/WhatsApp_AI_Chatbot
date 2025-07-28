WhatsApp AI Chatbot
This AI Chatbot automates WhatsApp replies using Groq's LLM, reading chats via pyautogui and pyperclip, and responding in a personalized Hinglish/Gujlish style based on conversation context and sentiment. While currently configured for WhatsApp Web, its core AI logic is adaptable for other messenger platforms with UI automation adjustments.

Features
AI-Powered Responses: Utilizes Groq's powerful Large Language Models (LLMs) to generate human-like replies.

WhatsApp Automation: Automates message reading and sending on WhatsApp Web using GUI automation (pyautogui).

Contextual Conversations: Builds conversation history to provide relevant and coherent responses.

Multilingual & Sentiment Aware: Detects language (Hindi, Gujarati, English) and sentiment to tailor the bot's tone and response style.

Configurable Bot Persona: Easily customize the bot's name and conversation memory length via environment variables.

Smart Polling: Implements an exponential backoff mechanism to reduce resource usage when no new messages require a reply.

Error Handling: Includes robust error handling for GUI interactions and API calls.

Technologies Used
Python 3.x: The core programming language.

Groq API: Powers the conversational AI, utilizing models like meta-llama/llama-4-scout-17b-16e-instruct for intelligent responses.

pyautogui: Automates mouse and keyboard interactions for screen scraping and UI control.

pyperclip: Facilitates copying and pasting text to/from the system clipboard.

python-dotenv: Manages environment variables securely (e.g., API keys).

textblob: Provides sentiment analysis capabilities.

langdetect: Detects the language of incoming messages.

re (Regular Expressions): Used for robust chat parsing and cleaning.

time: For managing delays and polling intervals.

Setup and Installation
Follow these steps to get the AI Chatbot up and running on your local machine:

1. Prerequisites
Python 3.8+: Ensure Python is installed. You can download it from python.org.

pip: Python's package installer, usually comes with Python.

2. Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

(Replace your-username and your-repo-name with your actual GitHub details)

3. Set up Environment Variables
Create a file named .env in the root directory of your project (the same directory as chatbot.py). Add the following variables:

GROQ_API_KEY="gsk_YOUR_GROQ_API_KEY_HERE"
BOT_NAME="Kushal, Mummy" # Your bot's name(s), comma-separated if multiple variants
KEEP_LAST_N_MESSAGES=8 # Number of past messages to send to the LLM for context

GROQ_API_KEY: Obtain your API key from the Groq Console. Keep this key secret and never commit it to version control.

BOT_NAME: Define the name(s) your bot will use or be referred to. This helps the bot understand when a message is from itself.

KEEP_LAST_N_MESSAGES: Controls how many of the most recent messages are sent to the LLM for conversational context.

4. Install Dependencies
Install the required Python packages using pip:

pip install -r requirements.txt

requirements.txt content:

certifi==2025.7.9
dotenv==0.9.9
groq==0.29.0
langdetect==1.0.9
PyAutoGUI==0.9.54
pyperclip==1.9.0
python-dotenv==1.1.1
regex==2024.11.6
textblob==0.19.0

5. Download NLTK Data for TextBlob
textblob relies on NLTK data. After installing textblob, run the following command to download the necessary corpora:

python -m textblob.download_corpora lite

This will download only the essential data for basic textblob functionalities.

6. Adjust PyAutoGUI Coordinates (Crucial Step!)
This project uses pyautogui to interact with the WhatsApp Web interface by clicking and dragging at specific screen coordinates. These coordinates are hardcoded in chatbot.py and are highly dependent on your screen resolution and WhatsApp Web layout. They will need to be adjusted for your specific setup.

To find your coordinates:

Open WhatsApp Web on your browser.

Run the get_cursor.py script:

python get_cursor.py

Move your mouse cursor to the following locations on your screen and note down the (x, y) coordinates printed by get_cursor.py:

WHATSAPP_ICON_COORD: The coordinate where you click to open WhatsApp (e.g., from your taskbar/dock).

CHAT_SELECT_START_COORD: The top-left corner of the chat area where messages begin.

CHAT_SELECT_END_COORD: The bottom-right corner of the chat area where messages end.

DESELECT_CLICK_COORD: An empty area in WhatsApp Web where you can click to deselect text after copying (e.g., near the top-right of the chat window).

CHAT_INPUT_COORD: The coordinate of the message input box at the bottom of the chat.

Open chatbot.py and update the WHATSAPP_ICON_COORD, CHAT_SELECT_START_COORD, CHAT_SELECT_END_COORD, DESELECT_CLICK_COORD, and CHAT_INPUT_COORD variables with your newly found coordinates.

Example of get_cursor.py output:

(1248, 1050) # Example coordinate

7. OS-Specific PyAutoGUI Dependencies (Linux/macOS)
While PyAutoGUI is cross-platform, some operating systems require additional system-level packages for full functionality (especially for screenshots and robust control).

For Linux:

sudo apt-get install scrot # For pyautogui.screenshot()
sudo apt-get install python3-xlib # For mouse/keyboard control
sudo apt-get install python3-tk # For PyAutoGUI's alert/message boxes

For macOS:

pip install pyobjc-core pyobjc

Usage
Once you have configured the coordinates and installed all dependencies:

Ensure WhatsApp Web is open and visible on your screen.

Run the main chatbot script:

python chatbot.py

The bot will periodically check for new messages, generate replies using the Groq LLM, and send them. You will see console output indicating its actions.

Limitations
Hardcoded Coordinates: The primary limitation is the reliance on fixed screen coordinates, making it sensitive to screen resolution changes or UI updates in WhatsApp Web.

WhatsApp Web Format: The chat parsing logic (clean_whatsapp_chat, is_last_message_from_sender) is specifically designed for WhatsApp's clipboard text format. Changes to this format by WhatsApp could break the parsing.

UI Automation Fragility: Automating GUI interactions is less robust than using official APIs. Unexpected pop-ups, network delays, or minor UI changes can disrupt the bot's operation.

No Official API: This project works by simulating user interaction, as WhatsApp does not provide an official public API for this kind of automation.

Examples
grok_example.py: This file provides a simple, standalone example of how to interact with the Groq LLM using the groq Python library. It demonstrates basic chat completion without the UI automation aspect.

License
This project is open-source and available under the MIT License. (It's recommended to create a LICENSE file in your repository).
