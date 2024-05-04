import asyncio
import argparse
from urllib.parse import urlparse
import os

from lib.generic import TargetStorage


async def main(domain):
    target = urlparse(urlparse(domain).netloc or urlparse(domain).path)
    target = TargetStorage.get(target)

    print(f"\033[1;32;48m[TARGET]: {domain}\033[1;37;0m\n")
    await target.basic_info(domain)
    print(f"\n\033[91m[1] Target Sudomains Search\033[0m")
    print(f"\033[91m[2] Target DirSearch\033[0m")

    choice = int(input("\033[91m>>> \033[0m"))
    match choice:
        case 1:
            target.get_subdomains()
        case 2:
            target.get_pathes()
        case _:
            print("\033[91m[!] Invalid choice\033[0m")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Recon Tool")
    parser.add_argument(
        "-t",
        "--target",
        required=True,
        help="Target website domain (https and http supported)",
    )
    args = parser.parse_args()
    os.system("cls" if os.name == "nt" else "clear")

    text = """
============================================================================
  ____    _____    ____    ___    _   _     _____    ___     ___    _     
 |  _ \  | ____|  / ___|  / _ \  | \ | |   |_   _|  / _ \   / _ \  | |    
 | |_) | |  _|   | |     | | | | |  \| |     | |   | | | | | | | | | |    
 |  _ <  | |___  | |___  | |_| | | |\  |     | |   | |_| | | |_| | | |___ 
 |_| \_\ |_____|  \____|  \___/  |_| \_|     |_|    \___/   \___/  |_____|

============================================================================
"""
    print(f"\033[91m{text}\033[0m")
    asyncio.run(main(args.target))
