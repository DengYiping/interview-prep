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

from typing import List, Set
from concurrent.futures import ThreadPoolExecutor
import threading
from urllib.parse import urlparse


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
        # Extract hostname from startUrl
        hostname = self._get_hostname(startUrl)
        
        # Thread-safe set to store visited URLs
        visited = set()
        visited_lock = threading.Lock()
        
        # Queue for URLs to crawl
        to_crawl = [startUrl]
        to_crawl_lock = threading.Lock()
        
        def crawl_worker():
            """Worker function for crawling URLs."""
            while True:
                # Get next URL to crawl
                with to_crawl_lock:
                    if not to_crawl:
                        break
                    current_url = to_crawl.pop(0)
                
                # Check if already visited
                with visited_lock:
                    if current_url in visited:
                        continue
                    visited.add(current_url)
                
                # Get URLs from current page
                urls = htmlParser.getUrls(current_url)
                
                # Add URLs with same hostname to crawl queue
                with to_crawl_lock:
                    for url in urls:
                        if (self._get_hostname(url) == hostname and 
                            url not in visited):
                            to_crawl.append(url)
        
        # Use ThreadPoolExecutor for multithreading
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit multiple worker threads
            futures = []
            for _ in range(10):
                futures.append(executor.submit(crawl_worker))
            
            # Wait for all workers to complete
            for future in futures:
                future.result()
        
        return list(visited)
    
    def _get_hostname(self, url: str) -> str:
        """
        Extract hostname from URL.
        
        Args:
            url: The URL to extract hostname from
            
        Returns:
            The hostname of the URL
        """
        return urlparse(url).netloc


class SolutionOptimized:
    """
    Optimized version using a more efficient multithreading approach.
    """
    
    def crawl(self, startUrl: str, htmlParser: HtmlParser) -> List[str]:
        """
        Optimized crawl implementation with better thread management.
        
        Args:
            startUrl: The starting URL to crawl from
            htmlParser: Interface to get URLs from a webpage
            
        Returns:
            List of all URLs under the same hostname
        """
        hostname = self._get_hostname(startUrl)
        
        # Thread-safe structures
        visited = set()
        to_visit = {startUrl}
        lock = threading.Lock()
        
        def crawl_page(url: str) -> List[str]:
            """Crawl a single page and return new URLs to visit."""
            urls = htmlParser.getUrls(url)
            new_urls = []
            
            for new_url in urls:
                if self._get_hostname(new_url) == hostname:
                    with lock:
                        if new_url not in visited and new_url not in to_visit:
                            to_visit.add(new_url)
                            new_urls.append(new_url)
            
            return new_urls
        
        # Process URLs level by level
        with ThreadPoolExecutor(max_workers=8) as executor:
            while to_visit:
                # Get current batch of URLs to process
                with lock:
                    current_batch = list(to_visit)
                    to_visit.clear()
                    visited.update(current_batch)
                
                # Process current batch in parallel
                futures = [executor.submit(crawl_page, url) for url in current_batch]
                
                # Collect results
                for future in futures:
                    new_urls = future.result()
                    # New URLs are already added to to_visit in crawl_page
        
        return list(visited)
    
    def _get_hostname(self, url: str) -> str:
        """Extract hostname from URL."""
        return urlparse(url).netloc