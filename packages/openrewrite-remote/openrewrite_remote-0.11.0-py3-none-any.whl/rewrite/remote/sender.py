from __future__ import absolute_import

import decimal
from abc import ABC, abstractmethod
from dataclasses import fields
from pathlib import Path
from typing import Dict, Type, Any, Callable, ClassVar, TypeVar, Generic, Protocol, List, TYPE_CHECKING
from uuid import UUID

import cbor2
from cbor2 import CBOREncoder
from rewrite import Tree, Markers, Marker, ParseErrorVisitor, Cursor, Style
from rewrite.remote.type_utils import to_java_type_name, to_java_field_name, to_java_type_name_from_value
from rewrite.visitor import TreeVisitor

from . import remote_utils
from .event import *
from .remote_utils import Operation

if TYPE_CHECKING:
    from .remoting import RemotingContext

A = TypeVar('A')
T = TypeVar('T', bound=Tree)
V = TypeVar('V')
I = TypeVar('I')


class Sender(Protocol):
    def send(self, after: T, before: Optional[T], ctx: 'SenderContext') -> None:
        ...


class OmniSender(Sender):
    def send(self, after: Tree, before: Optional[Tree], ctx: 'SenderContext'):
        sender = ctx.new_sender(type(after))
        sender.send(after, before, ctx)


class TreeSender(Protocol):
    def send_node(self, diff_event: DiffEvent, visitor: Callable[['TreeSender'], None]):
        ...

    def send_value(self, diff_event: DiffEvent):
        ...

    def flush(self):
        ...


