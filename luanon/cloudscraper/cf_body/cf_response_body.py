"""
    Tác giả: GnU
    Ngày tạo: 11/05/2023
    ©2023 LuaNonTeam
"""

import base64

from typing import override
from dataclasses import dataclass

from .cf_base_body import CfBaseBody


@dataclass
class CfResponseBody(CfBaseBody):
    __slots__ = ["c_ray"]
    c_ray: str

    @override
    def encode(self, value: str) -> str:
        # Hàm này không cần thiết
        return value

    @override
    def decode(self, value: str) -> str:
        binary = base64.b64decode(value.encode()).decode("latin1")
        result = []
        num_1 = 32
        for char in self.c_ray + "_0":
            num_1 ^= ord(char)
        for index, char in enumerate(binary):
            num_2 = ord(char)
            result.append(chr(((num_2 & 255) - num_1 - index % 65535 + 65535) % 255))
        value = "".join(result)
        if not value.startswith("window._"):
            # TODO: tìm hàm decode và thêm vào đây
            pass
        return value
