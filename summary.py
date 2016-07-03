from bs4 import BeautifulSoup
import nltk
from nltk import sent_tokenize


def getContentArticle(article,numberOfSentences):
    if(article.get('content')):
        soup = BeautifulSoup(article['content']['content'],"html.parser")
        articleContent = soup.get_text()

        contentSplit = sent_tokenize(articleContent)
        if contentSplit.__len__()>numberOfSentences:
            return contentSplit[0:numberOfSentences]
        else:
            return contentSplit

    elif(article.get('summary')):
        soup = BeautifulSoup(article['summary']['content'],"html.parser")
        articleContent = soup.get_text()

        contentSplit = sent_tokenize(articleContent)
        if contentSplit.__len__()>numberOfSentences:
            return contentSplit[0:numberOfSentences]
        else:
            return contentSplit
