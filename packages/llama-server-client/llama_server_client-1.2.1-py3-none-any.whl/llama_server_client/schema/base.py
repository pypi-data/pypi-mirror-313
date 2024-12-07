import json
from abc import ABC
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, Optional, TypeVar, Type
from uuid import UUID

import msgpack
from dacite import from_dict


def encoder_default(obj: Any) -> Any:
    """
    Custom encoder for serializing objects to be used with msgpack.

    :param obj: The object to be serialized. :return: A serialized representation of the object, converting UUIDs to
    bytes, datetimes to timestamps, and Enums to their values.
    """
    if isinstance(obj, UUID):
        return obj.bytes
    if isinstance(obj, datetime):
        return int(obj.timestamp() * 1_000_000_000)
    if isinstance(obj, Enum):
        return obj.value
    return obj


def decode_with_map(obj: Any, decode_map: Dict[str, Any]) -> Any:
    """
    Decodes an object using a provided mapping of keys to functions, facilitating custom deserialization.

    :param obj: The object to be decoded.
    :param decode_map: A dictionary mapping attribute names to their decoding functions.
    :return: The decoded object with its attributes transformed as per the decode map.
    """
    for key, func in decode_map.items():
        if key in obj and obj[key] is not None:
            if func == UUID:
                obj[key] = func(bytes=obj[key])
                continue
            if func == datetime:
                obj[key] = func.fromtimestamp(int(obj[key]) / 1_000_000_000, tz=timezone.utc)
            else:
                obj[key] = func(obj[key])
    return obj


def json_serializer(obj):
    """
    Custom serializer for JSON, specifically handling UUIDs, datetimes, and Enums.

    :param obj: The object to be serialized. :return: A JSON-friendly representation of the object, converting UUIDs
    to strings, datetimes to ISO format, and Enums to their names.
    """
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.name
    raise TypeError(f"Type {type(obj)} not serializable")


T = TypeVar("T")


@dataclass
class Base(ABC):
    """
    Base is an abstract data class providing serialization and deserialization methods for MessagePack and JSON.

    It offers a standard approach to pack and unpack data across different data classes.
    """

    def msgpack_pack(self) -> Optional[bytes]:
        """
        Serializes the object to MessagePack format.

        :return: The object serialized in MessagePack format as bytes, or None if serialization fails.
        """
        return msgpack.packb(asdict(self), default=encoder_default, use_bin_type=True)

    def to_json_str(self, indent: int = None, exclude_none: bool = True) -> str:
        """
        Converts the object to a JSON string, optionally excluding fields with null values.

        :param indent: The number of spaces for indentation.
        :param exclude_none: Whether to exclude fields with null values. Default is True.
        :return: The object serialized as a JSON string with indentation for readability.
        """
        if exclude_none:
            obj_dict = asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
        else:
            obj_dict = asdict(self)

        return json.dumps(obj_dict, default=json_serializer, indent=indent)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        """
        Provides a mapping for decoding the fields of an object.

        :return: A dictionary where keys are field names and values are their corresponding data types or decoding
        functions.
        """
        return {}

    @classmethod
    def decode_default(cls: Type[T],
                       data: Any
                       ) -> Optional[T]:
        """
        Decodes a dictionary into an object of class T using the class's decode map.

        :param data: The dictionary to decode.
        :return: An instance of class T created from the decoded data, or None if decoding fails.
        """
        return decode_with_map(data, cls.decode_map())

    @classmethod
    def msgpack_unpack(cls: Type[T],
                       data: Any
                       ) -> Optional[T]:
        """
        Unpacks MessagePack data into an object of class T.

        :param data: The MessagePack data to unpack.
        :return: An instance of class T created from the unpacked data, or None if unpacking fails.
        """
        unpacked_dict = msgpack.unpackb(data, object_hook=cls.decode_default,
                                        strict_map_key=False,
                                        raw=False)
        return from_dict(cls, unpacked_dict)


T = TypeVar('T', bound=Base)
