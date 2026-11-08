import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "9120376953:AAG7xxKbAQDZISNyAxZpS1Qp-PD6Eo_MDRw")
DEFAULT_STYLE = os.getenv("DEFAULT_STYLE", "smart")

