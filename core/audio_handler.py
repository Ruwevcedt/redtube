import re
import subprocess
import glob
import shutil
from drawer import music_list

# musiclist = []  # TODO : change this to object


def get_audio_duration(audio_path: str) -> str:
    """
    Return Audio Filename to Audio File's Duraion

    test.mp3 -> str(360.03)

    :param audio_path: Audio Path(str)
    :return: Audio Duration str(second)
    """
    # TODO : Make Below Asyncable
    process = subprocess.Popen(['/usr/local/bin/ffmpeg', '-i', audio_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    # ...
    matches = re.search('Duration:\s(?P<hh>\d+?):(?P<mm>\d+?):(?P<ss>\d+\.\d+?),', stdout.decode('utf-8'), re.DOTALL)
    hour, minute, second = int(matches.group('hh')), int(matches.group('mm')), float(matches.group('ss'))
    duration = str(3600 * hour + 60 * minute + second)[:6]
    return duration


def update_music():         # TODO : refactoring this function
    global music_list
    musics = glob.glob("music/*")
    print(musics)

    for music in musics:
        musicname = music.split('/')[-1].split('.')
        print(musicname)

        imgname = "picture/{}.jpg".format(musicname[0])
        # img = imgname if imgname in glob("picture/*.jpg") else "None."
        if imgname in glob.glob("picture/*.jpg"):
            img = imgname
        else:
            img = 'None.'

        if musicname[-1] == 'mp4':
            if not "music/" + musicname[0] + '.aac' in musics:
                print('log :', 'generating aac file')
                shutil.copyfile(
                    "music/{}.mp4".format(musicname[0]),
                    "music/{}.aac".format(musicname[0])
                )

                musicname = musicname[0] + '.aac'
                print(musicname)

                music_list.append({
                    'track': len(music_list) + 1,
                    'name': musicname,
                    'length': get_audio_duration(music),
                    'path': "player/" + musicname,
                    'capture' : img
                })
            else:
                pass
        else:
            musicname = musicname[0] + '.' + musicname[-1]
            print(musicname)

            music_list.append({
                'track': len(music_list) + 1,
                'name': musicname,
                'length': get_audio_duration(music),
                'path': "player/" + musicname,
                'capture' : img
            })
    print(music_list)
