import ipaddress
import json
from abc import ABC, abstractmethod
from typing import List, Literal

import psutil
from ambient_backend_api_client.models import InterfaceTypeEnum, NetworkInterface
from result import Ok

from ambient_client_common.utils import logger


class InterfaceService(ABC):
    @abstractmethod
    async def get_network_interfaces(self) -> List[NetworkInterface]:
        """Get network interfaces on the device."""


class LinuxInterfaceService(InterfaceService):
    def __init__(self) -> None:
        self._running = False
        self._error = Ok("initialized")

    def determine_if_ipv4_or_ipv6(
        self, address: str
    ) -> Literal["ipv4", "ipv6", "unknown"]:
        try:
            ip_obj = ipaddress.ip_address(address)
        except ValueError as e:
            logger.error("Error parsing IP address: {}", e)
            return "unknown"
        if ip_obj.version == 4:
            return "ipv4"
        elif ip_obj.version == 6:
            return "ipv6"

    async def get_network_interfaces(self) -> List[NetworkInterface]:
        logger.info("Starting to fetch network interface details.")
        interfaces = psutil.net_if_addrs()
        logger.debug("Interfaces: {}", json.dumps(interfaces, indent=4))
        network_interfaces: List[NetworkInterface] = []

        for interface_name, addresses in interfaces.items():
            logger.debug("Processing {} interface ...", interface_name)
            logger.debug("Addresses: {}", addresses)

            for addr in addresses:
                existing_interface = next(
                    (
                        interface_
                        for interface_ in network_interfaces
                        if interface_.name == interface_name
                    ),
                    None,
                )
                if existing_interface:
                    logger.debug(
                        "Interface {} already exists in network interfaces.",
                        interface_name,
                    )
                    existing_addr = (
                        existing_interface.ipv4_address
                        or existing_interface.ipv6_address
                    )
                    if self.determine_if_ipv4_or_ipv6(existing_addr) == "ipv4":
                        if self.determine_if_ipv4_or_ipv6(addr.address) == "ipv6":
                            existing_interface.ipv6_address = (
                                addr.address.split("%")[0]
                                if "%" in addr.address
                                else addr.address
                            )
                    elif self.determine_if_ipv4_or_ipv6(existing_addr) == "ipv6":
                        if self.determine_if_ipv4_or_ipv6(addr.address) == "ipv4":
                            existing_interface.ipv4_address = addr.address
                    continue
                details = {
                    "name": f"{interface_name}",
                    # Default to OTHER, adjust logic as needed
                    "type": InterfaceTypeEnum.UNKNOWN,
                }
                logger.debug("Address: {}", addr)
                ip_version = self.determine_if_ipv4_or_ipv6(addr.address)
                if ip_version == "ipv4":
                    details["ipv4_address"] = addr.address
                    details["netmask"] = addr.netmask
                elif ip_version == "ipv6":
                    details["ipv6_address"] = addr.address
                else:
                    logger.error("Unknown IP version for address: {}", addr.address)
                    continue
                details["broadcast"] = addr.broadcast

                # Interface type heuristic
                wifi_heuristics = ["wi-fi", "wifi", "wlan"]
                ethernet_heuristics = [
                    "eth",
                    "enp",
                    "ens",
                    "eno",
                    "enx",
                    "docker",
                    "lo",
                    "br",
                ]

                if any(
                    heuristic in interface_name.lower() for heuristic in wifi_heuristics
                ):
                    details["type"] = InterfaceTypeEnum.WIFI
                elif any(
                    heuristic in interface_name.lower()
                    for heuristic in ethernet_heuristics
                ):
                    details["type"] = InterfaceTypeEnum.ETHERNET

                network_interface = NetworkInterface(**details)
                logger.debug(
                    "Network Interface: {}", network_interface.model_dump_json(indent=4)
                )
                network_interfaces.append(network_interface)
            logger.info(f"Added {interface_name} to network interfaces.")

        logger.info("Completed fetching all network interfaces.")
        return network_interfaces
