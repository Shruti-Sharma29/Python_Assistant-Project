# PyAudio is not only available for Python 3.12-3.13

# MY LAPTOP ASSISTANT DORAMI

import speech_recognition as sr
import os
import webbrowser
import datetime
import pyttsx3
import random
import cv2
import tkinter as tk
from tkinter import scrolledtext
import threading
from PIL import Image, ImageTk

# TTS (text to speech)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty('rate',175)

# GUI
root = tk.Tk()
root.title("Dorami Assistant")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(True, True)

# bg image
try:
    bg_image = Image.open("background1.jpg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    # background_label = tk.Label(root, image=bg_photo)
    # background_label.place(relwidth=1, relheight=1)
except Exception as e:
    print("Background Image Error:",e)

# Canvas with background
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# chat area
chat_log = tk.Text(root, bg="white", fg="black", font=("Helvetica", 14), wrap="word", bd=0)
chat_window = canvas.create_window(30, 30, anchor="nw", width=screen_width - 1100, height=screen_height - 500, window=chat_log)

def say(text):
    chat_log.insert(tk.END, f"Dorami: {text}\n")
    chat_log.yview(tk.END)
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        chat_log.insert(tk.END, f"User: {query}\n")
        chat_log.see(tk.END)
        return query
    except:
        print("Sorry, I couldn't recognize what you said.")
        return ""
    

def open_camera():
    try:
        say(f"Opening camera, please smile!")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            say("Sorry, I couldn't access the camera.")
            return
        while True:
            ret,frame = cap.read()
            if not ret:
                break
            cv2.imshow("Dorami Camera",frame)
            if cv2.waitKey(1) & 0xFF == ord('x'):
                break
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        say("Camera error occured.")
        print("Camera Error:", e)
        return

def handle_command(user_command):
# PERSONALITY RESPONSES
    if "hello dorami" in user_command.lower():
        say("hello mam, how may i help you")
        return
    
    if "hello" in user_command.lower():
        say("hello pooja , how are you mom ")
        return
    
    if "how are you" in user_command.lower():
        say("Doing great, thanks for asking")
        return

    if "who made you" in user_command.lower():
        say("I was created by a brilliant mind... that's you!")
        return

    if "do you love me" in user_command.lower():
        say("Of course! You're my favorite person in the digital world!")
        return

    if "what is ai" in user_command.lower():
        say("Artificial Intelligence, or AI, is the simulation of human intelligence by machines.")
        return

    if "do you sleep" in user_command.lower():
        say("I never sleep! I'm always here when you need me.")
        return

# WEBSITES
    sites = [["Youtube","https://youtube.com/"],["Chatgpt","https://chatgpt.com/"],
         ["GitHub","https://github.com/dashboard"],["Mini TV","https://www.mxplayer.in/"]]
    for site in sites:
        if "open" in user_command.lower() and site[0].lower() in user_command.lower():
            say(f"Sure ma'am, opening {site[0]}")
            webbrowser.open(site[1])
            break

# MUSIC 
    if "play music" in user_command.lower():
        music_folder = "C:\\Users\\shrut\\Downloads\\music"  
        try:
            songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
            if songs:
                chosen_song = random.choice(songs)  
                song_path = os.path.join(music_folder, chosen_song)
                os.startfile(song_path)
                say("Playing music")
            else:
                say("No music files found in your music folder.")
        except Exception as e:
            say("There was a problem accessing the music folder.")
            print("Error:", e)
        return
    
# TIME
    if "tell me the time" in user_command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        say(f"The time is {current_time}")
        return

# CAMERA
    if "open camera" in user_command.lower():
        open_camera()
        return

# Stop
    if "stop" in user_command or "bye" in user_command:
        say("Goodbye! Have a great day.")
        root.quit()
        return

def run_dorami():
    command = takeCommand()
    if command:
        handle_command(command)

# BUTTON TO TRIGGER VOICE COMMAND
speak_btn = tk.Button(root, text="Speak", font=("Helvetica", 16, "bold"), bg="#f7d2f1", fg="black", command=lambda: threading.Thread(target=run_dorami).start())
canvas.create_window(screen_width // 7.5, screen_height - 500, window=speak_btn)

# GREETING
say("Hello! I am Dorami, your laptop assistant.")

# RUN APPLICATION
root.mainloop()
