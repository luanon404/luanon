import requests
from dataclasses import dataclass


@dataclass
class HCaptcha:
    __slots__ = ["host", "site_key"]
    host: str
    site_key: str
    worker: int = 1
    session: requests.Session = requests.Session()
    debug: bool = False

    def solve(self, referer: str = "", worker: int = 1):
        worker = worker or self.worker
