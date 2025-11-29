#!/usr/bin/env python3
"""
KRL Analytics Suite - Performance Benchmarks

Comprehensive benchmarking for all major components.
Generates performance reports and identifies optimization opportunities.
"""

import gc
import os
import sys
import time
import json
import tracemalloc
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd


@dataclass
class BenchmarkResult:
    """Single benchmark result."""
    name: str
    category: str
    n_observations: int
    execution_time: float
    memory_peak_mb: float
    memory_current_mb: float
    throughput: float  # obs/sec
    success: bool
    error: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass 
class BenchmarkSuite:
    """Collection of benchmark results."""
    suite_name: str
    timestamp: str
    system_info: Dict[str, str]
    results: List[BenchmarkResult] = field(default_factory=list)
    
    def add_result(self, result: BenchmarkResult):
        self.results.append(result)
    
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(r) for r in self.results])
    
    def summary(self) -> str:
        df = self.to_dataframe()
        lines = [
            f"\n{'='*70}",
            f"BENCHMARK SUMMARY: {self.suite_name}",
            f"{'='*70}",
            f"Timestamp: {self.timestamp}",
            f"Total benchmarks: {len(self.results)}",
            f"Successful: {df['success'].sum()}",
            f"Failed: {(~df['success']).sum()}",
            f"",
            f"{'Category':<25} {'Avg Time (s)':<15} {'Avg Memory (MB)':<15} {'Throughput':<15}",
            f"{'-'*70}",
        ]
        
        for cat in df['category'].unique():
            cat_df = df[df['category'] == cat]
            lines.append(
                f"{cat:<25} {cat_df['execution_time'].mean():<15.3f} "
                f"{cat_df['memory_peak_mb'].mean():<15.1f} "
                f"{cat_df['throughput'].mean():<15.0f}"
            )
        
        lines.append(f"{'='*70}\n")
        return '\n'.join(lines)
    
    def save(self, path: str):
        """Save results to JSON."""
        with open(path, 'w') as f:
            json.dump({
                'suite_name': self.suite_name,
                'timestamp': self.timestamp,
                'system_info': self.system_info,
                'results': [asdict(r) for r in self.results],
            }, f, indent=2)


def get_system_info() -> Dict[str, str]:
    """Collect system information."""
    import platform
    
    info = {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'processor': platform.processor(),
        'cpu_count': str(os.cpu_count()),
    }
    
    try:
        import psutil
        info['total_memory_gb'] = f"{psutil.virtual_memory().total / 1e9:.1f}"
    except ImportError:
        info['total_memory_gb'] = 'unknown'
    
    try:
        import torch
        info['cuda_available'] = str(torch.cuda.is_available())
        if torch.cuda.is_available():
            info['cuda_device'] = torch.cuda.get_device_name(0)
    except ImportError:
        info['cuda_available'] = 'pytorch not installed'
    
    return info


def benchmark(
    func: Callable,
    name: str,
    category: str,
    n_obs: int,
    n_runs: int = 3,
    warmup: int = 1,
) -> BenchmarkResult:
    """
    Run a benchmark with timing and memory tracking.
    
    Args:
        func: Function to benchmark (no args)
        name: Benchmark name
        category: Category (e.g., 'spatial', 'causal')
        n_obs: Number of observations
        n_runs: Number of timed runs
        warmup: Number of warmup runs
    
    Returns:
        BenchmarkResult
    """
    # Warmup
    for _ in range(warmup):
        try:
            gc.collect()
            func()
        except Exception:
            pass
    
    # Timed runs
    times = []
    memory_peaks = []
    memory_currents = []
    success = True
    error = None
    
    for _ in range(n_runs):
        gc.collect()
        tracemalloc.start()
        
        try:
            start = time.perf_counter()
            func()
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            
            current, peak = tracemalloc.get_traced_memory()
            memory_peaks.append(peak / 1e6)
            memory_currents.append(current / 1e6)
            
        except Exception as e:
            success = False
            error = str(e)
            times.append(float('inf'))
            memory_peaks.append(0)
            memory_currents.append(0)
        
        finally:
            tracemalloc.stop()
    
    avg_time = np.mean(times)
    throughput = n_obs / avg_time if avg_time > 0 and avg_time != float('inf') else 0
    
    return BenchmarkResult(
        name=name,
        category=category,
        n_observations=n_obs,
        execution_time=avg_time,
        memory_peak_mb=np.max(memory_peaks),
        memory_current_mb=np.mean(memory_currents),
        throughput=throughput,
        success=success,
        error=error,
    )


# =============================================================================
# BENCHMARK FUNCTIONS
# =============================================================================

