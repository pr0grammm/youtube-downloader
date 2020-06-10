from ytDownloader_pkg import app
from flask import render_template, request
from ytDownloader_pkg import mp4conv
from flask_httpauth import HTTPBasicAuth
'''
auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    if username == 'reshma' and password == 'reshma':
        return True
    else:
        return False
'''
@app.route('/')
def landing_page():
    try:
        return render_template('landing_page.html')
    except Exception as e:
        return render_template('error.html',Error =str(e))


@app.route('/download', methods=['post'])
def download_page():
    try:
        if request.method == 'POST':
            data = request.form
            url = data['url']
            (video_details, available_streams) = mp4conv.getSignedURL(url)
            return render_template('download_page.html', Video_details = video_details, Available_streams = available_streams)
    except Exception as e:
        return render_template('error.html',Error =str(e))

