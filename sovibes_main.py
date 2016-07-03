from newspaper import Article
from parse_task import parseEntry
from feedlyclient import getMix

streamid = 'feed/http://feeds.gawker.com/kotaku/vip'

jsonMixEntries = getMix(streamid,'20','24','1','en')

for item in jsonMixEntries['items']:
    parseEntry.delay(item)