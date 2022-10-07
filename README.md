# Save Text Receipt To Database API's

Extract data from text file receipt and save into database. Also find the blocks in text receipt.\
Every block is separated with Empty line or line with dashes(-). Also find position of every block.

### `Run Application With Docker`

I write docker-compose.yml file. You can run it. Also i use postgresql database.\
But you need to set database default which youn want to run in settings file.

```
docker compose up --build
docker compose down
```

### `Run Application On Terminal`

Using python 3.10.6 version.\
All commands for MACOS.\
Create virtual environment and activate environment.

'''
python3 -m venv venv
source venv/bin/activate
'''

Install requirements.

'''
pip3 install -r requirements.txt
'''

migrate and Run application with sqlite3

'''
python3 manage.py migrate
python3 manage.py runserver
'''

Application is running successfully on your Mac.
