from pytube import YouTube as YT
import urllib


def vid_aud(vid_url):
    yt = YT(vid_url).streams.all()

    img = urllib.request.urlretrieve(YT(vid_url).thumbnail_url, YT(vid_url).title + '.jpg')
    print(img)

    for index, stream in enumerate(yt):
        print(index, stream)

        if stream.mime_type == "audio/mp4":
            print(f"downloading : {stream}")
            #yt[index].download(os.path.join(os.path.split(os.path.abspath(__file__))[0], "templates/"))
            return print(f"downlaoded : {stream}")


vid_aud("https://www.youtube.com/watch?v=SvARxobwJyM&t=0s&list=LLmRv6Hi7SVI01a1SeA6W1ww&index=14")
