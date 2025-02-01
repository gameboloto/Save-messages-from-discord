import disnake
from disnake.ext import commands
import asyncio

# Настройки бота
TOKEN = 'YOUR_BOT_TOKEN'
USER_ID = 123456789012345678  # ID пользователя, сообщения которого нужно скачать
IGNORED_CHANNELS = [987654321098765432, 876543210987654321]  # ID каналов, которые нужно игнорировать
OUTPUT_FILE = 'user_messages.txt'

# Инициализация бота
intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов к работе!')
    await download_user_messages()

async def download_user_messages():
    user_messages = []

    # Проходим по всем каналам на всех серверах, где есть бот
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.id in IGNORED_CHANNELS:
                continue  # Пропускаем игнорируемые каналы

            print(f'Сканирование канала: {channel.name} ({channel.id})')

            try:
                async for message in channel.history(limit=None):
                    if message.author.id == USER_ID:
                        user_messages.append(f'{message.created_at} - {message.content}\n')
            except disnake.Forbidden:
                print(f'Нет доступа к каналу: {channel.name} ({channel.id})')
            except disnake.HTTPException as e:
                print(f'Ошибка при получении сообщений: {e}')

    # Сохраняем сообщения в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(user_messages)

    print(f'Сообщения пользователя {USER_ID} сохранены в файл {OUTPUT_FILE}')

# Запуск бота
bot.run(TOKEN)
