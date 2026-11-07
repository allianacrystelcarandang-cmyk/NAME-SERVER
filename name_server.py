import asyncio
import json
from datetime import datetime

HOST = '127.0.0.1'
SERVIZI={"time":(HOST,6001),"echo": (HOST,6002)}

#funzione per la risposta
async def reply(writer,data):
    payload = json.loads(data)+"\n"
    writer.write(payload.encode())
    await writer.drain()

