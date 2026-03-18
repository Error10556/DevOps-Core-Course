"""
DevOps Info Service
Main application module
"""
import json
from flask import Flask, Response, jsonify, request
from datetime import datetime, timezone
import logging
import os
import platform
import socket
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from asyncio import Lock


HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


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


class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        rec = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if "http" in record.__dict__:
            rec["http"] = record.http
        return json.dumps(rec)


logger = logging.Logger(__name__, logging.INFO if not DEBUG else logging.DEBUG)
stderrhandler = logging.StreamHandler()
logger.addHandler(stderrhandler)
stderrhandler.setFormatter(JSONFormatter())
app: Flask = Flask(__name__)


def get_system_info() -> dict[str, str | int | None]:
    """Collect system information."""
    return {
        'hostname':         socket.gethostname(),
        'platform':         platform.system(),
        'platform_version': platform.version(),
        'architecture':     platform.machine(),
        'cpu_count':        os.cpu_count(),
        'python_version':   platform.python_version()
    }


def get_uptime() -> dict[str, int | str | None]:
    def word_plural(number: int) -> str:
        """Used for grammar when composing human-readable uptime (uptime_human)"""
        return 's' if number != 1 else ''

    now = datetime.now(timezone.utc)
    delta = now - START_TIME
    seconds = int(delta.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    loctime = now.astimezone()
    tzinfo = loctime.tzinfo
    if tzinfo is not None:
        tzinfo = str(tzinfo)
    return {
        'uptime_seconds': seconds,
        'uptime_human':   f"{hours} hour{word_plural(hours)}, " +
                          f"{minutes} minute{word_plural(minutes)}",
        'current_time':   loctime.isoformat(timespec='milliseconds'),
        'timezone':       tzinfo,
    }


def get_request_info() -> dict[str, str | None]:
    return {
        "client_ip":  request.remote_addr,
        "user_agent": request.headers.get('User-Agent'),
        "method":     request.method,
        "path":       request.path,
    }


def get_http_extra_info():
    return {
        "http": {
            "location": request.path,
            "method": request.method,
            "ip": request.remote_addr,
        }
    }


@app.route('/')
@prometheus.http_request_duration_seconds.labels('GET', '/').time()
@prometheus.http_requests_in_progress.track_inprogress()
def index():
    """Main endpoint - service and system information."""
    logger.debug(f'Request: {request.method} {request.path}', extra=get_http_extra_info())
    with prometheus.system_info_duration_seconds.time():
        response = {
            'service': {
                'name':        'devops-info-service',
                'version':     '1.0.0',
                'description': 'DevOps course info service',
                'framework':   'Flask'
            },
            'system':  get_system_info(),
            'runtime': get_uptime(),
            'request': get_request_info(),
            'endpoints': [
                {"path": "/",       "method": "GET", "description": "Service information"},
                {"path": "/health", "method": "GET", "description": "Health check"}
            ]
        }
    return jsonify(response)


@app.route('/health')
@prometheus.http_request_duration_seconds.labels('GET', '/health').time()
@prometheus.http_requests_in_progress.track_inprogress()
def health():
    logger.debug(f'Request: {request.method} {request.path}', extra=get_http_extra_info())
    return jsonify({
        'status':         'healthy',
        'timestamp':      datetime.now(timezone.utc).isoformat(),
        'uptime_seconds': get_uptime()['uptime_seconds']
    })


@app.route('/metrics')
@prometheus.http_request_duration_seconds.labels('GET', '/metrics').time()
@prometheus.http_requests_in_progress.track_inprogress()
def metrics():
    return generate_latest()


@app.errorhandler(404)
@prometheus.http_request_duration_seconds.time()
def notfound_handler(e):
    logger.info('A 404 Not Found error occured', extra=get_http_extra_info())
    return jsonify({
        'error':   'Not Found',
        'message': 'Endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    logger.error('Internal Server Error 500', extra=get_http_extra_info())
    return jsonify({
        'error':   'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


@app.after_request
def after_request(response: Response):
    prometheus.http_requests_total.labels(request.method, request.path, str(response.status_code)).inc()
    return response


START_TIME = datetime.now(timezone.utc)
logger.info('Application starting... Configured with log level=%s', 'DEBUG' if DEBUG else 'INFO')
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
