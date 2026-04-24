def test_ui_header_present(client):
    response = client.get("/")
    assert b"ACEest Functional Fitness" in response.data