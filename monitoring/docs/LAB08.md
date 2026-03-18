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

# Task 2

### All targets up

![targets](/monitoring/docs/L8t2_targets_up.png)

### Successful query

![query](/monitoring/docs/L8t2_query.png)

### Prometheus config

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

# Storage retention (Prometheus 3.x config-based retention)
storage:
  tsdb:
    retention:
      time: 15d
      size: 10GB

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'app'
    static_configs:
      - targets: ['devops-infoservice:5000']

  - job_name: 'loki'
    static_configs:
      - targets: ['loki:3100']

  - job_name: 'grafana'
    static_configs:
      - targets: ['grafana:3000']
```
