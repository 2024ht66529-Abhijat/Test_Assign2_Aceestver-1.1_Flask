def test_calorie_calculation_fl(client):
    response = client.post(
        "/",
        data={"weight": "70", "program": "Fat Loss (FL)"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Estimated Calories" in response.data