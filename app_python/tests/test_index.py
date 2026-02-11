import app
import re


"""
{
  "endpoints": [
    {
      "description": "Service information",
      "method": "GET",
      "path": "/"
    },
    {
      "description": "Health check",
      "method": "GET",
      "path": "/health"
    }
  ],
  "request": {
    "client_ip": "127.0.0.1",
    "method": "GET",
    "path": "/",
    "user_agent": "curl/8.18.0"
  },
  "runtime": {
    "current_time": "2026-01-26T15:56:22.043+03:00",
    "timezone": "MSK",
    "uptime_human": "0 hours, 2 minutes",
    "uptime_seconds": 160
  },
  "service": {
    "description": "DevOps course info service",
    "framework": "Flask",
    "name": "devops-info-service",
    "version": "1.0.0"
  },
  "system": {
    "architecture": "x86_64",
    "cpu_count": 16,
    "hostname": "timur-ficus",
    "platform": "Linux",
    "platform_version": "#1 SMP PREEMPT_DYNAMIC Sun, 18 Jan 2026 00:34:07 +0000",
    "python_version": "3.14.2"
  }
}
"""


def validate_endpoints(endpts):
    assert isinstance(endpts, list)
    assert len(endpts) >= 2
    assert all(isinstance(i, dict) for i in endpts)
    assert all(set(i.keys()).issuperset({"description", "method", "path"}) for i in endpts)
    locmethod = {i['path']: i['method'] for i in endpts}
    assert '/' in locmethod
    assert '/health' in locmethod
    assert locmethod['/'] == 'GET'
    assert locmethod['/health'] == 'GET'


def validate_request(req):
    assert isinstance(req, dict)
    assert set(req.keys()) == {"client_ip", "method", "path", "user_agent"}
    assert all(isinstance(i, str) for i in req.values())
    assert req['method'] == 'GET'
    assert req['path'] == '/'


def validate_runtime(rt):
    assert isinstance(rt, dict)
    assert set(rt.keys()) == {"current_time", "timezone", "uptime_human", "uptime_seconds"}
    assert re.fullmatch(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.\d\d\d((\+|-)\d\d:\d\d)?', rt['current_time'])
    assert isinstance(rt['timezone'], str)
    assert isinstance(rt['uptime_human'], str)
    assert isinstance(rt['uptime_seconds'], int)
    assert rt['uptime_seconds'] >= 0


def validate_service(desc):
    assert isinstance(desc, dict)
    assert set(desc.keys()) == {"description", "framework", "name", "version"}
    assert all(isinstance(v, str) for v in desc.values())


def validate_system(sysinfo):
    assert isinstance(sysinfo, dict)
    assert set(sysinfo.keys()) == {
        "architecture",
        "cpu_count",
        "hostname",
        "platform",
        "platform_version",
        "python_version"
    }
    assert all((isinstance(v, str)) ^ (k == 'cpu_count') for k, v in sysinfo.items())
    assert isinstance(sysinfo['cpu_count'], int)
    assert sysinfo['cpu_count'] > 0


def test_index():
    app.app.testing = True
    with app.app.test_client() as client:
        for _ in range(3):
            response = client.get('/')
            assert response.status_code == 200
            assert response.is_json
            d = response.json
            assert isinstance(d, dict)
            assert set(d.keys()) == {"endpoints", "request", "runtime", "service", "system"}
            validate_endpoints(d["endpoints"])
            validate_request(d["request"])
            validate_runtime(d["runtime"])
            validate_service(d["service"])
            validate_system(d["system"])
