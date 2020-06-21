from pytube import YouTube, Playlist
from pprint import pprint
import re
import uuid
#import tempfile
import shutil
import os

saveLocation = "playlists/"
playlist_regex = re.compile(r'^https://www\.youtube\.com/playlist\?list=.*$')
video_regex = re.compile(r'https://www\.youtube\.com/watch\?v=.*')

def human_readable(bytes):
    val = (bytes) / (1024*1024)
    return str(round(val, 2)) + " MB"

def getSignedURL(url:str):
    #url = 'https://www.youtube.com/watch?v=_hIZNaBH0lw&list=PL3tRBEVW0hiBSL5AIcxjbctIsKF_Az0ok'

    if re.match(playlist_regex, url) is not None :
        print("***PLAYLIST****\n");
        playlist = Playlist(url)
        title = playlist.title;
        #thumbnail_url = playlist.thumbnail_url;

        playlist_details = {'title': title, 'thumbnail_url':'thumbnail_url'}
    
        available_videos = []
        for link in playlist.video_urls:
            video = YouTube(link)
            title = video.title;
            thumbnail_url = video.thumbnail_url;

            video_details = {'title': title, 'thumbnail_url':thumbnail_url}
            all_streams = video.streams
            best_stream = all_streams.get_highest_resolution()
            available_videos.append({**video_details, 'quality':best_stream.resolution, 'format':best_stream.subtype, 'size': human_readable(best_stream.filesize), 'url': best_stream.url, 'link':link})
            pprint(available_videos)

        return "playlist", available_videos


    elif re.match(video_regex, url) is not None:
        video = YouTube(url)

        #print(video.extract.video_info_url('8xg3vE8Ie_E', 'https://www.youtube.com/watch?v=8xg3vE8Ie_E'))
        #all_progressive_streams = video.streams.filter(progressive = True, file_extension = 'mp4').order_by('resolution').desc()
        #print(all_progressive_streams)

        title = video.title;
        thumbnail_url = video.thumbnail_url;

        video_details = {'title': title, 'thumbnail_url':thumbnail_url}

        all_streams = video.streams

        #all_progressive_mp4 = all_streams.filter(progressive = True, file_extension = 'mp4') 

        best_stream = [all_streams.get_highest_resolution()]

        available_streams  =[]
        for stream in best_stream :
            available_streams.append({**video_details, 'quality':stream.resolution, 'format':stream.subtype, 'size': human_readable(stream.filesize), 'url': stream.url})

        #return best_stream.url

        #best_stream.download()

        #print("finished downloading")
        print(video_details, available_streams)
        return "video", available_streams

    else:
        return (None,) * 2

def zip(links):
    #tf = tempfile.TemporaryDirectory(prefix=saveLocation,delete=False)
    dirname = str(uuid.uuid4())
    loc = saveLocation+dirname
    for i,link in enumerate(links):
        video = YouTube(link)
        all_streams = video.streams
        best_stream = all_streams.get_highest_resolution()
        file_path=best_stream.download(output_path=loc, filename_prefix=str(i+1)+"_");
        print(file_path)
    shutil.make_archive(loc,"zip","playlists/",dirname)
    return dirname



if __name__ == '__main__':

    #url = 'https://www.youtube.com/watch?v=PIh2xe4jnpk'
    url= "https://www.youtube.com/watch?v=fivFmhp2cxM"
    video_details, available_streams = getSignedURL(url)
    for stream in available_streams:
        print(stream)
        stream['stream'].download(video_details['title'])



