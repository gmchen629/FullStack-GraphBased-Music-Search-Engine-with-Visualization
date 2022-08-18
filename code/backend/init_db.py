import sqlite3
from datetime import timedelta
from sqlite3 import Error
from audio_feature_extractor import find_song
import csv

db_name = "music_database"
# create table + insert data from data/*.csv files
def init_db():
    connection = connect_db()
    create_table("music_data", connection)
    create_table("music_recommend", connection)
    create_table("user_feedback", connection)
    create_table("movie_feedback", connection)
    create_table("music_feedback", connection)
    insert_data_from_csv("music_data", "data/music_data.csv", connection)
    insert_data_from_csv("music_recommend", "data/r_result.csv", connection)

    return connection

# return sqlite handler for db_name
def connect_db():
    try:
        connection = sqlite3.connect("music_database")
        connection.row_factory = sqlite3.Row
        print("Connected database successfully!")
        return connection
    except Error as e:
        print("Error occurred: " + str(e))

# create table + insert data from data/*.csv files
def create_table(tbname, connection):
    try:
        drop_sql = "DROP TABLE IF EXISTS " + tbname
        connection.execute(drop_sql)
        if (tbname == "music_data"):
            insert_sql = "create table music_data (music_id text, music_name text, release_year integer, artists text,  danceability float, duration integer, energy float, liveness float, popularity integer);"
            connection.execute(insert_sql)
        elif (tbname == "music_recommend"):
            insert_sql = "create table music_recommend (music_id text, music_name text, release_year integer, r_top5 text);"
            connection.execute(insert_sql)
        elif tbname == "user_feedback":
            insert_sql = "create table user_feedback (user_feedback integer)"
            connection.execute(insert_sql)
        elif tbname == "music_feedback":
            insert_sql = "create table music_feedback (music_feedback integer)"
            connection.execute(insert_sql)
        connection.commit()

    except Error as e:
        print("Error occurred: " + str(e))
        return
    print("Create {} table successfully!".format(tbname))

def insert_data_from_csv(tbname, file_path, connection):
    # insert data
    try:
        with open(file_path, encoding = 'utf8') as f:
            file = csv.reader(f)
            for data in list(file)[1:]:
                if (tbname == "music_data"):
                    connection.execute("insert into music_data values(?,?,?,?,?,?,?,?,?)",(data[8],data[14],data[1],data[3],float(data[4]) * 100, data[5],float(data[6]) * 100, float(data[11]) * 100, data[15]))
                if (tbname == "music_recommend"):
                    connection.execute("insert into music_recommend values(?,?,?,?)",(data[0],data[1],data[2],data[3]))
        connection.commit()
    except Error as e:
        print("Error occurred: " + str(e))
        return
    print("Insert data from {} successfully!".format(file_path))

def insert_data_from_api(tbname, data, connection):
    # insert data
    try:
        if (tbname == "music_data"):
            artist_name = "['" + data['artist_name'] + "']"
            connection.execute("insert into music_data values(?,?,?,?,?,?,?,?,?)",(data['id'],data['name'],data['year'],artist_name,float(data['danceability']), data['duration_ms'], float(data['energy']), float(data['liveness']), data['popularity']))
            print("insert new data into db from api successfully!")
            print(data)
            connection.commit()
            return
    except Error as e:
        print("Error occurred: " + str(e))
        return

def query_recommend_name_list(music_name, music_year = None):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        if music_year != None:
            query = f"select * from music_recommend where music_name = '{music_name}' and release_year = {music_year} order by release_year desc limit 1;"
        else:
            query = f"select * from music_recommend where music_name = '{music_name}' order by release_year desc limit 1;"
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("can't find from db")
            return None
        else:
            print('get from db')
            id_lists_db = rows[0]['r_top5'][1:-1].split(",")
            return query_recommend_lists(id_lists_db, music_name)


    except Error as e:
        print("Error occurred: " + str(e))

def query_recommend_lists(lists_from_db, music_name):
    temp_list = []
    for i in range(len(lists_from_db)):
        temp_list.append(lists_from_db[i][1:-1])

    recommend_res = {"music_name" : music_name, 'children': []}
    for r_m in temp_list:
        f = 0
        l = len(r_m) - 1
        while f < l :
            if r_m[f] != ' ' and r_m[f] != "'" and r_m[l] != ' ' and r_m[l] != "'":
                break
            elif r_m[f] == ' ' or r_m[f] == "'":
                f += 1
            elif r_m[l] == ' ' or r_m[l] == "'":
                l -= 1
        recommend_res['children'].append(query_music_name(r_m[f:l+1]))

    print("recommendation name list:")
    print(recommend_res)
    return recommend_res

