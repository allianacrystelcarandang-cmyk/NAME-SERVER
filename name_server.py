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

#funzione per la gestione del nome
async def gestioneNome(reader, writer):
    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            try:
                data = json.loads(line.decode())
                if data.get("cmd")== "lookup":
                    servizio=data.get("servizio")

                    if servizio in SERVIZI:
                        host, port = SERVIZI[servizio]
                        risposta={ "stato":"ok", "servizio":servizio, "host":host, "port":port}






