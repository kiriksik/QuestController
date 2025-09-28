import mido
import asyncio
from config import MIDI_PORT, COMMANDS, NOTE_ON

try:
    outport = mido.open_output(MIDI_PORT)
except IOError:
    outport = None
    print(f"[WARN] MIDI порт '{MIDI_PORT}' не найден")


mapping = {}
base_note = 60  # начнём с До первой октавы
for i, cmd in enumerate(COMMANDS):
    note = base_note + i
    mapping[cmd] = mido.Message("note_on", channel=0, note=note, velocity=100)
    mapping[cmd.replace("on", "off")] = mido.Message("note_off", channel=0, note=note)

async def send_midi(cmd: str):
    if outport and cmd in mapping:
        msg = mapping[cmd]
        outport.send(msg)

        # 300 мс
        if msg.type == "note_on":
            await asyncio.sleep(NOTE_ON)
            note_off = mido.Message("note_off", channel=msg.channel, note=msg.note)
            outport.send(note_off)
    else:
        raise ValueError(f"Неизвестная команда MIDI: {cmd}")

