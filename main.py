import imaplib
import json

import requests
import io
from flask import Flask, send_file
from flask_restful import Api, Resource
import os
from PIL import *
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
app=Flask(__name__,template_folder='test')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
api = Api(app)

def TwoFactorAuth():
    host = 'imap.mail.ru'
    user = 'wilcoz@list.ru'
    passwordapp = 'ishjcBFZzkH7TN1UUBNk'
    password = 'LCMeK!Gs4Jxc-AZ'
    port = '993'
    mailbox = 'INBOX.subfolder'

    mail = imaplib.IMAP4_SSL('imap.mail.ru')
    mail.login(user, passwordapp)

    mail.list()
    mail.select("inbox")

    result, data = mail.search(None, "ALL")

    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]

    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    code = raw_email_string.split('******')[1]
    return code

def get_image(uid):
    return requests.get(f"https://legendware.pw/get_avatar.php?id={uid}").content


headers = {"Referer": "https://legendware.pw/index.php/login",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33',
           'cookie': '_ym_uid=1633091021523726229; _ga=GA1.2.1404680202.1634832405; _ym_d=1648876305; '
                     'cf_clearance=OyPqDO3mQ7ZQTPh0IFgogUx.lzZ3vcncvacmt1LDrek-1653153413-0-150; _ym_isad=2; '
                     '_ym_visorc=w; xf_tfa_trust=_QvuSHlKEBhxwZ4TXUZH69UqwrCK1Qem; '
                     '__cf_bm=DumNMxy6kr0QgIJSNbSp8.XzaC6cgPc0VsmSL3jRNuQ-1654629461-0'
                     '-AWpg7t002Q1s9ixKvDGI10J2HJoLW46+X41wQt1Rsg1imxcq5dz3p74DYRQEoaOdkd06IjifBkC3e46wEj1c54yZq'
                     '+uSy3zPpx/IwtT4SM60RE6ByXTf0BUuLrpIRFobuQ==; xf_session=LT5rDPEsiUQc6LIT6dfL-kCtu_yE8q1V; '
                     'xf_csrf=lCk1zHWFoH4J1dbY; _ga_35W34R8JLX=GS1.2.1654628436.542.1.1654630183.0'}
ROOT_URL = 'https://legendware.pw/login/login'
USERNAME, PASSWORD = 'INSHALLAAAAAAAAAAAAAAAAAA', 'LCMeK!Gs4Jxc-AZ'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 ' \
             'Safari/537.36 Edg/102.0.1245.33 '

with requests.Session() as c:
    login_data = {'login': USERNAME, 'password': PASSWORD, 'remember': '1', '_xfRedirect': 'https://legendware.pw/'
                  }
    login_request = c.post(ROOT_URL, data=login_data, headers=headers)
    # print(c.get(ROOT_URL).text)
    TFAurl = 'https://legendware.pw/login/two-step?_xfRedirect=https%3A%2F%2Flegendware.pw%2F&remember=1/'
    try:
        TFA_data = {'code': TwoFactorAuth()}
        c.post(TFAurl, data=TFA_data)
    except:
        print("TFA ERROR")
    token = c.get('https://legendware.pw/').text.split('name="_xfToken" value="')[1].split('"')[0]
    print(token)

class Quote(Resource):
    @app.route('/')
    @app.route('/index')
    def get(self, name):

            url = f"https://legendware.pw/index.php?members/find&q={name}&_xfRequestUri=members&_xfWithData=1&_xfToken={token}&_xfResponseType=json"
            r = c.get(url)
            schema = r.text
            schemajson = json.loads(schema)
            textschem = str(schemajson)
            uid = textschem.split(r'data-user-id="')[1].split('"')[0]
            return send_file(io.BytesIO(get_image(uid)), mimetype='image/jpg')



api.add_resource(Quote, "/userinfo", "/userinfo/", "/userinfo/<path:name>")

if __name__ == "__main__":
    app.run(debug=True)
