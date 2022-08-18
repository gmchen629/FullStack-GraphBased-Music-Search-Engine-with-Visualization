import sqlite3
from sqlite3 import Error

def query_user_feedback():
    try:
        connection = sqlite3.connect('music_database')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        query = "select avg(user_feedback) as avg_user_feedback from " + "user_feedback"
        # print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        # print("Query executed successfully")
        return {
            'current_user_feedback': data[0]['avg_user_feedback']
        }
    except Error as e:
        print("Error occurred: " + str(e))
        return

def query_music_feedback():
    try:
        connection = sqlite3.connect('music_database')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        query = "select avg(music_feedback) as avg_music_feedback from " + "music_feedback"
        # print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        # print("Query executed successfully")
        return {
            'current_music_feedback': data[0]['avg_music_feedback'] * 10
        }
    except Error as e:
        print("Error occurred: " + str(e))
        return