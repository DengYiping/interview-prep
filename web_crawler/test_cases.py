"""
Test cases for LeetCode 1242: Web Crawler Multithreaded

This file contains test cases based on the LeetCode problem examples.
"""

from solution import Solution, SolutionOptimized, HtmlParser


def test_case_1():
    """
    Test Case 1:
    URLs = [
        "http://news.yahoo.com",
        "http://news.yahoo.com/news",
        "http://news.yahoo.com/news/topics/",
        "http://news.google.com",
        "http://news.yahoo.com/us"
    ]
    Edges = [[2,0],[2,1],[3,2],[3,1],[0,4]]
    startUrl = "http://news.yahoo.com/news/topics/"
    
    Expected output: 
    [
        "http://news.yahoo.com",
        "http://news.yahoo.com/news",
        "http://news.yahoo.com/news/topics/",
        "http://news.yahoo.com/us"
    ]
    """
    urls_data = {
        "http://news.yahoo.com": ["http://news.yahoo.com/us"],
        "http://news.yahoo.com/news": [],
        "http://news.yahoo.com/news/topics/": [
            "http://news.yahoo.com",
            "http://news.yahoo.com/news"
        ],
        "http://news.google.com": [
            "http://news.yahoo.com/news/topics/",
            "http://news.yahoo.com/news"
        ],
        "http://news.yahoo.com/us": []
    }
    
    parser = HtmlParser(urls_data)
    start_url = "http://news.yahoo.com/news/topics/"
    
    expected = {
        "http://news.yahoo.com",
        "http://news.yahoo.com/news",
        "http://news.yahoo.com/news/topics/",
        "http://news.yahoo.com/us"
    }
    
    return {
        "name": "Test Case 1 - Yahoo News Crawl",
        "parser": parser,
        "start_url": start_url,
        "expected": expected,
        "description": "Crawl yahoo.com domain starting from topics page"
    }


def test_case_2():
    """
    Test Case 2:
    URLs = [
        "http://news.yahoo.com",
        "http://news.yahoo.com/news",
        "http://news.yahoo.com/news/topics/",
        "http://news.google.com"
    ]
    Edges = [[0,2],[2,1],[3,2],[3,1],[3,0]]
    startUrl = "http://news.google.com"
    
    Expected output: ["http://news.google.com"]
    (Only Google domain, yahoo.com links are filtered out)
    """
    urls_data = {
        "http://news.yahoo.com": ["http://news.yahoo.com/news/topics/"],
        "http://news.yahoo.com/news": [],
        "http://news.yahoo.com/news/topics/": ["http://news.yahoo.com/news"],
        "http://news.google.com": [
            "http://news.yahoo.com/news/topics/",
            "http://news.yahoo.com/news",
            "http://news.yahoo.com"
        ]
    }
    
    parser = HtmlParser(urls_data)
    start_url = "http://news.google.com"
    
    expected = {"http://news.google.com"}
    
    return {
        "name": "Test Case 2 - Google Domain Only",
        "parser": parser,
        "start_url": start_url,
        "expected": expected,
        "description": "Crawl google.com domain, should not visit yahoo.com links"
    }


def test_case_3():
    """
    Test Case 3: Simple linear chain
    """
    urls_data = {
        "http://example.com": ["http://example.com/page1"],
        "http://example.com/page1": ["http://example.com/page2"],
        "http://example.com/page2": ["http://example.com/page3"],
        "http://example.com/page3": []
    }
    
    parser = HtmlParser(urls_data)
    start_url = "http://example.com"
    
    expected = {
        "http://example.com",
        "http://example.com/page1",
        "http://example.com/page2",
        "http://example.com/page3"
    }
    
    return {
        "name": "Test Case 3 - Linear Chain",
        "parser": parser,
        "start_url": start_url,
        "expected": expected,
        "description": "Crawl a linear chain of pages"
    }


def test_case_4():
    """
    Test Case 4: Circular references
    """
    urls_data = {
        "http://test.com/a": ["http://test.com/b", "http://test.com/c"],
        "http://test.com/b": ["http://test.com/a", "http://test.com/d"],
        "http://test.com/c": ["http://test.com/a"],
        "http://test.com/d": ["http://test.com/b"]
    }
    
    parser = HtmlParser(urls_data)
    start_url = "http://test.com/a"
    
    expected = {
        "http://test.com/a",
        "http://test.com/b",
        "http://test.com/c",
        "http://test.com/d"
    }
    
    return {
        "name": "Test Case 4 - Circular References",
        "parser": parser,
        "start_url": start_url,
        "expected": expected,
        "description": "Crawl pages with circular references"
    }


def test_case_5():
    """
    Test Case 5: Mixed domains
    """
    urls_data = {
        "http://site1.com": [
            "http://site1.com/page1",
            "http://site2.com/page1",  # Different domain - should be ignored
            "http://site1.com/page2"
        ],
        "http://site1.com/page1": ["http://site1.com/page3"],
        "http://site1.com/page2": ["http://site2.com/page2"],  # Different domain - should be ignored
        "http://site1.com/page3": [],
        "http://site2.com/page1": ["http://site2.com/page2"],
        "http://site2.com/page2": []
    }
    
    parser = HtmlParser(urls_data)
    start_url = "http://site1.com"
    
    expected = {
        "http://site1.com",
        "http://site1.com/page1",
        "http://site1.com/page2",
        "http://site1.com/page3"
    }
    
    return {
        "name": "Test Case 5 - Mixed Domains",
        "parser": parser,
        "start_url": start_url,
        "expected": expected,
        "description": "Crawl with mixed domains, should filter out different domains"
    }


def get_all_test_cases():
    """Get all test cases for the web crawler problem."""
    return [
        test_case_1(),
        test_case_2(),
        test_case_3(),
        test_case_4(),
        test_case_5()
    ]