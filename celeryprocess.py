from tasks import downloadMedia
import os
from datetime import datetime
import json
from urllib.request import urlopen
import stat

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

gamingStreamIdList =["feed/http://feeds.gawker.com/kotaku/vip"]
topimageurls=[]
i =0

for streamid in gamingStreamIdList:
    print (i)
    i+=1
    command = 'http://cloud.feedly.com/v3/mixes/contents?streamId='+streamid+'&count=20&hours=2&backfill=1&locale=en'
    snippetFilePath = 'polygon.json'
    mixesJsonData = mixRequest(streamid, '50', '2', '1', 'en')
    j=json.loads(mixesJsonData)
    for item in j['items']:
        if item.get('visual'):
            topimageurls.append(item['visual']['url'])



for topimageurl in topimageurls:
    downloadMedia.delay(topimageurl)