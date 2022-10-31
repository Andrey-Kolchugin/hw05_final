# hw05_final
Проект мини-соцсети 

Позволяет быстро развернуть и настроить Backend со следующим функционалом:

* Публикация и просмотр постов
* Публикация и просмотр комментариев к постам
* Регистрация и авторизация пользователей
* Подписка на избранных пользователей
* Администрирование через django-admin

### Версия языка

Проект создан на python 3.9.1

### Локальная установка и запуск проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Andrey-Kolchugin/hw05_final.git
```

```
cd hw05_final
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Создать суперюзера:
```
python3 manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```
