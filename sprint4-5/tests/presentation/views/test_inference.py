import pytest


def test_inference_should_return_ok(client, input_data):
    # passa apenas se o bucket estiver público ou se tiver o devido acesso
    response = client.post("api/v1/inference", json=input_data)

    assert response.status_code == 200
    assert "result" in response.json()
    assert response.json()["result"] in [1, 2, 3]


@pytest.mark.usefixtures("mock_load_model")
def test_inference_should_return_internal_server_error(client, input_data):
    response = client.post("api/v1/inference", json=input_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "Erro ao carregar o modelo do S3."}
