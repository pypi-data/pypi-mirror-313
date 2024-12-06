import base64
from datetime import date, datetime, time, timedelta, timezone
from typing import Any
import json
import sys

from dateutil.parser import parse
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.ipc as ipc


class SarusJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, np.ndarray):
            return {"_type": "numpy.ndarray", "data": obj.tolist()}
        elif isinstance(obj, pd.DataFrame):
            return {
                "_type": "pandas.DataFrame",
                "data": obj.to_json(date_format="iso"),
            }
        elif isinstance(obj, pd.Series):
            return {
                "_type": "pandas.Series",
                "data": obj.to_json(date_format="iso"),
            }
        elif isinstance(obj, pd.Timestamp):
            return {"_type": "pandas.Timestamp", "data": obj.isoformat()}
        elif isinstance(obj, datetime):
            return {"_type": "datetime", "data": obj.isoformat()}
        elif isinstance(obj, timedelta):
            return {"_type": "timedelta", "data": obj.total_seconds()}
        elif isinstance(obj, timezone):
            utcoffset_result = obj.utcoffset(None)
            if utcoffset_result is not None:
                return {
                    "_type": "timezone",
                    "data": utcoffset_result.total_seconds(),
                }
            else:
                raise ValueError("Invalid timezone object")
        elif isinstance(obj, time):
            return {"_type": "time", "data": obj.isoformat()}
        elif isinstance(obj, date):
            return {"_type": "date", "data": obj.isoformat()}
        elif isinstance(obj, np.generic):
            if np.issubdtype(obj, np.complexfloating):
                complex_obj = obj.astype(np.complex128)
                return {
                    "_type": "numpy.complex",
                    "data": {
                        '"real"': complex_obj.real,
                        '"imag"': complex_obj.imag,
                    },
                }
            else:
                return {"_type": "numpy.generic", "data": obj.item()}
        elif isinstance(obj, pd.MultiIndex):
            return {
                "_type": "pandas.MultiIndex",
                "data": obj.tolist(),
                "names": obj.names,
                "levels": [level.tolist() for level in obj.levels],
                "codes": list(obj.codes),
            }
        elif isinstance(obj, pd.Index):
            return {
                "_type": "pandas.Index",
                "class": type(obj).__name__,
                "data": obj.tolist(),
                "dtype": str(obj.dtype),
            }
        elif isinstance(obj, pd.Period):
            return {
                "_type": "pandas.Period",
                "data": str(obj),
                "freq": obj.freqstr,
            }
        elif isinstance(obj, pd.Timedelta):
            return {"_type": "pandas.Timedelta", "data": obj.value}
        elif isinstance(obj, pd.Interval):
            return {"_type": "pandas.Interval", "data": (obj.left, obj.right)}
        elif isinstance(obj, pd.Categorical):
            return {
                "_type": "pandas.Categorical",
                "data": obj.tolist(),
                "categories": obj.categories.tolist(),
                "ordered": obj.ordered,
            }
        elif isinstance(obj, type):
            return {
                "_type": "class",
                "data": {'"name"': obj.__name__, '"module"': obj.__module__},
            }
        elif isinstance(obj, pd.api.extensions.ExtensionDtype):
            return {"_type": "dtype", "data": str(obj)}
        elif isinstance(obj, slice):
            return {"_type": "slice", "data": (obj.start, obj.stop, obj.step)}
        elif isinstance(obj, range):
            return {
                "_type": "range",
                "data": {
                    '"start"': obj.start,
                    '"stop"': obj.stop,
                    '"step"': obj.step,
                },
            }
        elif isinstance(obj, pa.Table):
            sink = pa.BufferOutputStream()
            writer = ipc.new_stream(sink, obj.schema)
            writer.write_table(obj)
            writer.close()
            serialized_data = (
                sink.getvalue()
            )  # This is the serialized data in a byte array format
            base64_encoded_data = base64.b64encode(serialized_data).decode(
                "utf-8"
            )
            return {"_type": "pa.Table", "data": base64_encoded_data}
        return super().default(obj)

    def encode_obj(self, obj: Any) -> Any:
        if isinstance(obj, tuple):
            return {
                "_type": "tuple",
                "data": [self.encode_obj(v) for v in obj],
            }
        elif isinstance(obj, list):
            return [self.encode_obj(v) for v in obj]
        elif isinstance(obj, dict):
            return {self.encode(k): self.encode_obj(v) for k, v in obj.items()}
        return obj

    def encode(self, obj: Any) -> str:
        obj_transformed = self.encode_obj(obj)
        return super().encode(obj_transformed)

    @classmethod
    def encode_bytes(cls, obj: Any) -> bytes:
        encoder = cls()
        return (encoder.encode(obj)).encode("utf-8")


