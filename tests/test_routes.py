def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest Functional Fitness System" in response.data