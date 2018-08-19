from pytube import YouTube
import pytube.exceptions
import urllib


def youtube_video_getter(youtube_url):
    youtube_streams = YouTube(youtube_url).streams.all()

    for index, stream in enumerate(youtube_streams):
        print(index, stream)

        if stream.mime_type == "audio/mp4":
            print("downloading : ", stream)
            youtube_streams[index].download("music/")
            print("downlaoded : ", stream)

            youtube_thumbnail_url = YouTube(youtube_url).thumbnail_url
            try:
                youtube_thumbnail_url = youtube_thumbnail_url.replace('default.jpg', 'hqdefault.jpg')
            except:
                pass
                #^if hqdefault.jpg doesn't exist let default.jpg go

            print("thumbnail url : ", youtube_thumbnail_url)
            urllib.request.urlretrieve(youtube_thumbnail_url, "picture/{}.jpg".format("".join(filter(lambda x: x if x not in "~\"#%&*:<>?\/{|}" else False, YouTube(youtube_url).title)), ''))
            return print("downlaod end")

    return print("err : no audio/mp4 file")
