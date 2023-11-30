"""
    Tác giả: GnU
    Ngày tạo: 11/09/2023
    ©2023 LuaNonTeam
"""

from luanon.base import base_install, base_uninstall

packages = {
    "python": [
        "requests==2.31.0",
        "brotli==1.1.0"
    ],
    "nodejs": []
}

Install = lambda: base_install(packages)
Uninstall = lambda: base_uninstall(packages)
