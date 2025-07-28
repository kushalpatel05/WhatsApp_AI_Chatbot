# AI Chatbot for WhatsApp 
AI Chatbot automates WhatsApp replies using Groq's powerful Large Language Model (LLM), reading chats via `pyautogui` and `pyperclip` for seamless desktop integration. It's designed to respond in a personalized Hinglish/Gujlish style, adapting to conversation context and sentiment. While currently configured for WhatsApp Web, its core AI logic is highly adaptable for integration with other messenger platforms through UI automation adjustments.

## Features
* **Automated WhatsApp Replies** :- Automatically reads new messages from WhatsApp Web and generates relevant responses.
* **Groq LLM Integration** :- Leverages Groq's high-performance LLMs (e.g., LLaMA-4 Scout) for intelligent and contextual replies.
* **Multilingual and Cultural Tone** :- Detects language (Hindi, Gujarati, English) and adjusts response tone to a friendly, casual Hinglish/Gujlish style, incorporating emojis and slang.
* **Sentiment Awareness** :- Analyzes the sentiment of incoming messages and adjusts the bot's tone to be supportive, cheerful, or empathetic.
* **Conversation Memory** :- Maintains a short-term memory of recent messages to provide contextually relevant replies.
* **Error Handling** :- Includes robust error handling for UI interactions and API calls, with a smart polling mechanism to reduce resource usage.
* **Configurable** :- Easy to set up with environment variables for API keys, bot name, and conversation memory depth.

## Technologies Used
* **Python 3.12.6** :- The core programming language.
* **Groq API** :- Powers the conversational AI, utilizing the LLaMA 4 model for intelligent responses.
* **pyautogui** :- Automates keyboard and mouse interactions for reading chat history and sending messages on WhatsApp Web.
* **pyperclip** :- Manages copy-paste operations to/from the system clipboard for chat data transfer.
* **python-dotenv** :- To manage environment variables securely (API keys and configurations).
* **textblob** :- Provides sentiment analysis capabilities.
* **langdetect** :- Detects the language of chat messages.
* **re** :- Python's built-in module for regular expressions, used for parsing chat history.
* **os, time** :- Standard Python libraries for system interaction and date/time operations.

## Setup and Installation
Follow these steps to get the AI Chatbot up and running on your local machine:
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```
    (Replace `your-username` and `your-repo-name` with your actual GitHub details.)
    
2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
    
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Configure Environment Variables:**
    Create a file named `.env` in the root directory of your project (the same directory as `chatbot.py`) and add the following:
    ```
    GROQ_API_KEY="gsk_YOUR_GROQ_API_KEY_HERE"
    BOT_NAME="Kushal" # Or your desired bot name, comma-separated for multiple variants (e.g., "Kushal, Buddy")
    KEEP_LAST_N_MESSAGES=8 # Number of last messages to keep for context (default: 6)
    ```
    * Get your `GROQ_API_KEY` from the [Groq Console](https://console.groq.com/keys).

5.  **Adjust PyAutoGUI Coordinates:**
    This script relies on fixed screen coordinates, which are highly dependent on your screen resolution and WhatsApp Web layout.
    * Open WhatsApp Web on your browser.
    * Run the `get_cursor.py` script included in this repository:
        ```bash
        python get_cursor.py
        ```
    * Move your mouse cursor over the following elements on your WhatsApp Web interface and note down the printed `(X, Y)` coordinates:
        * The WhatsApp desktop application icon (if you click it to open WhatsApp initially).
        * The top-left corner of the main chat area (where messages start).
        * The bottom-right corner of the main chat area (to select all visible messages).
        * An empty space within the chat window to deselect text after copying.
        * The message input box at the bottom of the chat.
    * Update the corresponding coordinate variables in `chatbot.py` (e.g., `WHATSAPP_ICON_COORD`, `CHAT_SELECT_START_COORD`, `CHAT_SELECT_END_COORD`, `DESELECT_CLICK_COORD`, `CHAT_INPUT_COORD`) with your newly found coordinates.
      
## Usage
To start the AI Chatbot, ensure WhatsApp Web is open and logged in on your desktop. Then run:
```bash
python chatbot.py
```
The bot will continuously monitor your WhatsApp chats and respond to new messages from others based on the configured logic.
