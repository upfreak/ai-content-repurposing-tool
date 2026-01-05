import os
from dotenv import load_dotenv
load_dotenv()
from urllib.parse import unquote
import psycopg2

import os as _os
from dotenv import dotenv_values
print('cwd:', _os.getcwd())
print('.env exists:', _os.path.exists('.env'))
print('env file contents:')
print(open('.env','r',encoding='utf8').read())
print('dotenv_values parse:')
print(dotenv_values('.env'))

url = os.getenv('DATABASE_URL')
print('DATABASE_URL from os.environ:', url)
print('DATABASE_URL from dotenv_values:', dotenv_values('.env').get('DATABASE_URL'))
try:
    # psycopg2 can accept a DSN or keyword args
    conn = psycopg2.connect(dsn=url)
    print('Connected successfully')
    conn.close()
except Exception as e:
    print('Connection failed:', repr(e))
    # try parsing URL
    try:
        from sqlalchemy.engine.url import make_url
        u = make_url(url)
        print('Parsed password:', u.password)
    except Exception:
        pass
