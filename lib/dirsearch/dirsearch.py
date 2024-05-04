from rich.progress import Progress
import aiohttp
from typing import Dict, Tuple
from enum import Enum
from pathlib import Path

import utils

positive_results: Dict[str, Dict[str, str]] = {}


class StatusCategory(Enum):
    SUCCESS = "success"
    DENIED = "denied"
    AUTH = "auth"
    ERROR = "error"


class DirSearch:
    STATUS_CODE_MAP = {
        403: StatusCategory.DENIED,
        401: StatusCategory.AUTH,
    }

    def __init__(self, target: Path) -> None:
        """
        Initialize the DirSearch object.

        :param target: A Path object representing the target path.
        """
        self.target = target
        self.paths = utils.read_file("lib/dirsearch/paths.txt")

        self.progress_bar = Progress()
        self.progress_task = self.progress_bar.add_task(
            "[red]Status: ", total=len(self.paths)
        )
        self.counter = {
            StatusCategory.SUCCESS: 0,
            StatusCategory.DENIED: 0,
            StatusCategory.AUTH: 0,
        }

    def update_counters(self, status_code: int) -> StatusCategory:
        """
        Update the counters based on the status code received.

        :param status_code: The HTTP status code from the response.
        :return: The status category for the received status code.
        """
        category = self.STATUS_CODE_MAP.get(status_code, StatusCategory.SUCCESS)
        self.counter[category] += 1
        return category

    async def search_paths(self) -> None:
        """
        Asynchronously search for valid paths on the target.
        """
        async with aiohttp.ClientSession() as session:
            for path in self.paths:
                for scheme in ["https", "http"]:
                    full_url = f"{scheme}://{self.target}/{path}"
                    try:
                        response = await session.get(full_url)
                        status_category = self.update_counters(response.status)
                        utils.custom_print(
                            f"{full_url} | {response.status}", status_category.value
                        )
                        positive_results[full_url] = {"status": str(response.status)}
                    except aiohttp.ClientError as error:
                        utils.custom_print(
                            f"Error requesting {full_url}: {error}",
                            StatusCategory.ERROR.value,
                        )
                    finally:
                        self.progress_bar.update(
                            self.progress_task,
                            advance=1,
                            description=f"200: {self.counter[StatusCategory.SUCCESS]} | "
                            f"401: {self.counter[StatusCategory.AUTH]} | "
                            f"403: {self.counter[StatusCategory.DENIED]}",
                        )

        utils.custom_print(
            f"DIRSEARCH FINISHED [SAVED TO - dirsearch.{self.target}.txt]",
            StatusCategory.SUCCESS.value,
        )
        await utils.write_to_file(
            positive_results, self.target, file_name=f"dirsearch.{self.target}"
        )
