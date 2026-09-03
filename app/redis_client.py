import redis 

redis_client = redis.Redis(
  host="localhost",
  port=6379,
  db = 0,
  decode_responses=True
)


# Первый запрос
# сервер -> база данных (медленно) -> Сохранили в Redis -> Ответ
# повторный запрос
# Сервер -> Redis -> Ответ 