class SenderContext(Generic[T]):
    Registry: Dict[Type, Callable[[], Sender]] = {}

    def __init__(self, sender: 'TreeSender', visitor: TreeVisitor = None, before: Optional[Any] = None):
        self.sender = sender
        self.visitor = visitor
        self.before = before

    def new_sender(self, type_: Type) -> Sender:
        for entry_type, factory in self.Registry.items():
            # FIXME find better solution
            try:
                if type_.__bases__.__contains__(entry_type) or issubclass(type_, entry_type):
                    return factory()
            except:
                pass
        raise ValueError(f"Unsupported sender type: {type_}")

    def fork(self, visitor: TreeVisitor, before: Optional[Any] = None) -> 'SenderContext':
        return SenderContext(self.sender, visitor, before)

    def visit(self, consumer: Callable[[V, 'SenderContext'], None], after: V, before: Optional[V] = None):
        save_before = self.before
        self.before = before
        consumer(after, self)
        self.before = save_before

    def send_tree(self, after: T, ctx: 'SenderContext'):
        after.accept(self.visitor, ctx)

    def send_any_tree(self, after: T, before: Optional[T]):
        OmniSender().send(after, before, self)

    def send_node(self, owner: A, extractor: Callable[[A], Optional[V]], details: Callable[[V, 'SenderContext'], None]):
        self.send_node_internal(extractor(owner), extractor(self.before) if self.before is not None else None, details)

    def send_value(self, owner, value_extractor: Callable[[T], Optional[V]]):
        after_value = value_extractor(owner)
        before_value = value_extractor(self.before) if self.before is not None else None
        self.send_value_internal(after_value, before_value)

    def send_typed_value(self, owner: A, value_extractor: Callable[[A], V]):
        after_value = value_extractor(owner)
        before_value = value_extractor(self.before) if self.before is not None else None
        self.send_typed_value_internal(after_value, before_value)

    def send_list_event(self, after: Optional[List[V]], before: Optional[List[V]]) -> bool:
        if after == before:
            evt = DiffEvent(EventType.NoChange, None, None)
        elif before is None:
            evt = DiffEvent(EventType.Add, None, len(after) if after is not None else 0)
        elif after is None:
            evt = DiffEvent(EventType.Delete, None, None)
        else:
            evt = DiffEvent(EventType.Update, None, len(after))

        self.sender.send_value(evt)
        return evt.event_type != EventType.NoChange and evt.event_type != EventType.Delete

    def send_nodes(self, owner: A, element_extractor: Callable[[A], List[V]],
                   details: Callable[[V, 'SenderContext'], None], id_function: Callable[[V], I]):
        after_list = element_extractor(owner)
        before_list = element_extractor(self.before) if self.before is not None else None

        if self.send_list_event(after_list, before_list):
            if before_list is not None:
                self.sender.send_value(DiffEvent(EventType.StartList, None, None))

            remote_utils.calculate_list_diff(
                before_list or [],
                after_list,
                id_function,
                lambda op, _1, _2, bv, av: {
                    Operation.Delete: lambda: self.send_node_internal(av, bv, details),
                    Operation.NoChange: lambda: self.send_node_internal(av, bv, details),
                    Operation.Add: lambda: self.send_node_internal(av, bv, details),
                    Operation.Update: lambda: self.send_node_internal(av, bv, details),
                    Operation.Move: lambda: NotImplementedError("Unexpected operation: " + str(op))
                }[op]()
            )

            if before_list is not None:
                self.sender.send_value(DiffEvent(EventType.EndList, None, None))

    def send_values(self, owner, value_extractor: Callable[[T], List[V]], id_function: Callable[[V], I]):
        after_list = value_extractor(owner)
        before_list = value_extractor(self.before) if self.before is not None else None

        if self.send_list_event(after_list, before_list):
            if before_list is not None:
                self.sender.send_value(DiffEvent(EventType.StartList, None, None))

            remote_utils.calculate_list_diff(
                before_list or [],
                after_list,
                id_function,
                lambda op, _1, _2, bv, av: {
                    Operation.Delete: lambda: self.send_value_internal(av, bv),
                    Operation.NoChange: lambda: self.send_value_internal(av, bv),
                    Operation.Add: lambda: self.send_value_internal(av, bv),
                    Operation.Update: lambda: self.send_value_internal(av, bv),
                    Operation.Move: lambda: NotImplementedError("Unexpected operation: " + str(op))
                }[op]()
            )

            if before_list is not None:
                self.sender.send_value(DiffEvent(EventType.EndList, None, None))

    def send_typed_values(self, owner: T, value_extractor: Callable[[T], List[V]], id_function: Callable[[V], I]):
        after_list = value_extractor(owner)
        before_list = value_extractor(self.before) if self.before is not None else None

        if self.send_list_event(after_list, before_list):
            if before_list is not None:
                self.sender.send_value(DiffEvent(EventType.StartList, None, None))

            remote_utils.calculate_list_diff(
                before_list or [],
                after_list,
                id_function,
                lambda op, _1, _2, bv, av: {
                    Operation.Delete: lambda: self.send_typed_value_internal(av, bv),
                    Operation.NoChange: lambda: self.send_typed_value_internal(av, bv),
                    Operation.Add: lambda: self.send_typed_value_internal(av, bv),
                    Operation.Update: lambda: self.send_typed_value_internal(av, bv),
                    Operation.Move: lambda: NotImplementedError("Unexpected operation: " + str(op))
                }[op]()
            )

            if before_list is not None:
                self.sender.send_value(DiffEvent(EventType.EndList, None, None))

    def send_markers(self, markers: Markers, ignore):
        self.send_value(markers, lambda ms: ms.id)
        self.send_values(markers, lambda ms: ms.markers, lambda ms: ms.id)

    def send_tree_visitor(self, after: T, ctx: 'SenderContext'):
        after.accept(self.visitor, ctx)

    @staticmethod
    def register(type_: Type, sender_factory: Callable[[], Sender]):
        SenderContext.Registry[type_] = sender_factory

    @staticmethod
    def are_equal(after: Optional[V], before: Optional[V]) -> bool:
        if after is None or before is None:
            return after == before

        return isinstance(after, (Tree, Markers)) or isinstance(before, (Tree, Markers))

    def send_node_internal(self, after: Optional[V], before: Optional[V],
                           details: Callable[[V, 'SenderContext'], None]):
        if self.are_equal(after, before):
            evt = DiffEvent(EventType.NoChange, None, None)
        elif before is None:
            concrete_type = to_java_type_name(type(after)) if after is not None else None
            evt = DiffEvent(EventType.Add, concrete_type, None)
        elif after is None:
            evt = DiffEvent(EventType.Delete, None, None)
        else:
            evt = DiffEvent(EventType.Update, None, None)

        self.sender.send_node(evt, lambda _: self.visit(details, after, before))

    def send_value_internal(self, after: V, before: Optional[V]):
        if self.before is not None and self.are_equal(after, before):
            evt = DiffEvent(EventType.NoChange, None, None)
        elif self.before is None or before is None:
            concrete_type = to_java_type_name(type(after)) if isinstance(after, Marker) else None
            evt = DiffEvent(EventType.Add, concrete_type, after)
        elif after is None:
            evt = DiffEvent(EventType.Delete, None, None)
        else:
            evt = DiffEvent(EventType.Update, None, after)

        self.sender.send_value(evt)

    def send_typed_value_internal(self, after: V, before: Optional[V]):
        if self.before is not None and self.are_equal(after, before):
            evt = DiffEvent(EventType.NoChange, None, None)
        elif self.before is None or before is None:
            concrete_type = to_java_type_name_from_value(after) if after is not None else None
            evt = DiffEvent(EventType.Add, concrete_type, after)
        elif after is None:
            evt = DiffEvent(EventType.Delete, None, None)
        else:
            evt = DiffEvent(EventType.Update, None, after)

        self.sender.send_value(evt)


