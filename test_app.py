from app import app

def test_home():
    response = app.test_client().get("/")
    assert response.status_code == 200

def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_notes():
    response = app.test_client().get("/notes")
    assert response.status_code == 200

def test_notes_etudiant():
    response = app.test_client().get("/notes?etudiant=Amina")
    assert response.status_code == 200

def test_health_version():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["version"] == "1.0"
