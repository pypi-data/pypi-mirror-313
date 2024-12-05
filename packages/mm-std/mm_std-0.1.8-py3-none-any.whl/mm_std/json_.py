import json
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from json import JSONEncoder
from typing import Any

from pydantic import BaseModel

from mm_std.result import Err, Ok


class CustomJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Ok):
            return {"ok": o.ok}
        if isinstance(o, Err):
            return {"err": o.err}
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, datetime | date):
            return o.isoformat()
        if is_dataclass(o) and not isinstance(o, type):
            return asdict(o)
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, BaseModel):
            return o.model_dump()
        if isinstance(o, Exception):
            return str(o)
        return JSONEncoder.default(self, o)


def json_dumps(data: object) -> str:
    return json.dumps(data, cls=CustomJSONEncoder)
