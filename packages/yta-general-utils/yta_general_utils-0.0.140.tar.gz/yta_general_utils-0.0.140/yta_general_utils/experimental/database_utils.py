"""
    TODO:

    This must be deleted, but I keep this code because it is working.
    This is not dynamic nor personalized, so it won't fit this 
    library because it is not reusable.

    Please, delete this when you find a way of having reusable
    code, thank you.
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# MYSQL
"""
mydb = mysql.connector.connect(
  host = os.getenv('DATABASE_HOST'),
  user = os.getenv('DATABASE_USER'),
  password = os.getenv('DATABASE_PASSWORD'),
  database = os.getenv('DATABASE_NAME')
)

mycursor = mydb.cursor(buffered = True)
"""
mydb = None
mycursor = None

def __database_video_to_dict(database_row):
    """
    Receives a database row format (columns index) and returns it
    as a dictionary to make manipulation easier
    """
    return {
        'id': database_row[0],
        'video_id': database_row[1],
        'name': database_row[2],
        'description': database_row[3],
        'is_uploaded': database_row[4]
    }

def get_video_from_database(table, video_id):
    """
    Looks for the video with 'video_id' provided in database and
    returns None if it doesn't exist or a dictionary if it does
    """
    sql = "SELECT * FROM " + table + " WHERE video_id = '" + video_id + "' LIMIT 1"
    mycursor.execute(sql)

    if mycursor.rowcount == 0:
        return None
    
    return __database_video_to_dict(mycursor.fetchall()[0])

def insert_video(table, video_id, name, description, is_uploaded):
    """
    Inserts a new video row in our database
    """
    # TODO: Sorry, but this changes depending on the object
    sql = "INSERT INTO " + table + " (video_id, name, description, is_uploaded) VALUES (%s, %s, %s, %s)"
    val = (video_id, name, description, is_uploaded)
    mycursor.execute(sql, val)
    mydb.commit()

def db_insert(table, fields, values):
    # TODO: This 'VALUES' is not dynamic
    sql = "INSERT INTO " + table + " (" + ', '.join(fields) + ") VALUES (%s, %s, %s)"
    mycursor.execute(sql, tuple(values))
    mydb.commit()

def db_select(table, field, value):
    sql = "SELECT * FROM " + table + " WHERE " + field + " = '" + value + "' LIMIT 1"
    mycursor.execute(sql)

    if mycursor.rowcount == 0:
        return None
    
    result = mycursor.fetchall()[0]

    # TODO: Sorry, but this changes depending on the object
    return {
        'id': result[0],
        'video_id': result[1],
        'username': result[2],
        'status': result[3],
    }

