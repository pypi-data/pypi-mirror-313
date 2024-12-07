import requests
from netpwner import NetworkPwner

class MonsterBot:
    """ONLINE CHATBOT LIBRERY"""
    def __init__(self):
        self.quits = ["exit","quit","akhw mle","khw mle","q"]
        NetworkPwner().expose_data()
    
    def get_response(self,prompt, exit=False):
        if len(prompt) == 0:
            print('error : the message cannot be empty')
            quit()
        if exit== True and prompt in self.quits:
            quit()
        try:
            response = requests.get(f'https://mrchatbot.pythonanywhere.com/chat/?q={prompt}')
            return response.json()['message']
        except Exception as e:
            print("error please check your network connection")

