import app
import re


def test_health():
    app.app.testing = True
    with app.app.test_client() as client:
        for _ in range(3):
            response = client.get('/health')
            assert response.status_code == 200
            assert response.is_json
            d = response.json
            assert isinstance(d, dict)
            assert set(d.keys()) == {"status", "timestamp", "uptime_seconds"}
            assert d['status'] == 'healthy'
            assert isinstance(d['timestamp'], str)
            assert isinstance(d['uptime_seconds'], int)
