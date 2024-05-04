import socket

import aiohttp
from censys.search import CensysHosts
from rich.progress import Progress
from dataclasses import dataclass
from typing import Dict, Optional

import utils

positive_results: Dict[str, dict] = {}
censys = CensysHosts()


@dataclass
class Censys:
    subdomain: str
    ip: int

    async def search(self) -> None:
        port_service_list = []
        query_result = censys.search(self.ip, per_page=5)
        query = query_result()
        if len(query) > 0:
            services = query[0].get("services")

            for service in services:
                port = service["port"]
                service_name = service["service_name"]
                protocol = service["transport_protocol"]
                await utils.custom_print(
                    f"Port: {port}, Service: {service_name}, Protocol: {protocol}",
                    suffix="port"
                )
                port_service_list.append(f"Port: {port}, Service: {service_name}")

            positive_results[self.subdomain] = {
                "ip": self.ip,
                "port_service_list": port_service_list,
            }


class GetSubdomains:
    def __init__(self, target) -> None:
        self.target = target.path
        self.subdomains = utils.read_file("lib/subdomains/subdomains.txt")
        self.wildcard_record = self.get_record(
            f"nsfhsdjhfhasdfhsdfhjkfjsdfhsdf.{self.target}"
        )

        self.progress_bar = Progress()
        self.progress = self.progress_bar.add_task(
            "[red]Status: ", total=len(self.subdomains)
        )
        self.success = self.forbidden = self.auth = 0

    @staticmethod
    def get_record(domain: str) -> Optional[str]:
        try:
            ip = socket.gethostbyname(domain)
            return ip
        except socket.gaierror:
            return

    async def search_subdomains(self) -> None:
        with self.progress_bar:
            for subdomain in self.subdomains:
                full_domain = f"https://{subdomain}.{self.target}"

                requested_domain = self.get_record(f"{subdomain}.{self.target}")

                if not requested_domain or requested_domain == self.wildcard_record:
                    # await utils.custom_print(f"{full_domain} | Wildcard Record", "error")
                    self.progress_bar.update(
                        self.progress,
                        advance=1,
                        description=f"200: {self.success} | 401: {self.auth} | 403: {self.forbidden}",
                    )
                    continue

                try:
                    connector = aiohttp.TCPConnector(verify_ssl=False)
                    async with aiohttp.ClientSession(connector=connector) as session:
                        async with session.get(full_domain) as response:
                            print("stat" + response.status)
                            await utils.custom_print(
                                f"{full_domain} | {response.status} | {requested_domain}",
                                "success",
                            )
                            match response.status:
                                case 200:
                                    self.success += 1
                                case 401:
                                    self.auth += 1
                                case 403:
                                    self.forbidden += 1

                            await Censys(subdomain, requested_domain).search()

                except (Exception, BaseException):
                    await utils.custom_print(
                        f"{full_domain} | {requested_domain}", "success"
                    )
                    self.success += 1

                    await Censys(subdomain, requested_domain).search()

                self.progress_bar.update(
                    self.progress,
                    advance=1,
                    description=f"200: {self.success} | 401: {self.auth} | 403: {self.forbidden}",
                )

            else:
                await utils.custom_print(
                    f"SUBDOMAINS SEARCH FINISHED [SAVED TO - sudomains.{self.target}.txt]",
                    "success",
                )
                await utils.write_to_file(
                    positive_results, self.target, f"subdomains.{self.target}"
                )
