import urllib
from urllib import request
from celery import Celery
import os
from datetime import datetime

app = Celery('tasks',broker='amqp://ec2-52-207-213-180.compute-1.amazonaws.com:5672')


@app.task
def downloadMedia(mediaurl):

    try:

        downloadpath = os.getcwd() + '/Media'
        if not os._exists(downloadpath):
            os.makedirs(downloadpath)
            print(downloadpath)
            os.chmod(downloadpath, 0o0777)

        topimageurlsplit = mediaurl.split('/')
        imagefilepath = downloadpath + '/' + topimageurlsplit[topimageurlsplit.__len__() - 1]
        urllib.request.urlretrieve(mediaurl,imagefilepath)
    except:
        print('impossible to download media @ : ' + mediaurl)

