from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.enums import ParseMode

from config import Config

start_bot = Bot(Config.token, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp_new_bots = Dispatcher(events_isolation=SimpleEventIsolation())

