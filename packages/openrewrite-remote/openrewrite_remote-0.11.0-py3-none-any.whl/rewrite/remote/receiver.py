from collections import OrderedDict
from enum import Enum
from pathlib import Path
from typing import Protocol, TypeVar, Optional, Type, Dict, Callable, List, cast, Iterable, Any, Tuple, \
    get_args, TYPE_CHECKING
from uuid import UUID

import cbor2
from cbor2 import CBORDecoder
from rewrite import Markers, Marker, ParseErrorVisitor

from rewrite import Tree, TreeVisitor, Cursor, FileAttributes
from rewrite.remote.event import DiffEvent, EventType
from . import remote_utils, type_utils

if TYPE_CHECKING:
    from .remoting import RemotingContext

A = TypeVar('T')
T = TypeVar('T', bound=Tree)
V = TypeVar('V')
I = TypeVar('I')
P = TypeVar('P')


class Receiver(Protocol):
    def fork(self, context: 'ReceiverContext') -> 'ReceiverContext':
        ...

    def receive(self, before: Optional[T], ctx: 'ReceiverContext') -> object:
        ...


class OmniReceiver(Receiver):
    def fork(self, ctx: 'ReceiverContext') -> 'ReceiverContext':
        raise NotImplementedError("Cannot fork OmniReceiver")

    def receive(self, before: Optional['Tree'], ctx: 'ReceiverContext') -> 'Tree':
        visitor = self.Visitor()
        return visitor.visit(before, ctx)

    class Visitor(TreeVisitor[Tree, 'ReceiverContext']):
        def visit(self, tree: Optional[Tree], ctx: 'ReceiverContext', parent: Optional[Cursor] = None) -> Optional[
            Tree]:
            self.cursor = Cursor(self.cursor, tree)
            tree = ctx.polymorphic_receive_tree(tree)
            self.cursor = self.cursor.parent
            return tree


class TreeReceiver(Protocol):
    def receive_node(self) -> DiffEvent:
        ...

    def receive_value(self, expected_type: Type) -> DiffEvent:
        ...


class ReceiverFactory(Protocol):
    def create(self, type_name: str, ctx: 'ReceiverContext') -> Tree:
        ...


class DetailsReceiver(Protocol[T]):
    def receive_details(self, before: Optional[T], type: Optional[Type[T]], ctx: 'ReceiverContext') -> T:
        pass


class ReceiverContext:
    Registry: Dict[Type, Callable[[], Receiver]] = OrderedDict()

    def __init__(self, receiver: TreeReceiver, visitor: Optional[TreeVisitor] = None,
                 factory: ReceiverFactory = None):
        self.receiver = receiver
        self.visitor = visitor
        self.factory = factory

    def fork(self, visitor: TreeVisitor, factory: ReceiverFactory) -> 'ReceiverContext':
        return ReceiverContext(self.receiver, visitor, factory)

    def receive_any_tree(self, before) -> T:
        return OmniReceiver().receive(before, self)

    def receive_tree(self, before: Optional[Tree], tree_type: Optional[str], ctx: 'ReceiverContext') -> Tree:
        if before:
            return before.accept(self.visitor, ctx)
        else:
            return self.factory.create(tree_type, ctx)

    def polymorphic_receive_tree(self, before: Optional[Tree]) -> Optional[Tree]:
        diff_event = self.receiver.receive_node()
        if diff_event.event_type in (EventType.Add, EventType.Update):
            tree_receiver = self.new_receiver(diff_event.concrete_type or type(before).__name__)
            forked = tree_receiver.fork(self)
            return forked.receive_tree(
                None if diff_event.event_type == EventType.Add else before,
                diff_event.concrete_type, forked
            )
        elif diff_event.event_type == EventType.Delete:
            return None
        else:
            return before

    def new_receiver(self, type_name: str) -> Receiver:
        type_ = type_utils.get_type(type_name)
        for entry_type, factory in self.Registry.items():
            if issubclass(type_, entry_type):
                return factory()
        raise ValueError(f"Unsupported receiver type: {type_name}")

    def receive_node(self, before: Optional[A],
                     details: Callable[[Optional[A], Optional[str], 'ReceiverContext'], A]) -> Optional[A]:
        evt = self.receiver.receive_node()
        if evt.event_type == EventType.Delete:
            return None
        elif evt.event_type == EventType.Add:
            return details(None, evt.concrete_type, self)
        elif evt.event_type == EventType.Update:
            return details(before, evt.concrete_type, self)
        return before

    def receive_markers(self, before: Optional[Markers], type: Optional[str], ctx: 'ReceiverContext') -> Markers:
        id_ = self.receive_value(getattr(before, 'id', None), UUID)
        after_markers = self.receive_values(getattr(before, 'markers', None), Marker)
        if before:
            return before.with_id(id_).with_markers(after_markers)
        else:
            return Markers(id_, after_markers)

    def receive_nodes(self, before: Optional[List[A]], details: Callable[[Optional[A], Optional[str], 'ReceiverContext'], A]) -> Optional[List[A]]:
        return remote_utils.receive_nodes(before, details, self)

    def receive_values(self, before: Optional[List[V]], type: Type) -> Optional[List[V]]:
        return remote_utils.receive_values(before, type, self)

    def receive_value(self, before: Optional[V], type: Type) -> Optional[V]:
        return self.receive_value0(before, type)

    def receive_value0(self, before: Optional[V], type: Type) -> Optional[V]:
        evt = self.receiver.receive_value(type)
        if evt.event_type in (EventType.Update, EventType.Add):
            return evt.msg
        elif evt.event_type == EventType.Delete:
            return None
        return before

    @staticmethod
    def register(type_: Type, receiver_factory: Callable[[], Receiver]):
        ReceiverContext.Registry[type_] = receiver_factory


