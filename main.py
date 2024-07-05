import requests
from bs4 import BeautifulSoup
import json          # Для обработки полученных результатов
import time          # Для задержки между запросами
import os            # Для работы с файлами
import pandas as pd  # Для формирования датафрейма с результатами
import sqlite3

def get_vacancies():
    hh_req = requests.get('https://api.hh.ru/vacancies')
    return hh_req.json() if hh_req.status_code == 200 else print(f'Error {hh_req.status_code}')

def vac2db(vacancies):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    
    ''')

    connection.close()
