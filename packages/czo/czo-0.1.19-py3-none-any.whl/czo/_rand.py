import hashlib
import ipaddress
import random
import secrets
import shutil
import string
import uuid
import warnings
from typing import Literal

from .utils import add_help

# 设置警告过滤器
warnings.filterwarnings("always")


@add_help
class Random:
    """
    随机生成一些测试数据
    """

    def help() -> None: ...

    @staticmethod
    def file(data: str | None = None) -> tuple:
        """
        生成随机文件并返回文件路径和文件的 MD5 哈希值。

        该函数用于生成一个随机文件，并返回该文件的路径和MD5哈希值。
        可以通过传入参数指定文件内容，默认为None。函数首先生成一个随机字符串作为
        临时文件的名称。然后，根据传入的内容将文件写入临时文件中。
        最后，使用hashlib库计算临时文件的MD5哈希值，并将临时文件移动到指定路径上。
        函数返回一个包含文件路径和MD5哈希值的元组。

        Args:
            data (str | None, optional): 文件内容，默认为 None。

        Returns:
            tuple: 包含文件路径和文件的 MD5 哈希值的元组。

        Example:
            ```python
            result = random_file(data='Hello, World!')
            print(result)  # 输出: ("./file", "a1b2c3d4e5f6...")
            ```
        """

        rand_str: list[str] = random.sample(string.ascii_letters + string.digits, 20)
        random_value: str = "".join(rand_str) + "\n" + str(uuid.uuid4())

        temp_name = f".{Random.random_hash()}"
        with open(temp_name, "w") as w:
            if data is not None:
                w.write(f"{data}\n{random_value}")
            else:
                w.write(f"{random_value}")
        with open(temp_name, "rb") as r:
            md5: str = hashlib.md5(r.read()).hexdigest()
        temp_path: str = f"./{md5}"
        shutil.move(temp_name, temp_path)
        return temp_path, md5

    @staticmethod
    def str(
        length: int = 1, is_zh: bool = False, mark: bool = False, is_int: bool = False
    ) -> str:
        """
        生成指定长度的随机大小写字母、数字组成的字符串。

        Args:
            length (int): 字符串长度。越短重复的概率越高。
            is_zh (bool, optional): 是否包含中文字符，默认为 False。
            mark (bool, optional): 默认生成的字符串是否包含标点符号，默认为 False。
            is_int (bool, optional): 是否生成随机整数字符串，默认为 False。

        Returns:
            str: 生成的随机字符串。

        Examples:
        >>> print(Random.str(1))

        """

        def Unicode() -> str:
            result: Literal[""] = ""
            for _ in range(length):
                char = chr(random.randint(0x4E00, 0x9FA5))
                result += char
            return result

        if is_zh:
            return Unicode()

        if is_int:
            return "".join(str(secrets.randbelow(10)) for _ in range(length))

        # 选择字符集
        characters = string.ascii_letters + string.digits

        if mark:
            characters += string.punctuation

        sys_random = random.SystemRandom()
        return "".join(
            sys_random.choice(string.ascii_letters + string.digits)
            for _ in range(length)
        )

    @staticmethod
    def hash(len: int | None = None) -> str:
        """
        生成一个随机的MD5哈希字符串。

        Args:
        - len: int | None - 生成的哈希字符串的长度。如果为None，则返回完整的MD5哈希字符串（32个字符）。

        Returns:
        - str: 生成的MD5哈希字符串。根据`len`参数可能被截断。
        """

        letters = string.printable
        rand = "".join(random.sample(letters, 10))
        hash = hashlib.md5(rand.encode()).hexdigest()
        return hash[:len]

    @staticmethod
    def hash_uuid4(len: int | None = None) -> str:
        """
        生成一个基于UUID4的随机哈希字符串。

        Args:
        - len: 需要返回的哈希字符串的长度。如果为None，则返回整个哈希字符串。

        Returns:
        - str: 根据指定长度生成的哈希字符串。
        """

        u4 = uuid.uuid4()
        hash = hashlib.md5(u4.bytes).hexdigest()
        return hash[:len]

    @staticmethod
    def ip(is_ipv6: bool = False) -> str:
        """
        生成一个随机的IP地址。
        """
        if is_ipv6:
            return ipaddress.IPv6Address(random.randint(0, 2**128 - 1)).compressed
        else:
            return ipaddress.IPv4Address(random.randint(0, 2**32 - 1)).compressed

    @staticmethod
    def ip_suffix_is_0(is_ipv6: bool = False, suffix: str = 0) -> str:
        """
        生成一个随机后缀为`0`|`suffix`的IP地址。
        """
        if is_ipv6:
            return (
                ":".join([f"{random.randint(0, 65535):x}" for _ in range(4)])
                + f"::{suffix}"
            )
        else:
            return (
                ".".join([f"{random.randint(0, 255)}" for _ in range(3)]) + f".{suffix}"
            )

    @staticmethod
    def ip_range(is_ipv6: bool = False):
        """
        生成一个IP地址范围，可以是IPv4或IPv6地址格式。

        Args:
        - is_ipv6: bool 值，用于指定生成IPv4还是IPv6地址范围。默认为False，表示生成IPv4地址范围。

        Returns:
        - 返回一个字符串，表示IP地址范围。如果is_ipv6为True，则返回IPv6地址范围，否则返回IPv4地址范围。
        """
        if is_ipv6:
            ip = ":".join([f"{random.randint(0, 65535):x}" for _ in range(4)])
            return f"{ip}::{random.randint(1, 10000):x}-{ip}::{random.randint(20000, 65500):x}"
        else:
            ip = ".".join([f"{random.randint(0, 255)}" for _ in range(3)])
            return f"{ip}.{random.randint(1, 100)}-{ip}.{random.randint(110, 254)}"

    @staticmethod
    def ip_netmask(is_ipv6: bool = False, netmask: int | None = None):
        """
        生成一个随机的IP子网掩码格式。
        """
        if is_ipv6:
            netmask = netmask if netmask is not None else random.randint(64, 128)
            return f"{Random.ip_suffix_is_0(True)}/{netmask}"
        else:
            netmask = netmask if netmask is not None else random.randint(8, 32)
            return f"{Random.ip_suffix_is_0()}/{netmask}"

    @staticmethod
    @property
    def mac():
        """
        生成一个随机的MAC。
        """
        mac_address = ":".join(
            [
                "{:02x}".format((uuid.getnode() >> elements) & 0xFF)
                for elements in range(0, 2 * 6, 2)
            ]
        )
        return mac_address
