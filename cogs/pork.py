# coding=utf-8
from discord.ext import commands
from discord import app_commands, Interaction
import json

async def setup(bot):
    await bot.add_cog(pork(bot))
    
class pork(commands.Cog):

    def __init__(self, bot, json_path="data/pork.json" , user_cache_path="data/user_data.json"):
        self.bot = bot
        self.msg = self.load_json(json_path)
        self.user_cache_path = user_cache_path
        self.user_data = {}
        print(f"Cog initialized with bot: {self.bot}")
    
    def load_json(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
        
    def save_json(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    def record_user_action(self, user_id, command, code=None):
        if user_id not in self.user_data:
            self.user_data[user_id] = []
        self.user_data[user_id].append({'command': command, 'code': code})
        self.save_json(self.user_cache_path, self.user_data)
        
    @app_commands.command(description='回復指令')
    async def reply(self, interaction: Interaction, code: str = None):
        try:
            if code is None or code == 'start': #排除 /replay start
                message = self.msg["_fail"]
            else:
                message = self.msg[code] if code in self.msg else self.msg["_fail"]
            await interaction.response.send_message(content=message,  ephemeral=True)
            
            if code == 'GAME':
                image_url = 'https://imgur.com/Utpl32S'
                await interaction.user.send(content=image_url)
            if code == 'HAND':
                image_url = 'https://imgur.com/VsDCyIQ'
                await interaction.user.send(content=image_url)
            if code == 'LURE':
                image_url = 'https://imgur.com/R6j9yRi'
                await interaction.user.send(content=image_url)
     
            self.record_user_action(interaction.user.id, 'reply', code)
        except Exception as e:
            print(f"錯誤：{str(e)}")
            await interaction.response.send_message(self.msg["_error"] ,  ephemeral=True)
    
    @app_commands.command(description='開始遊戲')
    async def start(self, interaction: Interaction):
        try:         
            message = self.msg["start"]          
            await interaction.user.send(content=message)
            await interaction.response.send_message(f"玩家{interaction.user.name}已經加入了遊戲")
     
        except Exception as e:
            print(f"錯誤：{str(e)}")
            await interaction.response.send_message(self.msg["_error"],  ephemeral=True)
              