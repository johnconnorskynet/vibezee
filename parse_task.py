import string
import unicodedata
from celery import Celery
from ttstask import stringToVoiceToS3

parseApp = Celery('parse_task',broker='amqp://ec2-54-208-99-39.compute-1.amazonaws.com:5672')

# Remove all forbidden chars to create file or folder
def removeDisallowedPathnameChars(filename):
    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(chr(c) for c in cleanedFilename if chr(c) in validFilenameChars)

@parseApp.task
def parseEntry(jsonItem):
    print (jsonItem['title'])
    # filename = removeDisallowedPathnameChars(jsonItem['title']) + '.mp3'
    # stringToVoiceToS3.delay(jsonItem['title'],filename)