class SarusJSONDecoder(json.JSONDecoder):
    def decode(self, s: str, *args: Any, **kwargs: Any) -> Any:
        obj = super().decode(s, *args, **kwargs)
        return self.decode_obj(obj)

    def decode_obj(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            if "_type" in obj:
                data = self.decode_obj(obj["data"])
                if obj["_type"] == "tuple":
                    return tuple(self.decode_obj(v) for v in data)
                elif obj["_type"] == "numpy.ndarray":
                    return np.array(data)
                elif obj["_type"] == "pandas.DataFrame":
                    return pd.read_json(data, convert_dates=True)
                elif obj["_type"] == "pandas.Series":
                    return pd.read_json(data, typ="series", convert_dates=True)
                elif obj["_type"] == "pandas.Timestamp":
                    return pd.Timestamp(data)
                elif obj["_type"] == "datetime":
                    return parse(data)
                elif obj["_type"] == "timedelta":
                    return timedelta(seconds=data)
                elif obj["_type"] == "timezone":
                    return timezone(timedelta(seconds=data))
                elif obj["_type"] == "time":
                    return parse(data).time()
                elif obj["_type"] == "date":
                    return parse(data).date()
                elif obj["_type"] == "numpy.generic":
                    return np.array(data).item()
                elif obj["_type"] == "numpy.complex":
                    return np.complex128(complex(data["real"], data["imag"]))
                elif obj["_type"] == "pandas.Index":
                    cls = getattr(pd, obj["class"])
                    return cls(data, dtype=obj["dtype"])
                elif obj["_type"] == "pandas.MultiIndex":
                    return pd.MultiIndex(
                        levels=[pd.Index(level) for level in obj["levels"]],
                        codes=self.decode_obj(obj["codes"]),
                        names=obj["names"],
                    )
                elif obj["_type"] == "pandas.Period":
                    return pd.Period(data, freq=obj["freq"])
                elif obj["_type"] == "pandas.Timedelta":
                    return pd.to_timedelta(data)
                elif obj["_type"] == "pandas.Interval":
                    return pd.Interval(*data)
                elif obj["_type"] == "pandas.Categorical":
                    return pd.Categorical(
                        data,
                        categories=obj["categories"],
                        ordered=obj["ordered"],
                    )
                elif obj["_type"] == "class":
                    if data["module"] in ["builtins", "numpy", "pandas"]:
                        cls = getattr(
                            sys.modules[data["module"]], data["name"]
                        )
                        if isinstance(cls, type):
                            return cls
                        else:
                            raise ValueError("Decoded object is not a type")
                    else:
                        raise ValueError("Invalid module name")
                elif obj["_type"] == "dtype":
                    return pd.api.types.pandas_dtype(data)
                elif obj["_type"] == "slice":
                    return slice(*data)
                elif obj["_type"] == "range":
                    return range(data["start"], data["stop"], data["step"])
                elif obj["_type"] == "pa.Table":
                    binary_data = base64.b64decode(obj["data"])
                    buffer = pa.py_buffer(binary_data)
                    reader = ipc.open_stream(buffer)
                    deserialized_table = reader.read_all()
                    return deserialized_table
            return {self.decode(k): self.decode_obj(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.decode_obj(v) for v in obj]
        return obj

    @classmethod
    def decode_bytes(cls, b: bytes, *args: Any, **kwargs: Any) -> Any:
        decoder = cls()
        return decoder.decode(b.decode("utf-8"), *args, **kwargs)
