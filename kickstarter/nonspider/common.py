import sqlite3
import string

def connect_db():
    connection = sqlite3.connect('kickstarter.sqlite3')
    connection.execute('CREATE TABLE IF NOT EXISTS rawnames (value TEXT PRIMARY KEY)')
    connection.execute('CREATE TABLE IF NOT EXISTS names (value TEXT PRIMARY KEY)')
    connection.execute('CREATE TABLE IF NOT EXISTS match_names (project_id INT PRIMARY KEY, value TEXT)')
    connection.execute('CREATE TABLE IF NOT EXISTS match_epic (project_id INT PRIMARY KEY, value TEXT)')
    connection.execute('CREATE TABLE IF NOT EXISTS match_zombie (project_id INT PRIMARY KEY, value TEXT)')
    connection.execute('CREATE TABLE IF NOT EXISTS match_genre (project_id INT PRIMARY KEY, value TEXT)')
    connection.execute('CREATE TABLE IF NOT EXISTS match_roguelike (project_id INT PRIMARY KEY, value TEXT)')
    connection.execute(
    '''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT UNIQUE,
        goal INTEGER,
        currency TEXT,
        date INTEGER,
        rawtext TEXT,
        web TEXT,
        match_genre_count INTEGER DEFAULT 0,
        match_names_count INTEGER DEFAULT 0,
        match_roguelike_count INTEGER DEFAULT 0,
        match_epic_count INTEGER DEFAULT 0,
        match_zombie_count INTEGER DEFAULT 0
    )
    ''')

    return connection

unicode_punctuation_map = dict((ord(char), None) for char in string.punctuation)
def strip_punctuation(s):
    return s.translate(unicode_punctuation_map)

