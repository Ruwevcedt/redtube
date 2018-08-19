from pytube import YouTube
import pytube.exceptions
# import for charge.py
import urllib
import shutil
import os


class VideoHandler:

    def __init__(self, url: str, audio_path="../music/", thumbnail_path="../picture/"):
        self.audio_download_path = audio_path
        self.thumbnail_download_path = thumbnail_path
        self.youtube_object = YouTube(url)
        self.title = self.youtube_object.title
        self.audio_object = self.youtube_object.streams.filter(only_audio=True, file_extension='mp4')

    def download_audio(self):
        if self.audio_object:
            self.audio_object.download(self.audio_download_path)

    def _thumbnail_resolution_check(self):
        return lambda thumbnail_url : thumbnail_url if self.youtube_object.thumbnail_url.replace('defualt.jpg', 'hqdefault.jpg') else self.youtube_object.thumbnail_url

    def download_thumbnail(self):
        _reshaped_title = "".join(filter(lambda x: x if x not in "~\"#%&*:<>?\/{|}" else False, self.title))
        urllib.request.urlretrieve(self._thumbnail_resolution_check(), f"{self.thumbnail_download_path}{_reshaped_title}.jpg") # TODO : Make this Asyncable

    def download_sequence(self):
        self.download_audio()
        self.download_thumbnail()


# test = VideoHandler("https://www.youtube.com/watch?v=q6EoRBvdVPQ")
# test.download_sequence()


def youtube_video_getter(youtube_url):
    youtube_streams = YouTube(youtube_url).streams.all()

    for index, stream in enumerate(youtube_streams):
        print(index, stream)

        if stream.mime_type == "audio/mp4":
            print("downloading : ", stream)
            youtube_streams[index].download("../music/")
            print("downlaoded : ", stream)
            print()

            youtube_thumbnail_url = YouTube(youtube_url).thumbnail_url

            try:
                youtube_thumbnail_url = youtube_thumbnail_url.replace('default.jpg', 'hqdefault.jpg')
            except:
                pass
                #^if hqdefault.jpg doesn't exist let default.jpg go

            print("thumbnail url : ", youtube_thumbnail_url)
            urllib.request.urlretrieve(youtube_thumbnail_url, "../picture/{}.jpg".format("".join(filter(lambda x: x if x not in "~\"#%&*:<>?\/{|}" else False, YouTube(youtube_url).title)), ''))
            return print("downlaod end")

    return print("err : no audio/mp4 file")



youtube_video_getter("https://www.youtube.com/watch?v=q6EoRBvdVPQ")
# StreamQuery : Audio_Object