def query_music_info(music_name, music_year = None):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        if (music_year != None):
            query = f"select * from music_data where music_name = '{music_name}' and release_year = {music_year} order by popularity desc, release_year desc limit 1;"
        else:
            query = f"select * from music_data where music_name = '{music_name}' order by popularity desc, release_year desc limit 1;"

        cursor.execute(query)
        rows = cursor.fetchall()

        # find new data from api
        if len(rows) == 0:
            print("can't find from db")
            print("search from api..")
            new_data = find_song(music_name, music_year)
            if (new_data == None):
                return
            print("insert new data into db...")
            insert_data_from_api("music_data", new_data, connection)
            duration_time = timedelta(milliseconds=new_data['duration_ms'])
            res = {'music_name' : str(new_data['name'])}

            res['children']= [
                {
                    "source": str(new_data['name']),
                    "target": "Artist",
                    "value": new_data['artist_name']
                }, {
                    "source": str(new_data['name']),
                    "target": "Year",
                    "value": str(new_data['year'])
                }, {
                    "source": str(new_data['name']),
                    "target": "Danceability",
                    "value": str(float("{:.2f}".format(new_data['danceability'])))
                }, {
                    "source": str(new_data['name']),
                    "target": "Energy",
                    "value": str(float("{:.2f}".format(new_data['energy'])))
                }, {
                    "source": str(new_data['name']),
                    "target": "Liveness",
                    "value": str(float("{:.2f}".format(new_data['liveness'])))
                }, {
                    "source": str(new_data['name']),
                    "target": "Popularity",
                    "value": str(float("{:.2f}".format(new_data['popularity'])))
                }, {
                    "source": str(new_data['name']),
                    "target": "Duration",
                    "value": str(duration_time)[2:7]

                }, {
                    "source": str(new_data['name']),
                    "target": "Click to Try",
                    "value": new_data['id']
                }]
            return res

        else:
            print('get from db')
            artist_name_str = ""
            for i in list(list(rows[0]['artists'])):
                check_list = ['[', "'", ']']
                if i not in check_list:
                    artist_name_str += i
            duration_time = timedelta(milliseconds=rows[0]['duration'])
            res = {'music_name' : rows[0]['music_name']}

            res['children']= [
                {
                    "source": rows[0]['music_name'],
                    "target": "Artist",
                    "value": artist_name_str
                }, {
                    "source": rows[0]['music_name'],
                    "target": "Year",
                    "value": str(rows[0]['release_year'])
                }, {
                    "source": rows[0]['music_name'],
                    "target": "Danceability",
                    "value": str(float("{:.2f}".format(rows[0]['danceability'])))
                }, {
                    "source": rows[0]['music_name'],
                    "target": "Energy",
                    "value": str(float("{:.2f}".format(rows[0]['energy'])))
                }, {
                    "source": rows[0]['music_name'],
                    "target": "Liveness",
                    "value": str(float("{:.2f}".format(rows[0]['liveness'])))
                }, {
                    "source": rows[0]['music_name'],
                    "target": "Popularity",
                    "value": str(float("{:.2f}".format(rows[0]['popularity'])))
                }, {
                    "source": rows[0]['music_name'],
                    "target": "Duration",
                    "value": str(duration_time)[2:7]

                }, {
                    "source": rows[0]['music_name'],
                    "target": "Click to Try",
                    "value": rows[0]['music_id']
                }]
            print(res)
            return res

    except Error as e:
        print("Error occurred: " + str(e))

# return name of music with id==music_id
def query_music_name(music_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        query = f"select music_name from music_data where music_id = '{music_id}' order by popularity desc, release_year desc limit 1;"
        cursor.execute(query)
        rows = cursor.fetchall()
        print("Get music name: " + rows[0]['music_name'])
        if len(rows) != 1:
            print(f"WARN: query_music_name: found {len(rows)} music_id for music_id = \'{music_id}\'")
            return None
        return {'name' : rows[0]['music_name']}
    except Error as e:
        print("Error occurred: " + str(e))
        return

def query_music_id(connection, music_name):
    try:
        cursor = connection.cursor()
        query = f"select music_id from music_data where music_name = '{music_name}' order by popularity desc, release_year desc desc limit 1;"
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) != 1:
            print(f"WARN: query_music_id: found {len(rows)} music_id for music_name = \'{music_name}\'")
            for r in rows:
                title = r['music_id']
                print(f'\t{title}')
            return None
        return rows[0]['music_id']
    except Error as e:
        print("Error occurred: " + str(e))
        return

def insert_new_feedback(tbname, feedback_data: list):
    try:
        connection = sqlite3.connect('music_database')
        cursor = connection.cursor()
        for feedback in feedback_data:
            if tbname == "user_feedback":
                connection.execute("insert into user_feedback values(?)",(str(feedback),))
            elif tbname == "music_feedback":
                connection.execute("insert into music_feedback values(?)",(str(feedback),))
            connection.commit()
    except Error as e:
        print("Error occurred: " + str(e))
        return
    print("Insert new {} successfully!".format(tbname))


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



if __name__== '__main__':
    try:
        db = init_db()
        print(query_music_id(db, "Lemon Tree"))
        query_music_info("Lemon Tree")
        # query_recommend_name_list('Le')
        # res = query_recommend_name_list(db, 'Attention', 2018)
        # new_data = find_song(res['children'][0]['name'])
        # insert_data_from_api("music_data", new_data,  db)
    except Error as e:
        print("Error occurred: " + str(e))
