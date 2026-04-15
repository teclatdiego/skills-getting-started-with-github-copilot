from urllib.parse import quote

def test_root_redirect(client):
    response = client.get("/")
    assert response.status_code == 200  # Assuming it serves the HTML directly
    assert "Mergington High School" in response.text

def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success(client):
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/signup", data=email)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity}" == data["message"]

def test_signup_activity_not_found(client):
    activity = "NonExistent"
    response = client.post(f"/activities/{activity}/signup", data="test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_signup_already_signed_up(client):
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    # First signup
    client.post(f"/activities/{activity}/signup", data=email)
    # Second attempt
    response = client.post(f"/activities/{activity}/signup", data=email)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"

def test_unregister_success(client):
    activity = "Chess Club"
    email = "unregister@mergington.edu"
    # First signup
    client.post(f"/activities/{activity}/signup", data=email)
    # Then unregister
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Unregistered {email} from {activity}" == data["message"]

def test_unregister_activity_not_found(client):
    activity = "NonExistent"
    response = client.delete(f"/activities/{activity}/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_unregister_not_signed_up(client):
    activity = "Chess Club"
    email = "notsigned@mergington.edu"
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not signed up for this activity"