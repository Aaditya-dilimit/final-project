import os
import csv
import smtplib
import webbrowser
import wikipedia
import pygame
import datetime
import pyttsx3
import speech_recognition as sr
import sys
import openai
import random
from newsapi import NewsApiClient
from newspaper import Article

def hello():
    speak("hello sir , I'm your virtual personal assistant")

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("Sir, I'm your assistant please tell me how may I help you")

def get_speech_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak("Please speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio_data = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio_data, language="en-in").lower()
        print(f"Speech input: {query}\n")
        return query
    except sr.UnknownValueError:
        speak("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        speak(f"Error with the speech recognition service; {e}")
        return None
        
def speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    
def open_site(strr):
    with open('sites.csv', 'r') as file:
        websites = list(csv.reader(file))

    lisss = strr.split()
    found = False

    for x in lisss:
        for website in websites:
            if x in website:
                url = website[1]
                speak(f"Opening {x}")
                webbrowser.open(url)
                found = True
                break 
        if found:
            break

    if not found:
        speak("Website isn't present in my list. Please say its URL.")
        url = get_speech_input()
        speak(f"Opening {url}")
        webbrowser.open(url)

def open_and_search():
    speak("Where do you want to search? Google or YouTube")
    search_engine = get_speech_input()

    speak(f"What do you want to search on {search_engine.capitalize()}: ")
    query = get_speech_input()

    search_url = f"https://www.{search_engine}.com/search?q={query}"
    webbrowser.open(search_url)

def search_wikipedia():
    speak("What do you want to know about")
    query = get_speech_input()

    try:
        result = wikipedia.summary(query, sentences=2)
        speak(f"Wikipedia Summary for '{query}':")
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Ambiguous term. Please choose a more specific query. Options: {', '.join(e.options)}")
    except wikipedia.exceptions.PageError:
        print(f"No page found for the term '{query}' on Wikipedia.")

def get_date_time_info(choice):
    current_datetime = datetime.datetime.now()

    if 'time' in choice:
        str_time = current_datetime.strftime("%H:%M:%S")
        speak(f"Sir, the time is {str_time}")
    elif 'year' in choice:
        year = current_datetime.year
        speak(f"Sir, the year is {year}")
    elif 'day' in choice:
        day = current_datetime.day
        speak(f"Sir, the day is {day}")
    elif 'month' in choice:
        month_name = current_datetime.strftime("%B")
        speak(f"Sir, the month is {month_name}")
    elif 'today' in choice:
        formatted_today = current_datetime.strftime("%Y-%B-%d")
        speak(f"Sir, today is {formatted_today}")
    elif 'date' in choice:
        date = current_datetime.date()
        speak(f"Sir, the date is {date}")

def send_email():
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')

        speak("What should I say?")
        content = get_speech_input()

        to = input("Enter receiver's email address: ")
        speak("Enter receiver's email address")
        server.sendmail('youremail@gmail.com', to, content)

        speak("Email has been sent!")
        server.close()
    except Exception as e:
        print(e)
        speak("Sorry my friend. I am not able to send this email")

def play_playlist():

    print("Which playlist do you want to play")
    choice = get_speech_input()
    playlists = {}  

    with open("playlist.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            playlist_name, playlist_path = row[0], row[1]
            playlists[playlist_name] = playlist_path

    playlist_path = playlists.get(choice)

    if playlist_path:
        speak(f"Playing {choice} songs")
        play_playlist(playlist_path)
    else:
        speak("Playlist not found")

    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

    audio_files = [file for file in os.listdir(playlist_path) if file.endswith(('.mp3', '.wav', '.ogg'))]

    if not audio_files:
        speak("No audio files found in the specified folder.")
        return

    print("Order of songs in this playlist is -")
    for i, audio_file in enumerate(audio_files):
        print(f"{i + 1} ==> {audio_file}")

    for audio_file in audio_files:
        file_path = os.path.join(playlist_path, audio_file)

        pygame.mixer.music.load(file_path)

        print(f"Playing: {audio_file}")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    print("All audio files played.")

def play_song(song_name):
    with open('songs.csv', 'r') as file:
        all_song_names = csv.reader(file)
        for row in all_song_names:
            if row[0] == song_name:
                song_path = row[1]

    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

    try:
        pygame.mixer.music.load(song_path)
        print(f"Playing: {song_path}")
        speak(f"Playing: {song_path}")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:
        print(f"Error: {e}")
    finally:
        pygame.mixer.quit()

def add_song():
    song_name = input("Enter the name of the song: ")
    speak("Enter the name of the song")
    song_path = input("Enter the path of the song's file: ")
    speak("Enter the path of the song's file")
    
    lis = [song_name, song_path]
    
    with open("songs.csv", 'a') as file:
        wr = csv.writer(file)
        wr.writerow(lis)

def add_playlist():
    song_name = input("Enter the name of the playlist: ")
    speak("Enter the name of the playlist")
    song_path = input("Enter the path of the playlist's directory: ")
    speak("Enter the path of the playlist's directory")
    
    lis = [song_name, song_path]
    
    with open("playlist.csv", 'a') as file:
        wr = csv.writer(file)
        wr.writerow(lis)

def music():
    print("Do you want to play a particular song or a playlist?")
    speak("Do you want to play a particular song or a playlist?")
    opt = get_speech_input()

    if 'song' in opt:
        speak("Please say the name of the song")
        song_name = get_speech_input()
        play_song(song_name)
    elif 'playlist' in opt:
        play_playlist()
    else:
        speak("Invalid option. Please say 'song' or 'playlist'.")

def toss():
    result = random.choice(["Heads","Tails"])
    print(result)

def use_chatgpt():
    openai.api_key = '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'
    speak("What do you want to ask to ChatGPT")
    prompt = get_speech_input()

    response = openai.Completion.create(engine="text-davinci-003",prompt=prompt,temperature=0.7,max_tokens=150,n=1)
    result = response['choices'][0]['text'].strip()
    speak(result)

def todo(choice):
    if 'add' in choice:
        add_todo()
    elif any(keyword in choice for keyword in ['disply','show']):
        show_todo()

def add_todo():
    speak("What do you want me to add in your to-do list")
    to_do = get_speech_input()
    deadline = input("Type Deadline: ")
    
    with open("todo.csv", 'r', newline="") as file:
        reader = csv.reader(file)
        
        for row in reader:
            if row and row[0] == to_do:
                speak("task already in the list")
                break
        
        else:
            with open("todo.csv", 'a', newline="") as file:
                wr = csv.writer(file)
                wr.writerow([to_do, deadline])
                speak("task added to the to-do list")

def show_todo():
    with open("todo.csv", 'r', newline="") as file:
        reader = csv.reader(file)
        for item in reader:
            print(f"task - {item[0]} and deadline - {item[1]}")

def headlines(topic):
    newsapi = NewsApiClient('29a1ce1fb06b4b87b6042c9ab1567c21')
    headlines = newsapi.get_top_headlines(q=topic, language='en')
    if headlines['totalResults'] > 0:
        headlines_list = []
        for article in headlines['articles']:
            speak(f"Headline: {article['title']}")
            print(f"Source: {article['url']}")
            print("-" * 30)
            headline = article['title']
            source = article['url']
            headlines_list.append((headline, source))
        return headlines_list
    else:
        print(f"No headlines found for the topic: {topic}")

def news_summary(headlines_list, index):
    if headlines_list and 0 <= index < len(headlines_list):
        headline, source = headlines_list[index]
    
        summary = get_article_summary(source)
      
        print(f"\nSummary for headline #{index + 1}:")
        print(f"Headline: {headline}")
        print(f"Source: {source}")
        print(f"Summary: {summary}")
    else:
        print("Invalid index. Please provide a valid index.")

def get_article_summary(article_url):
    article = Article(article_url)
    article.download()
    article.parse()
    article_text = article.text
    sentences = article_text.split('.')
    summary = '. '.join(sentences[:3])
    return summary

def news():
    speak("Topic for the news")
    topic = get_speech_input()

    for keyword in ["technology", "science", "business", "entertainment", "health", "sports", "politics", "world news", "environment", "education"]:
        if keyword in topic:
            topic = keyword
            break
    headlines(topic)
    speak("do you want summary on any new \n if yes tell me the headline number \n else type exit")
    
    while True:
        choice = input("Input : ")
        if choice.isnumeric():
            news_summary(headlines(), int(choice))
            break
        elif "exit" == choice :
            break
        else :
            print("Invalid Input")
            continue

def exit():
    speak("Bye sir! , Have a great day!")
    sys.exit()

def main():
    greet()

    while True:
        choice = get_speech_input()
        if choice:
            if "hello" in choice:
                hello()
            elif 'search' in choice:
                open_and_search()
            elif 'open' in choice:
                open_site(choice)
            elif 'wiki' in choice:
                search_wikipedia()
            elif any(keyword in choice for keyword in ['time', 'today', 'date', 'month', 'day']):
                get_date_time_info(choice)
            elif any(keyword in choice for keyword in ['gmail', 'mail', 'email']):
                send_email()
            elif any(keyword in choice for keyword in ['coin', 'toss']):
                toss()
            elif "add song" in choice:
                add_song()
            elif "add playlist" in choice:
                add_playlist()
            elif any(keyword in choice for keyword in ['use gpt', 'use chatgpt']):
                use_chatgpt()
            elif any(keyword in choice for keyword in ['bye', 'end program', 'exit program']):
                exit()
            elif any(keyword in choice for keyword in ['to do','todo','to-do']):
                todo(choice)
            else:
                speak(f"you said {choice}")
        else:
            print("Speech input is None. Please try again.")

main()