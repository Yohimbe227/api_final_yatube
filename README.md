<h1 align="center">Hi there, this is <a  target="_blank">API_Yatube</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">The best social network in the world!</h3>

### Для чего мне это понадобилось

Тренировка навыков и применение знаний по разработке API сервиса.

### Как запустить проект

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
