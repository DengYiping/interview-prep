#!/usr/bin/env python3
"""
Evaluation script for "finding duplicate files on a filesystem" interview question.

This script creates test scenarios and evaluates solutions for finding duplicate files
based on content hash (not just filename).
"""

import hashlib
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Set, Callable, Any
import sys


def create_test_filesystem() -> Path:
    """Create a temporary filesystem with known duplicate files for testing."""
    test_dir = Path(tempfile.mkdtemp(prefix="duplicate_test_"))
    
    # Create directory structure
    (test_dir / "dir1").mkdir()
    (test_dir / "dir2").mkdir()
    (test_dir / "dir1" / "subdir").mkdir()
    (test_dir / "empty_dir").mkdir()
    
    # Create test files with known content
    test_files = {
        "file1.txt": "Hello World",
        "dir1/file2.txt": "Hello World",  # Duplicate of file1.txt
        "dir1/file3.txt": "Different content",
        "dir2/file4.txt": "Hello World",  # Another duplicate
        "dir1/subdir/file5.txt": "Different content",  # Duplicate of file3.txt
        "binary_file1.bin": b"\x00\x01\x02\x03",
        "dir2/binary_file2.bin": b"\x00\x01\x02\x03",  # Binary duplicate
        "large_file.txt": "A" * 10000,
        "dir1/large_duplicate.txt": "A" * 10000,  # Large file duplicate
        "single_file.txt": "Unique content here",
    }
    
    for file_path, content in test_files.items():
        full_path = test_dir / file_path
        if isinstance(content, str):
            full_path.write_text(content)
        else:
            full_path.write_bytes(content)
    
    return test_dir


def calculate_expected_duplicates(test_dir: Path) -> Dict[str, Set[Path]]:
    """Calculate expected duplicate groups for the test filesystem."""
    content_to_files = {}
    
    for file_path in test_dir.rglob("*"):
        if file_path.is_file():
            try:
                with open(file_path, "rb") as f:
                    content_hash = hashlib.md5(f.read()).hexdigest()
                
                if content_hash not in content_to_files:
                    content_to_files[content_hash] = set()
                content_to_files[content_hash].add(file_path)
            except (IOError, OSError):
                continue
    
    # Return only groups with duplicates (size > 1)
    return {hash_val: files for hash_val, files in content_to_files.items() if len(files) > 1}


def normalize_result(result: Any) -> Dict[str, Set[Path]]:
    """Normalize different possible return formats to a standard format."""
    if isinstance(result, dict):
        # Handle dict of lists/sets
        normalized = {}
        for key, files in result.items():
            if isinstance(files, (list, set, tuple)):
                normalized[str(key)] = {Path(f) for f in files}
        return normalized
    
    elif isinstance(result, (list, set, tuple)):
        # Handle list of lists/groups
        normalized = {}
        for i, group in enumerate(result):
            if isinstance(group, (list, set, tuple)) and len(group) > 1:
                normalized[f"group_{i}"] = {Path(f) for f in group}
        return normalized
    
    return {}


def evaluate_correctness(solution_func: Callable, test_dir: Path) -> Dict[str, Any]:
    """Evaluate the correctness of a duplicate finding solution."""
    expected = calculate_expected_duplicates(test_dir)
    
    try:
        result = solution_func(str(test_dir))
        normalized_result = normalize_result(result)
    except Exception as e:
        return {
            "passed": False,
            "error": f"Function raised exception: {e}",
            "expected_groups": len(expected),
            "found_groups": 0
        }
    
    # Check if all expected duplicates were found
    expected_file_sets = set()
    for files in expected.values():
        expected_file_sets.add(frozenset(files))
    
    found_file_sets = set()
    for files in normalized_result.values():
        found_file_sets.add(frozenset(files))
    
    missing_groups = expected_file_sets - found_file_sets
    extra_groups = found_file_sets - expected_file_sets
    
    return {
        "passed": len(missing_groups) == 0 and len(extra_groups) == 0,
        "expected_groups": len(expected),
        "found_groups": len(normalized_result),
        "missing_groups": len(missing_groups),
        "extra_groups": len(extra_groups),
        "expected": expected,
        "result": normalized_result
    }


