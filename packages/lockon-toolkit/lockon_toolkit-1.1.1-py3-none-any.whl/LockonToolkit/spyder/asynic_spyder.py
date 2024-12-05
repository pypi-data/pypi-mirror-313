import aiohttp
import asyncio
from typing import Dict, List, Any, Tuple
from .MetaSpyder import MetaSpyder

_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


class AsyncSpider(MetaSpyder):
    headers = _DEFAULT_HEADERS

    def __init__(
        self,
        headers: Dict[str, str] = None,
        *args: Tuple[Any, ...],
        **kwargs: Dict[str, Any],
    ) -> None:
        """
        初始化AsyncSpider实例，继承自MetaSpyder，用于异步网络请求。

        参数:
            headers (Dict[str, str]): HTTP请求头信息。
            *args (Tuple[Any, ...]): 非关键字可变长度参数列表。
            **kwargs (Dict[str, Any]): 任意关键字参数。
        """
        super().__init__(*args, **kwargs)
        self.headers: Dict[str, str] = headers
        self.results: List[str] = []  # 存储异步请求结果

    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        设置HTTP请求头信息。

        参数:
            headers (Dict[str, str]): 请求头键值对字典。
        """
        self.headers = headers

    def post(self, url: str) -> None:
        """
        异步爬虫不支持POST请求，抛出异常。

        参数:
            url (str): 发送POST请求的目标URL。

        异常:
            NotImplementedError: 表示POST请求不被支持。
        """
        raise NotImplementedError("POST method not supported for async spider.")

    @staticmethod
    async def _fetch(session: aiohttp.ClientSession, url: str) -> str:
        """
        异步获取单个URL的内容。

        参数:
            session (aiohttp.ClientSession): aiohttp会话对象。
            url (str): 目标URL地址。

        返回:
            str: URL响应的内容。
        """
        async with session.get(url) as response:
            return await response.text()

    async def _run_async(self, url_list: List[str]) -> None:
        """
        执行异步请求，获取多个URL的内容。

        参数:
            url_list (List[str]): URL列表。

        返回:
            None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = [self._fetch(session, url) for url in url_list]
            html_contents = await asyncio.gather(*tasks)
            self.results.extend(html_contents)

    def get(self, url_list: List[str]) -> List[str]:
        """
        启动异步爬虫并返回结果。

        参数:
            url_list (List[str]): 要请求的URL列表。

        返回:
            List[str]: 请求得到的HTML内容列表。
        """
        asyncio.run(self._run_async(url_list))
        return self.results

# %%
if __name__ == "__main__":
    urls = [
        "https://www.cnblogs.com/qianpangzi/p/10922420.html#:~:text=%E5%A6%82%E4%BD%95%E6%89%BE%E5%87%BAnginx%E9%85%8D",
        "https://fugary.com/?p=532",
        "https://www.bilibili.com/",
    ]
    aspyder = AsyncSpider()
    aspyder.get(urls)