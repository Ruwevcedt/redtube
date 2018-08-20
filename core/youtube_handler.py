from drawer import music_list
import pytube
import urllib
import shutil
import os


class VideoHandler:

    def __init__(self, url: str, audio_path="music/", thumbnail_path="picture/"):
        self.audio_download_path = audio_path
        self.thumbnail_download_path = thumbnail_path

        self.youtube_object = pytube.YouTube(url)
        self.title = "".join(filter(lambda x: x if x not in "~\"\'#%&*:<>?\/{|}" else False, self.youtube_object.title))
        self.audio_object = self.youtube_object.streams.filter(only_audio=True, file_extension='mp4').fmt_streams[0]

    def _already_exists_check(self, extention: str):
        return True if os.path.exists(self.audio_download_path + self.title + "." + extention) else False

    def _download_audio(self):
        if self.audio_object:
            self.audio_object.download(self.audio_download_path)

    def _thumbnail_resolution_check(self):
        return self.youtube_object.thumbnail_url if self.youtube_object.thumbnail_url.replace('defualt.jpg', 'hqdefault.jpg') else self.youtube_object.thumbnail_url

    def _download_thumbnail(self):
        urllib.request.urlretrieve(self._thumbnail_resolution_check(),
                                   f"{self.thumbnail_download_path}{self.title}.jpg")  # TODO : Make this Asyncable

    def _change_extention(self):
        file_name = self.audio_download_path + self.title
        shutil.move(file_name + ".mp4", file_name + ".aac")

    def download_sequence(self):
        if not self._already_exists_check(extention="aac"):
            self._download_audio() if not self._already_exists_check(extention="mp4") else False
            self._change_extention()
            self._download_thumbnail()
            music_list.update()
