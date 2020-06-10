from pytube import YouTube
from pprint import pprint

def human_readable(bytes):
    val = (bytes) / (1024*1024)
    return str(round(val, 2)) + " MB"

def getSignedURL(url:str):
    #url = 'https://www.youtube.com/watch?v=_hIZNaBH0lw&list=PL3tRBEVW0hiBSL5AIcxjbctIsKF_Az0ok'
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
        available_streams.append({'stream':stream,'quality':stream.resolution, 'format':stream.subtype, 'size': human_readable(stream.filesize), 'url': stream.url})

    #return best_stream.url

    #best_stream.download()

    #print("finished downloading")
    print(video_details, available_streams)
    return video_details, available_streams

if __name__ == '__main__':

    #url = 'https://www.youtube.com/watch?v=PIh2xe4jnpk'
    url= "https://www.youtube.com/watch?v=fivFmhp2cxM"
    video_details, available_streams = getSignedURL(url)
    for stream in available_streams:
        print(stream)
        stream['stream'].download(video_details['title'])



