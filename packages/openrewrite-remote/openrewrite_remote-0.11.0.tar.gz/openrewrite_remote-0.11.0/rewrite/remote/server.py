import importlib
import importlib.resources
import os
import socket
import sys
import time
import traceback
import zipfile
from io import BytesIO, StringIO
from pathlib import Path
from typing import Optional

import cbor2
import select
from cbor2 import dumps
from rewrite import ParserInput, InMemoryExecutionContext, ExecutionContext, ParseError
from rewrite.python import Py
from rewrite.python.parser import PythonParserBuilder
from rewrite.remote import SenderContext, ReceiverContext, RemotingContext, RemotingMessenger, RemotingMessageType, \
    RemotePrinterFactory, OK, ParseErrorSender
from rewrite.python.remote.receiver import PythonReceiver
from rewrite.python.remote.sender import PythonSender

INACTIVITY_TIMEOUT = 300  # 5 minutes
_OK: int = 0
_ERROR: int = 1


def register_remoting_factories():
    SenderContext.register(ParseError, lambda: ParseErrorSender())
    SenderContext.register(Py, lambda: PythonSender())
    ReceiverContext.register(Py, lambda: PythonReceiver())


def find_free_port():
    """Find a free port by using the system to allocate a port for us."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        return s.getsockname()[1]


class Server:
    _port: Optional[int]
    _path: Optional[str]
    _remoting_context: RemotingContext
    _messenger: RemotingMessenger

    def __init__(self, port: int = None, path: str = None, timeout: int = INACTIVITY_TIMEOUT):
        self._port = port
        self._path = path
        self.timeout = timeout
        self._remoting_context = RemotingContext()
        self._messenger = RemotingMessenger(
            self._remoting_context,
            {
                'parse-python-source': self.parse_python_source,
                'parse-python-file': self.parse_python_file,
            }
        )

    def start(self):
        """Start the server and listen for connections on the given port."""
        if self._path:
            if os.path.exists(self._path):
                os.remove(self._path)
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.bind(self._path)
                s.listen()
                print(f"Server listening on Unix domain socket: {self._path}")
                while True:
                    conn, _ = s.accept()
                    with conn:
                        self.handle_client(conn)
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('localhost', self._port))
                s.listen(5)
                print(f"Server listening on port {self._port}")
                last_activity_time = time.time()
                while True:
                    s.settimeout(5)
                    try:
                        conn, addr = s.accept()
                        last_activity_time = time.time()  # Reset inactivity timer
                        with conn:
                            conn.settimeout(None)
                            self.handle_client(conn)
                    except socket.timeout:
                        current_time = time.time()
                        if current_time - last_activity_time >= self.timeout:
                            print("No new connections for 5 minutes, shutting down server.")
                            break

    def handle_client(self, sock: socket.socket) -> None:
        try:
            self._remoting_context.connect(sock)
            RemotePrinterFactory(self._remoting_context.client).set_current()

            sock.setblocking(True)
            while True:
                message_type = sock.recv(1)
                if not message_type:
                    return
                assert cbor2.load(BytesIO(message_type)) == RemotingMessageType.Request
                self._messenger.process_request(sock)

                readable, _, _ = select.select([sock], [], [], 0.01)
                if sock not in readable:
                    return

        except (OSError, IOError):
            # the socket was closed
            return
        except Exception as e:
            print(f"An error occurred while handling client: {e}")
            traceback.print_exc()
            if sock.fileno() != -1:
                try:
                    # Equivalent to C#'s stream.WriteTimeout = 1000;
                    sock.send(dumps(RemotingMessageType.Response))
                    sock.send(dumps(_ERROR))
                    sock.send(dumps(traceback.format_exc()))
                except (OSError, IOError):
                    # the socket was closed
                    return
                except Exception as inner_exception:
                    print(inner_exception)
        finally:
            sock.close()

    def parse_python_source(self, stream: BytesIO, sock: socket.socket, remoting_ctx: RemotingContext):
        remoting_ctx.reset()
        source = cbor2.load(stream)
        ctx = InMemoryExecutionContext()
        ctx.put_message(ExecutionContext.REQUIRE_PRINT_EQUALS_INPUT, False)
        for cu in PythonParserBuilder().build().parse_inputs(
                [ParserInput(Path('source.py'), None, True, lambda: StringIO(source))],
                None, ctx):
            response_stream = BytesIO()
            cbor2.dump(RemotingMessageType.Response, response_stream)
            cbor2.dump(OK, response_stream)
            source_stream = BytesIO()
            remoting_ctx.new_sender_context(source_stream).send_any_tree(cu, None)
            cbor2.dump(source_stream.getvalue(), response_stream)
            sock.sendall(response_stream.getvalue())

    def parse_python_file(self, stream: BytesIO, sock: socket.socket, remoting_ctx: RemotingContext):
        remoting_ctx.reset()
        path = cbor2.load(stream)
        ctx = InMemoryExecutionContext()
        ctx.put_message(ExecutionContext.REQUIRE_PRINT_EQUALS_INPUT, False)
        for cu in PythonParserBuilder().build().parse_inputs(
                [ParserInput(Path(path), None, True, lambda: read_file_contents(path))],
                None, ctx):
            response_stream = BytesIO()
            cbor2.dump(RemotingMessageType.Response, response_stream)
            cbor2.dump(OK, response_stream)
            source_stream = BytesIO()
            remoting_ctx.new_sender_context(source_stream).send_any_tree(cu, None)
            cbor2.dump(source_stream.getvalue(), response_stream)
            sock.sendall(response_stream.getvalue())


def read_file_contents(path):
    with open(path, 'r', newline='', encoding='utf-8') as file:
        return StringIO(file.read())


def read_data_from_zip():
    # Access the resource within the 'your_package.resources' package
    # 'data.zip' is the name of the file included
    with importlib.resources.open_binary('resources', 'rewrite-remote-java.zip') as f:
        # Open the zip file from the resource file stream
        with zipfile.ZipFile(f) as zip_file:
            # List the contents of the zip file
            print(zip_file.namelist())
            # Read a specific file inside the zip file (if you know the file name within it)
            with zip_file.open('rewrite-remote-java-0.2.0-SNAPSHOT/bin/rewrite-remote-java') as inner_file:
                data = inner_file.read()
                print(data.decode('utf-8'))


# Example usage
# read_data_from_zip()

if __name__ == "__main__":
    sys.setrecursionlimit(2000)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 54322
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else INACTIVITY_TIMEOUT
    register_remoting_factories()
    Server(port=port, timeout=timeout).start()
    # Server(port=find_free_port()).start()
    # Server(path=tempfile.gettempdir() + '/rewrite-csharp.sock').start()
