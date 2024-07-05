import requests
from bs4 import BeautifulSoup
import json  # Для обработки полученных результатов
import time  # Для задержки между запросами
import os  # Для работы с файлами
import pandas as pd  # Для формирования датафрейма с результатами
import sqlite3


def get_vacancies():
    hh_req = requests.get('https://api.hh.ru/vacancies')
    return hh_req.json() if hh_req.status_code == 200 else print(f'Error {hh_req.status_code}')


def vac2db(vacancies):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vacancies (
    id INTEGER PRIMARY KEY,
    name TEXT,
    area TEXT,
    salary_from INTEGER,
    salary_to INTEGER,
    currency TEXT,
    schedule TEXT,
    experience INTEGER
    )
    ''')

    for vacancy in vacancies['items']:
        cursor.execute('''
        INSERT OR IGNORE INTO vacancies(id, name, area, salary_from, salary_to, currency, schedule, experience)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vacancy['id'],
            vacancy['name'],
            vacancy['area']['name'],
            vacancy['salary']['from']
            if vacancy['salary'] else None,
            vacancy['salary']['to']
            if vacancy['salary'] else None,
            vacancy['salary']['currency']
            if vacancy['salary'] else None,
            vacancy['schedule']['name']
            if vacancy['schedule'] else None,
            vacancy['experience']['name']
            if vacancy['experience'] else None
        ))
    connection.commit()
    connection.close()


def filter_vacancies(min_salary=None, max_salary=None, area=None, schedule=None, experience=None):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM vacancies WHERE 1=1'
    params = []
    if min_salary is not None:
        query += ' AND salary_from >= ?'
        params.append(min_salary)
    if max_salary is not None:
        query += ' AND salary_to <= ?'
        params.append(max_salary)
    if area is not None:
        query += ' AND area = ?'
        params.append(area)
    if schedule is not None:
        query += ' AND schedule = ?'
        params.append(schedule)
    if experience is not None:
        query += ' AND experience = ?'
        params.append(experience)
    cursor.execute(query, params)
    results = cursor.fetchall()
    connection.close()
    return results
