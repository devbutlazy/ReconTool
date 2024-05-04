from urllib.parse import urlparse
import config
from pathlib import Path
import asyncio
import requests

from lib.dirsearch.dirsearch import DirSearch
from lib.subdomains.subdomains import GetSubdomains
from utils import custom_print


class Target:
    def __init__(self, domain: str, path: Path) -> None:
        self.domain = domain
        self.path = path
        self.user_agent = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
        }

    def get_subdomains(self):
        asyncio.create_task(GetSubdomains(self.domain).search_subdomains())

    def get_pathes(self):
        asyncio.create_task(DirSearch(self.domain).search_paths())

    async def basic_info(self, domain: str) -> None:
        domain = urlparse(domain).netloc or urlparse(domain).path
        data = requests.get(
            f"https://{domain}", allow_redirects=True, headers=self.user_agent
        )

        for subdata in data.headers:
            await custom_print(f"{subdata}: {data.headers[subdata]}", "additional")


class TargetStorage:
    @staticmethod
    def get(target: str) -> Target:
        target_path = Path(f"{config.TARGETS_STORAGE_PT}/{target}.txt")

        if not target_path.exists():
            target_path.mkdir()

        return Target(target, target_path)
