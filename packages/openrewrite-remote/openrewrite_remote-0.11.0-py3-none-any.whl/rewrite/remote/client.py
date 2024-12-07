import socket
import tempfile
from pathlib import Path

import rewrite.java.tree as j
import rewrite.python.tree as py
from rewrite import Markers
from rewrite.python import Py
from rewrite.java import Space, JavaType

from rewrite import random_id, Cursor, PrintOutputCapture
from rewrite.remote import RemotingContext, RemotePrinterFactory, SenderContext, ReceiverContext
from rewrite.remote.python.receiver import PythonReceiver
from rewrite.remote.python.sender import PythonSender

SenderContext.register(Py, lambda: PythonSender())
ReceiverContext.register(Py, lambda: PythonReceiver())

# Path to the Unix domain socket
SOCKET_PATH = tempfile.gettempdir() + '/rewrite-java.sock'

# Create a Unix domain socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the path where the server is listening
client.connect(('localhost', 65432))
print(f'Connected to {SOCKET_PATH}')

try:
    remoting = RemotingContext()
    remoting.connect(client)
    RemotePrinterFactory(remoting.client).set_current()

    literal = j.Literal(random_id(), Space.SINGLE_SPACE, Markers.EMPTY, True, 'True', None, JavaType.Primitive())
    assert_ = py.AssertStatement(random_id(), Space.EMPTY, Markers.EMPTY, [j.JRightPadded(literal, Space.EMPTY, Markers.EMPTY)])
    cu = py.CompilationUnit(random_id(), Space.EMPTY, Markers.EMPTY, Path('/foo.py'), None, None, False, None, [], [j.JRightPadded(assert_, Space.EMPTY, Markers.EMPTY)], Space.EMPTY)
    printed = cu.print(Cursor(None, Cursor.ROOT_VALUE), PrintOutputCapture(0))
    assert printed == 'assert True'
finally:
    client.close()
