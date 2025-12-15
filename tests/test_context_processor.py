from forca_app.models.user import User


def test_profile_renders_with_session_user(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['user_id'] = 99999
        sess['user_name'] = 'Session User'
        sess['user_email'] = 'session@example.com'
        sess['user_level'] = 3
        sess['user_points'] = 120

    resp = client.get('/user/profile')
    assert resp.status_code == 200
    assert b'Session User' in resp.data


def test_profile_renders_with_db_user(app):
    with app.app_context():
        u = User(name='DB User', email='db@example.com')
        u.set_password('test')
        from forca_app.extensions import db
        db.session.add(u)
        db.session.commit()
        user_id = u.id

    client = app.test_client()
    with client.session_transaction() as sess:
        sess['user_id'] = user_id

    resp = client.get('/user/profile')
    assert resp.status_code == 200
    assert b'DB User' in resp.data
