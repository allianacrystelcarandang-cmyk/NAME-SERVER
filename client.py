import asyncio
import json
NOME_SERVER_HOST="127.0.0.1"
NOME_SERVER_PORT=6000

async def richiestaNome(nomeServizio):
    print(" connessione al name server")
    reader, writer = await asyncio.open_connection(NOME_SERVER_HOST,NOME_SERVER_PORT)
    richiesta={"comando": "lookup", "servizio": nomeServizio}
    writer.write((json.dumps(richiesta)+"\n").encode())
    await writer.drain()

