import asyncio
import platform
import websockets
import json
import uuid
import hashlib
from datetime import datetime
from .sign import sign
from .logger import logger

class WebSocketClient:
    def __init__(self, server, app_id, app_secret):
        self.server = server
        self.app_id = app_id
        self.app_secret = app_secret
        self.reconnect_delay = 5
        self.running = False
        self.websocket = None
        self.process = None
        self.client_id = hashlib.md5(f"{str(uuid.uuid4())}::{int(datetime.now().timestamp() * 1000)}".encode('utf-8')).hexdigest()
        self._message_callback = None
        self._monitor_callback = None

    def set_message_handler(self, callback):
        self._message_callback = callback

    def set_monitor_handler(self, callback):
        self._monitor_callback = callback

    def connect(self):
        if not self.running:
            self.running = True
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self._websocket_loop())
            finally:
                loop.close()

    def disconnect(self):
        self.running = False

    async def _websocket_loop(self):
        while self.running:
            try:
                heartbeat_task = asyncio.create_task(self._heartbeat_loop())
                monitor_task = asyncio.create_task(self._monitor_loop())

                async with websockets.connect(self.server) as websocket:
                    self.websocket = websocket
                    logger.info(f'Connected to WebSocket server: {self.server}')
                    
                    while self.running:
                        try:
                            message = await websocket.recv()
                            logger.debug(f'Received message: {message}')
                            data = json.loads(message)
                            if self._message_callback:
                                asyncio.create_task(self._message_callback(data))
                            
                        except websockets.ConnectionClosed:
                            logger.info('WebSocket connection closed')
                            break
                            
                    heartbeat_task.cancel()
                    monitor_task.cancel()
                    try:
                        await heartbeat_task
                        await monitor_task
                    except asyncio.CancelledError:
                        pass
                    
            except Exception as e:
                logger.error(f'WebSocket connection error: {e}')

            if self.running:
                logger.info(f'Reconnecting in {self.reconnect_delay} seconds...')
                await asyncio.sleep(self.reconnect_delay)

    async def _heartbeat_loop(self):
        while self.running:
            try:
                await self.send_message('heartbeat', {})
            except Exception as e:
                logger.error(f'Error heartbeat: {e}')
            await asyncio.sleep(60)

    async def _monitor_loop(self):
        while self.running:
            try:
                if self._monitor_callback:
                    await self._monitor_callback()
            except Exception as e:
                logger.error(f'Error monitor: {e}')
            await asyncio.sleep(60)

    async def send_message(self, msg_type, data, trace_id = str(uuid.uuid4())):

        message = {
            'type': msg_type,
            'data': data,
            'appId': self.app_id,
            'clientId': self.client_id,
            'agentId': platform.node(),
            'traceId': trace_id,
            'timestamp': str(datetime.now().timestamp() * 1000)
        }
        message['signature'] = sign(message, self.app_secret)
        logger.debug(f'Send message: {message}')

        if self.websocket:
            await self.websocket.send(json.dumps(message))

