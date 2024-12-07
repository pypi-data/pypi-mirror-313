from __future__ import absolute_import

import socket
import threading
import traceback
from dataclasses import dataclass
from io import BytesIO
from threading import Lock
from typing import Any, Dict, Optional, Type, List, Tuple, Callable, cast, Union, BinaryIO

import cbor2
from cbor2 import dumps, loads, load
from rewrite import Recipe, InMemoryExecutionContext, Cursor, PrinterFactory, TreeVisitor, Tree
from rewrite.execution import DelegatingExecutionContext
from rewrite.remote import ValueSerializer, ValueDeserializer, SenderContext, ReceiverContext, JsonSender, JsonReceiver, \
    SerializationContext, DeserializationContext, remote_utils
from rewrite.tree import PrintOutputCapture, P
from rewrite.visitor import T


class RemotingContext:
    _remoting_thread_local = threading.local()
    _recipe_factories: Dict[str, Callable[[str, Dict[str, Any]], Recipe]] = {}
    _value_serializers: Dict[Type, ValueSerializer] = {}
    _value_deserializers: List[Tuple[Type, ValueDeserializer]] = []
    _object_to_id_map: Dict[int, int] = {}
    _id_to_object_map: Dict[int, Any] = {}

    def __init__(self):
        self._client = None

    @classmethod
    def current(cls) -> 'RemotingContext':
        result = getattr(cls._remoting_thread_local, 'context', None)
        if result is None:
            raise ValueError("No RemotingContext has been set")
        return result

    def set_current(self) -> None:
        cls = self.__class__
        cls._remoting_thread_local.context = self

    @property
    def client(self) -> Optional['RemotingClient']:
        return self._client

    def connect(self, sock: Any) -> 'RemotingContext':
        self._client = RemotingClient(self, sock)
        return self

    def close(self) -> None:
        self._client.close()

    def try_get_id(self, key: Any) -> Optional[int]:
        return self._object_to_id_map.get(id(key))

    def add(self, value: Any) -> int:
        object_id = len(self._object_to_id_map)
        self._object_to_id_map[id(value)] = object_id
        self._id_to_object_map[object_id] = value
        return object_id

    def add_by_id(self, key: int, value: Any) -> None:
        self._id_to_object_map[key] = value
        self._object_to_id_map[id(value)] = key

    def get_object(self, key: int) -> Optional[Any]:
        return self._id_to_object_map.get(key)

    def reset(self) -> None:
        self._object_to_id_map.clear()
        self._id_to_object_map.clear()

    def new_sender_context(self, output_stream: Any) -> 'SenderContext':
        return SenderContext(JsonSender(output_stream, SerializationContext(self, self._value_serializers)))

    def new_receiver_context(self, input_stream: Any) -> 'ReceiverContext':
        return ReceiverContext(JsonReceiver(input_stream, DeserializationContext(self, self._value_deserializers)))

    def copy(self) -> 'RemotingContext':
        return RemotingContext()

    def new_recipe(self, recipe_id: str, recipe_options: Any) -> 'Recipe':
        return self._recipe_factories[recipe_id](recipe_options)

    @classmethod
    def register_value_serializer(cls, serializer: ValueSerializer) -> None:
        cls._value_serializers[serializer.__annotations__['value']] = serializer

    @classmethod
    def register_value_deserializer(cls, deserializer: ValueDeserializer) -> None:
        for i in range(len(cls._value_deserializers)):
            type_ = cls._value_deserializers[i][0]
            if type_ == deserializer.__annotations__['data']:
                cls._value_deserializers[i] = (type_, deserializer)
                return
        cls._value_deserializers.append((deserializer.__annotations__['data'], deserializer))


class RemotingExecutionContextView(DelegatingExecutionContext):
    def __init__(self, delegate):
        super().__init__(delegate)
        self._delegate = delegate

    @staticmethod
    def view(ctx):
        if isinstance(ctx, RemotingExecutionContextView):
            return ctx
        return RemotingExecutionContextView(ctx)

    @property
    def remoting_context(self) -> RemotingContext:
        return self._delegate.get_message('remoting', RemotingContext.current())

    @remoting_context.setter
    def remoting_context(self, value: RemotingContext):
        value.set_current()
        self._delegate.put_message('remoting', value)


