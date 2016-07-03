import json
import os
import urllib
from datetime import datetime
import re
from urllib.request import urlopen

import youtube_dl
from bs4 import BeautifulSoup
from gtts import gTTS
from newspaper import Article

gamingStreamIdList =["feed/http://feeds.abcnews.com/abcnews/topstories"]
# gamingStreamIdList =["feed/http://feeds.gawker.com/kotaku/vip"]
              #        "feed/http://www.gamespot.com/rss/game_updates.php",
              #        "feed/http://feeds.ign.com/ign/games-all",
              #        "feed/http://n4g.com/rss/news?channel=&sort=latest",
              #        "feed/http://www.polygon.com/rss/index.xml"
		     # "feed/http://feeds.feedburner.com/Techcrunch",
              #        "feed/http://www.engadget.com/rss-full.xml",
              #        "feed/http://feeds.wired.com/wired/index",
              #        "feed/http://feeds.mashable.com/Mashable",
              #        "feed/http://feeds.arstechnica.com/arstechnica/index/",
		     # "feed/http://sethgodin.typepad.com/seths_blog/atom.xml",
              #        "feed/http://feeds2.feedburner.com/businessinsider",
              #        "feed/http://feeds.feedburner.com/entrepreneur/latest",
              #        "feed/http://feeds.harvardbusiness.org/harvardbusiness/",
              #        "feed/http://feeds.feedburner.com/fastcompany/headlines",
		     # "feed/http://rss.cnn.com/rss/cnn_topstories.rss",
              #        "feed/http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml",
              #        "feed/http://www.npr.org/rss/rss.php?id=1001",
              #        "feed/http://feeds.abcnews.com/abcnews/topstories",
		     # "feed/http://newsrss.bbc.co.uk/rss/sportonline_world_edition/front_page/rss.xml",
              #        "feed/http://www.skysports.com/rss/0,20514,11095,00.xml",
              #        "feed/http://www.skysports.com/rss/0,20514,11095,00.xml",
              #        "feed/http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/football/rss.xml",
              #        "feed/http://www.nfl.com/rss/rsslanding?searchString=home",
              #        "feed/http://www.nba.com/rss/nba_rss.xml",
		     # "feed/http://rss.news.yahoo.com/rss/celebrity",
              #        "feed/http://rss.people.com/web/people/rss/topheadlines/index.xml",
              #        "feed/http://wonderwall.msn.com/rss/all.xml"]

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


def containsYoutubeVideo(url):
    ytubeUrls =[]
    try:
        html = urlopen(url)
    except:
        return youtubeUrls
    soup = BeautifulSoup(html, "html.parser")
    href_tags = soup.find_all('iframe')
    for iframe in href_tags:
        if ' src' in str(iframe):
            if 'youtube' in str(iframe.attrs['src']):
                youtubeUrls.append(str(iframe.attrs['src']))
        if 'data-recommend-id' in str(iframe):
            id = str(iframe.attrs['data-recommend-id']).replace('youtube://', '')
            ytubeUrls.append('https://www.youtube.com/watch?v=' + id)

    return ytubeUrls


urls=[]
print (gamingStreamIdList.__len__())
i=0
topimageurls=[]
for streamid in gamingStreamIdList:
    print (i)
    i+=1
    command = 'http://cloud.feedly.com/v3/mixes/contents?streamId='+streamid+'&count=20&hours=2&backfill=1&locale=en'
    snippetFilePath = 'polygon.json'
    mixesJsonData = mixRequest(streamid, '50', '2', '1', 'en')
    j=json.loads(mixesJsonData)
    for item in j['items']:
        if j.get('alternate'):
            urls.append(item['alternate'][0]['href'])
        if item.get('visual'):
            topimageurls.append(item['visual']['url'])

# downloadpath = os.getcwd()+'/'+str(datetime.now().timestamp())
# os.makedirs(downloadpath)
# for topimageurl in topimageurls:
#     topimageurlsplit = topimageurl.split('/')
#     imagefilepath = downloadpath+ '/' + topimageurlsplit[topimageurlsplit.__len__()-1]
#     try:
#         urllib.request.urlretrieve(topimageurl,imagefilepath)
#     except:
#         continue


urlsWithYoutubeVideo=[]
youtubeUrls=[]


i=0
data = {}
data["title"] = ""
data["description"] = None
data["favicon"] = None
data["facebook"] = {}
data["twitter"] = {}


youtubeDownloader  = youtube_dl.YoutubeDL({'nocheckcertificate': True, 'max-filesize' : '250m', 'f' : str(22).encode('utf-8')})

