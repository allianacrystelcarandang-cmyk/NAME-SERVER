import asyncio
import json
NOME_SERVER_HOST="127.0.0.1"
NOME_SERVER_PORT=6000

async def richiestaNome(nomeServizio):
    print(" connessione al name server")
    reader, writer = await asyncio.open_connection(NOME_SERVER_HOST,NOME_SERVER_PORT)
    richiesta={"cmd": "lookup", "servizio": nomeServizio}
    writer.write((json.dumps(richiesta)+"\n").encode())
    await writer.drain()

    risposta=await reader.readline()
    rispostaJ=json.loads(risposta.decode())
    writer.close()
    await writer.wait_closed()
    return rispostaJ

async def connessione(host,port,messaggio):
    reader, writer = await asyncio.open_connection(host,port)
    writer.write((json.dumps(messaggio)+"\n").encode())
    await writer.drain()
    risposta=await reader.readline()
    rispostaJ=json.loads(risposta.decode())
    writer.close()
    await writer.wait_closed()
    return rispostaJ

async def main():
    informaazioniServizio = await richiestaNome("time")
    print(informaazioniServizio)

    if informaazioniServizio.get("stato") == "ok":  # se il servizio esiste guardi l'host e la porta
        host = informaazioniServizio.get("host")
        port = informaazioniServizio.get("port")

        messaggioTempo = {"cmd": "time"}

        oraAdesso = await connessione(host, port, messaggioTempo)
        print(oraAdesso)
    else:
        messaggioTempo = ("errore")


if __name__ == "__main__":
    asyncio.run(main())







