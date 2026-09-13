import os

import importlib

# VS Code/Pylance가 다른 Python 환경을 검사할 때도 가져오기 오류가
# 발생하지 않도록 런타임에 Discord.py를 불러옵니다.
discord = importlib.import_module("discord")
commands = importlib.import_module("discord.ext.commands")
from dotenv import load_dotenv


# ==========================================
# 기본 설정
# ==========================================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ==========================================
# 함수
# ==========================================


# 나중에 이곳에 코믹월드 관련 함수 추가


# ==========================================
# 이벤트
# ==========================================

@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user}")
    print(f"봇 ID: {bot.user.id}") # type: ignore


# ==========================================
# 명령어
# ==========================================


# 나중에 이곳에 Discord 명령어 추가


# ==========================================
# 봇 실행
# ==========================================

bot.run(TOKEN) # type: ignore