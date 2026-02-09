import webbrowser #for  using google
import speech_recognition as sr # to convert speech to text 
import pyttsx3 # to convert text to speech
import jarvis.song as song
import requests # to get direct information to veriable
import openai # to integrate ai with  code
import urllib.parse # for searching on google & youtube
import os # for open apps and more




r = sr.Recognizer()
engine = pyttsx3.init()
news_api="65a5e39021944e94a0a446640d4609c2"
def writeNote(c,title): # to append text to exicting file
   
    

# AppleScript to find and append to existing note
    script = f'''
    osascript -e '
    tell application "Notes"
        activate
        tell account "iCloud"
            set theNotes to notes of folder "Notes" 
            repeat with n in theNotes
                if name of n is "{title}" then
                    set body of n to body of n & "<br><br>{c}"
                    exit repeat
                end if
            end repeat
        end tell
    end tell'
    '''

    os.system(script)
def listen(): # for listening the commands
     with sr.Microphone() as source:
                 print("jarvis active...")
                 try:
                    audio = r.listen(source)
                    print("recognizing...")
                    command = r.recognize_google(audio)
                    print(command)
                    return command
                 except Exception as e:
                    print(e)
                    return ""

def ai_proccess(c): # if all other conditon is false the the command handal by ai
        openai.api_key = "##############"
    

        
        response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": c}
        ],
        max_tokens=150,
        temperature=0.7
        )
        return response['choices'][0]['message']['content']

def speak(text): # to convert text to speech
    engine.say(text)
    engine.runAndWait()

def action(c): # action on user command 
    if "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open spotify" in c.lower():
        os.system("open -a 'Spotify'")
    elif "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open wathsapp" in c.lower():
        os.system("open -a 'WathsApp'")
    elif "open" in c.lower():
        l= c.lower().replace("open","").strip().split() # for opeing apps on device
        k=[word.capitalize() for word in l]
        app_name=" ".join(k)
        os.system(f"open -a '{app_name}'")
        # name=" ".join(word.capitalize() for word in app.split())
           
    
    elif "news" in c.lower(): # for news 
        r=requests.get(f" https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}")
        if r.status_code == 200:
           data =r.json()
           articles = data.get("articles", [])
           for  article in articles:
             speak(article['title'])

    

    elif "search" in c.lower(): # for searching on google
        query = c.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")

    elif "play" in c.lower():# for playing on youtube
        query = c.replace("play", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
    elif "write a note" in c.lower(): # for writing a note in notes
            speak("sure sir what is the title of the note ??")
 
            title=listen() 
            #for creating a file in notes in icloude folder
            script = f'''
            osascript -e 'tell application "Notes"
                activate
                tell account "iCloud"
                    make new note at folder "Notes" with properties {{name:"{title}"}}
                end tell
            end tell'
            '''
            os.system(script)
            while True:
                speak("hmmmm")
                while True:
                 sentence=listen() # for listening the text
                 if(sentence != ""): # if user is not saying anything than wait until thay start saying
                     break # if thay say anything than break this 
                if "stop writing" in sentence: # if command in stop writing than break the proccess
                    speak("note comleted")
                    break
                
                
                
                writeNote(sentence,title) # appand the text to the given title
           


    

        
    # else :
    #    output= ai_proccess(c)
    #    speak(output)






if (__name__=="__main__"):
    while   True:
        
   
        try:
        
          with sr.Microphone() as source:
             print("Listening...")
             audio = r.listen(source,timeout=2,phrase_time_limit=1)
             print("recognizing...")
             word = r.recognize_google(audio)
             print(word)
          if(word.lower()=="jarvis"):
              speak("ya")
            
              action(listen())
        except Exception as e:
            print(e)
            
        
          