OK = 0
ERROR = 1


class RemotingMessenger:

    def __init__(self, context: RemotingContext,
                 additional_handlers: Dict[str, Callable[[BytesIO, socket.socket, RemotingContext], Any]] = None):
        self._context = context
        self._additional_handlers = additional_handlers or {}
        self._recipes = []
        self._state = None

    def process_request(self, sock: socket.socket) -> bool:
        stream = remote_utils.read_to_command_end(sock)
        command = cbor2.load(stream)

        try:
            if command == "hello":
                self.handle_hello_command(stream, sock)
            elif command == "reset":
                self.handle_reset_command(stream, sock)
            elif command == "load-recipe":
                self.handle_load_recipe_command(stream, sock)
            elif command == "run-recipe-visitor":
                self.handle_run_recipe_visitor_command(stream, sock)
            elif command == "print":
                self.handle_print_command(stream, sock)
            else:
                if command in self._additional_handlers:
                    self._additional_handlers[command](stream, sock, self._context)
                else:
                    raise NotImplementedError(f"Unsupported command: {command}")
        except:
            traceback.print_exc()
        finally:
            self.send_end_message(sock)

        return True

    def handle_hello_command(self, stream: BytesIO, sock: socket.socket):
        cbor2.load(stream)
        response_stream = BytesIO()
        cbor2.dump(RemotingMessageType.Response, response_stream)
        cbor2.dump(OK, response_stream)
        sock.sendall(response_stream.getvalue())

    def handle_reset_command(self, stream: BytesIO, sock: socket.socket):
        self._state = None
        self._context = self._context.copy()
        self._context.connect(socket.socket())
        self._recipes.clear()
        response_stream = BytesIO()
        cbor2.dump(RemotingMessageType.Response, response_stream)
        cbor2.dump(OK, response_stream)
        sock.sendall(response_stream.getvalue())

    def handle_load_recipe_command(self, stream: BytesIO, sock: socket.socket):
        recipe_id = cbor2.load(stream)
        recipe_options = cbor2.load(stream)
        recipe = self._context.new_recipe(recipe_id, recipe_options)
        self._recipes.append(recipe)

        response_stream = BytesIO()
        cbor2.dump(RemotingMessageType.Response, response_stream)
        cbor2.dump(OK, response_stream)
        cbor2.dump(len(self._recipes) - 1, response_stream)
        sock.sendall(response_stream.getvalue())

    def handle_run_recipe_visitor_command(self, stream: BytesIO, sock: socket.socket):
        recipe_index = cbor2.load(stream)
        recipe = self._recipes[recipe_index]
        received = self.receive_tree(sock, self._state)

        ctx = InMemoryExecutionContext()
        RemotingExecutionContextView.view(ctx).remoting_context = self._context
        self._state = recipe.get_visitor().visit(received, ctx)

        response_stream = BytesIO()
        cbor2.dump(RemotingMessageType.Response, response_stream)
        cbor2.dump(OK, response_stream)
        self.send_tree(response_stream, self._state, received)
        sock.sendall(response_stream.getvalue())

    def handle_print_command(self, stream: BytesIO, sock: socket.socket):
        received = self.receive_tree(sock, None)
        root_cursor = Cursor(None, Cursor.ROOT_VALUE)
        ctx = InMemoryExecutionContext()
        RemotingExecutionContextView.view(ctx).remoting_context = self._context
        print_output = received.print(Cursor(root_cursor, received), PrintOutputCapture(0))

        response_stream = BytesIO()
        cbor2.dump(RemotingMessageType.Response, response_stream)
        cbor2.dump(OK, response_stream)
        cbor2.dump(print_output, response_stream)
        sock.sendall(response_stream.getvalue())

    def send_request(self, sock: socket.socket, command: str, *args):
        sock.sendall(dumps(RemotingMessageType.Request))
        sock.sendall(dumps(command))
        for arg in args:
            # FIXME serialize properly
            sock.sendall(dumps(arg))
        self.send_end_message(sock)

    def __send_request_stream(self, sock: socket.socket, command: str, *args):
        sock.sendall(dumps(RemotingMessageType.Request))
        sock.sendall(dumps(command))
        for arg in args:
            arg(sock)
        self.send_end_message(sock)

    @staticmethod
    def send_end_message(sock):
        sock.sendall(b'\x81\x17')

    def send_print_request(self, sock: socket.socket, cursor: Cursor):
        self.__send_request_stream(sock, "print",
                                   lambda s: self.send_tree(s, cast(Tree, cursor.value)))
        if self.recv_byte(sock) != RemotingMessageType.Response:
            raise ValueError("Unexpected message type.")
        if self.recv_byte(sock) != 0:
            raise ValueError(f"Remote print failed: {loads(self.recv_all(sock))}")
        data = remote_utils.read_to_command_end(sock)
        print_msg = load(data)
        # end = load(data)  # end
        return print_msg

    def send_tree(self, sock: Union[BinaryIO, socket.socket], after: Tree, before: Optional[Tree] = None):
        b = BytesIO()
        self._context.new_sender_context(b).send_any_tree(after, before)
        sock.sendall(dumps(b.getvalue()))

    def receive_tree(self, data: Union[BinaryIO, socket.socket], before: Optional[Tree] = None):
        receiver_context = self._context.new_receiver_context(cbor2.load(data))
        return receiver_context.receive_any_tree(before)

    def send_run_recipe_request(self, sock: socket.socket, recipe, options: dict, source_files: list):
        self.__send_request_stream(sock, "run-recipe", lambda s: (
            sock.sendall(dumps(recipe)),
            sock.sendall(dumps(options)),
            sock.sendall(dumps(len(source_files))),
            *[self.send_tree(sock, sf, None) for sf in source_files]
        ))
        while self.recv_byte(sock) == RemotingMessageType.Request:
            self.process_request(sock)
        if self.recv_byte(sock) != RemotingMessageType.Response:
            raise ValueError("Unexpected message type.")
        if self.recv_byte(sock) != 0:
            raise ValueError(f"Remote recipe run failed: {loads(self.recv_all(sock))}")
        input_stream = remote_utils.read_to_command_end(sock)
        updated = [self.receive_tree(input_stream, sf) for sf in source_files]
        loads(input_stream)  # end
        return updated

    def send_reset_request(self, sock: socket.socket):
        self.send_request(sock, "reset")
        if self.recv_byte(sock) != RemotingMessageType.Response:
            raise ValueError("Unexpected message type.")
        if self.recv_byte(sock) != 0:
            raise ValueError(f"Remote reset failed: {loads(self.recv_all(sock))}")
        loads(self.recv_all(sock))  # command end

    def recv_byte(self, sock):
        return sock.recv(1)[0]

    def recv_all(self, sock, buffer_size=4096):
        data = b''
        while True:
            part = sock.recv(buffer_size)
            data += part
            if len(part) < buffer_size:
                break
        return data


