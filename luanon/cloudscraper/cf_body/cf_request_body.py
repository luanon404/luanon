"""
    Tác giả: GnU
    Ngày tạo: 11/05/2023
    ©2023 LuaNonTeam
"""

import json

from typing import override
from dataclasses import dataclass

from .cf_base_body import CfBaseBody
from .cf_lz_string import CfLzString


@dataclass
class CfRequestBody(CfBaseBody):
    __slots__ = ["secret_key"]
    secret_key: str

    @override
    def encode(self, value: dict) -> str:
        # Convert to javascript JSON object
        json_value = json.dumps(value, separators=(",", ":"))
        cf_lz_string = CfLzString(self.secret_key)
        value = cf_lz_string.text_to_base64(json_value)
        return value

    @override
    def decode(self, value: str) -> dict:
        cf_lz_string = CfLzString(self.secret_key)
        value = json.loads(cf_lz_string.base64_to_text(value))
        return value
