"""
LeetCode 1242: Web Crawler Multithreaded

Given a URL startUrl and an interface HtmlParser, implement a multi-threaded web crawler
to crawl all links that are under the same hostname as startUrl.

Return all URLs obtained by your web crawler in any order.

Your crawler should:
1. Start from the page: startUrl
2. Call HtmlParser.getUrls(url) to get all URLs from a webpage of a given URL
3. Do not crawl the same link twice
4. Explore only the links that are under the same hostname as startUrl

The HtmlParser interface:
class HtmlParser(object):
    def getUrls(self, url):
        # Returns a list of strings representing URLs
        pass
"""

import queue
from typing import List, Set, override
from queue import Queue
from urllib.parse import urlparse
from threading import Thread


class HtmlParser:
    """
    Mock HtmlParser interface for testing purposes.
    In the actual LeetCode problem, this would be provided.
    """

    def __init__(self, urls_data: dict):
        """
        Initialize with a dictionary mapping URLs to their connected URLs.

        Args:
            urls_data: Dictionary where keys are URLs and values are lists of connected URLs
        """
        self.urls_data = urls_data

    def getUrls(self, url: str) -> List[str]:
        """
        Get all URLs from a webpage of a given URL.

        Args:
            url: The URL to get connected URLs from

        Returns:
            List of URLs connected to the given URL
        """
        return self.urls_data.get(url, [])


class Solution:
    def crawl(self, startUrl: str, htmlParser: HtmlParser) -> List[str]:
        """
        Crawl all links under the same hostname as startUrl using multithreading.

        Args:
            startUrl: The starting URL to crawl from
            htmlParser: Interface to get URLs from a webpage

        Returns:
            List of all URLs under the same hostname
        """
        visited: Set[str] = set()
        self.dfs(startUrl, visited, htmlParser, self._get_hostname(startUrl))
        return list(visited)

    def dfs(
        self,
        currentUrl: str,
        visited: Set[str],
        htmlParser: HtmlParser,
        valid_host: str,
    ) -> None:
        if self._get_hostname(currentUrl) == valid_host and currentUrl not in visited:
            visited.add(currentUrl)
            urls = htmlParser.getUrls(currentUrl)
            for url in urls:
                self.dfs(url, visited, htmlParser, valid_host)
        return

    def _get_hostname(self, url: str):
        return urlparse(url).netloc


class SolutionOptimized(Solution):
    def process_add_queue(
        self,
        q: Queue[str],
        current: str,
        host: str,
        visited: Set[str],
        htmlParser: HtmlParser,
    ):
        if current not in visited and self._get_hostname(current) == host:
            visited.add(current)
            for url in htmlParser.getUrls(current):
                q.put(url)

    def worker(
        self,
        q: Queue[str],
        host: str,
        visited: Set[str],
        htmlParser: HtmlParser,
        worker_id: int,
    ):
        url = q.get()
        while url != "KILL":
            self.process_add_queue(q, url, host, visited, htmlParser)
            q.task_done()
            url = q.get()
        q.task_done()

    @override
    def crawl(self, startUrl: str, htmlParser: HtmlParser) -> List[str]:
        q = Queue()
        host = self._get_hostname(startUrl)
        visited: Set[str] = set()

        q.put(startUrl)

        for tid in range(10):
            thread = Thread(
                target=self.worker, args=(q, host, visited, htmlParser, tid)
            )
            thread.daemon = True
            thread.start()

        q.join()
        for tid in range(10):
            q.put("KILL")

        return list(visited)
