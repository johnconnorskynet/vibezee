import json
import string
from urllib.request import urlopen

import unicodedata
from newspaper import Article
from ttstask import stringToVoiceToS3
from pymongo import MongoClient

ApiUrl = "http://cloud.feedly.com"
Mixes = "/v3/mixes/contents?"

# Request to get a mix of the best article for a stream, return a JSON data stream
def mixRequest(streamId,count,hours,backfill,locale):
    Mixesrequest = ApiUrl + Mixes + 'streamId='+ streamId + '&' + 'count='+ count + '&' + 'hours='+ hours + '&' + 'backfill=' + backfill + '&' + 'locale='+locale
    #Call Mixes request
    MixResponse = urlopen(Mixesrequest)
    content = MixResponse.read()
    MixResponseText = content.decode('utf8')
    MixesJsonData = json.loads(MixResponseText)
    return MixResponseText


# Remove all forbidden chars to create file or folder
def removeDisallowedPathnameChars(filename):
    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(chr(c) for c in cleanedFilename if chr(c) in validFilenameChars)

streamid = "feed/http://www.engadget.com/rss-full.xml"

command = 'http://cloud.feedly.com/v3/mixes/contents?streamId='+streamid+'&count=20&hours=2&backfill=1&locale=en'
snippetFilePath = 'polygon.json'
mixesJsonData = mixRequest(streamid, '50', '4', '1', 'en')
mix=json.loads(mixesJsonData)
mongoClient = MongoClient()
vibezeeDb = mongoClient['vibezeeDb']
vibeCollection = vibezeeDb['vibeCollection']

for item in mix['items']:
    url = item['alternate'][0]['href']
    article = Article(url,keep_article_html=True)
    article.download()
    article.parse()
    article.nlp()
    content = item['title']+'. ' + article.summary
    filename = removeDisallowedPathnameChars(item['title']) + '.mp3'
    if vibeCollection.find_one({"id" : item['id']}):
        continue
    mongoVibeId = vibeCollection.insert(item)
    print(mongoVibeId)
    stringToVoiceToS3.delay(content,filename,mongoVibeId)

