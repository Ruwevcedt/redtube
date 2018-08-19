from pytube import YouTube as YTB
import pytube.exceptions
import urllib


def vid_aud(vid_url):
    yt = YTB(vid_url).streams.all()

    for index, stream in enumerate(yt):
        print(index, stream)

        if stream.mime_type == "audio/mp4":
            print("downloading : ", stream)
            yt[index].download("music/")
            print("downlaoded : ", stream)

            try:
                capture = YTB(vid_url).thumbnail_url.replace('default.jpg', 'hqdefault.jpg')
            except:
                capture = YTB(vid_url).thumbnail_url

            print("thumbnail : ", capture)
            urllib.request.urlretrieve(capture, "picture/{}.jpg".format("".join(filter(lambda x: x if x not in "~\"#%&*:<>?\/{|}" else False, YTB(vid_url).title)), ''))

            return print("downlaod end")

    return print("err : ", 'no audio/mp4 file')
