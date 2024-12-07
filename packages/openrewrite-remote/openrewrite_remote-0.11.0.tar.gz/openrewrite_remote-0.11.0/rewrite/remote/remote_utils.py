import socket
import struct
from enum import Enum, auto
from io import BytesIO
from typing import Callable, List, Optional, TypeVar, Dict, TYPE_CHECKING, Iterable, cast, Type

from cbor2 import CBORDecoder, CBORDecodeValueError

from .event import EventType

if TYPE_CHECKING:
    from .receiver import ReceiverContext, DetailsReceiver

T = TypeVar('T')
I = TypeVar('I')


class Operation(Enum):
    Add = auto()
    Delete = auto()
    NoChange = auto()
    Update = auto()
    Move = auto()


def receive_nodes(before: Optional[List[T]],
                  details: Callable[[Optional[T], Optional[str], 'ReceiverContext'], T],
                  ctx: 'ReceiverContext') -> Optional[List[T]]:
    list_event = ctx.receiver.receive_value(list)
    if list_event.event_type == EventType.NoChange:
        return before
    elif list_event.event_type == EventType.Delete:
        return None
    elif list_event.event_type == EventType.Add:
        after_size = list_event.msg
        after = [None] * after_size  # Preallocate list
        for i in range(after_size):
            diff_event = ctx.receiver.receive_node()
            if diff_event.event_type == EventType.Add:
                after[i] = details.receive_details(None, diff_event.concrete_type, ctx)
            elif diff_event.event_type == EventType.NoChange:
                after[i] = None  # Or some default value
            else:
                raise NotImplementedError(f"Unexpected operation: {diff_event.event_type}")
        return after
    elif list_event.event_type == EventType.Update:
        return _receive_updated_nodes(before, list_event.msg, details, ctx)
    else:
        raise NotImplementedError(f"Unexpected operation: {list_event.event_type}")


def _receive_updated_nodes(before: List[T],
                           after_size: int,
                           details: 'DetailsReceiver[T]',
                           ctx: 'ReceiverContext') -> List[T]:
    modified = False
    after_list = before
    evt = ctx.receiver.receive_node()
    if evt.event_type != EventType.StartList:
        raise ValueError(f"Expected start list event: {evt.event_type}")

    before_idx = 0
    while True:
        evt = ctx.receiver.receive_node()
        if evt.event_type in (EventType.NoChange, EventType.EndList):
            break

        if evt.event_type in (EventType.Delete, EventType.Update, EventType.Add):
            if not modified:
                after_list = _copy_range(before, before_idx)
                modified = True

        if evt.event_type == EventType.NoChange:
            if modified:
                after_list.append(before[before_idx])
            before_idx += 1
        elif evt.event_type == EventType.Delete:
            before_idx += 1
        elif evt.event_type == EventType.Update:
            after_list.append(details.receive_details(before[before_idx], evt.concrete_type, ctx))
            before_idx += 1
        elif evt.event_type == EventType.Add:
            after_list.append(details.receive_details(None, evt.concrete_type, ctx))

        if evt.event_type == EventType.EndList:
            break

    return after_list[:after_size] if len(after_list) > after_size else after_list


def receive_values(before: Optional[List[T]], type: Type, ctx: 'ReceiverContext') -> Optional[List[T]]:
    list_event = ctx.receiver.receive_value(list)
    if list_event.event_type == EventType.NoChange:
        return before
    elif list_event.event_type == EventType.Delete:
        return None
    elif list_event.event_type == EventType.Add:
        after_size = list_event.msg
        after = [None] * after_size  # Preallocate list
        for i in range(after_size):
            diff_event = ctx.receiver.receive_value(type)
            if diff_event.event_type == EventType.Add:
                after[i] = diff_event.msg
            elif diff_event.event_type == EventType.NoChange:
                after[i] = None  # Or some default value
            else:
                raise NotImplementedError(f"Unexpected operation: {diff_event.event_type}")
        return after
    elif list_event.event_type == EventType.Update:
        return _receive_updated_values(before, list_event.msg, type, ctx)
    else:
        raise NotImplementedError(f"Unexpected operation: {list_event.event_type}")


def _receive_updated_values(before: List[T], after_size: int, type: Type, ctx: 'ReceiverContext') -> List[T]:
    modified = False
    after_list = before
    evt = ctx.receiver.receive_node()
    if evt.event_type != EventType.StartList:
        raise ValueError(f"Expected start list event: {evt.event_type}")

    before_idx = 0
    while True:
        evt = ctx.receiver.receive_value(type)
        if evt.event_type in (EventType.NoChange, EventType.EndList):
            break

        if evt.event_type in (EventType.Delete, EventType.Update, EventType.Add):
            if not modified:
                after_list = _copy_range(before, before_idx)
                modified = True

        if evt.event_type == EventType.NoChange:
            if modified:
                after_list.append(before[before_idx])
            before_idx += 1
        elif evt.event_type == EventType.Delete:
            before_idx += 1
        elif evt.event_type in (EventType.Update, EventType.Add):
            after_list.append(evt.msg)
            if evt.event_type == EventType.Update:
                before_idx += 1

        if evt.event_type == EventType.EndList:
            break

    return after_list[:after_size] if len(after_list) > after_size else after_list


