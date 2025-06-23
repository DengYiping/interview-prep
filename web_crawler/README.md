# Web Crawler Multithreaded - LeetCode 1242

This repository contains a Python implementation of LeetCode problem 1242: Web Crawler Multithreaded.

## Problem Description

Given a URL `startUrl` and an interface `HtmlParser`, implement a multi-threaded web crawler to crawl all links that are under the same hostname as `startUrl`.

### Requirements

1. Start from the page: `startUrl`
2. Call `HtmlParser.getUrls(url)` to get all URLs from a webpage of a given URL
3. Do not crawl the same link twice
4. Explore only the links that are under the same hostname as `startUrl`
5. Use multithreading for performance

## Files Structure

- `solution.py` - Main solution implementations (basic and optimized)
- `test_cases.py` - Comprehensive test cases based on LeetCode examples
- `test_runner.py` - Test runner with performance comparison
- `pyproject.toml` - Project configuration

## Solution Implementations

### 1. Basic Solution (`Solution` class)
- Uses ThreadPoolExecutor with worker threads
- Thread-safe queue and visited set management
- Simple but effective multithreading approach

### 2. Optimized Solution (`SolutionOptimized` class)
- Level-by-level processing approach
- Better thread utilization
- Reduced lock contention

## Running the Code

### Run Tests
```bash
python test_runner.py
```

### Run Individual Test
```python
from solution import Solution
from test_cases import test_case_1

solution = Solution()
test = test_case_1()
result = solution.crawl(test["start_url"], test["parser"])
print(result)
```

### Development Setup
```bash
# Install development dependencies
pip install -e .[dev]

# Format code
black .

# Lint code
ruff check --fix .

# Run tests with pytest
pytest
```

## Key Features

- **Thread Safety**: Uses locks to protect shared data structures
- **Hostname Filtering**: Only crawls URLs from the same hostname
- **Duplicate Detection**: Prevents crawling the same URL multiple times
- **Performance Testing**: Includes performance comparison between implementations
- **Comprehensive Testing**: Multiple test cases covering edge cases

## Test Cases

1. **Yahoo News Crawl** - Complex interconnected pages
2. **Google Domain Only** - Cross-domain filtering
3. **Linear Chain** - Sequential page crawling
4. **Circular References** - Handling cycles in page links
5. **Mixed Domains** - Filtering out different domains

## Performance Considerations

- Uses ThreadPoolExecutor for efficient thread management
- Implements proper synchronization to avoid race conditions
- Optimized version reduces lock contention
- Configurable number of worker threads

## Time Complexity
- O(N + E) where N is the number of unique URLs and E is the number of edges (links)
- Space complexity: O(N) for storing visited URLs

## Threading Strategy

The solution uses a producer-consumer pattern where:
- Multiple threads consume URLs from a shared queue
- Each thread processes a URL and adds new URLs to the queue
- Thread-safe data structures ensure consistency
- Worker threads coordinate through locks and shared state