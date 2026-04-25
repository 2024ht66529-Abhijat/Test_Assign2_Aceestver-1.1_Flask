def test_home_route_status(client):
    response = client.get("/")
    assert response.status_code == 200