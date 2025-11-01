```bash
cp .env.example .env
docker-compose up -d --build
```

- Swagger: http://localhost:8000/docs  
- Главная: http://localhost:8000/

- `alice-key`
- `bob-key`
- `carol-key`

Пример запроса:
```
curl -H "api-key: alice-key" http://localhost:8000/api/tweets
```

- [x] Создать/удалить твит
- [x] Лайк/анлайк твита
- [x] Подписка/отписка
- [x] Лента (по подпискам, сортировка по популярности)
- [x] Медиа: загрузка, хранение на диске, отдача по `/api/media/{id}`
- [x] Документация Swagger из коробки
- [x] Docker Compose + PostgreSQL, данные сохраняются между рестартами
- [x] Unit-тесты (pytest); конфиги для ruff + mypy

- Для удобства сидирование демо-данных выполняется автоматически при старте (`SEED_ON_STARTUP=true`).
- Медиа-файлы складываются в `media/` (том Docker).

- Пагинация ленты и твитов
- Асинхронный стек (async SQLAlchemy + asyncpg)
- Nginx/SPA билд фронтенда
