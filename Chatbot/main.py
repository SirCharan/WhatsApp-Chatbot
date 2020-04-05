#Import the Chatbot and neccessary stuff
from chatterbot import ChatBot 
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from selenium import webdriver
import time
import pickle

#Open Whatsapp with WebDriver and manually login from your mobile phone
whatsapp = webdriver.Chrome('chromedriver_win32/chromedriver.exe') 
whatsapp.get('https://web.whatsapp.com/')

#Training the ChatBot
bot= ChatBot('Bot') 
trainer = ChatterBotCorpusTrainer(bot)

os.chdir('chatterbot-corpus-master\chatterbot-corpus-master\chatterbot_corpus\data/')
corpus_path = 'english/'
filename = 'final_model.sav'
try:
    loaded_model = pickle.load(open(filename, 'rb'))
except FileNotFoundError:
    for file in os.listdir(corpus_path):
        model=trainer.train(corpus_path+file)
        pickle.dump(model, open(filename, 'wb'))

#Indentifying contact person and opening chat
contact_name=input("Enter Name Of Contact:")
person=whatsapp.find_elements_by_xpath('//span[@title="{}"]'.format(contact_name))
person[0].click()

#Define a flag to check repeated messages
flag='NULL'

incoming_message_tag=''#Find the div class of the incoming message
message_box=''#Find the div class of the message box
send_button=''#Find the div class of the send message button 
while True:
    #Identify last sent message
        message=whatsapp.find_elements_by_xpath('//div[@class="{}"]'.format(incoming_message_tag))[-1].text.split('\n')[0]
    if message==flag:
        continue
        time.sleep(5)
    elif message=="bye":
        break
    else:
        #Sending Response
        print(message)
        reply = bot.get_response(message)
        flag=str(reply)
        box=whatsapp.find_element_by_class_name(message_box)
        box.click()
        box.send_keys(flag)
        print(" Reply Sent:----"+flag)
        send=whatsapp.find_element_by_class_name(send_button)
        send.click()
        flag=message
