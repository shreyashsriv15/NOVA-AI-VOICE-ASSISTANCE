import speech_recognition as sr
import webbrowser
import time
import musiclibrary
import requests
import google.generativeai as genai
import asyncio
import edge_tts
import pygame
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(
   api_key=os.getenv("GEMINI_API_KEY")
)

newsapi=os.getenv("NEWS_API_KEY")

weatherapi=os.getenv("WEATHER_API_KEY")
recognizer = sr.Recognizer()


model = genai.GenerativeModel("gemini-2.5-flash")



async def _speak(text):
    communicate = edge_tts.Communicate(
        text,
        voice="en-IN-NeerjaNeural"
    )

    await communicate.save("voice.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    try:
        os.remove("voice.mp3")
    except:
        pass

def speak(text):
    asyncio.run(_speak(text))

    
def aiProcess(command):
    prompt = f"""
    You are Nova.
    Answer in maximum 4 sentences.
    Be concise and conversational.

    User: {command}
    """

    response = model.generate_content(prompt)

    return response.candidates[0].content.parts[0].text

def get_weather(city):
   url=(
      f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={weatherapi}&units=metric"
   )
   r=requests.get(url)
   data=r.json()

   if data["cod"]!=200:
    return "City not Found"
   temp=data["main"]["temp"]
   desc = data["weather"][0]["description"]

   return f"The temperature in {city} is {temp} degree celsius with {desc}"

def process_command(c):
   if(c.lower()=="open google"):
      speak("opening google")
      webbrowser.open("https://google.com")
   elif("open facebook" in c.lower()):
       speak("opening facebook")
       webbrowser.open("https://facebook.com")
   elif("open youtube" in c.lower()):
       speak("opening youtube")
       webbrowser.open("https://youtube.com")
   elif("open linkedin" in c.lower()):
       speak("opening linkedin")
       webbrowser.open("https://linkedin.com")
   elif("open instagram" in c.lower()):
       speak("opening instagram")
       webbrowser.open("https://instagram.com")
   elif("open cha tgpt" in c.lower()):
       speak("opening chat gpt")
       webbrowser.open("https://chatgpt.com")
   elif(c.lower().startswith("play")):
      song=c.lower().replace("play"," ").strip()
      print(song)
      link = musiclibrary.music[song]
      if link:
       webbrowser.open(link)
      else :
         speak("Song not found")
         print(song)  
   elif ("news" in c.lower()):
      r=requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
      data = r.json()
      articles = data["articles"]
      # print(data) [for debugging]
      for article in articles[:5]:
        headline = article["title"]

        print(headline)
        speak(headline)

   elif("weather" in c.lower()):
      city=c.lower().replace("weather","").strip()
      if city:
         result=get_weather(city)
         print(result)
         speak(result)
      else:
         speak("Please tell me the city name")
      
         response = aiProcess(c)
         print(response)
         speak(response)
   elif "exit" in c.lower() or "quit" in c.lower():
    speak("Goodbye , Hope you have a great day ahead")
    exit()
  

      
   

if __name__ == "__main__":

    speak("Nova online. How may I assist you today?")

    while True:
      #   Listen for the wake word "Nova"
      #    obtain audio form the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
         print("Listening...")
         audio = r.listen(source)
         print("Recongnizing...")
         try:
            word = r.recognize_google(audio)
            print(repr(word))
            
            if(word.lower()=="nova"):
            
               speak("Yes sir!!")
               
               

               # Listen for the command 
               with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
                command = recognizer.recognize_google(audio)

                process_command(command)


        #  exception for wait time 
         except sr.WaitTimeoutError:
            print("No speech detected")
        # exceptional case when computer doesnt understan our voice
         except sr.UnknownValueError:
            print("Could not understand audio")
        # catch all block
         except Exception as e:
            print("Error:", e) 