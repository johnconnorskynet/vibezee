import json
from datetime import datetime, time
from urllib.request import urlopen

ApiUrl = "http://cloud.feedly.com"
Mixes = "/v3/mixes/contents?"
FeedMetadata = "/v3/search/feeds?"
Streams ="/v3/streams/contents?"
Search ="/v3/search/feeds?"

# Request to get a mix of the best article for a stream, return a JSON data stream
def getMix(streamId,count,hours,backfill,locale):
    Mixesrequest = ApiUrl + Mixes + 'streamId='+ streamId + '&' + 'count='+ count + '&' + 'hours='+ hours + '&' + 'backfill=' + backfill + '&' + 'locale='+locale
    #Call Mixes request
    MixResponse = urlopen(Mixesrequest)
    content = MixResponse.read()
    MixResponseText = content.decode('utf8')
    MixesJsonData = json.loads(MixResponseText)
    return MixesJsonData

def getStream( streamId, count, newerThan, continuation, ranked='newest', unreadOnly='0'):
    StreamRequest = ApiUrl + Streams + 'streamId=' + streamId + '&' + 'count='+ count + '&' + 'ranked=' + ranked + '&' + 'unreadOnly=' + unreadOnly + '&' + 'newerThan=' + newerThan +  '&' + 'continuation=' + continuation
    StreamResponse =  urlopen(StreamRequest)
    content = StreamResponse.read()
    StreamResponseText = content.decode('utf8')
    StreamJsonData = json.loads(StreamResponseText)
    return json.dumps(StreamJsonData, sort_keys=True, indent=2)

def searchFeeds(query,  locale, count=20):
    SearchRequest = ApiUrl + Search + 'query=' + query +  '&' + 'count=' + count +  '&' + 'locale=' + locale
    print (SearchRequest)
    SearchResponse = urlopen(SearchRequest)
    content = SearchResponse.read()
    SearchResponseText = content.decode('utf8')
    SearchJsonData = json.loads(SearchResponseText)
    return json.dumps(SearchJsonData, sort_keys=True, indent=2)


def getStreamIds(jsonDataText):
    streamIds = []
    jsonData = json.loads(jsonDataText)
    if jsonData.get('results'):
        for feed in jsonData['results']:
            if feed.get('feedId'):
                streamIds.append(feed['feedId'])
    return streamIds


# searchResults = searchFeeds('%23design','en','500')
# print (searchResults)
# streamIds = getStreamIds(searchResults)
#
# print(streamIds)
# newerthan = str(datetime.now().timestamp()-86400)
# articles = getStream(streamIds[0],'100',newerthan,'')
#
# with open('stream.html','w') as htmlstream :
#     streamsJson =  json.loads(searchResults)
#     velocity = 0.0
#     for stream in streamsJson['results']:
#         if stream.get('contentType'):
#             if stream['contentType']=='longform':
#                 htmlstream.write('<div>')
#                 if stream.get('coverUrl'):
#                     htmlstream.write('<img src='+stream['coverUrl']+' />')
#                     htmlstream.write('<br>')
#                     if stream.get('website'):
#                         htmlstream.write('<a href='+stream['website']+'>'+stream['title']+'</a>')
#                     if stream.get('facebookLikes'):
#                         htmlstream.write('<h1> FacebookLikes : '+str(stream['facebookLikes'])+'</h1>')
#                     if stream.get('twitterFollowers'):
#                         htmlstream.write('<h1> twitterFollowers : ' + str(stream['twitterFollowers']) + '</h1>')
#                     htmlstream.write('<h1> velocity : ' + str(stream['velocity']) + '</h1>')
#                     velocity+=stream['velocity']
#                     htmlstream.write('</div>')
#     htmlstream.write('<h1> Average number of articles per week :' + str(velocity)+'</h1>')
#     htmlstream.write('<h1> Number of streams :' + str(streamIds.__len__()) + '</h1>')
#     htmlstream.close()
#
#
# with open('article.html','w') as htmlarticle :
#     articlesJson =  json.loads(articles)
#
#     for article in articlesJson['items']:
#         htmlarticle.write('<div>')
#         if article.get('visual'):
#             htmlarticle.write('<img src='+article['visual']['url']+' width=400 height=400/>')
#             htmlarticle.write('<br>')
#             htmlarticle.write('<a href='+article['originId']+'>'+article['title']+'</a>')
#             htmlarticle.write('</div>')
#     htmlarticle.close()

