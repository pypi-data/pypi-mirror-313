# -*- coding: utf-8 -*-
import datetime

import numpy as np
import pandas as pd

from fosforml.schema import generate_service_schema


def test_get_all_schema():
    numeric_obj = 1
    float_obj = 1000.023
    string_obj = "test string"
    bool_obj = True
    dict_obj = {"abc": "pqr", "xyz": "qwerty"}
    array_obj = [
        [
            10.0,
            14.0,
            8.0,
            1.0,
            10.0,
            8.0,
            16.0,
            8.0,
            1.0,
            8.0,
            12.0,
            14.0,
            12.0,
            1.0,
            0.0,
        ]
    ]
    date_time_obj = datetime.datetime.now()

    test_data = {
        "numeric_obj": numeric_obj,
        "float_obj": float_obj,
        "string_obj": string_obj,
        "bool_obj": bool_obj,
        "dict_obj": dict_obj,
        "array_obj": array_obj,
        "date_time_obj": date_time_obj,
    }
    schema = generate_service_schema({}, numeric_obj)
    assert schema == {
        "input": {"type": "dict", "example": {}},
        "output": {"type": "integer", "format": "int64", "example": numeric_obj},
    }
    schema = generate_service_schema({}, float_obj)
    assert schema == {
        "input": {"type": "dict", "example": {}},
        "output": {"type": "number", "format": "double", "example": 1000.023},
    }
    schema = generate_service_schema({}, string_obj)
    assert schema == {
        "input": {"type": "dict", "example": {}},
        "output": {"type": "string", "example": string_obj},
    }
    schema = generate_service_schema({}, bool_obj)
    assert schema == {
        "input": {"type": "dict", "example": {}},
        "output": {"type": "boolean", "example": bool_obj},
    }
    schema = generate_service_schema({}, dict_obj)
    assert schema == {
        "input": {"type": "dict", "example": {}},
        "output": {"type": "dict", "example": dict_obj},
    }
    schema = generate_service_schema({}, array_obj)
    assert schema == {
        "input": {"type": "dict", "example": {}},
        "output": {"type": "array", "items": {"type": "object"}, "example": array_obj},
    }
    schema = generate_service_schema({}, date_time_obj)
    assert schema == {
        "input": {"type": "dict", "example": {}},
        "output": {
            "type": "string",
            "format": "date-time",
            "example": date_time_obj.strftime("%d-%m-%Y %H:%M:%S"),
        },
    }


def test_pandas_schema():
    test_data = ["sample", "string", "in", "pandas", "dataframe"]
    df = pd.DataFrame(test_data)
    schema = generate_service_schema({}, df)
    assert schema == {
        "input": {"type": "dict", "example": {}},
        "output": {
            "type": "pd.core.frame.DataFrame",
            "items": {"type": "object", "properties": {0: {"type": "string"}}},
            "example": [{0: "sample"}, {0: "string"}],
        },
    }


def test_ndarray_schema():
    arr = np.array([[1, 2, 3], [4, 2, 5]])
    schema = generate_service_schema(arr, arr)
    assert schema == {
        "input": {
            "type": "np.ndarray",
            "items": {"type": "array", "items": {"type": "integer", "format": "int64"}},
            "example": [[1, 2, 3], [4, 2, 5]],
        },
        "output": {
            "type": "np.ndarray",
            "items": {"type": "array", "items": {"type": "integer", "format": "int64"}},
            "example": [[1, 2, 3], [4, 2, 5]],
        },
    }
