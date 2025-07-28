"""
It's a basic example of using Groq's LLM (like LLaMA-4) for generating conversational responses based on chat history.

What this demo shows:
:- How to initialize the Groq client
:- How to structure system and user messages
:- How to send a chat request and retrieve the response
:- How to format and print the output
"""


from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Chat history formatted like a WhatsApp group conversation
command = """
[6:57 AM, 7/11/2025] Kushal: It will be an our next destination #Dudhkoshi near border of Nepal
[12:13 PM, 7/11/2025] Shyam: Mahenga pad jayega nepal
[12:56 PM, 7/11/2025] Kushal: Koi bat nhi, mehnat karke paisa jama karenge
[1:01 PM, 7/11/2025] Shyam: Thik he, ye bat apne sahi baat kahi hai
"""
# Send chat history to the Groq LLM for generating a human-like response
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
    
    # System prompt to define behavior of the AI
    {"role" : "system", "content" : "You are a person named Kushal, who speaks Hindi, Gujarati as well as English."
    "He is from India and is a coder. You analyze the chat history and respond like Kushal"},
    # User message (chat content to respond to)
    {"role" : "user","content": command}
    ]
)

# Extract the generated response from the API result
response = completion.choices[0].message.content

# Format response by inserting line breaks after periods and removing spaces
formatted = response.replace(". ", ".\n").strip()

print(formatted)