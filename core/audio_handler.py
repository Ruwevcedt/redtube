import re
import subprocess
import glob
import shutil
import os
# from drawer import music_list

# musiclist = []  # TODO : change this to object


class Music:
    """
    Music.path    => :return Absolute Path of :param: file_name
    Music.name    => :return Music.path's filename (ex: Music.path="/User/Desktop/music.aac"->"music")
    Music.length  => :return audio duration of Music.path (only with audio file)
    Music.capture => :return Music.path's Album Art if exists else return Default Album Art
    """

    __slots__ = (
        "file_name",
        "absolute_file_name",
        "file_name_without_extension",
        "extension",
        "capture_path",
        "music_duration"
    )

    def __init__(self, file_name: str, capture_path: str = "../picture"):
        self.file_name = file_name
        self.capture_path = os.path.abspath(capture_path)
        self.absolute_file_name = os.path.abspath(self.file_name)
        self.file_name_without_extension, self.extension = os.path.splitext(self.file_name)
        self.file_name_without_extension = os.path.split(self.file_name_without_extension)[1]
        self.music_duration = None

    @property
    def length(self):
        return self.music_duration if self.music_duration else self.get_audio_duration()

    @property
    def name(self):
        return self.file_name_without_extension

    @property
    def path(self):
        return f"player/{self.name}"

    @property
    def file_path(self):
        return self.absolute_file_name

    @property
    def capture(self):
        capture_path = f"{self.name}.jpg"
        return capture_path if os.path.exists(capture_path) else f"picture/pic01.jpg"

    def get_audio_duration(self) -> str:
        """
        Return Audio Filename to Audio File's Duraion

        test.mp3 -> str(360.03)

        :param audio_path: Audio Path(str)
        :return: Audio Duration str(second)
        """
        # TODO : Make Below Asyncable
        process = subprocess.Popen(['/usr/local/bin/ffmpeg', '-i', self.absolute_file_name],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        stdout, stderr = process.communicate()
        # ...
        matches = re.search('Duration:\s(?P<hh>\d+?):(?P<mm>\d+?):(?P<ss>\d+\.\d+?),', stdout.decode('utf-8'), re.DOTALL)
        hour, minute, second = int(matches.group('hh')), int(matches.group('mm')), float(matches.group('ss'))
        self.music_duration = str(3600 * hour + 60 * minute + second)[:6]
        return self.music_duration

    def __repr__(self):
        return str(dict(
            name=self.name,
            length=self.length,
            path=self.path,
            capture=self.capture
        ))


class MusicList:

    __slots__ = (
        "music_folder",
        "music_file_list",
        "name_list",
        "available_extension"
    )

    def __init__(self, music_folder: str):
        self.music_folder = music_folder
        self.music_file_list = []
        self.name_list = []
        self.available_extension = (".aac", ".mp3")
        self.update()

    def update(self):
        music_list = list(filter(lambda x: x if os.path.splitext(x)[1].lower() in self.available_extension else False
                                 , glob.glob(f"{self.music_folder}/*")))
        self.music_file_list = [Music(x) for x in music_list]
        self.name_list = [x.name for x in self.music_file_list]

    def search(self, name):
        try:
            return self.music_file_list[self.name_list.index(name)]
        except ValueError:
            return Music(f"{self.music_folder}/darude_sandstorm.mp3")

    def __iter__(self):
        for r in self.music_file_list:
            yield r

    def __getitem__(self, item):
        return self.music_file_list[item]

    def __len__(self):
        return len(self.music_file_list)


a = MusicList("../music")
