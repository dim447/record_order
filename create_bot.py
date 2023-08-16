from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

TOKEN1 = "5193152234:AAHrzbU1Q1jqYN4Zejbu7azzpvm9BF7fqx4"  # Токен телеграм AnapaTestBot
# TOKEN1 = "6004218271:AAEIvG8nf1vsEenq5nZ6hZBj5n9wKoL8T58" # @AnapaBoltalkaBot


bot = Bot(token=TOKEN1)
dp = Dispatcher(bot, storage=storage)