class RemotingMessageType:
    Request = 0
    Response = 1


class RemotingClient:
    def __init__(self, context, sock: socket.socket):
        self._messenger = RemotingMessenger(context)
        self._socket = sock
        self._lock = Lock()

    def close(self) -> None:
        self._socket.close()

    def hello(self):
        with self._lock:
            self._messenger.send_request(self._socket, "hello")

    def print(self, cursor):
        with self._lock:
            return self._messenger.send_print_request(self._socket, cursor)

    def reset(self):
        with self._lock:
            self._messenger.send_reset_request(self._socket)

    def run_recipe(self, recipe, options: dict, source_files: list):
        with self._lock:
            return self._messenger.send_run_recipe_request(self._socket, recipe, options, source_files)


@dataclass
class RemotePrinter(TreeVisitor[Any, PrintOutputCapture[P]]):
    _client: RemotingClient

    def visit(self, tree: Optional[Tree], p: PrintOutputCapture[P], parent: Optional[Cursor] = None) -> Optional[T]:
        self.cursor = Cursor(parent, tree)
        p.append(self._client.print(self.cursor))
        self.cursor = self.cursor.parent
        return tree


@dataclass
class RemotePrinterFactory(PrinterFactory):
    _client: RemotingClient

    def create_printer(self, cursor: Cursor) -> TreeVisitor[Any, PrintOutputCapture[P]]:
        return RemotePrinter(self._client)
