"""
    Tác giả: GnU
    Ngày tạo: 11/06/2023
    ©2023 LuaNonTeam
"""

from luanon.base import base_install, base_uninstall

packages = {
    "python": [
        "requests==2.31.0",
        "brotli==1.1.0"
    ],
    "nodejs": [
        "vm@0.1.0",
        # JSDOM
        "https://github.com/luanon404/jsdom-cloudflare/tarball/build --omit=dev"
    ]
}

Install = lambda: base_install(packages)
Uninstall = lambda: base_uninstall(packages)
