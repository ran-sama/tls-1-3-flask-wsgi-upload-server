#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, tempfile, secrets
from flask import Flask, request, redirect, session, abort, render_template, Response
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import FileTarget
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/media/kingdian/uploader_priv/"#with trailing slash
MY_UPLOAD_DIR = "/media/kingdian/uploader_priv"#no trailing slash
tempfile.tempdir = MY_UPLOAD_DIR

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'memcached'

@app.before_request
def require_login():
    allowed_routes = ['login', 'robots_dot_txt']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route("/robots.txt")
def robots_dot_txt():
    robots_txt = "User-agent: *\r\nDisallow: /"
    return Response(robots_txt, mimetype='text/plain')

@app.route('/')
def index():
    user = session['user']
    return """<!doctype html><style>body{color: #f8a830;background-color: #000000;}</style><head><title>Signed in</title></head><body><h1>Logged in as %s</h1><a href='/logout'>Click here to logout</a></body>""" % user

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        cl = int(request.content_length)
        if cl is not None and cl > 139:
            return abort(413)
        my_pass = request.form['sha512hash']
        if my_pass == 'aabbccddeeff0011223344556677889900':#MUST SET YOUR OWN PBKDF2 DERIVED KEY HERE
            session['user'] = "ran"
            return redirect('/upload')
        else:
            return render_template('error.html')
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        rand_name = "tmp-" + secrets.token_hex(4)
        file_ = FileTarget(os.path.join(tempfile.gettempdir(), rand_name))
        parser = StreamingFormDataParser(headers=request.headers)
        parser.register('file', file_)
        while True:
            chunk = request.stream.read(8192)
            if not chunk:
                break
            parser.data_received(chunk)
        old_file = os.path.join(MY_UPLOAD_DIR, rand_name)
        finalfilename = secure_filename(file_.multipart_filename)
        if not finalfilename:
            os.remove(os.path.join(MY_UPLOAD_DIR, rand_name))
            return """<!doctype html><style>body{color: #f8a830;background-color: #000000;}</style><head><title>File missing</title></head><body><h1>No file selected</h1></body>"""
        new_file = os.path.join(MY_UPLOAD_DIR, finalfilename)
        os.rename(old_file, new_file)
        filesize = os.path.getsize(UPLOAD_FOLDER + finalfilename)
        return render_template("success.html", bytes_rcvd=filesize)
    return render_template('upload.html')

@app.route('/logout')
def logout():
   session.pop('user', None)
   return redirect('/')
