import subprocess
import glob
import re
import os


#aac_list = glob.glob("music/*.aac")
#print(aac_list)
#print(os.popen(f"/usr/local/bin/ffmpeg -i '{aac_list[0]}' -loglevel info").readlines())

"""
process = subprocess.Popen(['/usr/local/bin/ffmpeg', '-i', aac_list[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout, stderr = process.communicate()

matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

print(f"{matches['hours']}:{matches['minuites']}:{matches['seconds']}")
"""


"""
command = ['/usr/local/bin/ffmpeg', '-i', aac_list[0]]

process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout, stderr = process.communicate()

matches = re.findall('Duration:\s{1}(?P<hh>\d+?):(?P<mm>\d+?):(?P<ss>\d+\.\d+?),', stdout.decode('utf-8'), re.DOTALL)
#print(f"{matches['hh']}:{matches['mm']}:{matches['ss']}")
print(matches)

hour, minuite, second = int(matches[0][0]), int(matches[0][1]), int(matches[0][2].split('.')[0])
print(hour, minuite, second)

duration = 3600 * hour + 60 * minuite + second
print(duration)
"""

def get_dur(afile_path):
    command = ['/usr/local/bin/ffmpeg', '-i', afile_path]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()

    matches = re.search(r'Duration:\s(?P<hh>\d+?):(?P<mm>\d+?):(?P<ss>\d+\.\d+?),', stdout.decode('utf-8'),
                         re.DOTALL)
    hour, minute, second = int(matches['hh']), int(matches['mm']), float(matches['ss'])
    duration = str(3600 * hour + 60 * minute + second)[:6]
    print(f"{afile_path} : {duration}")
    return duration


musiclist = glob.glob('music/*')
print('files : ', musiclist)

dur_dic = []

for music in musiclist:
    dur_dic.append({
        music : get_dur(music)
    })

print(dur_dic)