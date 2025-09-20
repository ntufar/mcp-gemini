# MCP Server Performance Benchmarking

This document outlines how to run performance benchmarks for the MCP Server and interpret the results.

## Running Performance Tests

Performance tests are implemented using `pytest-benchmark` and are located in `tests/performance/test_api_performance.py`.

### Prerequisites

- Python 3.9+
- `pip` (Python package installer)
- All project dependencies installed (including `pytest-benchmark`).

### Steps

1.  **Install Dependencies:**
    Ensure all dependencies, including `pytest-benchmark`, are installed:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the MCP Server:**
    The performance tests require the MCP Server to be running. Start the server in a separate terminal:
    ```bash
    uvicorn src.main:app --host 127.0.0.1 --port 8000
    ```

3.  **Execute Performance Tests:**
    Navigate to the project root directory and run `pytest` with the `--benchmark-histogram` and `--benchmark-json` flags to generate detailed results:
    ```bash
    pytest tests/performance/test_api_performance.py --benchmark-histogram --benchmark-json=benchmark_results.json
    ```
    - `--benchmark-histogram`: Generates a histogram of the test run times.
    - `--benchmark-json=benchmark_results.json`: Saves the benchmark results to a JSON file.

## Interpreting Results

`pytest-benchmark` provides various metrics to assess performance:

-   **Min/Max/Mean/Median**: These statistics give you an idea of the range and central tendency of your function's execution time.
-   **StdDev**: Standard deviation indicates the variability of the execution times. A lower standard deviation means more consistent performance.
-   **Rounds/Iterations**: The number of times the function was executed and measured.
-   **OPS (Operations Per Second)**: How many times your function can be executed per second. Higher is better.

For detailed analysis, you can use the generated `benchmark_results.json` file with `pytest-benchmark`'s command-line tools or integrate it into a CI/CD pipeline for trend analysis.

### Example Output (Console)

```text
-------------------------------- benchmark: 2 tests --------------------------------
Name (time in us)          Min      Max     Mean   StdDev    Rounds  Iterations
----------------------------------------------------------------------------------
test_list_directory_performance
                       100.000  200.000  150.000   20.000       100         10
test_read_file_performance
                       200.000  300.000  250.000   30.000       100         10
----------------------------------------------------------------------------------
```

## Future Performance Considerations

-   **Load Testing**: For simulating real-world traffic and identifying bottlenecks under heavy load, consider tools like Locust or JMeter.
-   **Profiling**: Use Python's built-in `cProfile` or external tools like `py-spy` to identify performance hotspots in your code.
-   **Monitoring**: Integrate with monitoring solutions (e.g., Prometheus, Grafana) to track performance metrics over time in production environments.