def benchmark_spatial_index(sizes: List[int] = [1000, 5000, 10000]) -> List[BenchmarkResult]:
    """Benchmark spatial indexing operations."""
    results = []
    
    try:
        from krl_geospatial.indexing import SpatialIndex
        import geopandas as gpd
        from shapely.geometry import Point
    except ImportError:
        return results
    
    for n in sizes:
        # Generate random points
        np.random.seed(42)
        coords = np.random.uniform(0, 100, (n, 2))
        gdf = gpd.GeoDataFrame(
            geometry=[Point(x, y) for x, y in coords],
            crs='EPSG:4326'
        )
        
        # Index build
        def build_index():
            idx = SpatialIndex()
            idx.build_from_geodataframe(gdf)
            return idx
        
        result = benchmark(
            build_index,
            name=f'SpatialIndex.build (n={n})',
            category='spatial_index',
            n_obs=n,
        )
        results.append(result)
        
        # Query benchmark
        idx = build_index()
        query_point = Point(50, 50)
        
        def query_nearest():
            for _ in range(100):
                idx.query_nearest(query_point, k=5)
        
        result = benchmark(
            query_nearest,
            name=f'SpatialIndex.query_nearest (n={n}, k=5, 100 queries)',
            category='spatial_index',
            n_obs=n,
        )
        results.append(result)
    
    return results


def benchmark_gwr(sizes: List[int] = [500, 1000, 2000]) -> List[BenchmarkResult]:
    """Benchmark GWR implementations."""
    results = []
    
    try:
        from krl_geospatial.econometrics import ParallelGWR
    except ImportError:
        return results
    
    for n in sizes:
        np.random.seed(42)
        coords = np.random.uniform(0, 100, (n, 2))
        X = np.random.randn(n, 3)
        y = 5 + 2*X[:,0] + 0.5*X[:,1] - X[:,2] + np.random.randn(n)
        
        for backend in ['sequential', 'dask']:
            def fit_gwr():
                model = ParallelGWR(backend=backend, verbose=False)
                return model.fit(y, X, coords, bandwidth=15.0)
            
            result = benchmark(
                fit_gwr,
                name=f'ParallelGWR.fit ({backend}, n={n})',
                category='gwr',
                n_obs=n,
            )
            results.append(result)
    
    return results


def benchmark_scm(sizes: List[int] = [50, 100, 200]) -> List[BenchmarkResult]:
    """Benchmark Synthetic Control Method."""
    results = []
    
    try:
        from krl_models.causal import SyntheticControlMethod
    except ImportError:
        return results
    
    for n_units in sizes:
        np.random.seed(42)
        T = 100
        treatment_period = 50
        
        # Generate panel data
        Y = np.random.randn(T, n_units)
        for t in range(treatment_period, T):
            Y[t, 0] += 2.0  # Treatment effect
        
        def fit_scm():
            scm = SyntheticControlMethod()
            return scm.fit(Y, treated_unit=0, treatment_period=treatment_period)
        
        result = benchmark(
            fit_scm,
            name=f'SCM.fit (units={n_units}, T={T})',
            category='causal',
            n_obs=n_units * T,
        )
        results.append(result)
    
    return results


def benchmark_multi_unit_scm(sizes: List[int] = [10, 20, 30]) -> List[BenchmarkResult]:
    """Benchmark Multi-Unit SCM."""
    results = []
    
    try:
        from krl_models.causal import MultiUnitSCM
    except ImportError:
        return results
    
    for n_treated in sizes:
        np.random.seed(42)
        T = 100
        n_units = n_treated + 50
        
        Y = np.random.randn(T, n_units)
        treated_units = list(range(n_treated))
        treatment_periods = [50] * n_treated
        
        def fit_mscm():
            mscm = MultiUnitSCM(cross_validation=False)
            return mscm.fit(Y, treated_units, treatment_periods)
        
        result = benchmark(
            fit_mscm,
            name=f'MultiUnitSCM.fit (treated={n_treated})',
            category='causal',
            n_obs=n_units * T,
        )
        results.append(result)
    
    return results


def benchmark_spatial_weights(sizes: List[int] = [500, 1000, 2000]) -> List[BenchmarkResult]:
    """Benchmark spatial weights construction."""
    results = []
    
    try:
        from krl_geospatial.indexing import RTreeQueenWeights, RTreeKNNWeights
        import geopandas as gpd
        from shapely.geometry import box
    except ImportError:
        return results
    
    for n in sizes:
        np.random.seed(42)
        # Create grid of polygons
        size = int(np.sqrt(n))
        polygons = []
        for i in range(size):
            for j in range(size):
                polygons.append(box(i, j, i+1, j+1))
        
        gdf = gpd.GeoDataFrame(geometry=polygons[:n], crs='EPSG:4326')
        
        def build_queen():
            return RTreeQueenWeights(gdf)
        
        result = benchmark(
            build_queen,
            name=f'RTreeQueenWeights (n={n})',
            category='spatial_weights',
            n_obs=n,
        )
        results.append(result)
        
        def build_knn():
            return RTreeKNNWeights(gdf, k=5)
        
        result = benchmark(
            build_knn,
            name=f'RTreeKNNWeights (n={n}, k=5)',
            category='spatial_weights',
            n_obs=n,
        )
        results.append(result)
    
    return results


