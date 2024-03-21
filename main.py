import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import pyautogui
import webbrowser
import openai
import sympy
import os
import shutil


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

engine.setProperty('rate', 140)
engine.setProperty('volume', 1)

weather_api_key = 'b4b34617e629b0d49d22604a60ef998c'
weather_base_url = 'http://api.openweathermap.org/data/2.5/weather'

openai.api_key = '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'

def talk(text):
    engine.say(text)
    engine.runAndWait()

def perform_complex_calculation(expression):
    try:
        x = sympy.symbols('x')
        result = sympy.simplify(expression)

        if 'sqrt' in expression:
            sqrt_value = sympy.sqrt(result)
            return f"The result is: {sqrt_value}"
        else:
            return f"The result is: {result}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                print(command)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return command

def get_day():
    try:
        current_date = datetime.date.today()
        day_of_the_week = current_date.strftime("%A")
        talk(f"Today is {day_of_the_week}")
    except Exception as e:
        talk("Sorry, I couldn't retrieve the day information")


def send_whatsapp_message(contact_name, message):

    contacts = {
        "khushi": " +917989944121",
        "nitish": "+917416909738",
        "dad":   "+9198493425924",
        "vaishu": "+917386543994"
    }

    try:
        if contact_name in contacts:
            contact_number = contacts[contact_name]
            pywhatkit.sendwhatmsg(contact_number, message, datetime.datetime.now().hour,
                                  datetime.datetime.now().minute + 1, wait_time=10)
            print(f"Message sent to {contact_name} ({contact_number}): {message}")
            talk(f"Message sent to {contact_name}: {message}")
            webbrowser.open('https://web.whatsapp.com/')
        else:
            print(f"Contact '{contact_name}' not found in your contacts.")
            talk(f"Contact '{contact_name}' not found in your contacts.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        talk("Sorry, I couldn't send the message.")

# Function to list files and directories in a given path
def list_files(path):
    try:
        files = os.listdir(path)
        return files
    except Exception as e:
        return str(e)

# Function to create a new directory
def create_directory(path, directory_name):
    try:
        new_dir = os.path.join(path, directory_name)
        os.mkdir(new_dir)
        return f"Directory '{directory_name}' created successfully."
    except Exception as e:
        return str(e)

# Function to create a new text file and write content to it
def create_text_file(path, file_name, content):
    try:
        with open(os.path.join(path, file_name), 'w') as file:
            file.write(content)
        return f"File '{file_name}' created and content written successfully."
    except Exception as e:
        return str(e)

# Function to read the content of a text file
def read_text_file(path, file_name):
    try:
        with open(os.path.join(path, file_name), 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return str(e)

# Function to delete a file or directory
def delete_file_or_directory(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
            return f"File '{os.path.basename(path)}' deleted successfully."
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return f"Directory '{os.path.basename(path)}' and its contents deleted successfully."
        else:
            return "Path not found."
    except Exception as e:
        return str(e)


def search_file_or_directory(root_path, name):
    try:
        for root, dirs, files in os.walk(root_path):
            if name in dirs or name in files:
                return os.path.join(root, name)
        return f"'{name}' not found."
    except Exception as e:
        return str(e)


def get_weather(city):
    try:
        params = {
            'q': city,
            'appid': weather_api_key,
            'units': 'metric'
        }
        response = requests.get(weather_base_url, params=params)
        weather_data = response.json()

        if weather_data['cod'] == 200:
            description = weather_data['weather'][0]['description']
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            city_name = weather_data['name']

            weather_message = f"The weather in {city_name} is {description}. The temperature is {temperature}°C, and humidity is {humidity}%."
            talk(weather_message)
        else:
            talk("Sorry, I couldn't fetch the weather information.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        talk("Sorry, I couldn't fetch the weather information.")

def answer_general_knowledge_question(question):
    try:
        result = wikipedia.summary(question, sentences=2)
        talk(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        talk("Sorry, I don't have information on that topic.")

        def view_to_do_list():
            if not to_do_list:
                talk("Your to-do list is empty.")
            else:
                talk("Here's your to-do list:")
                for i, task in enumerate(to_do_list, start=1):
                    talk(f"{i}. {task}")

to_do_list = []




def execute_command(command):
    if 'hey' in command:
        talk('Hi jashwanth! How may I assist you today?')

    elif 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is ' + time)

    elif 'date' in command:
        date = datetime.date.today()
        talk(date)

    elif "what's your name" in command:
        talk("I'm jarvis")

    elif 'day' in command:
        get_day()

    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
        print(joke)

    elif 'send a message' in command:
        talk("Whom do you want to send the message to?")
        contact_name = take_command()
        talk(f"What message do you want to send to {contact_name}?"
             f"")
        message = take_command()
        send_whatsapp_message(contact_name, message)


    elif 'add a task in my to do list' in command:
        talk("Sure, what task would you like to add?")
        task = take_command()
        to_do_list.append(task)
        talk(f"Got it! I've added '{task}' to your to-do list.")

    elif "what's in my to do list" in command:
        view_to_do_list()

    elif 'weather in' in command:
        city = command.replace('weather in', '').strip()
        get_weather(city)

    elif 'tell me ' in command:
        question = command.replace('tell me about', '').strip()
        answer_general_knowledge_question(question)

    elif 'open notepad' in command:
        talk('Opening Notepad.')
        pyautogui.hotkey('win', 'r')
        pyautogui.write('notepad')
        pyautogui.hotkey('enter')

    elif 'shutdown' in command:
        talk('Shutting down the computer.')
        pyautogui.hotkey('ctrl', 'alt', 'delete')
        pyautogui.press('right')
        pyautogui.press('right')
        pyautogui.press('right')
        pyautogui.press('enter')

    elif 'navigate to' in command:
        talk('for what location do you want to navigate to?')
        location = take_command()
        search_maps(location)

    elif 'ask open ai' in command:
        talk('What question would you like to ask OpenAI?')
        user_question = take_command()
        ask_openai(user_question)

    elif 'news' in command or 'get me the latest headlines' in command:
        talk('Sure! Fetching the latest news headlines.')
        get_news()

    elif 'calculate' in command:
        expression = command.replace('calculate', '')
        talk('Calculating')
        result = perform_complex_calculation(expression)
        talk(result)


    elif 'see you' in command:
        talk('Okay, bye! Have a good day!')
        exit()

    elif 'open browser' in command:
        talk('Opening browser')
        pyautogui.hotkey('win','r')
        pyautogui.write('brave')
        pyautogui.press('enter')


    elif 'list files' in command:
        path = input("enter the directory")
        result = list_files(path)
        talk(result)

    elif 'create directory' in command:
        path = input("Enter the directory path: ")
        directory_name = input("Enter the directory name: ")
        result = create_directory(path, directory_name)
        talk(result)

    elif 'create text file' in command:
        path = input("Enter the directory path: ")
        file_name = input("Enter the file name: ")
        content = input("Enter the file content: ")
        result = create_text_file(path, file_name, content)
        talk(result)

    elif 'read text file' in command:
        path = input("Enter the file path: ")
        result = read_text_file(path)
        talk(result)

    elif 'delete file' in command:
        path = input("Enter the file/directory path: ")
        result = delete_file_or_directory(path)
        talk(result)

    elif 'search file' in command:
        root_path = input("Enter the root directory path: ")
        name = input("Enter the file/directory name: ")
        result = search_file_or_directory(root_path, name)
        talk(result)

    elif 'thank you' in command:
        talk("It's my pleasure to assist you.Is there anything else I can help you with?")
        if 'no' or 'nothing' or 'nah' in command:
            exit()
        else:
            run_jarvis()

    elif 'whats in my to do list' in command:
        talk("here's your to do list" + view_to_do_list())


    else:
        talk("Sorry, I didn't get you. Can you please say it again?")



def get_news():
    api_key = 'd3c152afe5104248b2f6091e5d465843'
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

    response = requests.get(news_url)
    news_data = response.json()

    if 'articles' in news_data:
        articles = news_data['articles']
        talk('Here are the latest news headlines.')

        for article in articles:
            title = article['title']
            description = article['description']
            talk(title)
            talk(description)
            print(f'Title: {title}')
            print(f'Description: {description}')
            print('\n')

def search_maps(location):

    maps_url = f"https://www.google.com/maps/search/{location}"
    webbrowser.open(maps_url)

def ask_openai(user_question):
    try:
        response = openai.Completion.create(
                    engine="davinci",
            prompt=user_question,
            max_tokens=50
        )

        answer = response.choices[0].text.strip()
        talk(answer)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        talk("Sorry, I couldn't answer your question.")

def run_jarvis():
    command = take_command()
    print(command)
    execute_command(command)


while True:
    run_jarvis()
