"""
:author: Thomas Delaet <thomas@delaet.org>

Port for Domintell
:author: Zilvinas Binisevicius <zilvinas@binis.me>

"""
import socket
import time
import threading
import logging
from queue import Queue
import ssl
import serial
import serial.threaded
import websocket
import domipy

class Protocol(serial.threaded.Protocol):
    """Serial protocol."""

    def data_received(self, data):
        # pylint: disable-msg=E1101
        self.parser(data)


class DomintellException(Exception):
    """Domintell Exception."""
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)

class DomintellConnection():
    """
    Generic Domintell connection
    """
    def send(self, message, callback=None):
        """
        :return: None
        """
        raise NotImplementedError

class WSSConnection(DomintellConnection):
    """
        Wrapper for Secure Web Socket connection configuration
    """
    def __init__(self, address, parser=None, hello_interval=0):
        DomintellConnection.__init__(self)
        self.logger = logging.getLogger('domintell')
        self._address = address
        self.parser = parser
        self.hello_interval = hello_interval
        self.is_connected = False
        self.reconnect_interval = 30

        self.connect_socket()
        # build a read thread
        self._listen_process = threading.Thread(None, self.read_daemon,
                                         "domintell-process-reader", (), {})
        self._listen_process.daemon = True
        self._listen_process.start()

        # build a writer thread
        self._write_queue = Queue()
        self._write_process = threading.Thread(None, self.write_daemon,
                                               "domintell-connection-writer", (), {})
        self._write_process.daemon = True
        self._write_process.start()

        # build a ping thread
        self._hello_process = threading.Thread(None, self.hello_daemon,
                                            "domintell-ping-writer", (), {})
        self._hello_process.daemon = True

    def connect_socket(self):
        try:
            self._socket = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
            self._socket.connect(self._address)
            self.is_connected = True

        except OSError as osError:
            self.is_connected = False
            if osError.strerror == 'A socket operation was attempted to an unreachable host' :
                self.logger.error("Could not open socket, host is unreacheble")
                time.sleep(self.reconnect_interval)
            else:
                self.logger.error("Could not open socket, \
                              no messages are read or written to the bus")
                raise DomintellException("Could not open socket port") from osError
                
        except Exception as ex:
            self.is_connected = False
            self.logger.error("Could not open socket, \
                              no messages are read or written to the bus")
            raise DomintellException("Could not open socket port") from ex

    def stop(self):
        """Close socket."""
        self.logger.warning("Stop executed")
        try:
            self._socket.close()
        except Exception as ex:
            self.logger.error("Error while closing socket")
            raise DomintellException("Error while closing socket") from ex
        time.sleep(1)

    def feed_parser(self, data):
        """Parse received message."""
        lines = data.splitlines()

        for line in lines:
            self.parser.feed(data)

    def send(self, message, callback=None):
        """Add message to write queue."""
        assert isinstance(message, domipy.Message)
        self._write_queue.put_nowait((message, callback))

    def read_daemon(self):
        """Reads incoming data."""
        while True:
            try:
                data = self._socket.recv()
                self.feed_parser(data)
            except websocket.WebSocketConnectionClosedException :
                self.logger.warning("Read Deamon, connection closed")
                self.connect_socket() 

    def write_daemon(self):
        """Write thread."""
        while True:
            (message, callback) = self._write_queue.get(block=True)
            self.logger.info("Sending message to socket: %s", str(message))
            self.logger.debug("Sending controll message:  %s", message.to_string())
            try:
                if message.is_binary():
                    self._socket.send(message.to_string())
                else:
                    self._socket.send(bytes(message.to_string(),'ascii'))
            except websocket.WebSocketConnectionClosedException :
                self.logger.warning("Write Deamon, connection closed")
                self.connect_socket()

            time.sleep(0.3)
            if callback:
                callback()

    def hello_daemon(self):
        """Put hello message into write thread every hello_interval sec"""
        while True:
            ping_message = domipy.messages.Hello()
            self.send(ping_message)
            time.sleep(self.hello_interval)

    def start_hello(self, interval=-1):
        """
        Start sending HELLO message to server every minute.
        Server will end Login 'session' if no messages received
        in predefined interval (10mins default)
        """
        if interval > -1:
            self.hello_interval = interval

        if self.hello_interval > 0:
            if not self._hello_process.is_alive():
                self._hello_process.start()
