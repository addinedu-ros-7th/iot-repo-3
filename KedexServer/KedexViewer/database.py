# mysql module
import mysql.connector
from dotenv import load_dotenv
import os

# load .env
load_dotenv()

HOST_NAME=os.environ.get('host_name')
USER_NAME=os.environ.get('user_name')
USER_PASSWORD=os.environ.get('user_password')

# connect_database( hostname , username , password )
def connect_database(host_name=HOST_NAME,user_name=USER_NAME,user_password=USER_PASSWORD):
    mydb = mysql.connector.connect(
        host = host_name,
        port = 3306,
        user = user_name,
        password = user_password,
        database = "TEAM_3"
    )

    cursor = mydb.cursor()

    return mydb, cursor

def close_database(mydb, cursor):
    cursor.close()
    mydb.close()

# 
def excute_query(query):
    mydb, cursor = connect_database()
    try:
        cursor.execute(query);

        if query.strip().lower().startswith("select"):
            return cursor.fetchall()
        else :
            mydb.commit()
            print("success!!!")

    except mysql.connector.Error as err:
        print(err)

    finally:
        close_database(mydb=mydb,cursor=cursor)

# test 완료
# result = excute_query('select * from category;')
# print(result)
