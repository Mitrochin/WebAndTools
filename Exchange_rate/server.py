import aiofiles
import asyncio
import json
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from currency_service import CurrencyService
from datetime import datetime
from utils import ensure_log_directory

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()
    service = CurrencyService()

    def __init__(self):
        ensure_log_directory()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        # Отправка сообщения всем клиентам (Sending message to all clients)
        if self.clients:
            await asyncio.gather(*[client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        # Обработка входящих сообщений (Processing incoming messages)
        async for message in ws:
            if message.startswith('exchange'):
                parts = message.split()
                days = int(parts[1]) if len(parts) > 1 else 1
                if days > 10:
                    await ws.send("Number of days cannot be more than 10")
                else:
                    rates = await self.service.get_exchange_rates(days)
                    await self.log_command(message)
                    await ws.send(json.dumps(rates, indent=2))
            else:
                await self.send_to_clients(f"{ws.name}: {message}")

    @staticmethod
    async def log_command(command: str):
        # Логирование команды в файл (Logging command to file)
        async with aiofiles.open('logs/exchange_log.txt', mode='a') as file:
            await file.write(f'Command: {command}, Time: {datetime.now().isoformat()}\n')


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
