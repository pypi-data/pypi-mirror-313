import asyncio
import json
import logging
from typing import Any, Dict, Optional, Union

import websockets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocketClient:
    """
    Handles all the websocket related operations
    """

    def __init__(
        self,
        url: str,
        headers: Dict[str, str],
        loop: asyncio.AbstractEventLoop,
        json: bool = True,
    ):
        # URL is the WebSocket server URL.
        self.url = url

        # Headers to be sent with the WebSocket request.
        self.headers = headers

        # Event loop to use for async operations.
        self.loop = loop

        # WebSocket connection instance.
        self.__ws: Optional[websockets.WebSocketClientProtocol] = None

        # Logger for SocketClient.
        self._logger = logger.getChild(f"socketClient-{self.url}")

        # JSON flag to determine if the messages are JSON or not.
        self.json = json

    @property
    def ws(self) -> websockets.WebSocketClientProtocol:
        # Get the WebSocket connection, raising an error if not connected.
        if self.__ws is None:
            raise Exception("WebSocket is not connected")
        return self.__ws

    @property
    def connected(self) -> bool:
        # Return the connection status of the WebSocket.
        return self.__ws is not None and self.__ws.open

    async def connect(self):
        """
        Connect to the WebSocket server.
        """
        try:
            self._logger.info(f"Attempting to connect to WebSocket at {self.url}")
            self.__ws = await websockets.connect(self.url, extra_headers=self.headers)
            self._logger.info("WebSocket connection established")
            asyncio.create_task(self._listen())
        except Exception as e:
            self._logger.error(f"Error connecting to WebSocket: {e}")
            raise

    async def send(self, message: Any):
        """
        Send a message to the WebSocket server.
        """
        try:
            if not self.__ws:
                raise Exception("WebSocket is not connected")

            dump_data = json.dumps(message) if self.json else message

            self._logger.info(f"Sending message: {dump_data}")
            await self.__ws.send(dump_data)

        except Exception as e:
            self._logger.error(f"Error sending message: {e}")
            raise

    async def _listen(self):
        """
        Listen for messages from the WebSocket server.
        """
        try:
            if not self.__ws:
                raise Exception("WebSocket is not connected")

            self._logger.info("Started listening to WebSocket messages")
            async for message in self.__ws:
                self._logger.debug(f"Received message: {message}")
                await self._handle_message(message)
        except Exception as e:
            self._logger.error(f"Error listening to WebSocket: {e}")
            raise

    async def _handle_message(self, message: Union[str, bytes]):
        """
        Handle the message received from the WebSocket.
        """
        try:
            message_data = json.loads(message)
            self._logger.info(
                f"Handling message of type: {message_data.get('type', 'unknown')}"
            )
            await self.on_message(message_data)
        except json.JSONDecodeError as e:
            self._logger.error(f"Failed to decode message: {str(e)}")
        except Exception as e:
            self._logger.error(f"Unexpected error handling message: {str(e)}")
            self._logger.exception(e)

    async def on_message(self, message_data: Dict[str, str]):
        """
        Placeholder for handling messages, to be implemented by subclasses or instances.
        """
        self._logger.info(f"Received message: {message_data}")

    def close(self):
        """
        Close the WebSocket connection.
        """
        if self.__ws:
            self._logger.info("Closing WebSocket connection")
            self.loop.create_task(self.__ws.close())
