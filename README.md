# Реализация финального задания по социальной сети Yatube

добавлены подписки на авторов, картинки к постам, комментарии, кастомные страницы ошибок,
комментарии, оптимизация

### Для реализации использовались следующие технологии:

- Django REST framework
- Pillow
 
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Egor-junior/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
