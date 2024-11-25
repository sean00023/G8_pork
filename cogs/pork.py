# coding=utf-8
from discord.ext import commands
from discord import app_commands, Interaction
import json
import asyncio

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
        with open(filepath, 'a', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    def record_user_action(self, user_id, command, code=None):
        if user_id not in self.user_data:
            self.user_data[user_id] = []
        self.user_data[user_id].append({'command': command, 'code': code})
        self.save_json(self.user_cache_path, self.user_data)
        
    @app_commands.command()
    @app_commands.user_install()
    async def my_user_install_command(self, interaction: Interaction) -> None:
        print(f"玩家{interaction.user.name}已經加入了遊戲")
        await interaction.user.send(content=self.msg["start"])
    
        
    @app_commands.command(description='回復指令')
    async def reply(self, interaction: Interaction, code: str = None):
        if code == "我懂了":
            message = [
                item for item in self.msg
                if item["輸入指令"] == "\/reply" and item["參數"] == "我懂了" and item["訊息發送順序"] == 1.0
            ]
            await interaction.user.send(content=message["助手AI霸姬 回應"])
            if message["額外回應(比如影片\/圖片之類的)"]:
                await interaction.user.send(content=message["額外回應(比如影片\/圖片之類的)"])
            
            message_2 = [
                item for item in self.msg
                if item["輸入指令"] == "\/reply" and item["參數"] == "我懂了" and item["訊息發送順序"] == 2.0
            ]
            await asyncio.sleep(2)    # 等待    
            await interaction.user.send(content=message_2["助手AI霸姬 回應"])
            if message_2["額外回應(比如影片\/圖片之類的)"]:
                await interaction.user.send(content=message_2["額外回應(比如影片\/圖片之類的)"])
            
            message_3 = [
                item for item in self.msg
                if item["輸入指令"] == "\/reply" and item["參數"] == "我懂了" and item["訊息發送順序"] == 3.0
            ]
            await asyncio.sleep(2)    # 等待    
            await interaction.user.send(content=message_3["助手AI霸姬 回應"])
            if message_3["額外回應(比如影片\/圖片之類的)"]:
                await interaction.user.send(content=message_3["額外回應(比如影片\/圖片之類的)"])
        else:
            message = [
                item for item in self.msg
                if item["輸入指令"] == "\/reply" and item["參數"] == code
            ]
            
            if message:
                await interaction.user.send(content=message["助手AI霸姬 回應"])
                
                if message["額外回應(比如影片\/圖片之類的)"]:
                    await interaction.user.send(content=message["額外回應(比如影片\/圖片之類的)"])
     
        self.record_user_action(interaction.user.id, 'reply', code)
    
    @app_commands.command(description='開始遊戲')
    async def start(self, interaction: Interaction):
        message_1 = [
            item for item in self.msg
            if item["輸入指令"] == "\/start" and item["訊息發送順序"] == 1.0
        ]
        message_2 = [
            item for item in self.msg
            if item["輸入指令"] == "\/start" and item["訊息發送順序"] == 2.0
        ]
        message_3 = [
            item for item in self.msg
            if item["輸入指令"] == "\/start" and item["訊息發送順序"] == 3.0
        ]
        
        await interaction.response.send_message(f"玩家{interaction.user.name} 已經加入了遊戲")
        # 回應初始訊息
        await interaction.user.send(content=message_1["助手AI霸姬 回應"])
        await interaction.user.send(content=message_1["額外回應(比如影片\/圖片之類的)"])       
        await asyncio.sleep(2)    # 等待    
        # 發送第二個訊息
        await interaction.user.send(content=message_2["助手AI霸姬 回應"])
        await asyncio.sleep(2)  # 等待  
        # 發送第三個訊息
        await interaction.user.send(content=message_3["助手AI霸姬 回應"])
        await interaction.user.send(content=message_3["額外回應(比如影片\/圖片之類的)"])



