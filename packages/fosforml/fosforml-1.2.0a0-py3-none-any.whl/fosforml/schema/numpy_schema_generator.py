# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
from datetime import datetime

import numpy as np

from ..schema.base_schema_generator import BaseSchemaGenerator


class NumpySchemaGenerator(BaseSchemaGenerator):
    """Schema generator for numpy ndarray."""

    @classmethod
    def generate_schema(cls, ndarray):
        swagger_item_type = cls.get_swagger_for_dtype(ndarray.dtype)
        swagger_schema = cls.get_swagger_for_array_type(
            swagger_item_type, ndarray.shape
        )

        # Create a couple of example records
        count = min(len(ndarray), 2)
        examples = cls.get_swagger_examples(ndarray, swagger_schema["items"], count)
        swagger_schema["example"] = examples
        return swagger_schema

    @classmethod
    def _date_item_to_string(cls, date_item):
        return date_item.astype(datetime).strftime("%Y-%m-%d")

    @classmethod
    def _timestamp_item_to_string(cls, date_item):
        return date_item.astype(datetime).strftime("%Y-%m-%d %H:%M:%S,%f")
