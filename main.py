import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk, ImageSequence
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import random
import threading

# initialize the recognition and tts engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set the voice to female
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 


jokes = {
    "en": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call a fake noodle? an impasta!"
    ],
}

facts = {
    "fact":[
        "did you know that Bats are the only flying mammals",
        "did you know About 75 percent of the human brain is made of water.",
        "C I A is created to investigate the assassination of president george washington , so basically C I A is as old as the USA"
    ]
}

# variable to control listening state
is_listening = True

#   make her speak using the pyttxs3
def speak(text):
    engine.say(text)
    engine.runAndWait()

# its a function created to listen to commands or... uk
def listen():
    with sr.Microphone() as source:
        print("Adapting to environment...")
        recognizer.adjust_for_ambient_noise(source, duration=1) 
        print("\nListening...")   
        try:
            audio = recognizer.listen(source, timeout=10)
            print("Processing...")
            command = recognizer.recognize_google(audio, language="en-US")  
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Can you repeat?")
            return None
        except sr.RequestError as e:
            speak(f"Sorry, but , my speech service is down. ")
            return None
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return None

# the commands that user shout give...or input  
def handle_command(command, root, start_button):
    global is_listening
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "what's up" in command:
        speak("What's good?")
    elif "introduce yourself" in command :
        speak("sure ,... Hello everyone , "
        "I am Iris , a voice assistant created to help users in their daily life . "
        "I have many feature like telling time and date , opening apps , searching for music and information ."
        " I can also entertain you by telling you some hillarious jokes  . What makes me unique or special is that , unlike many voice assistant , i can continously listen for user command until user says stop listeng or exit , and also , "
        "I can automatically shut don if user says Shut down. So if u have question ,"
        " Feel free to ask")
    elif "who are you" in command or "what are you" in command :
        speak("I am iris , a voice assistant created to help you")
    elif "time" in command :
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "who created you" in command or "crafted you" in command :
        speak("I was created by the goated development team , The Debug Squad ")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}.")
    elif "open" in command or "launch" in command:
        app = command.replace("open", "").replace("launch" , "").strip()
        
        filler_words = ["iris", "irish"]
        for word in filler_words:
            app = app.replace(word, "").strip()

        speak(f"Opening {app}")
        if "chrome" in app:
            os.system("start chrome")
        elif "notepad" in app:
            os.system("notepad")
        elif "spotify" in app:
            webbrowser.open("https://open.spotify.com")
        elif "youtube" in app:
            webbrowser.open("https://www.youtube.com")
        elif "instagram" in app:
            webbrowser.open("https://www.instagram.com")
        elif "telegram" in app:
            telegram_path = r"C:\Users\NAOD\AppData\Roaming\Telegram Desktop\Telegram.exe"
            os.system(f'start "" "{telegram_path}"')
        elif "calculator" in app: 
            os.system("calc")
        elif "settings" in app:
            os.system("start ms-settings:")
        else:
            speak(f"Sorry, I don't know how to open {app}.")
    elif "joke" in command or "entertain me" in command:
        joke = random.choice(jokes["en"])
        speak(joke) 
    elif "tell me something interesting" in command :
        fact = random.choice(facts["fact"])
        speak(fact)
    elif "who" in command or "what" in command or "where" in command:
        speak("i am not sure but if u want me to search for an information , u can ask me to search for ya")

    elif "play" in command or "listen to" in command or "play the song" in command:
        song = command.replace("play", "").replace("listen to", "").replace("play the song", "").strip()

        filter_words = ["iris", "want", "irish"]
        for word in filter_words:
            song = song.replace(word, "").strip()

        if song:
            speak(f"opening {song} on Spotify")
            # Open Spotify search with the query
            search_url = f"https://open.spotify.com/search/{song.replace(' ', '%20')}"
            webbrowser.open(search_url)
        else:
            speak("Please tell me the name of the song or artist you want to play")
    elif "search" in command :
        speak("What would you like to search for?")
        search_query = listen()
        if search_query:
            search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            speak(f"Searching for {search_query} on Google.")
            webbrowser.open(search_url)
        else:
            speak("man c'mon u asked me to search and u aren't saying any shit")
    elif "stop listening" in command :
        speak("Sure, I stopped listening. Click the mic button to enable listening")
        is_listening = False
        start_button.config(state="normal")
    elif "exit" in command or "shut down" in command or "bye" in command :
        speak("Goodbye! Have a great day.")
        root.destroy()
    elif "iris" in command:
        speak("Yeah, user?")
    else:
        speak("Sorry, I don't have this feature currently.")



def start_listening(root, start_button):
    global is_listening 
    speak("Hello, I am Iris , your voice assistant. How can I assist you today?")
    while True:
        if is_listening:
            command = listen()
            if command:
                handle_command(command, root, start_button)
                if "exit" in command or "bye" in command:
                    break

# if u want to make it start listening again 
def enable_listening(start_button):
    global is_listening
    is_listening = True
    speak("hello again , how can i help")
    start_button.config(state="disabled")

# threading for the gif bg
class AnimatedGIF:
    def __init__(self, canvas, gif_path):
        self.canvas = canvas
        self.frames = []
        gif = Image.open(gif_path)
        self.width, self.height = 800, 600 # set the background to full with
        
        for frame in ImageSequence.Iterator(gif):
            frame = frame.resize((self.width, self.height), Image.Resampling.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(frame))
        
        self.current_frame = 0
        self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.frames[self.current_frame])
        self.running = True
        self.update_frame()

    def update_frame(self):
        if self.running:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.canvas.itemconfig(self.image_id, image=self.frames[self.current_frame])
            self.canvas.after(80, self.update_frame)


def create_gui():
    root = tk.Tk()
    root.title("I.R.I.S - Voice Assistant")
    root.geometry("800x600")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    gif_path = "Img/background.gif"
    AnimatedGIF(canvas, gif_path)

    logo_image = Image.open("Img/logoimg.png")
    logo_image = logo_image.resize((300, 100), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = Label(root, image=logo_photo, bg="#05001e")
    logo_label.image = logo_photo
    logo_label.place(relx=0.5, rely=0.18, anchor="center")  

    
    mic_image = Image.open("Img/mic.png")
    mic_image = mic_image.resize((80, 80), Image.Resampling.LANCZOS)
    mic_photo = ImageTk.PhotoImage(mic_image)

    
    mic_label = Label(
        root,
        image=mic_photo,
        bg="#05001e",  
        borderwidth=0,
        highlightthickness=0,
    )
    mic_label.image = mic_photo
    mic_label.place(relx=0.5, rely=0.9, anchor="center")

    
    mic_label.bind("<Button-1>", lambda event: threading.Thread(target=enable_listening, args=(mic_label,)).start())

    listening_thread = threading.Thread(target=start_listening, args=(root, mic_label))
    listening_thread.daemon = True
    listening_thread.start()

    root.mainloop()

if __name__ == "__main__":
    create_gui()