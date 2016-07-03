import json
import os
import string
from urllib.request import urlopen
import pyvona
import urllib
import unicodedata
from oauth2client.tools import argparser
import summary
import subprocess
import youtubeclient







# Initialize ivona voice
def initYvonaTtsEngine ():
    ivonaVoice = pyvona.create_voice("GDNAJVR7DOF5M332VY3Q","RMlAiEzHBrFdXY0lP7TLjKptE0SjCbBcgEzVPHDz")
    ivonaVoice.sentence_break=1000
    ivonaVoice.voice_name='Salli'
    # ivonaVoice.voice_name='Mathieu'
    ivonaVoice._codec='mp3'
    return ivonaVoice

# Text to speech, return the filepath of the tts file
def stringToVoice(string,filePath,ivonaVoice):
    ivonaVoice.fetch_voice(string,filePath)
    return filePath

# Request to get feed information
def feedRequest(feedId):
    FeedRequestBody =  ApiUrl +FeedMetadata
    FeedRequest = FeedRequestBody + 'query=' + feedId
    FeedResponse = urlopen(FeedRequest)
    FeedContent = FeedResponse.read()
    FeedResponseText = FeedContent.decode('utf8')
    FeedJsonData = json.loads(FeedResponseText)
    return FeedJsonData

# Request to get a mix of the best article for a stream, return a JSON data stream
def mixRequest(streamId,count,hours,backfill,locale):
    Mixesrequest = ApiUrl + Mixes + 'streamId='+ streamId + '&' + 'count='+ count + '&' + 'hours='+ hours + '&' + 'backfill=' + backfill + '&' + 'locale='+locale
    #Call Mixes request
    MixResponse = urlopen(Mixesrequest)
    content = MixResponse.read()
    MixResponseText = content.decode('utf8')
    MixesJsonData = json.loads(MixResponseText)
    return MixesJsonData

#Download the article visual
def downloadVisualArticle(article,filePath):

    articleTitle = getArticleTitle(article)
    articleTitleCleaned = removeDisallowedPathnameChars(articleTitle)
    articleVisualFileName = articleTitleCleaned+'.jpg'
    if(os.path.exists(filePath + articleVisualFileName)):
        return filePath + articleVisualFileName
    # articleVisualFileName = article['fingerprint']+'.jpg'
    #Donwload Visual to ArticleVisual folder
    try:
        urllib.request.urlretrieve(article['visual']['url'], filePath +'\\' + articleVisualFileName)
    except:
        pass
    finally:
        pass
    return filePath + articleVisualFileName

# Download the feed icon
def downloadFeedIcon (article,filePath):
    feedName = article['origin']['title']
    feedIconFileName = feedName+'.png'
    if(os.path.exists(filePath + feedIconFileName)):
        return filePath + feedIconFileName
    if article.get('webfeeds'):
        try:
            urllib.request.urlretrieve(article['webfeeds']['logo'], filePath +'\\' + feedIconFileName)
        except:
            pass
        finally:
            pass
    else:
        feedIconFileName = feedName+'.jpg'
        feedJsonData = feedRequest(streamId)
        if feedJsonData.get('results'):
            try:
                visualUrl = feedJsonData['results'][0]['visualUrl']
                urllib.request.urlretrieve(feedJsonData['results'][0]['visualUrl'], filePath +'\\' + feedIconFileName)
            except:
                pass
            finally:
                pass
    return filePath + feedIconFileName

# Remove all forbidden chars to create file or folder
def removeDisallowedPathnameChars(filename):
    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(chr(c) for c in cleanedFilename if chr(c) in validFilenameChars)

# Create the directory tree of working space
def initWorkSpace(articleTitle) :
    cleanedFolderName = removeDisallowedPathnameChars(articleTitle)
    workingSpacePath = os.getcwd()+'\\'+cleanedFolderName+'\\'
    workingSpaceGraphicsPath = workingSpacePath+'graphics'
    workingSpaceAudioPath = workingSpacePath+'audio'
    if not os.path.exists(workingSpacePath):
        os.makedirs(workingSpacePath)
        os.makedirs(workingSpaceGraphicsPath)
        os.makedirs(workingSpaceAudioPath)
        return workingSpacePath
    else :
        return workingSpacePath

