import asyncio
import json
from datetime import datetime

#BRAINSTORMING
#name server --> tiene elenco dei servizi che ho
#time server --> tiene il tempo e l'orario
#echo server --> manda il testo ricevuto al client


HOST = '127.0.0.1'
SERVIZI={"time":(HOST,6001),"echo": (HOST,6002)}

#funzione per la risposta
#riceve i dati e li trasforma i una stringa json e poi li invia al client in byte
async def reply(writer,data):
    payload = json.dumps(data)+"\n" #trasformo un dizionario in una str
    writer.write(payload.encode())
    await writer.drain() #aspetto che il buffer sia vuoto

#funzione per la gestione del nome
#controlla se il servizio richiesto esiste e restituisce l'ip e la porta del servizio
#senò stampa errore
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
                    else:
                        risposta={ "stato":"errore", "messaggio":"servizio non esistente"}
                else:
                    risposta={"stato":"errore", "messaggio":"comando non esistente"}

            except (json.decoder.JSONDecodeError,UnicodeDecodeError):
                risposta={"stato":"errore", "messaggio":"json non valido"}
                await reply(writer,risposta)
    finally:
        writer.close()
        await writer.wait_closed()

#gestione del tempo
#fa la stessa cosa di quello di prima ma gestisce le richieste di orario
#restituisce l'orario dformattattato

async def gestioneTempo(reader, writer):
    try:
        while True:
            line = await reader.readline()
            if not line:
                break

            try:
                data = json.loads(line.decode())
                if data.get("cmd")== "time":
                    ora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    risposta={ "stato":"ok", "time":ora}
                else:
                    risposta = {"stato": "errore", "messaggio": "comando non esistente"}

            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                risposta = {"stato": "errore", "messaggio": "json non valido"}
                await reply(writer, risposta)

    finally:
         writer.close()
         await writer.wait_closed()

#gestione echo
async def gestioneEcho(reader, writer):
    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            try:
                data = json.loads(line.decode())
                if data.get("cmd") == "echo" and "text" in data:
                    testo=data.get("text")
                    risposta={ "stato":"ok", "text":testo}
                else:
                    risposta={"stato":"errore", "messaggio":"comando non esistente"}
            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                risposta={"stato": "errore", "messaggio":"json non valido"}
            await reply(writer, risposta)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server_name= await asyncio.start_server(gestioneNome,HOST,6000)
    server_time= await asyncio.start_server(gestioneTempo,HOST,6001)
    server_echo = await asyncio.start_server(gestioneEcho,HOST,6002)

    print("name server iniziato sulla porta 6000")
    print("time server iniziato sulla porta 6001")
    print("echo server iniziato sulla porta 6002")
    async with server_name, server_time, server_echo:
        await asyncio.gather(
            server_name.serve_forever(),
            server_echo.serve_forever(),
            server_time.serve_forever(),
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("-- server spento --")