class ValueDeserializer(Protocol):
    def deserialize(self, type_: Optional[Type], reader: CBORDecoder, context: 'DeserializationContext') -> Optional[Any]:
        ...


class DefaultValueDeserializer(ValueDeserializer):
    def deserialize(self, expected_type: Optional[Type], reader: CBORDecoder, context: 'DeserializationContext') -> Any:
        cbor_map = reader.decode_map()
        error_message = "No deserializer found for: " + ", ".join(f"{k}: {v}" for k, v in cbor_map.items())
        raise NotImplementedError(error_message)


class DeserializationContext:
    DefaultDeserializer = DefaultValueDeserializer()

    def __init__(self, remoting_context: 'RemotingContext', value_deserializers: Optional[List[Tuple[Type, ValueDeserializer]]] = None):
        self.remoting_context = remoting_context
        self.value_deserializers = value_deserializers or []

    def deserialize(self, expected_type: Type, decoder: CBORDecoder) -> Any:
        value = decoder.decode()
        if value is None:
            return None

        if expected_type == UUID:
            return UUID(bytes=value)

        if expected_type == str:
            return value

        if expected_type == bool:
            return value

        if expected_type == list:
            return value

        if expected_type == int:
            return value

        if expected_type == Path:
            return Path(value)

        if expected_type == float:
            return value

        if issubclass(expected_type, Enum):
            return expected_type(value)

        state = decoder.peek_state()

        if state in {cbor2.CborReaderState.BOOLEAN, cbor2.CborReaderState.UNSIGNED_INT,
                     cbor2.CborReaderState.NEGATIVE_INT}:
            result = decoder.read_int()
            obj = self.remoting_context.get_object(result)
            return obj if obj is not None else result

        if state in {cbor2.CborReaderState.HALF_FLOAT, cbor2.CborReaderState.FLOAT, cbor2.CborReaderState.DOUBLE}:
            return decoder.read_double()

        if state == cbor2.CborReaderState.TEXT_STRING:
            str_value = decoder.read_text_string()
            if decoder.peek_state() == cbor2.CborReaderState.END_ARRAY:
                return str_value

            concrete_type = str_value if decoder.peek_state() != cbor2.CborReaderState.END_ARRAY else expected_type.__name__

            if concrete_type == "org.openrewrite.FileAttributes":
                map = decoder.read_cbor_map()
                return FileAttributes(None, None, None, False, False, False, 0)

            if concrete_type == "java.lang.String":
                return decoder.decode()
            if concrete_type == "java.lang.Boolean":
                return decoder.decode()
            if concrete_type == "java.lang.Integer":
                return decoder.decode()
            if concrete_type == "java.lang.Character":
                return decoder.decode()[0]
            if concrete_type == "java.lang.Long":
                return decoder.decode()
            if concrete_type == "java.lang.Double":
                return decoder.decode()
            if concrete_type == "java.lang.Float":
                return decoder.decode()
            if concrete_type == "java.math.BigInteger":
                return decoder.decode()
            if concrete_type == "java.math.BigDecimal":
                return decoder.decode()

            raise NotImplementedError(f"No deserialization implemented for: {concrete_type}")

        if state == cbor2.CborReaderState.ARRAY:
            decoder.read_array_start()
            concrete_type = decoder.read_text_string()
            actual_type = type_utils.get_type(concrete_type)
            for type_, deserializer in self.value_deserializers:
                if issubclass(actual_type, type_):
                    return deserializer.deserialize(actual_type, decoder, self)

        if state == cbor2.CborReaderState.MAP:
            if issubclass(expected_type, Marker):
                if decoder.peek_state() == cbor2.CborReaderState.UNSIGNED_INT:
                    obj_id = decoder.read_int()
                    return self.remoting_context.get_object(obj_id)

                marker_map = ValueDeserializer.read_cbor_map(decoder)

                if "@c" not in marker_map:
                    raise NotImplementedError("Expected @c key")

                concrete_type = marker_map["@c"]

                if concrete_type in {"org.openrewrite.marker.SearchResult", "Rewrite.Core.Marker.SearchResult"}:
                    desc = marker_map.get("description", None)
                    marker = SearchResult(UUID(bytes=marker_map["id"]), desc)
                else:
                    marker = UnknownJavaMarker(UUID(bytes=marker_map["id"]), marker_map)

                if "@ref" in marker_map:
                    self.remoting_context.add(marker_map["@ref"], marker)

                return marker

            decoder.read_map_start()
            if decoder.read_text_string() != "@c":
                raise NotImplementedError("Expected @c key")
            concrete_type = decoder.read_text_string()
            actual_type = type_utils.get_type(concrete_type)
            for type_, deserializer in self.value_deserializers:
                if issubclass(actual_type, type_):
                    return deserializer.deserialize(actual_type, decoder, self)
        raise NotImplementedError(f"No deserialization implemented for: {expected_type}")


