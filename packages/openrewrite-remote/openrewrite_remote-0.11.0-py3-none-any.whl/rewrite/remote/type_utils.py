import typing
from dataclasses import Field
from functools import lru_cache
from typing import Any, Type


def to_java_type_name_from_value(v: Any) -> str:
    if isinstance(v, bool):
        return 'java.lang.Boolean'
    elif isinstance(v, int):
        bit_length = v.bit_length()
        if  bit_length < 32:
            return 'java.lang.Integer'
        elif bit_length < 64:
            return 'java.lang.Long'
        else:
            return 'java.math.BigInteger'
    elif isinstance(v, complex):
        return 'java.lang.String'
    return to_java_type_name(type(v))


@lru_cache(maxsize=None)
def to_java_type_name(t: typing.Type) -> str:
    if t == bytes:
        # FIXME can we map this somehow?
        return None
    if t == bool:
        return 'java.lang.Boolean'
    if t == int:
        return 'java.lang.Integer'
    if t == str:
        return 'java.lang.String'
    if t == float:
        return 'java.lang.Double'
    if t == type(None):
        return 'null'
    if t.__module__.startswith('rewrite.java.support_types'):
        if t.__name__ == 'Space':
            return 'org.openrewrite.java.tree.Space'
        if t.__name__ == 'Comment':
            return 'org.openrewrite.java.tree.Comment'
        if t.__name__ == 'TextComment':
            return 'org.openrewrite.java.tree.TextComment'
        if t.__name__ == 'JLeftPadded':
            return 'org.openrewrite.java.tree.JLeftPadded'
        if t.__name__ == 'JRightPadded':
            return 'org.openrewrite.java.tree.JRightPadded'
        if t.__name__ == 'JContainer':
            return 'org.openrewrite.java.tree.JContainer'
    if t.__module__.startswith('rewrite.java.markers'):
        return 'org.openrewrite.java.marker.' + t.__qualname__
    if t.__module__.startswith('rewrite.java.tree'):
        return 'org.openrewrite.java.tree.J$' + t.__qualname__.replace('.', '$')
    if t.__module__.startswith('rewrite.python.support_types'):
        if t.__name__ == 'PyComment':
            return 'org.openrewrite.python.tree.PyComment'
        if t.__name__ == 'PyLeftPadded':
            return 'org.openrewrite.python.tree.PyLeftPadded'
        if t.__name__ == 'PyRightPadded':
            return 'org.openrewrite.python.tree.PyRightPadded'
        if t.__name__ == 'PyContainer':
            return 'org.openrewrite.python.tree.PyContainer'
    if t.__module__.startswith('rewrite.python.markers'):
        return 'org.openrewrite.python.marker.' + t.__qualname__
    if t.__module__.startswith('rewrite.python.style'):
        return 'org.openrewrite.python.style.' + t.__qualname__
    if t.__module__.startswith('rewrite.python.tree'):
        return 'org.openrewrite.python.tree.Py$' + t.__qualname__.replace('.', '$')
    if t.__module__.startswith('rewrite.marker'):
        if t.__name__ == 'ParseExceptionResult':
            return 'org.openrewrite.ParseExceptionResult'
        return 'org.openrewrite.marker.' + t.__qualname__.replace('.', '$')
    if t.__module__ == 'rewrite.parser' and t.__name__ == 'ParseError':
        return 'org.openrewrite.tree.ParseError'
    if t.__module__.startswith('rewrite.style'):
        return 'org.openrewrite.style.' + t.__qualname__
    if t.__module__.startswith('rewrite.') and t.__module__.endswith('.tree'):
        model = t.__module__.split('.')[1]
        return 'org.openrewrite.' + model + '.tree.' + model.capitalize() + '$' + t.__qualname__.replace('.', '$')
    return t.__module__ + '.' + t.__qualname__
    # raise NotImplementedError("to_java_type_name: " + str(o))


@lru_cache(maxsize=None)
def to_java_field_name(field: Field) -> str:
    return __convert_snake_to_camel(field.name[1:])


def __convert_snake_to_camel(field_name: str) -> str:
    # Remove leading underscore
    if field_name.startswith('_'):
        field_name = field_name[1:]

    # Convert snake case to camel case
    components = field_name.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


def get_type(type_name: str) -> Type:
    raise NotImplementedError("get_type for: " + type_name)
