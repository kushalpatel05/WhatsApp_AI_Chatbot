import pyautogui  # The pyautogui module in Python is used to automate mouse and keyboard actions.
import pyperclip  # The pyperclip module in Python is used to copy and paste text to/from the system clipboard  
import time       # The time module in Python provides functions to work with time — such as delays, current time, timestamps, and performance measurement.


while True:
    a = pyautogui.position()     # pyautogui.position() is used to get the current position of the mouse cursor on the screen. it is imported from := pyautugui_docs(General Functions)
    print(a)

    # Coordinates for the open app(whatsapp): 1248, 1050
    # select the text coordinates from: (664,170) to: (1874, 919)
    # for deselect click on the coordinates (1862,826)
    # coordinates (793,970) to click the chatbox of whatsapp web