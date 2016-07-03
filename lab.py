import json
import os
import string
import unicodedata
import threading
import webbrowser

import subprocess
import youtube_dl

# import nltk
# import subprocess
# from nltk import sent_tokenize
# from oauth2client.tools import argparser
import urllib
from urllib.request import urlopen

import pyvona
from bs4 import BeautifulSoup
from gtts import gTTS


def formatString(string,lenLineMax):
    splitString =  string.split()
    lenSplitString = splitString.__len__()
    len =0
    for n in range(0,lenSplitString-1):
        splitString[n]+=' '
        len+=splitString[n].__len__()
        if(len>lenLineMax):
            splitString[n-1]+="\n"
            len=splitString[n].__len__()

    return splitString

def mixRequest(streamId,count,hours,backfill,locale):
    Mixesrequest = ApiUrl + Mixes + 'streamId='+ streamId + '&' + 'count='+ count + '&' + 'hours='+ hours + '&' + 'backfill=' + backfill + '&' + 'locale='+locale
    #Call Mixes request
    MixResponse = urlopen(Mixesrequest)
    content = MixResponse.read()
    MixResponseText = content.decode('utf8')
    MixesJsonData = json.loads(MixResponseText)
    return MixesJsonData

# workSpace = os.getcwd()+'\\Archives\\Street Fighter V offline updates will go beyond a story mode\\'
# with open(workSpace+'concatt.txt','w') as outputFile:
#     outputFile.write('file '+ "'"+workSpace +"Street Fighter V offline updates will go beyond a story mode_vibe.mp4"+ "'\n")
#     outputFile.write('file '+ "'" + workSpace + "Street Fighter V offline updates will go beyond a story mode_vibe.mp4"+ "'\ny")
#
# ffmpegCommand = 'ffmpeg -f concat -i ' + '"'+workSpace+ 'concatt.txt"'+ ' -c copy output01.mp4'
# print(ffmpegCommand)
# subprocess.call(ffmpegCommand)

# raise
# sentence ="Floyd Mayweather doesn't care how famous you are -- he's gonna talk smack right to your face ... just ask rapper Jim Jones."
# sentence = ''.join(formatString(sentence,20))
# print (sentence)
# print(sentence[0:5])
# contensplit = sentence.split('.')
# print (contensplit)
#
# contensplit = sent_tokenize(sentence)
# print (contensplit)
# args = argparser.parse_args()
# youtube = youtubeclient.get_authenticated_service(args)
# youtubeclient.upload_vibe(youtube,'C:\\Users\\belgaloo\\PycharmProjects\\SoVibes\\snippet.json')

# def renderPrint(streamId):
#     print (streamId)
#     count = 0
#     count+=1
#
# try:
#     for i in range(0,3):
#         t = threading.Thread(target=renderPrint("streamId : "+i))
#         t.start()
#
# except:
#     print ("error spawning thread")

# Initialize ivona voice
def initYvonaTtsEngine ():
    ivonaVoice = pyvona.create_voice("GDNAJVR7DOF5M332VY3Q","RMlAiEzHBrFdXY0lP7TLjKptE0SjCbBcgEzVPHDz")
    ivonaVoice.sentence_break=1000
    ivonaVoice.voice_name='Salli'
    # ivonaVoice.voice_name='Mathieu'
    ivonaVoice._codec='mp3'
    return ivonaVoice