def benchmark_data_connectors() -> List[BenchmarkResult]:
    """Benchmark data connector operations (mocked)."""
    results = []
    
    # Mock connector benchmarks (actual API calls would be slow/rate-limited)
    for connector in ['FRED', 'Census', 'EJSCREEN']:
        n_series = 10
        
        def mock_fetch():
            time.sleep(0.01)  # Simulate network latency
            return np.random.randn(100, n_series)
        
        result = benchmark(
            mock_fetch,
            name=f'{connector}Connector.fetch (n_series={n_series})',
            category='data_connectors',
            n_obs=100 * n_series,
        )
        results.append(result)
    
    return results


def run_all_benchmarks(output_dir: str = 'benchmarks') -> BenchmarkSuite:
    """Run all benchmarks and generate report."""
    os.makedirs(output_dir, exist_ok=True)
    
    suite = BenchmarkSuite(
        suite_name='KRL Analytics Suite Full Benchmark',
        timestamp=datetime.now().isoformat(),
        system_info=get_system_info(),
    )
    
    print("Running KRL Analytics Suite Benchmarks...")
    print("="*60)
    
    # Run each benchmark category
    benchmark_funcs = [
        ('Spatial Index', benchmark_spatial_index),
        ('Spatial Weights', benchmark_spatial_weights),
        ('GWR', benchmark_gwr),
        ('SCM', benchmark_scm),
        ('Multi-Unit SCM', benchmark_multi_unit_scm),
        ('Data Connectors', benchmark_data_connectors),
    ]
    
    for name, func in benchmark_funcs:
        print(f"\n[{name}]")
        try:
            results = func()
            for r in results:
                suite.add_result(r)
                status = "✓" if r.success else "✗"
                print(f"  {status} {r.name}: {r.execution_time:.3f}s, {r.memory_peak_mb:.1f}MB")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    # Save results
    suite.save(os.path.join(output_dir, 'benchmark_results.json'))
    
    # Generate markdown report
    report = generate_report(suite)
    with open(os.path.join(output_dir, 'BENCHMARK_REPORT.md'), 'w') as f:
        f.write(report)
    
    print(suite.summary())
    print(f"\nResults saved to {output_dir}/")
    
    return suite


def generate_report(suite: BenchmarkSuite) -> str:
    """Generate markdown benchmark report."""
    df = suite.to_dataframe()
    
    lines = [
        "# KRL Analytics Suite - Benchmark Report",
        "",
        f"> Generated: {suite.timestamp}",
        "",
        "## System Information",
        "",
        "| Property | Value |",
        "|----------|-------|",
    ]
    
    for key, value in suite.system_info.items():
        lines.append(f"| {key} | {value} |")
    
    lines.extend([
        "",
        "## Summary by Category",
        "",
        "| Category | Avg Time (s) | Avg Memory (MB) | Avg Throughput (obs/s) |",
        "|----------|--------------|-----------------|------------------------|",
    ])
    
    for cat in df['category'].unique():
        cat_df = df[df['category'] == cat]
        lines.append(
            f"| {cat} | {cat_df['execution_time'].mean():.3f} | "
            f"{cat_df['memory_peak_mb'].mean():.1f} | "
            f"{cat_df['throughput'].mean():.0f} |"
        )
    
    lines.extend([
        "",
        "## Detailed Results",
        "",
    ])
    
    for cat in df['category'].unique():
        lines.append(f"### {cat.replace('_', ' ').title()}")
        lines.append("")
        lines.append("| Benchmark | N | Time (s) | Memory (MB) | Throughput | Status |")
        lines.append("|-----------|---|----------|-------------|------------|--------|")
        
        cat_df = df[df['category'] == cat]
        for _, row in cat_df.iterrows():
            status = "✓" if row['success'] else "✗"
            lines.append(
                f"| {row['name']} | {row['n_observations']:,} | "
                f"{row['execution_time']:.3f} | {row['memory_peak_mb']:.1f} | "
                f"{row['throughput']:.0f} | {status} |"
            )
        lines.append("")
    
    lines.extend([
        "## Optimization Recommendations",
        "",
        "Based on benchmark results:",
        "",
    ])
    
    # Add recommendations based on results
    slow_benchmarks = df[df['execution_time'] > 1.0]
    if len(slow_benchmarks) > 0:
        lines.append("### Slow Operations (>1s)")
        for _, row in slow_benchmarks.iterrows():
            lines.append(f"- **{row['name']}**: {row['execution_time']:.2f}s")
        lines.append("")
    
    memory_heavy = df[df['memory_peak_mb'] > 100]
    if len(memory_heavy) > 0:
        lines.append("### Memory-Intensive Operations (>100MB)")
        for _, row in memory_heavy.iterrows():
            lines.append(f"- **{row['name']}**: {row['memory_peak_mb']:.0f}MB")
        lines.append("")
    
    lines.extend([
        "---",
        "",
        "*Generated by KRL Benchmark Suite*",
    ])
    
    return '\n'.join(lines)


if __name__ == '__main__':
    run_all_benchmarks()
