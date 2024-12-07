# -*- coding: utf-8 -*-
from __future__ import absolute_import
import base64
from abc import ABCMeta, abstractmethod

from six import with_metaclass


class BaseSchemaGenerator(with_metaclass(ABCMeta)):
    """Abstract base class for Swagger scheme generatorself.

    TODO....
    """

    @classmethod
    @abstractmethod
    def generate_schema(cls, obj):
        """Must be implemented in sub-class."""
        pass

    _converters = {
        "float16": {"type": "number", "format": "float"},
        "float32": {"type": "number", "format": "float"},
        "float64": {"type": "number", "format": "double"},
        "int8": {"type": "integer", "format": "int8"},
        "int16": {"type": "integer", "format": "int16"},
        "int32": {"type": "integer", "format": "int32"},
        "int64": {"type": "integer", "format": "int64"},
        "uint8": {"type": "integer", "format": "uint8"},
        "uint16": {"type": "integer", "format": "uint16"},
        "uint32": {"type": "integer", "format": "uint32"},
        "uint64": {"type": "integer", "format": "uint64"},
        "bool": {"type": "boolean"},
        "object": {"type": "object"},
    }

    @classmethod
    def get_swagger_for_dtype(cls, dtype):
        if len(dtype) == 0:
            if dtype.subdtype is None:  # scalar type
                swag = cls._get_swagger_for_scalar_dtype(dtype)
            else:  # sub-array type
                swag_subtype = cls.get_swagger_for_dtype(dtype.subdtype[0])
                swag = cls.get_swagger_for_array_type(swag_subtype, dtype.subdtype[1])
        else:  # structured type
            properties = {
                name: cls.get_swagger_for_dtype(dtype[name]) for name in dtype.names
            }
            swag = {"type": "object", "properties": properties}
        return swag

    @classmethod
    def get_swagger_for_array_type(cls, item_swag_type, shape):
        swag = {"type": "array", "items": item_swag_type}
        if len(shape) > 1:
            for _ in range(len(shape) - 1):
                swag = {"type": "np.ndarray", "items": swag}
        return swag

    @classmethod
    def _get_swagger_for_scalar_dtype(cls, dtype):
        name = dtype.name.lower()
        if name in cls._converters:
            return cls._converters.get(name)
        elif name.startswith("datetime"):
            return {"type": "string", "format": "date-time"}
        elif name.startswith("str"):
            return {"type": "string"}
        elif name.startswith("bytes") or type_name.startswith("void"):
            return {"type": "string", "format": "binary"}
        elif name.startswith("timedelta"):
            return {"type": "string", "format": "timedelta"}
        else:
            raise TypeError("Unsupported data type '{}'".format(name))

    @classmethod
    def get_swagger_examples(cls, iterable, record_schema, count):
        examples = []
        for i in range(count):
            example = cls._get_swagger_example_record(record_schema, iterable[i])
            examples.append(example)
        return examples

    @classmethod
    def _get_swagger_example_record(cls, item_swagger_schema, data_item):
        item_type = item_swagger_schema["type"]
        if item_type == "object":
            if "properties" in item_swagger_schema:
                sample_swag = dict()
                for field in item_swagger_schema["properties"]:
                    sample_swag[field] = cls._get_swagger_example_record(
                        item_swagger_schema["properties"][field], data_item[field]
                    )
            elif "additionalProperties" in item_swagger_schema:
                sample_swag = dict()
                for field in data_item:
                    sample_swag[field] = cls._get_swagger_example_record(
                        item_swagger_schema["additionalProperties"], data_item[field]
                    )
            else:
                sample_swag = str(data_item)
        elif item_swagger_schema["type"] == "array":
            sample_swag = []
            subarray_item_swagger = item_swagger_schema["items"]
            for i in range(len(data_item)):
                array_item_sample = cls._get_swagger_example_record(
                    subarray_item_swagger, data_item[i]
                )
                sample_swag.append(array_item_sample)
        elif item_type == "number":
            sample_swag = float(data_item)
        elif item_type == "integer":
            sample_swag = int(data_item)
        elif item_type == "bool":
            sample_swag = bool(data_item)
        elif item_type == "string" and "format" in item_swagger_schema:
            if item_swagger_schema["format"] == "date":
                sample_swag = cls._date_item_to_string(data_item)
            elif item_swagger_schema["format"] == "date-time":
                sample_swag = cls._timestamp_item_to_string(data_item)
            elif item_swagger_schema["format"] == "binary":
                sample_swag = base64.b64encode(data_item).decode("utf-8")
            else:
                sample_swag = str(data_item)
        else:
            sample_swag = str(data_item)
        return sample_swag

    @classmethod
    @abstractmethod
    def _date_item_to_string(cls, date_item):
        pass

    @classmethod
    @abstractmethod
    def _timestamp_item_to_string(cls, date_item):
        pass
