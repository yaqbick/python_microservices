from flask import render_template, Flask,request,flash,url_for,redirect,session
from routes.upload_bp import upload_bp
from routes.auth_bp import auth_bp
from common import *
# from flask.ext.session import Session


app = Flask(__name__)

app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2000 * 1024 * 1024
app.config['JSON_ADD_STATUS'] = True


app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(auth_bp, url_prefix='/')



   



