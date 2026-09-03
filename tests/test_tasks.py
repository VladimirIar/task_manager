import pytest

# тут и была самая главная ошибка. clean_db передавался после auth_headers
# а следовательно, пользователь удалялся из таблицы, что и приводило к ошибке 404
# теперь тест работает корректно, как и задумывалось )
@pytest.mark.asyncio
async def test_get_empty_tasks(client, clean_db, auth_headers):
  response = await client.get("/tasks", headers=auth_headers)

  assert response.status_code == 200
  assert response.json() == []


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