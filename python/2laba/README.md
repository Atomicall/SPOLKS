# СПОЛКС - Python
Тут лежит 3 лабы.

## Setup
Все манипуляции производятся в терминале.

1. Склонируй репозиторий
```
git clone <repo-url|ssh>
```

2. Зайди в репозиторий командой:
```
cd ./<repo-name>
```

3. Запусти в командной строке команду для создания виртуальной среды Python в текущей директории:
```
python -m venv venv
```

4. Активируй среду командой:

*Windows:*
```
./venv/Scripts/activate
```
*Linux*
```
source ./venv/bin/activate
```

5. Установи зависимости проекта:
```
pip install -r requirements.txt
```

6. Настрой PYTHONPATH для того, чтобы Python видел модули проекта:
*Windows*
```
set PYTHONPATH=<path-to-your-project>;<path-to-your-project>/shared;<path-to-your-project>/client;<path-to-your-project>/server;%PYTHONPATH%;
```
Или же через настройку ручную в панеле по управлению переменными среды.

*Linux*
```
export PYTHONPATH="<path-to-your-project>:<path-to-your-project>/shared:<path-to-your-project>/client:<path-to-your-project>/server":$PYTHONPATH
```

7. Можно теперь запускать приложение:

*Client - зайти в папку **client***
```
python start_client.py
```
*Server - зайти в папку **server***
```
python start_server.py
```