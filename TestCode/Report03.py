import xml.sax
import string
import re
import datetime
import random
import pandas as pd

class SoccerContentHandler(xml.sax.ContentHandler):

    buffer = []
    soccerPlayer = False

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.currentData = ""
        self.cursor = {}
        self.players = 0
 
    def startElement(self, name, attrs):
        self.currentData = name
 
    def endElement(self, name):
        if name == "page" and 'TemplateName' in self.cursor:
            self.buffer.append(self.cursor)
        if name == "page":
            self.players+=1;
            self.soccerPlayer = False
            self.cursor = {}

        
 
    def characters(self, content):
        if self.currentData == "title" and not 'PageTitle' in self.cursor:
            self.cursor['PageTitle'] = content

        if self.currentData == "id" and not 'PageID' in self.cursor: 
            self.cursor['PageID'] = content

        if self.currentData == "text" and bool(re.search('축구 선수 정보',content)):
            self.cursor['TemplateName'] = '축구 선수 정보'
            self.soccerPlayer = True
            print(self.players)

        if self.soccerPlayer :
            if self.currentData == "text" and bool(re.search('출생일',content)):
                birth = re.findall("\d+", content)
                print(birth)
                if len(birth) == 3 :
                    if bool(re.match('^(19|20)\d{2}-(0[1-9]|1[012]|[1-9])-(0[1-9]|[12][0-9]|3[0-1]|[1-9])$', "".join(birth))) :
                        self.cursor['DateofBirth'] = datetime.date(int(birth[0]),int(birth[1]),int(birth[2])).isoformat()

            if self.currentData == "text" and bool(re.search('키',content)) and not 'Height' in self.cursor:
                trimtext = content.replace(" ", "")
                if bool(re.search('키=',trimtext)):
                    filter = re.sub('\?|\.|\!|\/|\;|\:|\[|\]','',trimtext)
                    height = re.findall("\d+", filter)
                    if len(height) > 0:
                        self.cursor['Height'] = int(height[0])

            if self.currentData == "text" and bool(re.search('현 소속팀',content)) and not 'Team' in self.cursor:
                str = re.search('\[\[([^\)]+)\]\]', content)
                if bool(str):
                    result = re.sub('\?|\.|\!|\/|\;|\:|\[|\]', '',str.group())
                    result = result.split('|')
                    self.cursor['Team'] = result[0]
                else :
                    self.cursor['Team'] = ""


def main(sourceFileName):
    source = open(sourceFileName, 'rt', encoding='UTF8')

    handler = SoccerContentHandler()
    xml.sax.parse(source, handler,)
    sampling = random.sample(handler.buffer, 10)
    
    data = pd.DataFrame(sampling, columns=['PageID','PageTitle','TemplateName','DateofBirth','Height','Team'])
    data.to_csv("SoccerPlayer.csv", sep=',', encoding='ms949', index = False)
 
if __name__ == "__main__":
    main("data/kowiki-20180401-pages-articles-multistream.xml")
