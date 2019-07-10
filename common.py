from flask import render_template, Flask,request,flash,url_for,redirect,json,make_response
import mysql.connector
def validation(result):
    file_ext=result.split(".")[-1]
    extensions = ["jpg", "gif", "png"]
    if file_ext in extensions:
        return True
    else:
        return False

UPLOAD_FOLDER = 'C:/Users/yaqbick/Desktop/Projects/static'

def create_response(json_arr,url,request):
    link=request.url
    link={'link':link}
    json_arr=json.loads(json_arr)
    json_arr.update(url)
    dictionary = {'message': 'Success', 'status':'200','data': json_arr }
    dictionary.update(link)
    dictionary = json.dumps(dictionary)
    response = make_response(dictionary, 200, {'Content-Type': 'application/json'})
    return response

def authorization(user,password):
    connection =connect_to_db()
    mycursor = connection.cursor()
    sql="SELECT password FROM python.users WHERE login= %s AND password=%s"
    user=str(user)
    password=str(password)
    val=(user,password)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()

    if not myresult:
        return False
    else:
        return True


def connect_to_db():
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jakubik7"
)
    return connection 

def user_exist(user,email):
    connection =connect_to_db()
    mycursor = connection.cursor()
    sql="SELECT * FROM python.users WHERE login= %s OR email=%s"
    user=str(user)
    email=str(email)
    val=(user,email)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()

    if not myresult:
        return False
    else:
        return True
    

def create_user_in_database(email,login,password):
    connection =connect_to_db()
    mycursor = connection.cursor()
    login=str(login)
    email=str(email)
    password=str(password)

    sql = "INSERT INTO python.users (email, login, password) VALUES (%s, %s,%s)"
    val = (email,login,password)
    mycursor.execute(sql, val)

    connection.commit()
    return "wynik"