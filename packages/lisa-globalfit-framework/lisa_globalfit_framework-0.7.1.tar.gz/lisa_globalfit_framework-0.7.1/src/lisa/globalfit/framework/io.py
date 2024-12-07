from dataclasses import asdict, is_dataclass
from datetime import datetime
from json import JSONEncoder, dumps

import numpy as np


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, datetime):
            return o.isoformat()
        if np.iscomplexobj(o):
            return str(o)
        return super().default(o)

    @classmethod
    def dumps(cls, o):
        return dumps(o, cls=cls)
