def test_register_and_login(app):
    client = app.test_client()

    # register
    resp = client.post('/auth/register', data={'name': 'Tester', 'email': 'tester@example.com', 'password': 'p'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Conta criada com sucesso' in resp.data

    # now login
    resp2 = client.post('/auth/login', data={'email': 'tester@example.com', 'password': 'p'}, follow_redirects=True)
    assert resp2.status_code == 200
    assert b'Login realizado com sucesso' in resp2.data


def test_login_missing_or_wrong_password(app):
    client = app.test_client()

    # missing password
    resp = client.post('/auth/login', data={'email': 'noone@example.com'}, follow_redirects=True)
    assert b'Preencha e-mail e senha' in resp.data

    # wrong password for existing user
    with app.app_context():
        from forca_app.extensions import db
        from forca_app.models.user import User
        u = User(name='U', email='u@example.com')
        u.set_password('right')
        db.session.add(u)
        db.session.commit()

    resp2 = client.post('/auth/login', data={'email': 'u@example.com', 'password': 'wrong'}, follow_redirects=True)
    assert b'E-mail ou senha incorretos' in resp2.data