def getArticleTitle (article):
    return article['title']

def getFeedName (article):
    return  article['origin']['title']

# Create scene json description file for vibe introduction
def createIntroRenderFile(workSpacePath,articleTitle,articleSource,articleVisualFilePath,feedIconFilePath):
    with open(os.getcwd()+'\\blender pattern\\pattern_vibes_desktop_intro.json') as data_file:
        jsonData = json.load(data_file)
        for blender_object in jsonData['blender_objects']:
            if(blender_object['object_name']=="title"):
                blender_object['string']=articleTitle
            elif (blender_object['object_name']=="source"):
                blender_object['string']=articleSource
            elif (blender_object['object_name']=="feed_icon"):
                blender_object['image_file_path']=feedIconFilePath
            elif (blender_object['object_name']=="article_visual"):
                blender_object['image_file_path']=articleVisualFilePath

    with open(workSpacePath+'\\pattern_vibes_desktop_intro.json',"w") as data_file_modified:
        data_file_modified.write(json.dumps(jsonData))


# Create scene json description file for vibe page
def createPageRenderFile(workSpacePath,sentence,feedName,articleVisualFilePath,feedIconFilePath):
    with open(os.getcwd()+'\\blender pattern\\pattern_vibes_desktop_page.json') as data_file:
        jsonData = json.load(data_file)
        for blender_object in jsonData['blender_objects']:
            if(blender_object['object_name']=="title"):
                blender_object['string']=sentence
            elif (blender_object['object_name']=="source"):
                blender_object['string']=feedName
            elif (blender_object['object_name']=="feed_icon"):
                blender_object['image_file_path']=feedIconFilePath
            elif (blender_object['object_name']=="article_visual"):
                blender_object['image_file_path']=articleVisualFilePath

    with open(workSpacePath+'\\pattern_vibes_desktop_page.json',"w") as data_file_modified:
        data_file_modified.write(json.dumps(jsonData))

# Create introduction for vibe article
def createVibeIntro(article):
    articleTitle = getArticleTitle(article)
    # Build article title tts file filepath
    articleTitleFileName = removeDisallowedPathnameChars(articleTitle)

    # Build tts file path
    articleTitleAudioFilePath = workSpaceAudio + articleTitleFileName[0:9]+'.mp3'

    # Build video file path
    articleTitleVideoFilePath = workSpace + articleTitleFileName+'.mp4'
    # if the vibe already exists stop
    vibeFilePath = workSpace+articleTitleFileName+'_vibe.mp4'
    if os.path.exists(vibeFilePath):
        return vibeFilePath

    #TTS article title
    stringToVoice(articleTitle,articleTitleAudioFilePath,ivonaVoice)

    #Download article graphics
    articleVisualFilePath = downloadVisualArticle(article,workSpaceGraphics)

     # If the article has no visual no need to vibe it
    if(os.path.exists(articleVisualFilePath)):
        #Download feed icon
        feedIconFilePath = downloadFeedIcon(article,workSpaceGraphics)

        # Create render file description
        createIntroRenderFile(workSpace,articleTitle,getFeedName(article),articleVisualFilePath,feedIconFilePath)

        #Render the vibe
        print('blender -b "blender pattern\pattern_vibes_desktop_intro.blend" -P blender_render_desktop_intro.py -- '+'"'+workSpace+'\\pattern_vibes_desktop_intro.json"'
                        +' --output '+ '"'+articleTitleVideoFilePath+'"')
        subprocess.call('blender -b "blender pattern\pattern_vibes_desktop_intro.blend" -P blender_render_desktop_intro.py -- '+'"'+workSpace+'\\pattern_vibes_desktop_intro.json"'
                        +' --output '+ '"'+articleTitleVideoFilePath+'"')


        if(os.path.exists(articleTitleAudioFilePath) and os.path.exists(articleTitleVideoFilePath)):

            print('ffmpeg -i  '+'"'+articleTitleVideoFilePath+'"'+ ' -i '  +'"'+articleTitleAudioFilePath+'"'+ ' "'+vibeFilePath+'"')
            subprocess.call('ffmpeg -i  '+'"'+articleTitleVideoFilePath+'"'+ ' -i '  +'"'+articleTitleAudioFilePath+'"'+ ' "'+vibeFilePath+'"')

    return vibeFilePath

