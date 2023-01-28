### API приложения для раскрашивания черно-белых изображений на основе [DeOldify](https://github.com/jantic/DeOldify).

#### 1. Команда проекта
 - Наймушин Алексей

#### 2. Основные используемые библиотеки
- [FastAPI](https://fastapi.tiangolo.com/)
- [DeOldify](https://github.com/jantic/DeOldify)
- [Torch](https://pytorch.org/)

#### 3. Запуск сервера
 - создаем и активируем локальное окружение;
 - устанавливаем необходимые пакеты из requirements.txt;
 - запускаем веб-сервер командой ```python -m uvicorn app:app -reload ``` (при запуске в [облаке Яндекс](https://cloud.yandex.ru/) дополнительно указываем параметр ```--host 0.0.0.0```

#### 4. Запуск в [docker](https://www.docker.com/)

Создаем контейнер
```
docker build . -t fastapiapp --progress=plain
```

Запускаем контейнер
```
docker run -p 8000:8000 fastapiapp
```