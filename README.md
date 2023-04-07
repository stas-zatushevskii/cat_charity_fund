Описание проекта QRKot:
    Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

Как запустить проект:

    Клонировать репозиторий и перейти в него в командной строке:

        git clone https://github.com/stas-zatushevskii/cat_charity_fund

    Cоздать и активировать виртуальное окружение:

        python / python3  -m venv env
        source env/bin/activate

    Установить зависимости из файла requirements.txt:

        python3 -m pip install --upgrade pip
        pip install -r requirements.txt

    Выполнить миграции:

        alembic revision --autogenerate -m "Name" -- создание миграции 
        alembic upgrade head  -- применение всех созданных миграций

    Запуск проекта:

        uvicorn main:app --reload 