#!/usr/bin/env python3
"""
Interview Question: Find Duplicate Files on a Filesystem

Implement a solution to find duplicate files in a directory based on content hash.
Your solution should handle the following requirements:

1. Find all files with identical content (not just same filename)
2. Return groups of duplicate files
3. Handle edge cases (empty directories, non-existent paths, permission errors)
4. Be efficient for large directories and files

The evaluate.py script will test your implementation with various scenarios.
"""

from pathlib import Path
from typing import Dict, List


def find_duplicates(directory: str) -> Dict[str, List[str]]:
    """
    Find duplicate files in a directory based on content hash.
    
    Args:
        directory: Path to the directory to search for duplicates
        
    Returns:
        Dictionary mapping hash values to lists of file paths that have the same content.
        Only returns groups with more than one file (actual duplicates).
        
    Raises:
        FileNotFoundError: If the directory doesn't exist
        PermissionError: If access is denied to the directory
    """
    # TODO: Implement your solution here
    # Hints:
    # - Use pathlib.Path for path operations
    # - Calculate content hash for each file (MD5 or SHA256)
    # - Group files by their hash values
    # - Handle errors gracefully
    # - Only return groups with multiple files
    
    pass


def main() -> None:
    """
    Main entry point for command-line usage.
    Run with: python solution.py <directory_path>
    """
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python solution.py <directory_path>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    try:
        duplicates = find_duplicates(directory)
        
        if not duplicates:
            print("No duplicate files found.")
        else:
            print(f"Found {len(duplicates)} group(s) of duplicate files:")
            for i, (file_hash, file_list) in enumerate(duplicates.items(), 1):
                print(f"\nGroup {i}:")
                for file_path in sorted(file_list):
                    print(f"  - {file_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()