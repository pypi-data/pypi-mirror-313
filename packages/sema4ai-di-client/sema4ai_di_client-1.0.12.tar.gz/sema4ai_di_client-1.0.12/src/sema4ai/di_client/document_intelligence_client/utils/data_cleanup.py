# type: ignore
import numpy as np
import pandas as pd
from typing import Any

def convert_to_python_types(data):
    """
    Convert a dictionary containing pandas/numpy data types to native Python data types,
    handling nested dictionaries and lists.
    """
    def convert_value(value):
        if isinstance(value, dict):
            return {k: convert_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [convert_value(v) for v in value]
        elif isinstance(value, (np.integer, np.int_)):
            return int(value)
        elif isinstance(value, (np.floating, np.float64)):
            return float(value)
        elif isinstance(value, (np.ndarray, list)):
            return [convert_value(v) for v in value]
        elif isinstance(value, pd.Timestamp):
            return value.to_pydatetime()
        elif isinstance(value, pd.Timedelta):
            return value.to_pytimedelta()
        elif isinstance(value, pd.Series):
            return value.apply(convert_value).tolist()
        elif isinstance(value, pd.DataFrame):
            return value.applymap(convert_value).to_dict(orient='list')
        elif isinstance(value, (np.bool_, bool)):
            return bool(value)
        elif pd.isna(value):
            return None
        else:
            return value

    return convert_value(data)
