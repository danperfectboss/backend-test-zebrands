import requests
#if do you wnat know more about the how to create a bot, go to my fithub profile and search "bot telegram"
class MessageTelegram:
    def __init__(self,text):
        self.text = text

    #this funtion is for send messages to telegram using python
    def sendMessage(self):
        #the chat id 
        id = "-1001391177861"
        #token send it by the botfather
        token = "1700551505:AAELnpXsEwcUJRhoo575eW-QfM28247Wtzc"
        text= self.text
        #with this url send the message to the chanel configurated previously
        url= "https://api.telegram.org/bot"+token+"/sendMessage"
        params = {
            'chat_id':id,
            'text': text 
        }
        requests.post(url, params=params)

