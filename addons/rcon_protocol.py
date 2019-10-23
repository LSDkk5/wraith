import socket
import ssl
import select
import struct
import time


class RconException(Exception):
    pass


class Rcon(object):
    socket = None

    def __init__(self, host, password, port=25575, tlsmode=0):
        self.host = host
        self.password = password
        self.port = port
        self.tlsmode = tlsmode

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, tb):
        self.disconnect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.tlsmode > 0:
            ctx = ssl.create_default_context()
            if self.tlsmode > 1:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            self.socket = ctx.wrap_socket(self.socket, server_hostname=self.host)
        self.socket.connect((self.host, self.port))
        self._send(3, self.password)

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def _read(self, length):
        data = b""
        while len(data) < length:
            data += self.socket.recv(length - len(data))
        return data

    def _send(self, out_type, out_data):
        if self.socket is None:
            raise RconException("Must connect before sending data")
        out_payload = struct.pack('<ii', 0, out_type) + out_data.encode('utf8') + b'\x00\x00'
        out_length = struct.pack('<i', len(out_payload))
        self.socket.send(out_length + out_payload)
        in_data = ""
        while True:
            in_length, = struct.unpack('<i', self._read(4))
            in_payload = self._read(in_length)
            in_id, in_type = struct.unpack('<ii', in_payload[:8])
            in_data_partial, in_padding = in_payload[8:-2], in_payload[-2:]
            if in_padding != b'\x00\x00':
                raise RconException("Incorrect padding")
            if in_id == -1:
                raise RconException("Login failed")
            in_data += in_data_partial.decode('utf8')
            if len(select.select([self.socket], [], [], 0)[0]) == 0:
                return in_data

    def command(self, command):
        result = self._send(2, command)
        time.sleep(0.003)
        return result