class SerializationContext:
    def __init__(self, remoting_context: 'RemotingContext',
                 value_serializers: Optional[Dict[Type, 'ValueSerializer']] = None):
        self.remoting_context = remoting_context
        self.value_serializers = value_serializers or {}

    def serialize(self, value: Any, type_name: Optional[str], encoder: CBOREncoder):
        if value is None:
            encoder.encode_none(None)
            return

        for type_cls, serializer in self.value_serializers.items():
            if isinstance(value, type_cls):
                serializer.serialize(value, type_name, encoder, self)
                return

        DefaultValueSerializer().serialize(value, type_name, encoder, self)


class JsonSender(TreeSender):
    Debug = False

    def __init__(self, stream, context: SerializationContext):
        self._stream = stream
        self._context = context
        self._encoder = cbor2.CBOREncoder(self._stream)

    def send_node(self, diff_event, visitor):

        if diff_event.event_type in (EventType.Add, EventType.Update):
            self._encoder.encode(
                [diff_event.event_type.value] if diff_event.concrete_type is None else [diff_event.event_type.value,
                                                                                        diff_event.concrete_type])

            if self.Debug:
                print(f"SEND: {diff_event}")

            visitor(self)
        elif diff_event.event_type in (EventType.Delete, EventType.NoChange):
            self._encoder.encode([diff_event.event_type.value])

            if self.Debug:
                print(f"SEND: {diff_event}")
        else:
            raise NotImplementedError()

    def send_value(self, diff_event):
        if diff_event.event_type in (EventType.Add, EventType.Update):
            self._encoder.encode_length(4, 3 if diff_event.concrete_type is not None else 2)
            self._encoder.encode_int(diff_event.event_type.value)
            if diff_event.concrete_type is not None:
                self._encoder.encode(diff_event.concrete_type)
            self._context.serialize(diff_event.msg, diff_event.concrete_type, self._encoder)
        elif diff_event.event_type in (EventType.Delete, EventType.NoChange, EventType.StartList, EventType.EndList):
            self._encoder.encode([diff_event.event_type.value])
        else:
            raise NotImplementedError()

        if self.Debug:
            print(f"SEND: {diff_event}")

    def flush(self):
        self._stream.flush()


INDEFINITE_ARRAY_START = b'\x9f'
INDEFINITE_MAP_START = b'\xbf'
BREAK_MARKER = b'\xff'


class ValueSerializer(ABC):

    @abstractmethod
    def serialize(self, value: Any, type_name: Optional[str], writer: CBOREncoder, context: SerializationContext):
        pass

    @staticmethod
    def write_object_using_reflection(value: Any, type_name: Optional[str], with_id: bool,
                                      encoder: CBOREncoder, context: SerializationContext):
        if type(value).__qualname__ == 'JavaType.Primitive':
            # FIXME implement type attribution support
            encoder.encode(['org.openrewrite.java.tree.JavaType$Primitive', 0])
            return
        if with_id and (id := context.remoting_context.try_get_id(value)):
            encoder.encode_int(id)
            return

        encoder.write(INDEFINITE_MAP_START)
        encoder.encode_string("@c")
        encoder.encode_string(type_name or to_java_type_name(type(value)))
        if with_id:
            encoder.encode_string("@ref")
            id = context.remoting_context.add(value)
            encoder.encode_int(id)

        for field in fields(value):
            if field.name[0] == '_' and (not hasattr(field.type, '__origin__') or field.type.__origin__ is not ClassVar):
                encoder.encode_string(to_java_field_name(field))
                context.serialize(getattr(value, field.name), None, encoder)
        encoder.write(BREAK_MARKER)


