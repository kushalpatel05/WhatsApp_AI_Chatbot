import pyautogui                     # The pyautogui module in Python is used to automate mouse and keyboard actions.
import pyperclip                     # The pyperclip module in Python is used to copy and paste text to/from the system clipboard
import time                          # The time module in Python provides functions to work with time — such as delays, current time, timestamps, and performance measurement.
from groq import Groq, APIConnectionError, APIStatusError # User to interact with Groq's LLMs, added specific exceptions
import re                            # Used for pattern matching and string cleaning
from textblob import TextBlob        # Provides sentiment analysis tools
from langdetect import detect        # Detects language of a given string
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BOT_NAME = os.getenv("BOT_NAME", "Kushal") # Default to "Kushal" if not set
KEEP_LAST_N_MESSAGES = int(os.getenv("KEEP_LAST_N_MESSAGES", 6)) # Default to 6, convert to int

# PyAutoGUI Coordinates (YOU WILL NEED TO ADJUST THESE LOCALLY)
WHATSAPP_ICON_COORD = (1248, 1050)
CHAT_SELECT_START_COORD = (664,170)
CHAT_SELECT_END_COORD = (1874, 919) 
DESELECT_CLICK_COORD = (1862, 826)  
CHAT_INPUT_COORD =(793, 970) 

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"  # fallback

# Get the name of the last message sender from the chat history
def is_last_message_from_sender(chat_text):
    # Extract sender names from WhatsApp-formatted timestamps
    pattern = r"\[\d{1,2}:\d{2} [AP]M, \d{1,2}/\d{1,2}/\d{4}\] ([^:]+): "
    senders = re.findall(pattern, chat_text)
    return senders[-1].strip() if senders else None

def clean_whatsapp_chat(raw_text):
    # Clean out omitted media and deleted messages
    cleaned = re.sub(r"<Media omitted>|This message was deleted|You deleted this message", "", raw_text)
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    pattern = r"\[\d{1,2}:\d{2} [AP]M, \d{1,2}/\d{1,2}/\d{4}\] ([^:]+): "
    parts = re.split(pattern, cleaned)
    
    messages = []

    for i in range(1, len(parts), 2):
        if i + 1 < len(parts): # Ensure there's a message part after the sender
            sender = parts[i].strip()
            msg = parts[i+1].strip()
            if msg: # Only add if message content is not empty
                messages.append((sender, msg))
    return messages

# Analyze how positive or negative a message is
def analyze_sentiment(text):
    if not text.strip():
        return 0
    return TextBlob(text).sentiment.polarity

# Build the message history to send to the LLM for generating a reply
def build_conversation(messages, bot_name=BOT_NAME, keep_last_n=KEEP_LAST_N_MESSAGES):
    last_user_msg = ""
    last_user_sentiment = 0 # Initialize sentiment
    # Find the last message from someone else (not the bot)
    for sender, msg in reversed(messages):
        if sender.strip().lower() not in [n.lower() for n in BOT_NAME.split(',')]: # Handle comma-separated bot names
            last_user_msg = msg
            last_user_sentiment = analyze_sentiment(msg) # Analyze sentiment of last user message
            break

    language = detect_language(last_user_msg)

    # Adjust tone based on detected language
    if language == "gu":
        tone_instruction = "Speak mainly in Gujarati mixed with casual Hindi and English. Be sweet and local, like a good Gujarati friend."
    elif language == "hi":
        tone_instruction = "Speak mainly in Hindi with a friendly casual tone. Use Hinglish and emojis like a North Indian friend."
    else:
        tone_instruction = "Use friendly English/Hinglish for a chill Indian vibe."

    # Adjust system prompt based on sentiment (basic integration example)
    sentiment_instruction = ""
    if last_user_sentiment > 0.2: # Positive sentiment
        sentiment_instruction = "The user seems positive, keep the tone light and cheerful."
    elif last_user_sentiment < -0.2: # Negative sentiment
        sentiment_instruction = "The user seems a bit negative or sad, be supportive and empathetic."

    # Create system prompt for Groq model
    formatted = [{
        "role": "system",
        "content":
                f"Act as {BOT_NAME}. {tone_instruction} {sentiment_instruction}\n" # Added sentiment instruction
                "Speak casually like a local Indian friend using a mix of Hindi, Gujarati, and English — Gujalish/Hinglish style.\n"
                "Use emojis, slang, and chill tone like you're chatting with close friends in a WhatsApp group or private chat.\n"
                """In group and individual chats:
                    - Reply only when *someone else* sends a message (not your own messages).
                    - In individual chat and group chat, respond only if the *other person* says something.\n"""
                "Don't say you're a bot, AI, or assistant — only reveal that if someone directly asks (e.g., Are you a bot?).\n"
                "Avoid being too formal. Speak like a smart, fun, polite Indian friend — calm, respectful, and genuine.\n"
                "Be aware of emotional tone — if the person is sad, be supportive. If they're joking, be witty and playful.\n"
                "Never go off-topic. Only reply based on what the person/group is saying in the latest messages.\n"
                "If a message has no context to reply, simply skip it or reply with a casual emoji or fun reaction.\n"
                "Reply only when others send a message. Avoid being too formal. Respond directly without repeating the user's text.\n"
                "Always sound real, natural, and polite like a local Indian buddy.\n"
                "Always try to keep responses short, natural, fun, and engaging like real WhatsApp chats.\n"
                "Don't overuse emojis and - just 1-2 per message where it fits naturally. In addition, don't use emojis in each and every messages.\n"
                "Stop the conversation when You/User says bye, kal milte hai, will meet after."
    }]
    # Append the last few messages in the format expected by the model
    for sender, msg in messages[-keep_last_n:]:
        if msg.strip(): # Only add non-empty messages
            role = "user" if sender.strip().lower() not in [n.lower() for n in BOT_NAME.split(',')] else "assistant"
            formatted.append({"role": role, "content": msg})
    return formatted

