# flask-https-tls13-wsgi-server
A powerful and secure upload server for uWSGI and Flask.

## Dependencies

https://pypi.org/project/Flask/  
https://pypi.org/project/uWSGI/  
https://pypi.org/project/Werkzeug/  
https://pypi.org/project/streaming-form-data/  

## How to launch the server

```uwsgi --ini /home/ran/uwsgi.ini```

## Screenshots

![alt text](https://raw.githubusercontent.com/ran-sama/flask-wsgi-upload-server/master/screenshots/login_page.png)

![alt text](https://raw.githubusercontent.com/ran-sama/flask-wsgi-upload-server/master/screenshots/logged_in.png)

![alt text](https://raw.githubusercontent.com/ran-sama/flask-wsgi-upload-server/master/screenshots/upload_dialogue.png)

![alt text](https://raw.githubusercontent.com/ran-sama/flask-wsgi-upload-server/master/screenshots/successful_upload.png)

![alt text](https://raw.githubusercontent.com/ran-sama/flask-wsgi-upload-server/master/screenshots/unauthorized.png)

## Generate your own PBKDF2 credentials

Edit the [derive_key.py](https://github.com/ran-sama/tls1-3-flask-wsgi-upload-server/blob/master/derive_key.py#L7) (or use the browser based derive_key.html) and state your username AND password as ONE single string:

```
$ python3 derive_key.py
Your salt (use in the login html):
qNv83XARvwWcGeBYPvbXAg==
Your PBKDF2 key (use in the WSGI code):
b31300bd83a0bfc3e5197df305fbc00b864526f6ac6ac4f91c4352a36fa79088
```

Must edit 
[server_UL.py](https://github.com/ran-sama/tls1-3-flask-wsgi-upload-server/blob/master/server_UL.py#L40) and [login.html](https://github.com/ran-sama/tls1-3-flask-wsgi-upload-server/blob/master/templates/login.html#L112) with your OWN keys. Don't use the defaults.

## Set your server key and certificate chain in the ini

As HTTPS upload server you must define paths to your cryptographic keys from i.e. letsencrypt inside the [uwsgi.ini](https://github.com/ran-sama/tls1-3-flask-wsgi-upload-server/blob/master/uwsgi.ini#L2) for uWSGI to use them.

## Upgrade to the highest possible security

You can compile a custom version of uWSGI that uses the stronger NID_secp384r1 instead of NID_X9_62_prime256v1:  
https://github.com/unbit/uwsgi/pull/2285/files

![alt text](https://raw.githubusercontent.com/ran-sama/tls1-3-flask-wsgi-upload-server/master/screenshots/ssllabs_rating.png)

![alt text](https://raw.githubusercontent.com/ran-sama/tls1-3-flask-wsgi-upload-server/master/screenshots/activate_curve384.png)

## License
Licensed under the WTFPL license.