def _copy_range(before: Iterable[T], j: int) -> List[T]:
    if isinstance(before, list):
        return before[:j]
    elif hasattr(before, 'getrange'):  # If the object has a 'getrange' method (e.g., an immutable list)
        return before.getrange(0, j)
    else:
        return list(before)[:j]


def calculate_list_diff(
        before: List[T],
        after: List[T],
        id_function: Callable[[T], I],
        consumer: Callable[[Operation, int, int, Optional[T], Optional[T]], None]
) -> None:
    before_idx, after_idx = 0, 0
    before_size, after_size = len(before), len(after)
    after_map = None

    while before_idx < before_size or after_idx < after_size:
        # Check if we've reached the end of either of the lists
        if before_idx >= before_size:
            consumer(Operation.Add, -1, after_idx, None, after[after_idx])
            after_idx += 1
            continue
        elif after_idx >= after_size:
            consumer(Operation.Delete, before_idx, -1, before[before_idx], None)
            before_idx += 1
            continue

        if before[before_idx] == after[after_idx]:
            consumer(
                Operation.NoChange,
                before_idx,
                after_idx,
                before[before_idx],
                after[after_idx]
            )
            before_idx += 1
            after_idx += 1
        else:
            before_id = id_function(before[before_idx])
            after_id = id_function(after[after_idx])

            if before_id == after_id:
                consumer(
                    Operation.Update,
                    before_idx,
                    after_idx,
                    before[before_idx],
                    after[after_idx]
                )
                before_idx += 1
                after_idx += 1
            else:
                if after_map is None:
                    after_map = create_index_map(after, after_idx, id_function)

                # If elements at current indices are not equal, figure out the operation
                if before_id not in after_map:
                    consumer(Operation.Delete, before_idx, -1, before[before_idx], None)
                    before_idx += 1
                else:
                    consumer(Operation.Add, -1, after_idx, None, after[after_idx])
                    after_idx += 1


def create_index_map(
        lst: List[T],
        from_index: int,
        id_function: Callable[[T], I]
) -> Dict[I, int]:
    result = {}
    for i in range(from_index, len(lst)):
        result[id_function(lst[i])] = i
    return result


def _decode_length(decoder: CBORDecoder, subtype: int, allow_indefinite: bool = False):
    if subtype < 24:
        return subtype
    elif subtype == 24:
        return decoder.read(1)[0]
    elif subtype == 25:
        return cast(int, struct.unpack(">H", decoder.read(2))[0])
    elif subtype == 26:
        return cast(int, struct.unpack(">L", decoder.read(4))[0])
    elif subtype == 27:
        return cast(int, struct.unpack(">Q", decoder.read(8))[0])
    elif subtype == 31 and allow_indefinite:
        return None
    else:
        raise CBORDecodeValueError(f"unknown unsigned integer subtype 0x{subtype:x}")

def decode_array_start(decoder: CBORDecoder):
    initial_byte = decoder.read(1)[0]
    major_type = initial_byte >> 5
    assert major_type == 4
    subtype = initial_byte & 31
    return _decode_length(decoder, subtype, allow_indefinite=True)


COPY_BUFFER_SIZE = 4096
COPY_BUFFER = bytearray(COPY_BUFFER_SIZE)
COMMAND_END = bytes([0x81, 0x17])

def read_to_command_end(sock: socket.socket) -> BytesIO:
    memory_stream = BytesIO()

    try:
        while True:
            bytes_read = sock.recv_into(COPY_BUFFER, len(COPY_BUFFER))
            if bytes_read == 0:
                break
            memory_stream.write(COPY_BUFFER[:bytes_read])
            if (bytes_read > 1 and
                    COPY_BUFFER[bytes_read - 2] == COMMAND_END[0] and
                    COPY_BUFFER[bytes_read - 1] == COMMAND_END[1]):
                break
            elif bytes_read == 1:
                original_position = memory_stream.tell()
                memory_stream.seek(-2, 1)  # Move back by 2 bytes
                if (memory_stream.read(1)[0] == COMMAND_END[0] and
                        memory_stream.read(1)[0] == COMMAND_END[1]):
                    memory_stream.seek(original_position)
                    break
    except socket.error as e:
        print(f"Socket error: {e}")

    memory_stream.seek(0)
    return memory_stream
