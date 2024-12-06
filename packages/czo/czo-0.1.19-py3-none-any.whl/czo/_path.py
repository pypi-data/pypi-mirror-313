import os
import shutil
import sys
from pathlib import Path

from .utils import add_help


@add_help
class PathLib:
    """
    处理文件相关的功能
    """

    def help() -> None: ...

    @staticmethod
    def clear_directory(path):
        """
        清空指定目录下的所有文件和子目录。

        Args:
            path:要清空的目录
        """
        if not os.path.exists(path):
            sys.exit("要清空的目录不存在")

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    @staticmethod
    def del_key_directory(path: str, keywords: str | list[str], confirm: bool = False):
        """
        清理指定目录中包含特定关键词的子目录。

        Args:
            path: str - 要清理的目录路径。
            keywords: str | list[str] - 要查找和处理的关键词或关键词列表。
            confirm: bool - 删除是不可逆的，默认仅打印找到的子目录路径。如果为True，则删除找到的子目录。

        Raises:
            KeyError - 如果关键词列表为空，则抛出此异常。

        Examples:
            >>> del_key_directory('C:/Users/user/Documents', 'example')
            >>> del_key_directory('C:/Users/user/Documents', ['example', 'test'])
            >>> del_key_directory('C:/Users/user/Documents', ['example', 'test'], confirm=True)
        """

        keys = []

        if len(keywords) < 1:
            raise KeyError(f"要查找的目录名称不能是空！")

        if isinstance(keywords, str):
            keys.append(keywords)

        if isinstance(keywords, list):
            keys.extend(keywords)

        for dirname, subdir, filenames in os.walk(path):
            for dir_name in subdir:
                if dir_name in keys:
                    dir_path = os.path.join(dirname, dir_name)
                    if confirm:
                        shutil.rmtree(dir_path)
                    else:
                        print(dir_path)

    @staticmethod
    def del_key_file(path: str, keywords: str, confirm: bool = False) -> None:
        """
        清理指定目录下包含特定关键字的文件。

        Args:
            path: 字符串，指定要搜索的目录路径。
            keywords: 字符串，指定要查找的关键字。
            confirm: 布尔值，默认为False。如果设置为True，则实际删除找到的文件；
                    如果为False，则只打印将要删除的文件名。

        Examples:
            >>> del_key_file('C:/Users/user/Documents', 'example')
            >>> del_key_file('C:/Users/user/Documents', 'example', confirm=True)
        """
        file_list = [
            os.path.join(dirname, filename)
            for dirname, subdir, filenames in os.walk(path)
            for filename in filenames
        ]

        for target_file in file_list:
            if keywords in target_file:
                if confirm:
                    os.remove(target_file)
                else:
                    print(f"删除文件：{target_file}")

    @staticmethod
    def rename_files(path: str, old_string, new_string, confirm=False):
        """
        替换文件名中的指定字符串。

        该函数遍历指定路径下的所有文件，如果文件名包含旧字符串，

        则将其替换为新字符串，并执行重命名操作。如果confirm参数为False，

        则不会真的重命名文件，只会打印出将要执行的操作。

        Args:
            path: str - 文件夹路径，从中搜索文件进行重命名。
            old_string: str - 需要被替换的旧字符串。
            new_string: str - 用于替换旧字符串的新字符串。
            confirm: bool - 是否真的执行重命名操作，默认为False，只打印将要执行的操作。

        Examples:
            >>> rename_files('C:/Users/user/Documents', 'example', 'test')
            >>> rename_files('C:/Users/user/Documents', 'example', 'test', confirm=True)
        """

        for dirname, subdir, filenames in os.walk(path):
            for filename in filenames:
                if old_string in filename:
                    old_file_path = os.path.join(dirname, filename)
                    new_file_name = filename.replace(old_string, new_string)
                    new_file_path = os.path.join(dirname, new_file_name)

                    if confirm:
                        os.rename(old_file_path, new_file_path)
                    else:
                        s_len = len(old_file_path.encode("gbk"))
                        print("*" * s_len)
                        print(f"{old_file_path}\n{new_file_path}")
                        print("*" * s_len)

    @staticmethod
    def del_key_row(file: str, key: str) -> None:
        """
        删除文件中和 key 相等的行

        Args:
            file : str
            key : str
        """
        with open(file, "r", encoding="utf8") as f:
            lines: list[str] = f.readlines()
        with open(file, "w", encoding="utf8") as f:
            for line in lines:
                if line.strip("\n") != key:
                    f.write(line)

    @staticmethod
    def get_dir_file_list(path: str) -> list:
        """
        获取path下所有文件的路径，包括子目录。
        """
        return [
            os.path.join(root, fn)
            for root, dirs, files in os.walk(path)
            for fn in files
        ]

    @staticmethod
    def mkdir(path) -> Path:
        """
        如果目录不存在就创建,支持多级目录

        Args:
            path:目录
        """

        p = Path(path)
        if not p.exists():
            p.mkdir(parents=True)
        return p

    @staticmethod
    def get_project_path(project_name: str) -> str:
        """
        根据项目名称获取项目根目录绝对路径
        """
        curPath: str = os.path.abspath(os.path.dirname(__file__))
        return curPath[: curPath.find(project_name) + len(project_name)]

    @staticmethod
    def is_none_then_mkdir(path: str | Path) -> Path:
        """如果指定的路径不存在，则创建该路径及其所有父路径。

        参数:
        - path: 字符串或Path类型，表示需要检查和可能创建的路径。

        返回值:
        - Path类型，表示处理后的路径对象。
        """

        if not isinstance(path, Path):
            path = Path(path)  # 将字符串类型的路径转换为Path对象

        if not path.exists():
            path.mkdir(parents=True)  # 如果路径不存在，则创建该路径及其所有父路径
        return path

    @staticmethod
    def move_videos_to_root(
        root_path, use_parent_dir_as_prefix=False, remove_empty_dirs=True
    ):
        """把源目录的子目录中的视频文件移动到源目录下

        参数:

        - use_parent_dir_as_prefix：设置为 True 时使用上一级目录名作为文件名前缀；设置为 False 时保持原文件名。

        - remove_empty_dirs：设置为 True 时，移动完文件后删除原目录（前提是目录为空）；设置为 False 时不删除目录。
        """

        # 定义视频文件格式
        video_extensions = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm"}
        moved_files_count = 0  # 初始化移动文件计数器

        # 遍历指定目录及其子目录
        for dirpath, _, filenames in os.walk(root_path, topdown=False):
            for filename in filenames:
                # 检查文件扩展名是否在视频格式列表中
                if any(filename.lower().endswith(ext) for ext in video_extensions):
                    source_path = os.path.join(dirpath, filename)

                    # 如果文件已经在根目录中，则跳过
                    if dirpath == root_path:
                        continue

                    # 使用上一级目录名作为文件名前缀（根据可选参数）
                    if use_parent_dir_as_prefix:
                        parent_dir_name = os.path.basename(os.path.dirname(source_path))
                        new_filename = f"{parent_dir_name}_{filename}"
                    else:
                        new_filename = filename

                    destination_path = os.path.join(root_path, new_filename)

                    # 若文件名冲突，则自动重命名
                    if os.path.exists(destination_path):
                        base, ext = os.path.splitext(new_filename)
                        count = 1
                        while os.path.exists(destination_path):
                            destination_path = os.path.join(
                                root_path, f"{base}_{count}{ext}"
                            )
                            count += 1

                    # 移动文件到目标目录
                    shutil.move(source_path, destination_path)
                    moved_files_count += 1  # 计数移动的文件
                    print(f"Moved: {source_path} -> {destination_path}")

            # 删除空目录（根据可选参数）
            if remove_empty_dirs and dirpath != root_path and not os.listdir(dirpath):
                os.rmdir(dirpath)
                print(f"Removed empty directory: {dirpath}")

        print(f"Total files moved: {moved_files_count}")