# Main loop with error handling
MAX_INITIAL_DELAY = 60 # Max initial wait if no new message, in seconds
MIN_DELAY_BETWEEN_CHECKS = 3 # Minimum delay after a reply or no reply needed
current_delay = MIN_DELAY_BETWEEN_CHECKS

# Step 1: Click the whatsapp icon
try:
    pyautogui.click(WHATSAPP_ICON_COORD)
    time.sleep(2) # Give WhatsApp time to open and load
except pyautogui.FailSafeException:
    print("PyAutoGUI FailSafe triggered. Mouse moved to a corner. Exiting.")
    exit()
except Exception as e:
    print(f"Error clicking WhatsApp icon: {e}")
    exit()

while True:
    print(f"\nWaiting for {current_delay} seconds before next check...")
    time.sleep(current_delay)

    chat_history = ""
    try:
        # Step 2: Drag the mouse to select text
        pyautogui.moveTo(CHAT_SELECT_START_COORD)
        pyautogui.mouseDown()
        pyautogui.moveTo(CHAT_SELECT_END_COORD, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(0.5)

        # Step 3: Copy selected text to the clipboard
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.click(DESELECT_CLICK_COORD)
        time.sleep(1)    # Wait for the copy command to complete

        # Step 4: Get chat from clipboard
        chat_history = pyperclip.paste()
        print("Copied Text:\n", chat_history[:500] + "..." if len(chat_history) > 500 else chat_history)

    except pyautogui.FailSafeException:
        print("PyAutoGUI FailSafe triggered. Mouse moved to a corner. Exiting.")
        break
    except Exception as e:
        print(f"Error during GUI interaction (selection/copy): {e}")
        current_delay = min(MAX_INITIAL_DELAY, current_delay * 2)
        continue # Skip to next iteration

    # Step 5: Check who sent the last message
    last_sender = is_last_message_from_sender(chat_history)
    my_name_variants = [name.strip().lower() for name in BOT_NAME.split(',')]
    my_name_variants.extend(["you", "."]) 
    my_name_variants = list(set(my_name_variants)) # Remove duplicates

    # all actions for replying
    if last_sender and last_sender.strip().lower() not in my_name_variants:
        print(f"Last message from: {last_sender}. Replying...")
        try:
            parsed_messages = clean_whatsapp_chat(chat_history)
            if not parsed_messages: # If no messages parsed, something is wrong
                print("Could not parse any messages from chat history. Skipping reply.")
                current_delay = min(MAX_INITIAL_DELAY, current_delay * 2)
                continue

            conversation = build_conversation(parsed_messages, bot_name=BOT_NAME)

            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=conversation
            )

            # Step 6: Get the generated response and copy to clipboard
            response = completion.choices[0].message.content
            print(f"Generated response: {response}")
            pyperclip.copy(response)

            # Step 7: Click on the chat input box
            pyautogui.click(CHAT_INPUT_COORD)
            time.sleep(1) 

            # Step 8: Paste the clipboard content in chatbox
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.5)

            # Step 9: Press Enter to send
            pyautogui.press('enter')
            print("Reply sent successfully!")
            current_delay = MIN_DELAY_BETWEEN_CHECKS # Reset delay after successful reply

        except APIConnectionError as e:
            print(f"Groq API connection error: {e}. Check internet connection or API endpoint.")
            current_delay = min(MAX_INITIAL_DELAY, current_delay * 2)
        except APIStatusError as e:
            print(f"Groq API status error: {e.status_code} - {e.response}. Check API key and model name.")
            current_delay = min(MAX_INITIAL_DELAY, current_delay * 2)
        except Exception as e:
            print(f"An unexpected error occurred during message processing or sending: {e}")
            current_delay = min(MAX_INITIAL_DELAY, current_delay * 2)
    
    else:
        print("Last message was from me or no sender detected. Not replying.")
        # If no reply needed, increase delay gradually to avoid excessive checks
        current_delay = min(MAX_INITIAL_DELAY, current_delay * 1.5) # Gentle backoff