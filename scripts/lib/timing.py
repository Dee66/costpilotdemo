"""
Performance Timing Decorator
Tracks execution time of test functions and suites
"""

import time
from functools import wraps
from typing import Dict, List, Callable, Any


# Global storage for timing data
_timing_data: Dict[str, List[float]] = {}


def timed(func: Callable) -> Callable:
    """
    Decorator to time function execution
    Records execution time in global timing data
    
    Usage:
        @timed
        def test_something():
            # test code
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            elapsed = end_time - start_time
            
            # Store timing data
            func_name = func.__name__
            if func_name not in _timing_data:
                _timing_data[func_name] = []
            _timing_data[func_name].append(elapsed)
    
    return wrapper


def get_timing_data() -> Dict[str, List[float]]:
    """
    Get all collected timing data
    
    Returns:
        Dictionary mapping function names to list of execution times
    """
    return _timing_data.copy()


def get_timing_summary() -> Dict[str, Dict[str, float]]:
    """
    Get summary statistics for all timed functions
    
    Returns:
        Dictionary with function names and their timing stats:
        - total: total time across all calls
        - count: number of calls
        - avg: average time per call
        - min: minimum time
        - max: maximum time
    """
    summary = {}
    
    for func_name, times in _timing_data.items():
        if times:
            summary[func_name] = {
                "total": sum(times),
                "count": len(times),
                "avg": sum(times) / len(times),
                "min": min(times),
                "max": max(times)
            }
    
    return summary


def get_slow_functions(threshold_ms: float = 1000) -> List[tuple]:
    """
    Get functions that exceed time threshold
    
    Args:
        threshold_ms: Time threshold in milliseconds (default: 1000ms = 1s)
        
    Returns:
        List of (function_name, avg_time_ms) tuples sorted by avg time descending
    """
    threshold_s = threshold_ms / 1000.0
    summary = get_timing_summary()
    
    slow_funcs = [
        (name, stats["avg"] * 1000)  # Convert to ms
        for name, stats in summary.items()
        if stats["avg"] > threshold_s
    ]
    
    # Sort by average time descending
    slow_funcs.sort(key=lambda x: x[1], reverse=True)
    
    return slow_funcs


def print_timing_report(threshold_ms: float = None, top_n: int = None):
    """
    Print formatted timing report
    
    Args:
        threshold_ms: Only show functions slower than this (in ms)
        top_n: Only show top N slowest functions
    """
    summary = get_timing_summary()
    
    if not summary:
        print("No timing data collected")
        return
    
    # Sort by average time descending
    sorted_funcs = sorted(
        summary.items(),
        key=lambda x: x[1]["avg"],
        reverse=True
    )
    
    # Apply filters
    if threshold_ms is not None:
        threshold_s = threshold_ms / 1000.0
        sorted_funcs = [
            (name, stats) 
            for name, stats in sorted_funcs 
            if stats["avg"] > threshold_s
        ]
    
    if top_n is not None:
        sorted_funcs = sorted_funcs[:top_n]
    
    # Print report
    print("\n" + "="*80)
    print("PERFORMANCE TIMING REPORT")
    print("="*80)
    
    if not sorted_funcs:
        print("No functions match the criteria")
        return
    
    print(f"\n{'Function':<40} {'Avg (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12} {'Calls':<8}")
    print("-" * 80)
    
    for func_name, stats in sorted_funcs:
        print(f"{func_name:<40} "
              f"{stats['avg']*1000:>10.2f}  "
              f"{stats['min']*1000:>10.2f}  "
              f"{stats['max']*1000:>10.2f}  "
              f"{stats['count']:>6}")
    
    # Print summary
    total_time = sum(stats["total"] for _, stats in summary.items())
    total_calls = sum(stats["count"] for _, stats in summary.items())
    
    print("-" * 80)
    print(f"Total Functions: {len(summary)}")
    print(f"Total Calls: {total_calls}")
    print(f"Total Time: {total_time:.3f}s ({total_time*1000:.2f}ms)")
    print()


def clear_timing_data():
    """Clear all collected timing data"""
    global _timing_data
    _timing_data.clear()


def export_timing_data(output_path: str, format: str = "json"):
    """
    Export timing data to file
    
    Args:
        output_path: Path to write output file
        format: Export format ('json' or 'csv')
    """
    from pathlib import Path
    
    if format == "json":
        import json
        summary = get_timing_summary()
        
        # Convert to serializable format
        output = {
            "summary": {
                name: {
                    "total_ms": stats["total"] * 1000,
                    "count": stats["count"],
                    "avg_ms": stats["avg"] * 1000,
                    "min_ms": stats["min"] * 1000,
                    "max_ms": stats["max"] * 1000
                }
                for name, stats in summary.items()
            },
            "raw_data": {
                name: [t * 1000 for t in times]
                for name, times in _timing_data.items()
            }
        }
        
        Path(output_path).write_text(json.dumps(output, indent=2))
        
    elif format == "csv":
        import csv
        summary = get_timing_summary()
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Function", "Total (ms)", "Count", "Avg (ms)", "Min (ms)", "Max (ms)"])
            
            for name, stats in sorted(summary.items()):
                writer.writerow([
                    name,
                    f"{stats['total'] * 1000:.3f}",
                    stats['count'],
                    f"{stats['avg'] * 1000:.3f}",
                    f"{stats['min'] * 1000:.3f}",
                    f"{stats['max'] * 1000:.3f}"
                ])
    else:
        raise ValueError(f"Unknown format: {format}. Supported: json, csv")


# Context manager for timing code blocks
class TimingContext:
    """
    Context manager for timing code blocks
    
    Usage:
        with TimingContext("my_operation"):
            # code to time
            expensive_operation()
    """
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start_time
        
        # Store timing data
        if self.name not in _timing_data:
            _timing_data[self.name] = []
        _timing_data[self.name].append(elapsed)
        
        return False  # Don't suppress exceptions
