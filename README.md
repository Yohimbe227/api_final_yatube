# Хайлоу, это API_Yatube<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
The best social network in the world!  
_(ну может слегка преувеличил)_

_**Основной стэк**_:  
![Python](https://img.shields.io/badge/python-3.7-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-3.1-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-ff1709?style=for-the-badge&logo=aiogram&logoColor=white&color=ff1709&labelColor=gray)

_**Мы наконец ушли от страшненьких Django templates!
Теперь можно попрактиковаться в разработке своего API посредством
Django REST fraemwork.**_

### Установка/Installation
Для windows python3 замените на python. Клонировать репозиторий и перейти в него
в командной строке:
```
git clone https://github.com/Yohimbe227/api_final_yatube
```
```
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение: для linux
```
python3 -m venv env
```
- Если у вас Linux/macOS
  ```
  source env/bin/activate
  ```
- Если у вас windows
  ```
  source env/scripts/activate
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
```