@add_help
class DirLib:
    """处理目录相关功能"""

    def __init__(self, directory_path: str | Path):
        # 创建 Path 对象
        self.directory: Path = Path(directory_path)

        # 使用 exists() 方法检查目录是否存在,不存在时新建
        if not self.directory.exists():
            self.directory.mkdir(parents=True)

    def help(): ...

    @property
    def is_directory_empty(self) -> bool:
        """
        检查目录是否为空。

        无需参数，方法内部会使用实例属性 `directory` 来代表需要检查的目录。
        目录下有空目录时也会判断为非空

        返回值:
            bool: 如果目录为空，则返回 True；否则返回 False。
        """

        # 使用 `any()` 函数和目录迭代器判断目录中是否至少有一个文件或子目录
        return not any(self.directory.iterdir())

    def rename_non_empty_directory(self, new_path: str | Path = None):
        """
        重命名非空目录。

        如果指定的目录不为空，则为其生成一个新的名称，如果指定新的路径，则将目录移动到该路径下，并在原路径上重命名。
        如果新的路径不存在，则会创建该路径。

        参数:
        - new_path: str | Path 类型，指定目录重命名后的新路径。如果为 None，则只重命名不移动目录。

        返回值:
        - Path 类型，表示重命名后的目录路径。如果目录为空，则返回 False。
        """
        # 检查目录是否为空，不为空则进行重命名
        if not self.is_directory_empty:

            serial_number: int = 1  # 初始化序列号，用于生成新的目录名称
            while True:
                # 生成新的目录名称，如果存在则递增序列号
                new_directory_name = f"{self.directory.stem}-{serial_number}"

                if new_path is None:
                    # 如果未指定新路径，则在原路径下重命名
                    new_directory_path = self.directory.parent / new_directory_name
                else:
                    # 如果指定了新路径，则在新路径下重命名
                    new_path = Path(new_path)
                    PathLib.is_none_then_mkdir(new_path)  # 确保新路径存在
                    new_directory_path: Path = new_path / new_directory_name

                if new_directory_path.exists():
                    serial_number += 1  # 如果新名称已存在，则递增序列号并重试
                    continue
                else:
                    break  # 找到可用的新名称，退出循环

            # 执行目录重命名操作
            self.directory.rename(new_directory_path)

            return new_directory_path
        else:
            # 目录为空，不进行重命名
            return False

    @staticmethod
    def delete_glob_file(dir_path: Path | str, file_name: str):
        """
        删除指定目录下匹配的文件

        Example:
            delete_glob_file(Path("./"), "*.json")
        """
        try:
            for file in dir_path.glob("qemu_info_*.json"):
                file.unlink()
        except Exception as e:
            return e

        return True
