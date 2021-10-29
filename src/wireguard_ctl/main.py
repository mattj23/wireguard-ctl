# from pyroute2 import NDB
# from pyroute2 import IPRoute
from typing import Optional, Any

from pr2modules.iproute.linux import IPRoute
from pprint import pprint
from dataclasses import dataclass


def _list_tuple_get(key_name, attrs) -> Optional[Any]:
    for key, value in attrs:
        if key == key_name:
            return value
    return None


@dataclass
class IpLink:
    name: str
    state: str
    index: int
    special_kind: str

    @staticmethod
    def parse(link_data):
        name = link_data.get_attr('IFLA_IFNAME')
        state = link_data.get_attr("IFLA_OPERSTATE")

        info_kind = ""
        link_info_attr = link_data.get_attr("IFLA_LINKINFO")
        if link_info_attr is not None:
            info_kind = link_info_attr.get_attr("IFLA_INFO_KIND")

        if not info_kind:
            if link_data['ifi_type'] == 1:
                info_kind = "ethernet"

        return IpLink(name, state, link_data['index'], info_kind)


@dataclass
class IpAddr:
    address: str
    prefix_len: int
    if_index: int

    @staticmethod
    def parse(addr_info):
        addr = addr_info.get_attrs("IFA_ADDRESS")
        if addr is not None:
            addr = addr[0]
        return IpAddr(addr, addr_info['prefixlen'], addr_info['index'])


def main():
    ip = IPRoute()
    links = []
    addresses = []
    for link_info in ip.get_links():
        link = IpLink.parse(link_info)
        links.append(link)
        results = [IpAddr.parse(i) for i in ip.get_addr(index=link.index)]
        addresses += results

    for route_info in ip.get_routes():
        pprint(route_info)
        print("\n\n============================\n\n")


if __name__ == '__main__':
    main()
