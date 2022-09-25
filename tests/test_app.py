from app import app


app.config['TESTING'] = True
web = app.test_client()

def test_index():
    rv = web.get('/', follow_redirects=True)
    assert rv.status_code == 404

    rv = web.get('/hello', follow_redirects=True)
    assert rv.status_code == 200
    assert b"Fill Out This Form, por favor" in rv.data

    data = {'name': 'Zed', 'greet': 'Hola'}
    rv = web.post('/hello', follow_redirects=True, data=data)
    assert b"Zed" in rv.data
    assert b"Hola" in rv.data