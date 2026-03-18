# Task 1

### Screenshot of `/metrics`

![metrics](/monitoring/docs/L8t1_metrics_endpoint.png)

### Definition of metrics

```python
# ...
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# ...

class PrometheusStats:
    http_requests_total: Counter
    http_request_duration_seconds: Histogram
    http_requests_in_progress: Gauge
    system_info_duration_seconds: Histogram

    def __init__(self):
        self.http_requests_total = Counter(
            'http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status']
        )
        self.http_request_duration_seconds = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration',
            ['method', 'endpoint']
        )
        self.http_requests_in_progress = Gauge(
            'http_requests_in_progress',
            'HTTP requests currently being processed'
        )
        self.system_info_duration_seconds = Histogram(
            'system_info_duration_seconds',
            'System stats collection time'
        )


prometheus = PrometheusStats()
# ...
```

### Explanation of metrics choice

The HTTP-related metrics in the declaration above are required by the lab.

The only logic-related metric that made sense in the context of the app is the system info query time, so I implemented
it similarly to `http_request_duration_seconds`, as a Histogram. I could subdivide it into queries to different parts of
the system, but the metric reports very low time consumption already, so I think there is no point in that.
