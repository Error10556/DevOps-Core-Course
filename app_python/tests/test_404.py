import flask
import app


def test_404():
    def assert_404(resp: flask.TestResponse, codes: set[int] | None = None):
        if codes is None:
            assert resp.status_code == 404
        else:
            assert resp.status_code in codes

    app.app.testing = True
    with app.app.test_client() as client:
        assert_404(client.get('/health/'))
        assert_404(client.get('/sdjc39042/sdcs/dcewcmscd/'))
        assert_404(client.get('/../../../../../../../etc/shadow'), {403, 404})