class DefaultValueSerializer(ValueSerializer):
    def serialize(self, value: Any, type_name: Optional[str], encoder: CBOREncoder, context: SerializationContext):
        if isinstance(value, (int, float, str, bool, decimal.Decimal)):
            encoder.encode(value)
        elif value is None:
            encoder.encode_none(None)
        elif isinstance(value, UUID):
            encoder.encode(value.bytes)
        elif isinstance(value, Enum):
            encoder.encode(value.value)
        elif isinstance(value, Path):
            encoder.encode(str(value))
        elif isinstance(value, (list, set, tuple)):
            encoder.encode_length(4, len(value))
            for item in value:
                context.serialize(item, None, encoder)
        elif isinstance(value, Markers):
            if (id := context.remoting_context.try_get_id(value)):
                encoder.encode_int(id)
            else:
                id = context.remoting_context.add(value)
                encoder.encode_length(5, 3)
                encoder.encode_string('@ref')
                encoder.encode_int(id)
                encoder.encode_string('id')
                encoder.encode_uuid(value.id)
                encoder.encode_string('markers')
                encoder.encode_length(4, len(value.markers))
                for marker in value.markers:
                    context.serialize(marker, None, encoder)
        elif isinstance(value, (Marker, Style)):
            if (id := context.remoting_context.try_get_id(value)):
                encoder.encode_int(id)
            else:
                id = context.remoting_context.add(value)
                encoder.write(INDEFINITE_MAP_START)
                encoder.encode_string("@c")
                encoder.encode_string(to_java_type_name(type(value)))
                encoder.encode_string('@ref')
                encoder.encode_int(id)
                for field in fields(value):
                    if field.name[0] == '_' and (not hasattr(field.type,
                                                            '__origin__') or field.type.__origin__ is not ClassVar):
                        encoder.encode_string(to_java_field_name(field))
                        context.serialize(getattr(value, field.name), None, encoder)
                encoder.write(BREAK_MARKER)
        elif isinstance(value, bytes):
            # FIXME verify that this can be deserialized
            encoder.encode(value)
        elif isinstance(value, complex):
            encoder.encode(str(value))
        else:
            ValueSerializer.write_object_using_reflection(value, type_name, False, encoder, context)


def delegate_based_serializer(delegate: Callable[[Any, Optional[str], CBOREncoder, SerializationContext], None]):
    class DelegateBasedSerializer(ValueSerializer):
        def serialize(self, value: Any, type_name: Optional[str], encoder: CBOREncoder, context: SerializationContext):
            delegate(value, type_name, encoder, context)

    return DelegateBasedSerializer


class ParseErrorSender(Sender):
    def send(self, after, before, ctx):
        visitor = self.Visitor()
        visitor.visit(after, ctx.fork(visitor, before))

    class Visitor(ParseErrorVisitor):
        def visit(self, tree, ctx, parent: Optional[Cursor] = None):
            self.cursor = Cursor(self.cursor, tree)
            ctx.send_node(tree, lambda x: x, ctx.send_tree)
            self.cursor = self.cursor.parent

            return tree

        def visit_parse_error(self, parse_error, ctx):
            ctx.send_value(parse_error, lambda v: v.id)
            ctx.send_node(parse_error, lambda v: v.markers, ctx.send_markers)
            ctx.send_value(parse_error, lambda v: v.source_path)
            ctx.send_typed_value(parse_error, lambda v: v.file_attributes)
            ctx.send_value(parse_error, lambda v: v.charset_name)
            ctx.send_value(parse_error, lambda v: v.charset_bom_marked)
            ctx.send_typed_value(parse_error, lambda v: v.checksum)
            ctx.send_value(parse_error, lambda v: v.text)
            # ctx.send_node(parse_error, lambda v: v.erroneous, ctx.send_tree)
            return parse_error
