from drawer import flask_login, music_list
import pytube
import urllib
import shutil
import os


class VideoHandler:

    def __init__(self, user: str, url: str, audio_path="music/", thumbnail_path="picture/"):
        self._path_assign(user, audio_path, thumbnail_path)
        self.user = user
        self.youtube_object = pytube.YouTube(url)
        self.title = "".join(filter(lambda x: x if x not in "~\"\'#%&*:<>?\/{|},\." else False, self.youtube_object.title))
        self.audio_object = self.youtube_object.streams.filter(only_audio=True, file_extension='mp4').fmt_streams[0]

    def _path_exists_check(self, path):
        os.mkdir(path) if not os.path.exists(path) else False

    def _already_exists_check(self, extension: str):
        return True if os.path.exists(self.audio_download_path + self.title + extension) else False

    def _download_audio(self):
        if self.audio_object:
            self.audio_object.download(self.audio_download_path)

    def _thumbnail_resolution_check(self):
        _higher_resolution = self.youtube_object.thumbnail_url.replace('default.jpg', 'hqdefault.jpg')
        return _higher_resolution if _higher_resolution else self.youtube_object.thumbnail_url

    def _download_thumbnail(self):
        urllib.request.urlretrieve(self._thumbnail_resolution_check(),
                                   f"{self.thumbnail_download_path}{self.title}.jpg")

    def _change_extension(self):
        file_name = self.audio_download_path + self.title
        shutil.move(file_name + ".mp4", file_name + ".aac")

    def _path_assign(self, user, audio_path, thumbnail_path):
        try:
            self.audio_download_path = f"{audio_path}{user}/"
            self.thumbnail_download_path = thumbnail_path
        except AttributeError:
            self.audio_download_path = audio_path
            self.thumbnail_download_path = thumbnail_path
        self._path_exists_check(self.audio_download_path)
        self._path_exists_check(self.thumbnail_download_path)

    def download_sequence(self):
        if not self._already_exists_check(extension=".aac"):
            self._download_audio() if not self._already_exists_check(extension=".mp4") else False
            self._change_extension()
            self._download_thumbnail()
            music_list[self.user].update()