# Create page vibe for a sentence of an article
def createVibePages(article):

    articleSentenceList=[]
    articleSentenceList = summary.getContentArticle(article,2)
    vibePagesFilePathList=[]
    if not articleSentenceList:
        return vibePagesFilePathList
    for sentence in articleSentenceList:
        if sentence == "Read more" or sentence == "Continue reading...":
            continue
        sentenceCleaned = removeDisallowedPathnameChars(sentence)
        sentenceAudioFilePath = workSpaceAudio + sentenceCleaned[0:9] +'.mp3'
        # Build video file path
        pageVideoFilePath = workSpace + sentenceCleaned[0:9]+'.mp4'
        # If the vibe already exist continue
        vibeFilePath = workSpace+sentenceCleaned[0:9]+'_vibe.mp4'
        if os.path.exists(vibeFilePath):
            vibePagesFilePathList.append(vibeFilePath)
            continue
        #TTS article title
        stringToVoice(sentence,sentenceAudioFilePath,ivonaVoice)

        #Download article graphics
        articleVisualFilePath = downloadVisualArticle(article,workSpaceGraphics)

        # If the article has no visual no need to vibe it
        if(os.path.exists(articleVisualFilePath)):
            #Download feed icon
            feedIconFilePath = downloadFeedIcon(article,workSpaceGraphics)
            # Create render file description
            createPageRenderFile(workSpace,sentence,getFeedName(article),articleVisualFilePath,feedIconFilePath)

            #Render the vibe
            print('blender -b "blender pattern\pattern_vibes_desktop_page.blend" -P blender_render_desktop_intro.py -- '+'"'+workSpace+'\\pattern_vibes_desktop_page.json"'
                            +' --output '+ '"'+pageVideoFilePath+'"')
            subprocess.call('blender -b "blender pattern\pattern_vibes_desktop_page.blend" -P blender_render_desktop_intro.py -- '+'"'+workSpace+'\\pattern_vibes_desktop_page.json" '
                            '--time 2 '+' --output '+ '"'+pageVideoFilePath+'"')


        if(os.path.exists(sentenceAudioFilePath) and os.path.exists(pageVideoFilePath)):
            print('ffmpeg -i  '+'"'+pageVideoFilePath+'"'+ ' -i '  +'"'+sentenceAudioFilePath+'"'+ ' "'+vibeFilePath+'"')
            subprocess.call('ffmpeg -i  '+'"'+pageVideoFilePath+'"'+ ' -i '  +'"'+sentenceAudioFilePath+'"'+ ' "'+vibeFilePath+'"')
        vibePagesFilePathList.append(vibeFilePath)

    return vibePagesFilePathList

# Stitch Mp4 video
def stitchMp4Video(filePathList,stitchedVideoFilePath):
    with open(workSpace+'concat_mp4.txt','w') as outputFile:
        for filePath in filePathList:
            outputFile.write('file '+ "'" + filePath +"'\n")
        outputFile.close()
        ffmpegCommand = 'ffmpeg -f concat -i ' + '"'+workSpace+ 'concat_mp4.txt"'+ ' -c copy '+ '"'+stitchedVideoFilePath+ '"'
        print(ffmpegCommand)
        subprocess.call(ffmpegCommand)
    return stitchedVideoFilePath

