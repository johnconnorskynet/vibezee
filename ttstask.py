import urllib
from urllib import request

import boto3
from celery import Celery
import os
from datetime import datetime
import pyvona
from boto.s3.connection import S3Connection
from pymongo import MongoClient

ttsapp = Celery('ttstask',broker='amqp://ec2-54-234-242-80.compute-1.amazonaws.com:5672')

# Initialize ivona voice
def initYvonaTtsEngine ():
    ivonaVoice = pyvona.create_voice("GDNAJVR7DOF5M332VY3Q","RMlAiEzHBrFdXY0lP7TLjKptE0SjCbBcgEzVPHDz")
    ivonaVoice.sentence_break=1000
    ivonaVoice.voice_name='Salli'
    # ivonaVoice.voice_name='Mathieu'
    ivonaVoice._codec='mp3'
    return ivonaVoice


@ttsapp.task
# Text to speech, return the filepath of the tts file
def stringToVoiceToS3(string,fileName,mongoVibeId):
    # Init tts engine
    ivonaVoice = initYvonaTtsEngine()

    #Create S3 connection
    s3Conn = S3Connection('AKIAIJHTD67I5KSO2XTA','bQJ1YLy4GtZn9QR3oqJFWMIugQQwByWvsHiodNqV')
    s3Resource = boto3.resource('s3')

    # TTS content and save locally
    if not os.path.exists(os.getcwd()+'/Media/'):
        os.mkdir(os.getcwd()+'/Media/')

    filepath = os.getcwd()+'/Media/'+fileName
    print (filepath)

    ivonaVoice.fetch_voice(string,filepath)

    # Save audio to S3 bucket
    vibeZeeBucket = s3Resource.Bucket('vibezeebucket')
    s3 = boto3.client('s3')
    S3url = s3.generate_presigned_url(ExpiresIn=2592000,
        ClientMethod='get_object',
        Params={
            'Bucket': 'vibezeebucket',
            'Key': fileName
        }
    )

    s3Result = s3Resource.Bucket('vibezeebucket').upload_file(filepath, fileName)
    vibeObject = s3Resource.Object('vibezeebucket',fileName)
    vibeObject.wait_until_exists()
    print(vibeObject.get())

    # Update vibe in database
    mongoClient = MongoClient()
    vibezeeDb = mongoClient['vibezeeDb']
    vibeCollection = vibezeeDb['vibeCollection']
    print(mongoVibeId)
    vibeCollection.update_one({"_id" : mongoVibeId},{"$set": {"VibeS3Url" : S3url}},True)


    print (s3Result)
    return s3Result
