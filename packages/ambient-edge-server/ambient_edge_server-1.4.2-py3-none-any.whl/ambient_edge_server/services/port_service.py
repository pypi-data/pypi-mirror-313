import asyncio
import socket
import subprocess
from typing import Any, Dict, Set

import websockets
from cryptography.fernet import Fernet

from ambient_client_common.utils import logger


class PortService:
    """
    Currently not used
    """

    def __init__(self) -> None:
        self._forwarded_ports = {}
        self._server_processes = {}
        self.tasks: Set[asyncio.Task] = set()

    async def init(self) -> None:
        pass

    async def cleanup(self) -> None:
        logger.info("Cleaning up PortService ...")
        # Terminate any active SSH processes
        process: subprocess.Popen
        for process in self._server_processes.values():
            process.terminate()
        self._server_processes.clear()
        logger.info("PortService cleanup complete")

    async def get_ports(self) -> Dict[int, str]:
        pass

    async def get_port(self, port: int) -> Any:
        pass

    async def get_port_forwards(self) -> Dict[int, str]:
        pass

    async def forward_port(self, port: int, websocket_url: str) -> None:
        logger.info(f"Forwarding port {port} to {websocket_url} ...")
        task = asyncio.create_task(self.forward_port_task(port, websocket_url))
        self.tasks.add(task)
        task.add_done_callback(lambda task: self.tasks.remove(task))

    async def forward_port_task(self, port: int, websocket_url: str) -> None:
        try:
            # Connect to the WebSocket server
            async with websockets.connect(websocket_url) as websocket:
                self._forwarded_ports[port] = websocket_url
                logger.debug(
                    "added port {} to forwarded_ports [ws url: {} ]",
                    port,
                    self.forwarded_ports.get(port),
                )

                # Receive the encryption key from the server
                key = await websocket.recv()
                fernet = Fernet(key.encode())
                logger.debug("created fernet key [ {} chars ]", len(key))

                # Forward traffic between WebSocket and local port (asynchronous)
                logger.info("forwarding traffic between WebSocket and local port ...")

                async def send_to_websocket(reader: asyncio.StreamReader) -> None:
                    while True:
                        data = await reader.read(1024)
                        logger.debug(
                            "received data from local port [ {} bytes ]", len(data)
                        )
                        if not data:
                            break
                        await websocket.send(fernet.encrypt(data))

                async def receive_from_websocket(writer: asyncio.StreamWriter) -> None:
                    async for message in websocket:
                        logger.debug(
                            "sending data to local port [ {} bytes]", len(message)
                        )
                        writer.write(fernet.decrypt(message))
                        await writer.drain()

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.bind(("localhost", port))  # Bind to the local port
                    sock.listen(1)
                    conn, addr = sock.accept()
                    with conn:
                        reader, writer = asyncio.StreamReader(), asyncio.StreamWriter(
                            conn, None, None, True
                        )
                        await asyncio.gather(
                            send_to_websocket(reader), receive_from_websocket(writer)
                        )

        except Exception as e:
            print(f"Error forwarding port {port}: {e}")

    @property
    def forwarded_ports(self) -> Dict[int, str]:
        """Currently forwarded ports

        Returns:
            Dict[int, str]: Dictionary of shape {port: websocket_url}
        """
        return self._forwarded_ports

    @forwarded_ports.setter
    def forwarded_ports(self, value: Dict[int, str]) -> None:
        self._forwarded_ports = value