def evaluate_edge_cases(solution_func: Callable) -> List[Dict[str, Any]]:
    """Test edge cases for the duplicate finding solution."""
    edge_cases = []
    
    # Test 1: Empty directory
    empty_dir = Path(tempfile.mkdtemp(prefix="empty_test_"))
    try:
        result = solution_func(str(empty_dir))
        normalized = normalize_result(result)
        edge_cases.append({
            "name": "Empty directory",
            "passed": len(normalized) == 0,
            "description": "Should handle empty directories gracefully"
        })
    except Exception as e:
        edge_cases.append({
            "name": "Empty directory",
            "passed": False,
            "error": str(e),
            "description": "Should handle empty directories gracefully"
        })
    finally:
        shutil.rmtree(empty_dir)
    
    # Test 2: Non-existent directory
    try:
        result = solution_func("/non/existent/path")
        edge_cases.append({
            "name": "Non-existent directory",
            "passed": False,
            "description": "Should handle non-existent paths appropriately"
        })
    except Exception:
        edge_cases.append({
            "name": "Non-existent directory",
            "passed": True,
            "description": "Should handle non-existent paths appropriately"
        })
    
    # Test 3: Single file (no duplicates)
    single_dir = Path(tempfile.mkdtemp(prefix="single_test_"))
    (single_dir / "only_file.txt").write_text("unique content")
    try:
        result = solution_func(str(single_dir))
        normalized = normalize_result(result)
        edge_cases.append({
            "name": "Single file (no duplicates)",
            "passed": len(normalized) == 0,
            "description": "Should return empty result when no duplicates exist"
        })
    except Exception as e:
        edge_cases.append({
            "name": "Single file (no duplicates)",
            "passed": False,
            "error": str(e),
            "description": "Should return empty result when no duplicates exist"
        })
    finally:
        shutil.rmtree(single_dir)
    
    return edge_cases


def run_evaluation(solution_func: Callable) -> Dict[str, Any]:
    """Run complete evaluation of a duplicate finding solution."""
    print("Creating test filesystem...")
    test_dir = create_test_filesystem()
    
    try:
        print(f"Test directory created at: {test_dir}")
        
        # Basic correctness test
        print("\nEvaluating correctness...")
        correctness = evaluate_correctness(solution_func, test_dir)
        
        # Edge cases
        print("Testing edge cases...")
        edge_cases = evaluate_edge_cases(solution_func)
        
        # Performance test (basic)
        print("Testing performance...")
        import time
        start_time = time.time()
        try:
            solution_func(str(test_dir))
            execution_time = time.time() - start_time
            performance_passed = execution_time < 5.0  # Should complete in reasonable time
        except Exception:
            execution_time = float('inf')
            performance_passed = False
        
        return {
            "correctness": correctness,
            "edge_cases": edge_cases,
            "performance": {
                "execution_time": execution_time,
                "passed": performance_passed
            },
            "overall_passed": (
                correctness["passed"] and 
                all(case["passed"] for case in edge_cases) and 
                performance_passed
            )
        }
    
    finally:
        # Cleanup
        print(f"\nCleaning up test directory: {test_dir}")
        shutil.rmtree(test_dir)


def print_results(results: Dict[str, Any]) -> None:
    """Print evaluation results in a readable format."""
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    
    # Correctness
    correctness = results["correctness"]
    print(f"\nCORRECTNESS: {'✅ PASSED' if correctness['passed'] else '❌ FAILED'}")
    print(f"  Expected duplicate groups: {correctness['expected_groups']}")
    print(f"  Found duplicate groups: {correctness['found_groups']}")
    
    if not correctness["passed"]:
        print(f"  Missing groups: {correctness['missing_groups']}")
        print(f"  Extra groups: {correctness['extra_groups']}")
        if "error" in correctness:
            print(f"  Error: {correctness['error']}")
    
    # Edge cases
    print(f"\nEDGE CASES:")
    for case in results["edge_cases"]:
        status = "✅ PASSED" if case["passed"] else "❌ FAILED"
        print(f"  {case['name']}: {status}")
        if not case["passed"] and "error" in case:
            print(f"    Error: {case['error']}")
    
    # Performance
    perf = results["performance"]
    print(f"\nPERFORMANCE: {'✅ PASSED' if perf['passed'] else '❌ FAILED'}")
    if perf["execution_time"] != float('inf'):
        print(f"  Execution time: {perf['execution_time']:.3f} seconds")
    else:
        print("  Execution time: Failed to complete")
    
    # Overall
    print(f"\nOVERALL: {'✅ PASSED' if results['overall_passed'] else '❌ FAILED'}")


def main():
    """Main entry point for the evaluation script."""
    if len(sys.argv) < 2:
        print("Usage: python evaluate.py <solution_module>")
        print("Example: python evaluate.py solution")
        sys.exit(1)
    
    module_name = sys.argv[1]
    
    try:
        # Import the solution module
        solution_module = __import__(module_name)
        
        # Look for a function that finds duplicates
        possible_function_names = [
            'find_duplicates',
            'find_duplicate_files',
            'get_duplicates',
            'duplicate_finder',
            'main'
        ]
        
        solution_func = None
        for func_name in possible_function_names:
            if hasattr(solution_module, func_name):
                solution_func = getattr(solution_module, func_name)
                print(f"Found solution function: {func_name}")
                break
        
        if solution_func is None:
            print(f"Could not find a solution function in {module_name}.py")
            print(f"Expected one of: {', '.join(possible_function_names)}")
            sys.exit(1)
        
        # Run evaluation
        results = run_evaluation(solution_func)
        print_results(results)
        
        # Exit with appropriate code
        sys.exit(0 if results["overall_passed"] else 1)
        
    except ImportError as e:
        print(f"Could not import module '{module_name}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during evaluation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()