for url in urls:
    i+=1
    print(url)

    html = urlopen(url)




    soup = BeautifulSoup(html, "html.parser")
    href_tags = soup.find_all('iframe')
    print (url)
    if soup.findAll('iframe', attrs={'data-recommend-id': re.compile("^youtube")}):
        for tag in soup.findAll('iframe', attrs={'data-recommend-id': re.compile("^youtube")}):
            if 'data-recommend-id' in tag.attrs:
                id_youtube = str(tag['data-recommend-id']).replace('youtube://','')
                print('   https://www.youtube.com/watch?v='+id_youtube)
                try:
                    infos = youtubeDownloader.extract_info('https://www.youtube.com/watch?v=' + id_youtube,False)
                except:
                    continue
                print ('Video duration :' + str(infos['duration']/60) + ' min')
                if infos['duration']<600:
                    try:
                        youtubeDownloader.extract_info('https://www.youtube.com/watch?v=' + id_youtube, True)
                    except:
                        continue
                print ('https://www.youtube.com/watch?v='+id_youtube+' downloading')


    if soup.findAll('iframe', attrs={'class': re.compile("^youtube")}):
        for tag in soup.findAll('iframe', attrs={'class': re.compile("^youtube")}):
            if 'src' in tag.attrs:
                id_youtube = str(tag['src']).split('?')[0]
                print(id_youtube)

    if soup.findAll('video', attrs={'src': re.compile("^http")}):
        for tag in soup.findAll('video', attrs={'src': re.compile("^http")}):
            if 'src' in tag.attrs:
                print('  ' + str(tag['src']))


    # if soup.findAll('a', attrs={'href' : re.compile("^http")}):
    #     for tag in soup.findAll('a', attrs={'href' : re.compile("^http")}):
    #         print(str(tag['href']))
    #
    # if soup.findAll('div', attrs={'class': re.compile("^player")}):
    #     for tag in soup.findAll('div', attrs={'class': re.compile("^player")}):
    #         if 'data-config' in tag.attrs:
    #             print('  ' + str(tag['data-config']))

    # if soup.findAll('meta', attrs={'name': re.compile("^twitter")}):
    #     for tag in soup.findAll('meta', attrs={'name': re.compile("^twitter")}):
    #         tag_type = tag['name']
    #         if 'content' in tag.attrs:
    #             data["twitter"][tag_type] = tag['content']
    #             if tag_type == "twitter:description" and data["description"] is None:
    #                 data["description"] = tag["content"]
    # # print(data)
    #
    # if soup.findAll('img', attrs={'src': re.compile("^http")}):
    #     for tag in soup.findAll('img', attrs={'class': re.compile("^Natural")}):
    #         if 'data_srcset' in tag.attrs:
    #             print(tag['data_srcset'])
    #
    # if soup.findAll('iframe', attrs={'id': re.compile("^twitter")}):
    #     for tag in soup.findAll('iframe', attrs={'id': re.compile("^twitter")}):
    #         if 'id' in tag.attrs:
    #             print(tag['id'])
    #
    # if soup.findAll('img', attrs={'src': re.compile("^")}):
    #     for tag in soup.findAll('img', attrs={'src': re.compile("^")}):
    #         if 'data-webm-src' in tag.attrs:
    #             print(tag['data-webm-src'])

    # for iframe in href_tags:
    #     print(iframe)
    #     iframeChildren = iframe.findChildren()
    #     for iframechild in iframeChildren:
    #         print(iframechild)
    # article = Article(url,keep_article_html=True)
    # article.download()
    # # print(article.html)
    # article.parse()
    # with open(str(i)+'.html','w') as article_html:
    #     article_html.write('<a href='+url+'> link</a>')
    #     article_html.write(article.html)
    #     # article_html.write(html)






    # print('Title : '+ article.title)
    #
    # article.nlp()
    # print('Keywords : ')
    # for keyword in article.keywords :
    #     print(keyword)
    # print('Text : ' + article.summary)
    # print('Image links :')
    #
    # for imageurl in article.images:
    #     print (imageurl)
    # print('Movie links :' )
    # for videourl in article.movies :
    #     print (videourl)
    # print('\n\n\n')


#
# for url in urls:
#     tubeUrls = containsYoutubeVideo(url)
#     if tubeUrls:
#         print('url containing youtube video : '+url)
#         urlsWithYoutubeVideo.append(url)
#         youtubeUrls.append(tubeUrls)
#
# print (urlsWithYoutubeVideo)
