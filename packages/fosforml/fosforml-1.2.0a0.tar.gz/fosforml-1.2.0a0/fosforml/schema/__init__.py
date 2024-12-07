# -*- coding: utf-8 -*-
import base64
import datetime
import json

import numpy as np
import pandas as pd
import pytz

from fosforml.schema.numpy_schema_generator import NumpySchemaGenerator
from fosforml.schema.pandas_schema_generator import PandasSchemaGenerator


def generate_service_schema(inputs, outputs):

    input_schema = _generate_obj_schema(inputs)
    output_schema = _generate_obj_schema(outputs)
    return {"input": input_schema, "output": output_schema}


def _generate_obj_schema(obj):

    if isinstance(obj, pd.core.frame.DataFrame):
        schema = PandasSchemaGenerator.generate_schema(obj)
    elif isinstance(obj, np.ndarray):
        schema = NumpySchemaGenerator.generate_schema(obj)
    else:
        schema = get_swagger_from_python_sample(obj)
    return schema


def get_swagger_from_python_sample(python_data):
    """Generate swagger schema definition for python primitive object."""
    if python_data is None:
        raise ValueError("Python data cannot be None")

    schema = None

    # Python 3 specific type handling
    if type(python_data) is int:
        schema = {"type": "integer", "format": "int64", "example": python_data}
    elif type(python_data) is bytes:
        # Bytes type is not json serializable so will convert to a base 64 string for the sample
        sample = base64.b64encode(python_data).decode("utf-8")
        schema = {"type": "string", "format": "byte", "example": sample}
    elif type(python_data) is range:
        schema = _get_swagger_for_list(
            python_data, {"type": "integer", "format": "int64"}
        )

    # All Python versions handling
    if type(python_data) is str:
        schema = {"type": "string", "example": python_data}
    elif type(python_data) is float:
        schema = {"type": "number", "format": "double", "example": python_data}
    elif type(python_data) is bool:
        schema = {"type": "boolean", "example": python_data}
    elif type(python_data) is datetime.date:
        sample = python_data.strftime("%d-%m-%Y")
        schema = {"type": "string", "format": "date", "example": sample}
    elif type(python_data) is datetime.datetime:
        date_time_with_zone = python_data
        if python_data.tzinfo is None:
            # If no timezone data is passed in, consider UTC
            date_time_with_zone = datetime.datetime(
                python_data.year,
                python_data.month,
                python_data.day,
                python_data.hour,
                python_data.minute,
                python_data.second,
                python_data.microsecond,
                pytz.utc,
            )
        sample = date_time_with_zone.strftime("%d-%m-%Y %H:%M:%S")
        schema = {"type": "string", "format": "date-time", "example": sample}
    elif type(python_data) is datetime.time:
        time_with_zone = python_data
        if python_data.tzinfo is None:
            # If no timezone data is passed in, consider UTC
            time_with_zone = datetime.time(
                python_data.hour,
                python_data.minute,
                python_data.second,
                python_data.microsecond,
                pytz.utc,
            )
        sample = time_with_zone.strftime("%H:%M:%S")
        schema = {"type": "string", "format": "time", "example": sample}
    elif isinstance(python_data, bytearray):
        # Bytes type is not json serializable so will convert to a base 64 string for the sample
        sample = base64.b64encode(python_data).decode("utf-8")
        schema = {"type": "string", "format": "byte", "example": sample}
    elif type(python_data) is list or type(python_data) is tuple:
        schema = _get_swagger_for_list(python_data)
    elif type(python_data) is dict:
        schema = {"type": "dict", "example": python_data}
    # If we didn't match any type yet, try out best to fit this to an object
    if schema is None:
        schema = {"type": "object", "example": python_data}

    # ensure the schema is JSON serializable
    try:
        json.dumps(schema)
    except TypeError as te:
        raise TypeError("ERR_PYTHON_DATA_NOT_JSON_SERIALIZABLE")

    return schema


def _get_swagger_for_list(python_data, item_swagger_type={"type": "object"}):
    sample_size = min(len(python_data), 2)
    sample = []
    for i in range(sample_size):
        sample.append(python_data[i])
    return {"type": "array", "items": item_swagger_type, "example": sample}
