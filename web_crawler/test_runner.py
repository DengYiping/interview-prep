"""
Test runner for LeetCode 1242: Web Crawler Multithreaded

This script runs all test cases and validates the solutions.
"""

import time
from typing import Set
from solution import Solution, SolutionOptimized
from test_cases import get_all_test_cases


def run_test_case(solution_class, test_case: dict) -> dict:
    """
    Run a single test case and return results.
    
    Args:
        solution_class: The solution class to test
        test_case: Dictionary containing test case data
        
    Returns:
        Dictionary with test results
    """
    solution = solution_class()
    
    start_time = time.time()
    result = solution.crawl(test_case["start_url"], test_case["parser"])
    end_time = time.time()
    
    result_set = set(result)
    expected_set = test_case["expected"]
    
    passed = result_set == expected_set
    
    return {
        "name": test_case["name"],
        "description": test_case["description"],
        "passed": passed,
        "execution_time": end_time - start_time,
        "result": result_set,
        "expected": expected_set,
        "missing_urls": expected_set - result_set,
        "extra_urls": result_set - expected_set
    }


def run_all_tests():
    """Run all test cases for both solution implementations."""
    test_cases = get_all_test_cases()
    solutions = [
        ("Basic Solution", Solution),
        ("Optimized Solution", SolutionOptimized)
    ]
    
    print("=" * 80)
    print("LeetCode 1242: Web Crawler Multithreaded - Test Results")
    print("=" * 80)
    
    for solution_name, solution_class in solutions:
        print(f"\n{solution_name}")
        print("-" * 50)
        
        total_tests = len(test_cases)
        passed_tests = 0
        total_time = 0
        
        for test_case in test_cases:
            result = run_test_case(solution_class, test_case)
            total_time += result["execution_time"]
            
            if result["passed"]:
                passed_tests += 1
                status = "✅ PASSED"
            else:
                status = "❌ FAILED"
            
            print(f"{status} - {result['name']}")
            print(f"  Description: {result['description']}")
            print(f"  Execution Time: {result['execution_time']:.4f}s")
            
            if not result["passed"]:
                print(f"  Expected: {sorted(result['expected'])}")
                print(f"  Got:      {sorted(result['result'])}")
                if result["missing_urls"]:
                    print(f"  Missing:  {sorted(result['missing_urls'])}")
                if result["extra_urls"]:
                    print(f"  Extra:    {sorted(result['extra_urls'])}")
            
            print()
        
        print(f"Summary: {passed_tests}/{total_tests} tests passed")
        print(f"Total execution time: {total_time:.4f}s")
        print(f"Average time per test: {total_time/total_tests:.4f}s")


def run_performance_test():
    """Run performance comparison between solutions."""
    print("\n" + "=" * 80)
    print("Performance Comparison")
    print("=" * 80)
    
    # Create a larger test case for performance testing
    large_urls_data = {}
    base_url = "http://performance.test"
    
    # Create a tree-like structure with 100 URLs
    for i in range(100):
        url = f"{base_url}/page{i}"
        connections = []
        
        # Each page connects to 2-3 other pages
        for j in range(min(3, 100 - i - 1)):
            if i + j + 1 < 100:
                connections.append(f"{base_url}/page{i + j + 1}")
        
        large_urls_data[url] = connections
    
    from solution import HtmlParser
    large_parser = HtmlParser(large_urls_data)
    
    solutions = [
        ("Basic Solution", Solution),
        ("Optimized Solution", SolutionOptimized)
    ]
    
    for solution_name, solution_class in solutions:
        solution = solution_class()
        
        start_time = time.time()
        result = solution.crawl(f"{base_url}/page0", large_parser)
        end_time = time.time()
        
        print(f"{solution_name}:")
        print(f"  URLs crawled: {len(result)}")
        print(f"  Execution time: {end_time - start_time:.4f}s")
        print()


if __name__ == "__main__":
    run_all_tests()
    run_performance_test()