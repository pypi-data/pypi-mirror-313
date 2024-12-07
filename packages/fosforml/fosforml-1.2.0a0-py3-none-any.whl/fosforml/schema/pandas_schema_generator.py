# -*- coding: utf-8 -*-

from __future__ import absolute_import
from datetime import datetime

import numpy as np
import pandas as pd

from ..schema.base_schema_generator import BaseSchemaGenerator


class PandasSchemaGenerator(BaseSchemaGenerator):
    """Schema generator for pandas dataframe."""

    @classmethod
    def generate_schema(cls, df):
        cnames = df.columns.values.tolist()
        dtypes = df.dtypes.tolist()
        properties = {}
        for cname, dtype in zip(cnames, dtypes):
            if dtype.name == "object" and type(df[cname][0]) is str:
                dtype = np.dtype("str")
            properties[cname] = cls.get_swagger_for_dtype(dtype)

        record_schema = {"type": "object", "properties": properties}
        # Create a couple of example records
        count = min(len(df), 2)
        examples = cls.get_swagger_examples(df.iloc, record_schema, count)
        schema = {
            "type": "pd.core.frame.DataFrame",
            "items": record_schema,
            "example": examples,
        }
        return schema

    @classmethod
    def _date_item_to_string(cls, date_item):
        return date_item.astype(datetime).strftime("%Y-%m-%d")

    @classmethod
    def _timestamp_item_to_string(cls, date_item):
        return pd.Timestamp(date_item).to_pydatetime().strftime("%Y-%m-%d %H:%M:%S,%f")