def saveArticleData(article, workSpace):
    articleTitle = getArticleTitle(article)
    articleTitle = removeDisallowedPathnameChars(articleTitle)
    articleDataFilePath = workSpace+articleTitle+'.json'

    with open(articleDataFilePath,'w') as outputFile:
        json.dump(article,outputFile)
    return articleDataFilePath

def getVibeDescription(article):
    description = ""
    articleSentenceList = summary.getContentArticle(article,2)
    if articleSentenceList:
        description += ''.join(articleSentenceList)

    description += '\n To read the article click on: \n' + article['alternate'][0]['href'] + '\n'
    description += 'Subscribe to SoVibes channel and get daily teasers of articles from all around the web!!!'
    return  description


def createSnippetUploadFile(article,vibeFilePath):
    vibefilepath = vibeFilePath
    title = getArticleTitle(article)[0:99]
    description = getVibeDescription(article)
    if article.get('keywords'):
        tags = article['keywords']
    else:
        tags =[]
    categoryId = 22
    privacyStatus = 'public'

    snippetUploadFilePath = workSpace+'snippetUpload.json'
    with open(snippetUploadFilePath,"w") as snippetFile:
        json.dump({
            'vibefilepath':vibefilepath,
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': categoryId,
            'privacyStatus': privacyStatus
        },snippetFile,indent=4)
        snippetFile.close()
    return snippetUploadFilePath

# Init et get instance of an ivonaVoice
ivonaVoice = initYvonaTtsEngine()
articleVisualFilePath=""
feedIconFilePath=""


# Mix request default parameter
count = "2"
hours = "2"
backfill = "1"
locale = "en"

#streamId = "feed/http://www.engadget.com/rss-full.xml"
# streamId = "feed/http://omg.yahoo.com/latest/rss/news"
# streamId = "feed/http://feeds.gawker.com/lifehacker/vip"

techStreamIdList = ["feed/http://feeds.feedburner.com/Techcrunch",
                    "feed/http://www.engadget.com/rss-full.xml",
                    "feed/http://feeds.wired.com/wired/index",
                    "feed/http://feeds.mashable.com/Mashable",
                    "feed/http://feeds.arstechnica.com/arstechnica/index/"]

businessStreamIdList =["feed/http://sethgodin.typepad.com/seths_blog/atom.xml",
                       "feed/http://feeds2.feedburner.com/businessinsider",
                       "feed/http://feeds.feedburner.com/entrepreneur/latest",
                       "feed/http://feeds.harvardbusiness.org/harvardbusiness/",
                       "feed/http://feeds.feedburner.com/fastcompany/headlines"]

newsStreamIdList =[ "feed/http://rss.cnn.com/rss/cnn_topstories.rss",
                    "feed/http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml",
                    "feed/http://www.npr.org/rss/rss.php?id=1001",
                    "feed/http://feeds.abcnews.com/abcnews/topstories",
                    "feed/http://feeds.huffingtonpost.com/huffingtonpost/LatestNews"]

sportStreamIdList = ["feed/http://newsrss.bbc.co.uk/rss/sportonline_world_edition/front_page/rss.xml",
                     "feed/http://www.skysports.com/rss/0,20514,11095,00.xml",
                     "feed/http://www.skysports.com/rss/0,20514,11095,00.xml",
                     "feed/http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/football/rss.xml",
                     "feed/http://www.nfl.com/rss/rsslanding?searchString=home",
                     "feed/http://www.nba.com/rss/nba_rss.xml"]

celebrityStreamIdList=["feed/http://rss.news.yahoo.com/rss/celebrity",
                       "feed/http://rss.people.com/web/people/rss/topheadlines/index.xml",
                       "feed/http://wonderwall.msn.com/rss/all.xml"]

gamingStreamIdList =["feed/http://feeds.gawker.com/kotaku/vip",
                     "feed/http://www.gamespot.com/rss/game_updates.php",
                     "feed/http://feeds.ign.com/ign/games-all",
                     "feed/http://n4g.com/rss/news?channel=&sort=latest",
                     "feed/http://www.polygon.com/rss/index.xml"]

