import pytest


@pytest.mark.asyncio
async def test_get_empty_tasks(client, auth_headers):
  response = await client.get("/tasks", headers=auth_headers)

  assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_task(client, auth_headers):
  response = await client.post(
    "/tasks",
    json={
      "title": "Тестовая задача",
      "description": "Описание"
    },
    headers=auth_headers
  )

  assert response.status_code == 201
  data = response.json()
  assert data["title"] == "Тестовая задача"
  assert data["description"] == "Описание"

@pytest.mark.asyncio 
async def test_get_nonexistent_endpoint(client, auth_headers):
  response = await client.get("/tasks/999", headers=auth_headers)

  assert response.status_code == 405
  assert response.json()["detail"] == "Method Not Allowed"