class JsonReceiver(TreeReceiver):
    DEBUG = False

    def __init__(self, stream, context: DeserializationContext):
        super().__init__()
        self._stream = stream
        self._decoder = cbor2.CBORDecoder(self._stream)
        self._context = context
        self._count = 0

    def receive_node(self):
        array = self._decoder.decode()
        if isinstance(array, list):
            event_type = EventType(cast(int, array[0]))
            msg = None
            concrete_type = None

            if event_type in {EventType.Add, EventType.Update}:
                if event_type == EventType.Add and isinstance(array[1], str):
                    concrete_type = array[1]

            elif event_type not in {EventType.Delete, EventType.NoChange, EventType.StartList, EventType.EndList}:
                raise NotImplementedError(event_type)

            if self.DEBUG:
                print(f"[{self._count}] {DiffEvent(event_type, concrete_type, msg)}")
            self._count += 1
            return DiffEvent(event_type, concrete_type, msg)

        else:
            raise NotImplementedError(f"Unexpected state: {type(array)}")

    def receive_value(self, expected_type: Type):
        length = remote_utils.decode_array_start(self._decoder)
        event_type = EventType(self._decoder.decode())
        msg = None
        concrete_type = None

        if event_type in {EventType.Add, EventType.Update}:
            if (bool(get_args(expected_type)) and
                    issubclass(expected_type, (list, Iterable))):
                # special case for list events
                msg = self._decoder.decode()
            else:
                msg = self._context.deserialize(expected_type, self._decoder)

        elif event_type not in {EventType.Delete, EventType.NoChange, EventType.StartList, EventType.EndList}:
            raise NotImplementedError(event_type)

        if length is None:
            array_end = self._decoder.decode()
            # assert array_end == break_marker

        if self.DEBUG:
            print(f"[{self._count}] {DiffEvent(event_type, concrete_type, msg)}")
        self._count += 1
        return DiffEvent(event_type, concrete_type, msg)


class ParseErrorReceiver(Receiver):
    def fork(self, ctx):
        return ctx.fork(self.Visitor(), self.Factory())

    def receive(self, before, ctx):
        forked = self.fork(ctx)
        return forked.visitor.visit(before, forked)

    class Visitor(ParseErrorVisitor):
        def visit(self, tree, ctx, parent: Optional[Cursor] = None):
            self.cursor = Cursor(self.cursor, tree)
            tree = ctx.receive_node(tree, ctx.receive_tree)
            self.cursor = self.cursor.parent
            return tree

        def visit_parse_error(self, parse_error, ctx):
            parse_error = parse_error.with_id(ctx.receive_value(parse_error.id))
            parse_error = parse_error.with_markers(ctx.receive_node(parse_error.markers, ctx.receive_markers))
            parse_error = parse_error.with_source_path(ctx.receive_value(parse_error.source_path))
            parse_error = parse_error.with_file_attributes(ctx.receive_value(parse_error.file_attributes))
            parse_error = parse_error.with_charset_name(ctx.receive_value(parse_error.charset_name))
            parse_error = parse_error.with_charset_bom_marked(ctx.receive_value(parse_error.charset_bom_marked))
            parse_error = parse_error.with_checksum(ctx.receive_value(parse_error.checksum))
            parse_error = parse_error.with_text(ctx.receive_value(parse_error.text))
            # parse_error = parse_error.with_erroneous(ctx.receive_tree(parse_error.erroneous))
            return parse_error

    class Factory(ReceiverFactory):
        def create(self, type_, ctx):
            if type_ in ["rewrite.parser.ParseError", "org.openrewrite.tree.ParseError"]:
                return ParseError(
                    ctx.receive_value(None),
                    ctx.receive_node(None, ctx.receive_markers),
                    ctx.receive_value(None),
                    ctx.receive_value(None),
                    ctx.receive_value(None),
                    ctx.receive_value(None),
                    ctx.receive_value(None),
                    ctx.receive_value(None),
                    None  # ctx.receive_tree(None)
                )
            raise NotImplementedError("No factory method for type: " + type_)