# # Init et get instance of an ivonaVoice
# ivonaVoice = initYvonaTtsEngine()
#
# # Text to speech, return the filepath of the tts file
# def stringToVoice(string,filePath,ivonaVoice):
#     ivonaVoice.fetch_voice(string,filePath)
#     return filePath
# stringtospeech = "Thanks to the Paramount Vault Millennium Actress, one of anime director Satoshi Kon's feature films, is now available to watch on YouTube for free. " \
#                  "The 2002 film is the latest addition to the Paramount Vault, a collection of full-length movies and short clips, all viewable for free. " \
#                  "The sci-fi fantasy follows the titular actress as she recounts her career to a documentary film crew. Like other Kon films, the story gets more bizarre from there, thanks to its non-linear, time-traveling narrative. " \
#                  "The entire movie is streaming in its original Japanese and includes English subtitles. Millennium Actress is one of the more acclaimed films featured in the Paramount Vault, which teases the inclusion of Clueless, Airplane! and other classics in a trailer featured on the channel. " \
#                  "Among the few other films of note available to stream are Masters of the Universe and The Texas Chainsaw Massacre 2. " \
#                  "Kon was well regarded by anime and art film fans alike for his unconventional storytelling. Millennium Actress followed Perfect Blue, his debut feature from 1998 that inspired Western films like Requiem for a Dream. " \
#                  "Perhaps his best known work is 2006's Paprika, a movie about detectives who travel inside of dreams. "
#
# stringToVoice(stringtospeech,"ttsVoice.mp3",ivonaVoice)
#
# html = "<img alt=\"\" src=\"https://cdn3.vox-cdn.com/thumbor/d_W6eXI7zIkim1KUyKbBh9yzbMc=/9x43:725x446/640x360/cdn0.vox-cdn.com/uploads/chorus_image/image/49614785/Screen_Shot_2016-05-17_at_5.09.53_PM.0.0.png\">\n<p>Thanks to the Paramount Vault</p> <p><i>Millennium Actress</i>, one of anime director Satoshi Kon's feature films, is now available to watch on YouTube for free. The 2002 film is the latest addition to <a target=\"_blank\" href=\"https://www.youtube.com/c/paramountvault\">the Paramount Vault</a>, a collection of full-length movies and short clips, all viewable for free.</p>\n<p>The sci-fi fantasy follows the titular actress as she recounts her career to a documentary film crew. Like other Kon films, the story gets more bizarre from there, thanks to its non-linear, time-traveling narrative. The entire movie is streaming in its original Japanese and includes English subtitles; you can check it out above.</p>\n<p><i>Millennium Actress</i> is one of the<a target=\"_blank\" href=\"http://www.nytimes.com/movie/review?res=9A07EED6133BF931A2575AC0A9659C8B63\"> more acclaimed</a> films featured in the Paramount Vault, which teases the inclusion of <i>Clueless,</i> <i>Airplane! </i>and other classics in <a target=\"_blank\" href=\"https://www.youtube.com/watch?v=PayN4UpPzOA\">a trailer </a>featured on the channel. Among the few other films of note available to stream are <i>Masters of the Universe</i> and <i>The Texas Chainsaw Massacre 2</i>.</p>\n<p>Kon was well regarded by anime and art film fans alike for his unconventional storytelling. <i>Millennium Actress </i>followed <i>Perfect Blue</i>, his debut feature from 1998 that <a target=\"_blank\" href=\"http://www.dazeddigital.com/artsandculture/article/26075/1/the-cult-japanese-filmmaker-that-inspired-darren-aronofsky\">inspired Western films</a> like <i>Requiem for a Dream</i>. Perhaps his best known work is 2006's <i>Paprika</i>, a movie about detectives who travel inside of dreams. <a target=\"_blank\" href=\"http://www.rogerebert.com/scanners/inception-has-christopher-nolan-forgotten-how-to-dream\">American critics like Roger Ebert </a>regularly cited parallels between it and <i>Inception</i>, Christopher Nolan's later live-action film.</p>\n<p>Although Kon died from cancer in 2010, leaving behind an unfinished film, his work continues to be the subject of critical study and praise. The video below, from 2014, shows some of the cinematic techniques the director used to make a mark on anime — and film overall.</p>\n<p><iframe height=\"360\" width=\"640\" src=\"https://player.vimeo.com/video/101675469?color=f0a400\"></iframe></p>"
#
# soup = BeautifulSoup(html,"html.parser")
#
# href_tags = soup.find_all('iframe')
# print (href_tags[0].attrs['src'])
#
#
# print (href_tags)
#
# youtubeDownloader  = youtube_dl.YoutubeDL({'nocheckcertificate': True})
# youtubeDownloader.extract_info("https://www.youtube.com/watch?v=KSZ4tSoumNk",download=True)
# url="http://www.engadget.com/2016/05/30/asus-transformer-pc/"
# html = urlopen(url)
# soup = BeautifulSoup(html,"html.parser")
# href_tags = soup.find_all('iframe')
#
# for iframe in href_tags:
#     print (iframe)
# image_tags = soup.find_all('img')
#
# for image in image_tags:
#     print(image)
#
# with open('iframe.html','w') as outputFile:
#     for iframe in href_tags:
#         outputFile.write(str(iframe)+'<br>')
#     for image in image_tags:
#         outputFile.write(str(image)+'<br>')
#
# outputFile.close()
# print('file://' + os.getcwd()+'/iframe.html')
#
#
# youtubeDownloader  = youtube_dl.YoutubeDL({'nocheckcertificate': True})
# for iframe in href_tags:
#     try:
#
#         if 'data-recommend-id' not in str(iframe) :
#             youtubeDownloader.extract_info(iframe.attrs['src'], download=True)
#         else:
#
#             id = str(iframe.attrs['data-recommend-id']).replace('youtube://','')
#             youtubeDownloader.extract_info('https://www.youtube.com/watch?v='+id,download=True)
#
#     except:
#         continue


# tts=gTTS('新华社北京5月31日电 在“六一”国际儿童节即将到来之际，中共中央总书记、国家主席、中央军委主席习近平给大陈岛老垦荒队员的后代、浙江省台州市椒江区12名小学生回信，祝他们节日快乐，祝全国小朋友节日快乐。', lang='zh-cn')
# tts.save('chinese.mp3')

imagelocation = (0,1,2)
print (imagelocation[1])