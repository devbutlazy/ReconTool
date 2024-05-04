from typing import Dict, List, Literal
import aiofiles


def read_file(txt_file: str) -> List[str]:
    """
    Reads a text file line by line, strips each line of whitespace,
    and returns a list of the processed lines.

    Parameters:
    txt_file (str): The path to the text file to be read.

    Returns:
    List[str]: A list containing the stripped lines from the file.

    Raises:
    FileNotFoundError: If the text file does not exist.
    IOError: If an error occurs during file reading.
    """
    subdomains = []
    try:
        with open(txt_file, "r") as file:
            subdomains = [line.strip() for line in file]
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {txt_file} was not found.")
    except IOError as e:
        raise IOError(f"An error occurred while reading {txt_file}: {e}")

    return subdomains


def custom_print(
    text: str,
    suffix: Literal[
        "success", "error", "port", "denied", "auth", "additional"
    ] = "success",
) -> None:
    """
    Prints colored text to the console to visually distinguish the type of message.

    Parameters:
    - text (str): The text to be printed.
    - suffix (Literal["success", "error", "port", "denied", "auth", "additional"],
      optional): The category of the message which dictates the color of the prefix.
      Defaults to "success".

    Supported suffixes and their meanings:
    - "success": Indicates a successful operation.
    - "error": Indicates an error has occurred.
    - "denied": Indicates access denial or permission issues.
    - "auth": Indicates authentication failures.
    - "port": Pertains to network ports.
    - "additional": Indicates additional information.

    Returns:
    - None
    """
    suffixes = {
        "success": "\033[1;32mSUCCESS\033[0m",
        "error": "\033[1;31mERROR\033[0m",
        "denied": "\033[1;33mDENIED\033[0m",
        "auth": "\033[1;31mNOAUTH\033[0m",
        "port": "\033[1;34mPORT\033[0m",
        "additional": "\033[1;34m*\033[0m",
    }

    # Ensure the reset code is used to avoid coloring the entire text.
    reset_code = "\033[0m"
    colored_suffix = f"{suffixes[suffix]}{reset_code}"
    print(f"[{colored_suffix}] {text}")


async def write_to_file(
    positive_results: Dict[str, dict], edited_domain: str, file_name: str
) -> None:
    """
    Asynchronously writes the details of positive results to a specified file.

    This function creates a .txt file named according to the 'file_name' parameter and
    writes the details of each subdomain's positive results, including its IP address
    and a list of port-service pairs.

    Parameters:
    - positive_results (Dict[str, dict]): A mapping from subdomains to their respective
      positive findings.
    - edited_domain (str): The domain name that has been modified.
    - file_name (str): The base name of the file to which the results will be written.

    Returns:
    - None

    Raises:
    - Exception: If an I/O or any other error occurs while attempting to write to the file.
    """
    try:
        # Open the file in write mode with UTF-8 encoding, ignoring encoding errors.
        async with aiofiles.open(
            f"{file_name}.txt", mode="w", encoding="utf-8", errors="ignore"
        ) as file:
            # Iterate through the positive results dictionary.
            for subdomain, data in positive_results.items():
                ip = data.get("ip", "")
                port_service_list = data.get("port_service_list", [])

                # Write the subdomain, edited domain, and IP address to the file.
                await file.write(f"https://{subdomain}.{edited_domain} | IP: {ip}\n")
                await file.write("{\n")

                # Write each port-service pair.
                for port_service in port_service_list:
                    port, service = port_service.split(", ")
                    await file.write(f"    {port} | {service}\n")

                await file.write("}\n")

    except (Exception, BaseException) as error:
        # Use a more professional logging method to record exceptions.
        custom_print(f"An error occurred while writing to the file: {error}", "error")
