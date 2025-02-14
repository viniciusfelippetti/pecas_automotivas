from typing import Type, TypeVar, get_type_hints, get_origin, get_args, Union, Dict, Any
from dataclasses import fields, is_dataclass, asdict
from django.db.models import Model
from comum.base_transport import BaseTransport
from django.db.models.fields.files import FieldFile

T = TypeVar("T", bound=BaseTransport)
R = TypeVar("R", bound=Model)


def serializer(instance: R, dataclass_type: Type[T]) -> Dict[str, Any]:
    data = {}
    type_hints = get_type_hints(dataclass_type)

    for field in fields(dataclass_type):
        value = getattr(instance, field.name)
        field_type = type_hints[field.name]
        origin = get_origin(field_type)

        if origin is list:
            item_type = get_args(field_type)[0]
            related_manager = list(value.all()) if hasattr(value, "all") else value
            data[field.name] = [serializer(item, item_type) for item in related_manager]

        elif origin is Union and type(None) in get_args(field_type):
            inner_type = get_args(field_type)[0]
            if value is not None:
                if is_dataclass(inner_type):
                    data[field.name] = serializer(value, inner_type)
                else:
                    data[field.name] = value
            else:
                data[field.name] = None

        elif is_dataclass(field_type):
            data[field.name] = serializer(value, field_type)

        elif isinstance(value, FieldFile):
            data[field.name] = value.url if value else None

        else:
            data[field.name] = value

    return asdict(dataclass_type(**data))