# # Fashion
# fashionStreamIdList = ["feed/http://www.fashionsquad.com/feed/",
#                 "feed/http://feeds.feedburner.com/fashionistacom"
#                 "feed/http://feeds2.feedburner.com/TheArtOfManliness"
#                 ]

# celebrityStreamIdList,techStreamIdList,
themeList = [celebrityStreamIdList,gamingStreamIdList,techStreamIdList,newsStreamIdList,businessStreamIdList,sportStreamIdList]
# themeList = [gamingStreamIdList]
for streamIdList in themeList:
    for streamId in streamIdList:
        # Request mix of best article
        mixesJsonData = mixRequest(streamId,count,hours,backfill,locale)

        # Create for each article its vibe
        for article in mixesJsonData['items']:

            # Init vibe workspace
            description = ""
            description += '\nTo read the article click on: \n' + article['alternate'][0]['href'] + '\n'
            description += 'Subscribe to SoVibes channel and everyday get teasers of articles from all around the web!!!'
            print (description)
            articleTitle = getArticleTitle(article)
            workSpace = initWorkSpace(articleTitle)
            workSpaceGraphics = workSpace+'graphics\\'
            workSpaceAudio = workSpace+'audio\\'


            vibePagesFilePaths = []
            articleTitleFileName = removeDisallowedPathnameChars(articleTitle)
            articleTitleVideoFilePath = workSpace + articleTitleFileName+'.mp4'

            vibeIntroFilePath = createVibeIntro(article)
            if not os.path.exists(vibeIntroFilePath):
                print ("No visual, no vibe")
                continue


            saveArticleData(article,workSpace)

            vibePagesFilePaths = createVibePages(article)

            vibePagesFilePaths.insert(0,vibeIntroFilePath)

            stitchedVideoFilePath = workSpace + articleTitleFileName + "_stitched_vibe.mp4"
            if os.path.exists(stitchedVideoFilePath):
                print ("vibe already exists")
                continue
            if stitchedVideoFilePath.__len__()>256:
                stitchedVideoFilePath = workSpace + articleTitleFileName[0:9] +  "_stitched_vibe.mp4"
                if os.path.exists(stitchedVideoFilePath):
                    print ("vibe already exists")
                    continue
            finalVideoFilePath = workSpace + articleTitle + "_vibe_final.mp4"
            if not os.path.exists(stitchedVideoFilePath):
                stitchMp4Video(vibePagesFilePaths,stitchedVideoFilePath)

            snippetFilPath = createSnippetUploadFile(article,stitchedVideoFilePath)
            if os.path.exists(snippetFilPath):
                args = argparser.parse_args()
                youtube = youtubeclient.get_authenticated_service(args)
                youtubeclient.upload_vibe(youtube,snippetFilPath)

            # if os.path.exists(stitchedVideoFilePath):
            #     backgroundAudioFilePath = os.getcwd()+'\\vibe background music\\Sweltering Days_R48K_V50.mp3'
            #     if os.path.exists(backgroundAudioFilePath):
            #         audioVibeFilePath = workSpaceAudio+ articleTitle + "_audio_vibe.mp3"
            #         subprocess.call('ffmpeg-i  '+'"'+stitchedVideoFilePath+'"' + '"'+audioVibeFilePath+'"')
            #         audioVibeFinalFilePath = workSpaceAudio+ articleTitle + "_audio_vibe_final.mp3"
            #         print('ffmpeg -i  '+'"'+audioVibeFilePath+'"'+ ' -i '  +'"'+backgroundAudioFilePath+'"'+' -filter_complex amix=inputs=2:duration=shortest -c:a libmp3lame '+ '"'+audioVibeFinalFilePath+'"')
            #         subprocess.call('ffmpeg-i  '+'"'+audioVibeFilePath+'"'+ ' -i '  +'"'+backgroundAudioFilePath+'"'+' -filter_complex amix=inputs=2:duration=shortest -c:a libmp3lame '+ '"'+audioVibeFinalFilePath+'"')












