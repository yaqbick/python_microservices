import os, json,requests, jwt
from flask import Blueprint, render_template, abort, request, redirect, flash, Flask, url_for,Response, make_response,session
from common import *
from werkzeug.utils import secure_filename
from flask_json import json_response
# from flask.ext.session import Session

upload_bp = Blueprint('upload', __name__, template_folder='templates')

@upload_bp.route('/', methods=['GET','POST'])
def index(fileName=''):
    if session.get('logged_in') == True:
        user=session.get('user')
        host=request.host

        if request.method == 'POST':
            if  request.content_type == 'application/json':
                url={'url':" http://"+host+"/upload/files/"+ fileName}
                json_arr= request.data.decode('utf-8')
                response=create_response(json_arr,url,request)
                # response = make_response(dictionary, 200, {'Content-Type': 'application/json'})
                return response

            else:
                if 'pic' not in request.files:
                    if 'multipart/form-data' in request.content_type:
                        if not 'file' in request.files:
                            return 'uzupełnij klucz(file)'
                        else:
                            json_arr={'data':"no editional data"}
                            json_arr=json.dumps(json_arr)
                            file=request.files['file']
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(UPLOAD_FOLDER, filename))
                            url={'url':" http://"+host+"/upload/files/"+ filename}
                            response=create_response(json_arr,url,request)
                            # response = make_response(dictionary, 200, {'Content-Type': 'application/json'})
                            return response
                            # return 'dodano plik ' + filename
                    else:
                        flash('Nie wybrano pliku')
                        return render_template("upload/index.html")


                else:
                    file = request.files['pic']
                    filename = file.filename

                    # if validation(filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    flash("plik " + filename + " został dodany")
                    return render_template("upload/index.html", url="/static/"+ filename)
                    # else: 
                    #     flash("plik nie jest obrazem")
                    #     return render_template("upload/index.html")

        if request.method == 'GET':
                return render_template("upload/index.html",user=user)
    else:
        return redirect(url_for('/.login'))
        
   
    
@upload_bp.route('/files/<fileName>', methods=['GET'])
def getName(fileName):

        host=request.host

        path='/Users/yaqbick/Desktop/Projects/static'
        pics_long= os.listdir(path)
        pics_short=[]

        for pic in pics_long:
            pics_short.append(pic.split('.')[0])
            if fileName==pic.split('.')[0]:
                fileName_ext=pic

        if fileName not in pics_short :
            fileName='nie znaleziono zdjecia'
            url={'url': fileName}
        else:
            url={'url':" http://"+host+"/upload/files/"+ fileName_ext}

        fileName = secure_filename(fileName)

        if  request.content_type == 'application/json':
            json_arr={'data':"no editional data"}
            json_arr=json.dumps(json_arr)
            response=create_response(json_arr,url,request)

            # response = make_response(dictionary, 200, {'Content-Type': 'application/json'})
            return response
        else:
            return render_template("upload/image.html", url="/static/"+ fileName_ext)

@upload_bp.route('/remote', methods=['GET','POST'])
def upload_remote():
    encoded = jwt.encode({'user': 'admin'}, 'secret', algorithm='HS256')
    password="dupa"
    if request.method == 'POST':
        token=str(request.form['token'])[2:-1]

        try:
            decoded =jwt.decode(token, 'secret', algorithms=['HS256'])
            user=decoded['user']
        except jwt.InvalidTokenError:
            return "zły token"

        if authorization(user,password):
            file = request.files['files']
            if file==None:
                return "brak pliku"
            else:
                json_arr={'data':"no editional data"}
                json_arr=json.dumps(json_arr)
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                host=request.host
                url={'url':" http://"+host+"/upload/remote/"}
                response=create_response(json_arr,url,request)
                # response = make_response(dictionary, 200, {'Content-Type': "multipart/form-data"})       
                return response
        else:
            return "nie masz uprawnień do wysłania tego pliku"
    else:
        return render_template("upload/index_remote.html",token=encoded)


