import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import time 
import wikipedia
import pywhatkit as pwk
import subprocess
import user_config
import smtplib


engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',160)


def speak(Audio):
    engine.say(Audio)
    engine.runAndWait()

def command():
    content = " " 
    while content == " " :     
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
         print("Say something!")
         audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
         content =  r.recognize_google(audio , language = 'en-in')
         print("you said...." + content)
        except Exception as e:
         print("please try again...")

    return content

def main_process():
    while True:
     request = command().lower()
     #for giving response on saying hello keyword
     if 'friday' in request:
        speak("Hello sir , how may i assist you ")

     #if user want to play music    
     elif 'play music' in request:
        speak("playing music..") 
        song = random.randint(1,3)
        if song ==1:
           webbrowser.open("https://youtu.be/FZLadzn5i6Q?si=SgLr_vQ7UbhSltfj")
        elif song==2:
           webbrowser.open("https://youtu.be/kKljXVVkgS4?si=gml6TOZbSiVwfX25")
        elif song==3:
           webbrowser.open("https://youtu.be/9T-Zbxg9X_4?si=dcu7Wm3cPuW-gbKF")  

      #for asking the date and time         
     elif 'what is the time now' in request:
        now_time = datetime.datetime.now().strftime("%H:%M")
        speak("Current time is " + str(now_time))   
     elif 'tell me the day' in request:
        now_day = datetime.datetime.now().strftime("%d:%m:%Y")
        speak("today is " + str(now_day))   

      #making and adding tasks in our todo list  
     elif 'new task' in request:
        task = request.replace("new task" , "")
        task = task.strip()
        if task!= "":
           speak("adding task" + task)
           with open("todo.txt", "a") as file:
              file.write(task + "\n")

      # deleting the task from your todo list
     elif 'delete task' in request:
        task_todelete = request.replace("delete task","").strip()
        if task_todelete != "":
           with open("todo.txt","r") as file:
              tasks = file.readlines()
           tasks = [task.strip() for task in tasks if task.strip() != task_todelete] 

           with open("todo.txt","w") as file:
              for task in tasks:
                 file.write(task + "/n") 
           speak(f"deleted task : {task_todelete} ")
        else:
           speak("specify the task to delete") 

     #to open and read your todo list
     elif 'speak the task' in request:
        with open("todo.txt","r") as file:
           speak("the work we have to do today is " + file.read())

     #to give notification in your laptop     
     elif 'show work' in request:
        with open ("todo.txt","r") as file:
           tasks = file.read()
        notification.notify(
           title = "Today's work",
           message = tasks
        )
      # opening any website on google
     elif 'open ' in request:
        website = request.replace("open","").strip()
        if not website.startswith(("https://","http://")):
           if "." not in website:
              website += ".com"
           website = "https://" + website  
        webbrowser.open(website)
        speak(f"opening{website}")


     # to open any app in your desktop    
     elif 'go to' in request:
        query = request.replace("go to",'')
        pyautogui.press("super")
        pyautogui.typewrite(query)
        pyautogui.sleep(2)
        pyautogui.press("enter")
        speak(f"openning :{query}")

    # to take screenshort 
     elif 'take screenshot' in request:
        screenshot_name = "screenshort_" + str(int(time.time())) + ".png" 
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_name)
        speak(f"Screen shot saved as {screenshot_name}")

# using wikipedia for searching any of the keyword 
     elif 'give information about' in request:
        #request = request.replace("Friday",'').strip()
        print("searching for : ", request)
        request = request.replace("give information about",'')
        request = request.replace("Friday",'')
        
        print(request)
        result = wikipedia.summary(request , sentences=3)
        print(result)
        speak(result)
#searching on google  
     elif 'google search about' in request:
        request = request.replace("Friday",'')
        request = request.replace("google search about",'')
        webbrowser.open("https://www.google.com/search?q="+request)
        speak ("here's the result you want")
#sending whatsapp message
     elif 'send message' in request:       
        try:  
           speak("who do you want to send message")
           contact_name = command()
           unwanted_words = ["send message to", "send","whatsapp", "message", "to","tu"]
           for word in unwanted_words:
              contact_name = contact_name.replace(word, "").strip()
           speak("What message do you want to send")
           message = command()

           subprocess.run(["cmd","/c","start whatsapp://"],shell=True)
           time.sleep(3)

           pyautogui.hotkey("ctrl","f")
           time.sleep(1)

           pyautogui.write(contact_name)
           time.sleep(1)

           pyautogui.press("down")
           time.sleep(1)
           pyautogui.press("enter")
           time.sleep(1)           

           pyautogui.write(message)
           time.sleep(1)
           pyautogui.press("enter")

           speak(f"message send to {contact_name}")
        except Exception as e:
           speak("sorry I couldn't send the message please try again")
           print("Error",e)   
        #sending emails    
     elif 'send email' in request:
        s = smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login("devc51290@gmail.com",user_config.gmail_password)
        message = """ 
      this is the mail sent through my ai agent 

""" 
        s.sendmail("devc51290@gmail.com","praveen08042002@gmail.com",message)
        s.quit()
        speak("email is successfully sent") 

   #  elif 'send email' in request:
   #         try:
   #          # 🎤 Ask for recipient's email via voice command
   #          speak("Whom do you want to send an email?")
   #          reciver_email = command()  # ✅ CALL function to get the actual email

   #          # 🔹 Clean email (replace "at the rate" with "@")
   #          reciver_email = reciver_email.replace("at the rate", "@")

   #          # 🔹 Remove unwanted words
   #          unwanted_words = ["send email to", "send", "mail", "email", "to", "tu", " ","I","want"]
   #          for word in unwanted_words:
   #                reciver_email = reciver_email.replace(word, "").strip()

   #          speak("What should be the subject of the email?")
   #          subject = command()

   #          speak("What should be the content of the email?")
   #          content = command()

   #          # 📩 Email Structure
   #          email_body = f"Subject: {subject}\n\n{content}"

   #          # 🎯 Gmail SMTP Configuration
   #          senders_email = "devc51290@gmail.com"  # 👈 Replace with your Gmail
   #          senders_password = ""  # 👈 Use Gmail App Password (Not normal password!)

   #          # 🔹 SMTP Server Setup
   #          server = smtplib.SMTP("smtp.gmail.com", 587)
   #          server.starttls()
   #          server.login(senders_email, senders_password)
   #          server.sendmail(senders_email, reciver_email, email_body)
   #          server.quit()

   #          speak(f"Email has been successfully sent to {reciver_email}")

   #         except Exception as e:
   #          speak("Sorry, I couldn't send the email. Please try again.")
   #          print("Error:", e)
     elif  'wake up jarvis' in request :  # Example voice command: "ask AI what is the meaning of life?"
        
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')       #getting details of current voice
        engine.setProperty('voice',voices[0].id)
        engine.setProperty('rate',180)
        speak("yes sir , Any Question? feel free to ask I can help you with that")
        
        while True: 
         user_question = command()  # Function to capture voice input

         if 'thanks jarvis' in user_question.lower():
            speak("my pleasure sir, now friday will take care of you, if you need anthing please let me know")
            
            
            engine.stop()  
            engine = pyttsx3.init()  
            voices = engine.getProperty('voices')  
               
               # Switch back to Female Voice (Voice 1) for Friday
            engine.setProperty('voice', voices[1].id)  
            engine.setProperty('rate', 160)
            speak("Friday is now active, sir.")  
            break  # Exit Jarvis mode

         ai_response = openai_request.chat_with_ai(user_question)
         print(ai_response)
         speak(ai_response)



main_process()           