"""
DevOps Info Service
Main application module
"""
from datetime import datetime, timezone
from flask import Flask, jsonify, request
import logging
import os
import platform
import socket
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

logging.basicConfig(
    level=logging.INFO if not DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
app = Flask(__name__)


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
        'uptime_human':   f"{hours} hour{word_plural(hours)}, {minutes} minute{word_plural(minutes)}",
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


@app.route('/')
def index():
    logger.debug(f'Request: {request.method} {request.path}')
    """Main endpoint - service and system information."""
    return jsonify({
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
            {"path": "/"      , "method": "GET", "description": "Service information"},
            {"path": "/health", "method": "GET", "description": "Health check"}
        ]
    })


@app.route('/health')
def health():
    logger.debug(f'Request: {request.method} {request.path}')
    return jsonify({
        'status':         'healthy',
        'timestamp':      datetime.now(timezone.utc).isoformat(),
        'uptime_seconds': get_uptime()['uptime_seconds']
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error':   'Not Found',
        'message': 'Endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error':   'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


START_TIME = datetime.now(timezone.utc)
logger.info('Application starting...')
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
