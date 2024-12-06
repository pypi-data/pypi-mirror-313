import ipaddress
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Generator, Union

from .utils import add_help


@add_help
class NetLib:

    def help() -> None: ...

    @staticmethod
    def cidr(address: str, netmask_or_prefix: int | str) -> dict[str, Any] | ValueError:
        """
        根据指定的网络和前缀长度计算CIDR信息。

        Args:
        - network: 字符串，指定的网络地址，可以是IPv4或IPv6格式。
        - prefix: 整数，网络的前缀长度。

        Returns:
        - 字典，包含CIDR信息，包括主机数量、地址范围、网络地址、广播地址和子网掩码。
        - 如果参数无效，返回ValueError异常。

        Examples:
        >>> print(Net.cidr('192.168.1.0', 24))

        >>> print(Net.cidr('240e::0', 64))
        """

        try:
            ip_type: ipaddress.IPv6Network | ipaddress.IPv4Network = (
                ipaddress.IPv6Network if ":" in address else ipaddress.IPv4Network
            )
            cidr = ip_type(f"{address}/{netmask_or_prefix}")

            # 输出网络地址、子网掩码、广播地址等信息
            host_count = cidr.num_addresses - 2
            range = (
                str(cidr.network_address + 1) + "-" + str(cidr.broadcast_address - 1)
            )
            network_address = str(cidr.network_address)
            broadcast_address = str(cidr.broadcast_address)
            netmask = str(cidr.netmask)
            prefixlen = cidr.prefixlen

            return {
                "host_count": host_count,
                "range": range,
                "network_address": network_address,
                "broadcast_address": broadcast_address,
                "prefixlen": prefixlen,
                "netmask": netmask,
            }

        except ValueError as e:
            return e

    @staticmethod
    def ipaddress_generator(
        number: int, max: int | None = None, is_ipv6: bool = False, **kwargs
    ) -> Generator[list[str], Any, None]:
        """
        生成指定数量的IP地址序列。

        Args:
        - number: 每次生成的IP地址数量。
        - max: 生成IP地址的最大数量, 为空时使用 number。
        - is_ipv6: 是否生成IPv6地址，默认生成IPv4地址。
        - **kwargs: 可选参数，用于指定IP地址的a、b、c、d、e、f、g、h初始值。

        Returns:
        - Generator: 生成器，每次返回number个IP地址组成的列表，直到生成max个IP地址为止。

        Examples:
        >>> for i in NetLib.ipaddress_generator(10, max=100):
        ...    print(";".join(map(lambda x: f"http://{x}", i)))

        >>> ip_list = [ip for sublist in NetLib.ipaddress_generator(10, a=100) for ip in sublist]

        """
        a: int = kwargs.get("a", 1)
        b: int = kwargs.get("b", 1)
        c: int = kwargs.get("c", 1)
        d: int = kwargs.get("d", 1)
        e: int = kwargs.get("e", 1)
        f: int = kwargs.get("f", 1)
        g: int = kwargs.get("g", 1)
        h: int = kwargs.get("h", 1)

        if max is None:
            max = number

        if is_ipv6 is False:
            a_range: int = 256
            b_range: int = 256
            c_range: int = 256
            d_range: int = 255
            ip_list: list = []
            count: int = 0
            for _ in range(1, max + 1):
                ip_list.append(ipaddress.IPv4Address(f"{a}.{b}.{c}.{d}").compressed)
                count += 1
                d += 1

                if d == d_range:
                    d = 1
                    c = c + 1
                    if c == c_range:
                        c = 1
                        b = b + 1
                        if b == b_range:
                            b = 1
                            a = a + 1
                            if a == a_range:
                                a = 1

                if len(ip_list) % number == 0:
                    yield ip_list
                    ip_list = []
                if max == count and len(ip_list) != 0:
                    yield ip_list
        else:
            a_range: int = 65536
            b_range: int = 65536
            c_range: int = 65536
            d_range: int = 65536
            e_range: int = 65536
            f_range: int = 65536
            g_range: int = 65536
            h_range: int = 65536
            ip_list: list = []
            count: int = 0
            for _ in range(1, max + 1):
                ip_list.append(
                    ipaddress.IPv6Address(
                        f"{a:04x}:{b:04x}:{c:04x}:{d:04x}:{e:04x}:{f:04x}:{g:04x}:{h:04x}"
                    ).compressed
                )
                count += 1
                h += 1

                if h == h_range:
                    h = 1
                    g = g + 1
                    if g == g_range:
                        g = 1
                        f = f + 1
                        if f == f_range:
                            f = 1
                            e = e + 1
                            if e == e_range:
                                e = 1
                                d = d + 1
                                if d == d_range:
                                    d = 1
                                    c = c + 1
                                    if c == c_range:
                                        c = 1
                                        b = b + 1
                                        if b == b_range:
                                            b = 1
                                            a = a + 1
                                            if a == a_range:
                                                a = 1

                if len(ip_list) % number == 0:
                    yield ip_list
                    ip_list = []
                if max == count and len(ip_list) != 0:
                    yield ip_list

    @staticmethod
    def generate_ip_list(
        number: int,
        *,
        is_ipv6: bool = False,
        ip_str: str | None = None,
        v6_exploded: bool = False,
    ) -> list[str]:
        """
        生成指定数量的IP地址字符串列表。

        参数:
        - number: 生成IP地址的数量。
        - is_ipv6: 指示是否生成IPv6地址。
        - ip_str: 指定IP地址字符串，如果提供了该参数，则使用该字符串作为起始IP地址。
        - v6_exploded: 指示生成的IPv6地址是否以展开格式表示。

        返回值:
        - 一个包含生成的IP地址字符串的列表。

        示例:
        >>> print(NetLib.generate_ip_list(3, ip_str="192.168.1.1"))

        >>> print(NetLib.generate_ip_list(3, is_ipv6=True, ip_str="2001:db8::1"))

        """
        if is_ipv6:
            if ip_str is None:
                ipv6 = int(ipaddress.ip_address("2001:db8:0:42:0:8a2e:370:1"))
            else:
                ipv6 = int(ipaddress.ip_address(ip_str))

            if v6_exploded:
                return [ipaddress.IPv6Address(ipv6 + i).exploded for i in range(number)]
            return [ipaddress.IPv6Address(ipv6 + i).compressed for i in range(number)]

        if ip_str is None:
            ipv4 = int(ipaddress.ip_address("1.0.0.1"))
        else:
            ipv4 = int(ipaddress.ip_address(ip_str))
        return [ipaddress.IPv4Address(ipv4 + i).compressed for i in range(number)]

    @staticmethod
    def is_ip_in_range(
        ip_str: str,
        subnet_str: Union[str, None] = None,
        *,
        src_ip: str | None = None,
        dst_ip: str | None = None,
    ) -> bool:
        """检查 IP 地址是否在指定的子网或 IP 范围内。

        参数:
        - ip_str: 要检查的 IP 地址。
        - subnet_str: 可选的子网（CIDR 形式或 IP 范围，格式为 'start_ip-end_ip'）。
        - src_ip: 可选的起始 IP 地址，当没有提供 `subnet_str` 时使用。
        - dst_ip: 可选的结束 IP 地址，当没有提供 `subnet_str` 时使用。

        返回值:
        - 如果 IP 地址在指定范围内，则返回 True;否则返回 False。

        示例:
        - is_ip_in_range("192.168.1.10", "192.168.1.0/24")
        - is_ip_in_range("192.168.1.10", "192.168.1.1-192.168.1.20")
        - is_ip_in_range("192.168.1.10", src_ip="192.168.1.1", dst_ip="192.168.1.20")

        - is_ip_in_range("2a00::110:1", "2a00::110:0/116")
        - is_ip_in_range("2a00::110:1", "2a00::110:1-2a00::110:fff")
        """
        ip: IPv4Address | IPv6Address = ipaddress.ip_address(ip_str)

        if subnet_str:
            if "/" in subnet_str:
                ip_network = ipaddress.ip_network(subnet_str, strict=False)
                return ip in ip_network
            elif "-" in subnet_str:
                start_ip_str, end_ip_str = map(str.strip, subnet_str.split("-"))
                start_ip, end_ip = ipaddress.ip_address(
                    start_ip_str
                ), ipaddress.ip_address(end_ip_str)
                return start_ip <= ip <= end_ip

        if src_ip and dst_ip:
            start_ip, end_ip = ipaddress.ip_address(src_ip), ipaddress.ip_address(
                dst_ip
            )
            return start_ip <= ip <= end_ip

        return False

    @staticmethod
    def mac_generator(
        number: int, max: int = 10, **kwargs
    ) -> Generator[list, Any, None]:
        """
        生成MAC地址
        """
        a: int = kwargs.get("a", 255)
        b: int = kwargs.get("b", 255)
        c: int = kwargs.get("c", 255)
        d: int = kwargs.get("d", 1)
        e: int = kwargs.get("e", 1)
        f: int = kwargs.get("f", 1)
        a_range: int = 256
        b_range: int = 256
        c_range: int = 256
        d_range: int = 256
        e_range: int = 256
        f_range: int = 256
        count = 0
        mac_list = []
        for _ in range(1, max + 1):
            mac_list.append(f"{a:02x}:{b:02x}:{c:02x}:{d:02x}:{e:02x}:{f:02x}")
            count += 1
            f += 1
            if f == f_range:
                f = 1
                e = e + 1
                if e == e_range:
                    e = 1
                    d = d + 1
                    if d == d_range:
                        d = 1
                        c = c + 1
                        if c == c_range:
                            c = 1
                            b = b + 1
                            if b == b_range:
                                b = 1
                                a = a + 1
                                if a == a_range:
                                    a = 1
            if len(mac_list) % number == 0:
                yield mac_list
                mac_list = []
            if max == count and len(mac_list) != 0:
                yield mac_list

    @staticmethod
    def cidr_to_subnet(cidr):
        """从子网掩码位数获取IPv4地址

        Example:
        >>> NetLib.cidr_to_subnet(24)
        '255.255.255.0'
        """
        return str(ipaddress.IPv4Network(f"0.0.0.0/{cidr}").netmask)
