from ytDownloader_pkg import app
from flask import render_template, request, send_from_directory
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
            if data['submit'] == "search":
                url = data['url']
                (option, available_streams) = mp4conv.getSignedURL(url)
                if option == "video":
                    return render_template('download_page_video.html', Option = option, Available_streams = available_streams)
                elif option == "playlist":
                    return render_template('download_page_playlist.html', Option = option, Available_videos = available_streams)
            elif data['submit'] == "zip":
                links = data.getlist('video')
                filename = mp4conv.zip(links)
                return render_template('download_location.html', Filename = filename)

    except Exception as e:
        return render_template('error.html',Error =str(e))

@app.route('/download-link/<uuid:filename>',methods=['get'])
def download_file(filename):
    directory = "/home/reshma/ytDownloader/playlists"
    filename = str(filename)+".zip"
    return send_from_directory(directory = directory, filename = filename,as_attachment=True)


