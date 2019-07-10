import os, json,requests, jwt
from flask import Blueprint, render_template, abort, request, redirect, flash, Flask, url_for,Response, make_response,session
from common import *
from werkzeug.utils import secure_filename
from flask_json import json_response
# from flask.ext.session import Session

auth_bp = Blueprint('/', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    host=request.host
    if request.method == 'POST':
        if  request.content_type == 'application/json':
            json_arr= request.data
            url={'url':" http://"+host+"/login"}
            response=create_response(json_arr,url,request)
            return response
        else:
            user=request.form['login']
            password=request.form['password']
            if authorization(user,password):
                session['logged_in'] = True
                session['user'] = user
                return redirect(url_for('upload.index'))
            else:
                flash('login/hasło nieprawidłowe!')
                return render_template("auth/login.html")
    else: 
        return render_template("auth/login.html")

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    host=request.host
    if request.method == 'POST':
        if  request.content_type == 'application/json':
            # create_user_in_database()
            flash('Pomyślnie dodano użytkownika')
            json_arr= request.data
            url={'url':" http://"+host+"/login"}
            response=create_response(json_arr,url,request)
            return response

        else:
            email=request.form['email']
            login=request.form['login']
            password=request.form['password']
            if user_exist(login,email):
                flash('Podany login/E-Mail już istnieje')
                return render_template("auth/register.html")
            else:
                create_user_in_database(email,login,password)
                flash('Pomyślnie dodano użytkownika')
                return redirect(url_for('/.login'))
 
    else:
        return render_template("auth/register.html")

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    session['logged_in'] = False
    return redirect(url_for('/.login'))