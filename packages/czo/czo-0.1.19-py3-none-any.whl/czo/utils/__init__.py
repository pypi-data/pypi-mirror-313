import inspect
import unicodedata

from .__meta import Singleton


def count_chr_length(text, no_ascii=2) -> int:
    """
    将 ASCII 字符计算为 1 个单位长度。

    将大部分非 ASCII 字符（如汉字、日文、韩文等）计算为 2 个单位长度。
    """
    length = 0
    for c in text:
        if unicodedata.east_asian_width(c) in ["F", "W"]:
            length += no_ascii  # 全角宽度字符
        else:
            length += 1  # 半角宽度字符
    return length


def _get_methods_and_properties_with_docs(cls):
    """通过这个函数，可以方便地获取类的所有公共方法和属性，并以一种格式化的方式输出它们的名称和文档注释。"""
    methods_and_properties: dict[str, str] = {}

    # 获取类的文档注释
    class_doc: str | None = inspect.getdoc(cls)
    if class_doc is not None:
        methods_and_properties["__class__"] = f"C: {class_doc}".split("\n")[0]

    # 获取类的所有成员（包括方法和属性）
    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):  # 过滤掉私有方法
            continue
        elif inspect.isfunction(member):
            prefix = "F: "
        elif isinstance(member, property):
            prefix = "P: "
        elif inspect.ismethod(member):
            prefix = "M: "

        # 提取文档注释的第一行，并为功能加上标签
        methods_and_properties[name] = (
            f"{prefix}{inspect.getdoc(member)}".split("\n")[0]
            if name != "help"
            else f"{prefix}可以方便地获取{cls.__name__}类的所有公共方法和属性，并以一种格式化的方式输出它们的名称和文档注释。"
        )

    max_doc_length: int = 0
    max_method_length: int = 0

    # 计算方法名和文档注释的最大长度
    for method, doc in methods_and_properties.items():
        if len(method) > max_method_length:
            max_method_length = len(method)

        if (length := count_chr_length(doc)) > max_doc_length:
            max_doc_length = length

    # 总长度为方法名最长的长度加上文档注释最长的长度再加上3个单位长度的间隔
    max_length: int = max_doc_length + max_method_length + 3

    print(f" {'-' * max_length}")

    tag: str = f"【{cls.__name__}】 F|P|M 分别表示 函数|属性|方法 。C 是类的文档注释。"
    tag_length: int = count_chr_length(tag)
    print(f"| {tag}{' ' * (max_length-tag_length-2)} |")
    print(f"|{'-'*(max_length)}|")

    # 打印方法和属性及其文档注释
    help_print = None
    for method, doc in methods_and_properties.items():
        info = f"| {method:<{max_method_length}} {doc}"
        while count_chr_length(info) < max_length:
            info += " "
        # 始终在最后输出帮助方法
        if method == "help":
            help_print = info + " |"
            continue
        print(info + " |")
    print(help_print)
    print(f" {'-'*max_length}")


def add_help(cls):
    """通过这个装饰器，可以方便地为类添加一个help 方法，该方法可以方便地获取类的所有公共方法和属性，并以一种格式化的方式输出它们的名称和文档注释。"""
    cls.help = lambda: _get_methods_and_properties_with_docs(cls)
    return cls
