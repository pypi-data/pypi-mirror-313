from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


class MetaSpyder(ABC):
    # 类级别的字典存储HTTP请求头信息
    headers: Dict[str, str] = {}

    def __init__(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        """
        初始化MetaSpyder实例，接受任意数量的位置参数和关键字参数。

        参数:
            *args (Tuple[Any, ...]): 非关键字可变长度参数列表。
            **kwargs (Dict[str, Any]): 任意关键字参数。
        """
        self.args: Tuple[Any, ...] = args
        self.kwargs: Dict[str, Any] = kwargs

    @abstractmethod
    def get(self, url: str) -> None:
        """
        抽象方法，执行HTTP GET请求。

        参数:
            url (str): 发送GET请求的目标URL。

        异常:
            NotImplementedError: 本方法为抽象方法，需要在子类中实现。
        """
        pass

    @abstractmethod
    def post(self, url: str) -> None:
        """
        抽象方法，执行HTTP POST请求。

        参数:
            url (str): 发送POST请求的目标URL。

        异常:
            NotImplementedError: 本方法为抽象方法，需要在子类中实现。
        """
        pass

    @abstractmethod
    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        抽象方法，设置HTTP请求头信息。

        参数:
            headers (Dict[str, str]): 请求头键值对字典。

        异常:
            NotImplementedError: 本方法为抽象方法，需要在子类中实现。
        """
        pass
