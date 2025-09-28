import os

from rtmidi.midiconstants import NOTE_ON

# --- Общие настройки ---
MEDIA_DIR = os.getenv("MEDIA_DIR", "./static/media") # Путь до файлов музыки
TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "./static/templates") # Путь до шаблонов страниц
MIDI_PORT = os.getenv("MIDI_PORT", "loopMIDI Port 1") # Имя порта MIDI из loopMidi
ARDUINO_BASE_URL = os.getenv("ARDUINO_BASE_URL", "http://192.168.0.55") # Адрес arduino
NOTE_ON = 0.3 # Время проигрыша ноты

# --- Состояние объектов ---
STATE = {
    "Свет_на_картину": False,
    "Кнопка_в_полу_1": False,
    "Кнопка_в_полу_2": False,
    "Кнопка_в_полу_3": False,
    "Светильник_1": False,
    "Светильник_2": False,
    "Светильник_3": False,
    "Светильник_4": False,
    "Светильник_5": False,
    "Светильник_6": False,
    "Символ_1": False,
    "Символ_2": False,
    "Символ_3": False,
    "Символ_4": False,
    "Символ_5": False,
    "Символ_6": False,
    "Статуетка_1": False,
    "Статуетка_2": False,
    "Статуетка_3": False,
}

# --- Все команды Arduino ---
COMMANDS = [
    "BYon", "BXon", "ADon", "AEon", "AFon", "AHon", "ANon", "AIon", "AOon",
    "AJon", "APon", "AKon", "AQon", "ALon", "ARon", "AMon", "ASon", "ATon",
    "AUon", "AWon", "AYon", "AZon", "BAon", "BBon", "BCon", "BEon", "BIon",
    "BJon", "BLon", "BKon", "BRon", "BPon", "BOon", "BMon", "BNon", "BSon",
    "BWon", "AAon", "ABon", "BTon", "BUon", "BVon"
]