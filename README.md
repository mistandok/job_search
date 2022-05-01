#### Установка проекта

- установить версию python 3.10
- создать виртуальное окружение 
```shell script
python3.10 -m venv venv
```
- активировать виртуальное окружение
```shell script
source venv/bin/activate
```
- установить зависимости
```shell script
pip install -r requirements.txt
```
- запустить тестовый django-проект
```shell script
./manage.py runserver
```
- открыть в браузере http://127.0.0.1:8000 

#### Тестовые пользователи (логин/пароль:):

- mistandok/rockwood (есть компания, есть вакансия с откликами от других пользователей)
- vacancy_owner/rockwood (есть компания, есть несколько вакансий без откликов)
- empty/rockwood (пустой пользователь без компаний и без вакансий)
