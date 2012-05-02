## Matthias Orlowski
## 04/29/2012
## Script to parse ecolex.org entries

#!/opt/local/bin/python2.7

import urllib2
from BeautifulSoup import BeautifulSoup
from kitchen.text.converters import to_unicode
from gApi import defineApi
from gTranslate import translate, identify

class EcoLexResult(object):

    def __init__(self,entryurl, gApi = None):
        #check for google api key, request if necessary
        if gApi != None:
            self.gApi = defineApi(gApi)
        else:
            self.gApi = defineApi()

        self.entryurl = entryurl
        table = self.getHTMLTable()
        fieldList = self.getFieldList(table)
        entryList = self.getEntryList(table)
        
        self.ecolex_id = self.getEntry('Legislation ID number',fieldList,entryList)
        self.name = self.getEntry('Title of tex',fieldList,entryList)
        self.country = self.getEntry('Country',fieldList,entryList)
        self.date = self.getEntry('Date of tex',fieldList,entryList)
        self.legtype = self.getEntry('Type of documen',fieldList,entryList)
        self.source = self.getEntry('Source',fieldList,entryList)
        self.fulltext = self.getUrl('Link to full tex',fieldList,entryList)
        self.abstract = self.getEntry('Abstrac',fieldList,entryList)

        # concatenate subject and keywords only of there are entries
        keywordsA = self.getEntry('Keyword(s)',fieldList,entryList)
        keywordsB = self.getEntry('Subject(s)',fieldList,entryList)
        if keywordsA != None and keywordsB != None:
            self.keywords = keywordsA + '; ' + keywordsB
        elif keywordsA != None and keywordsB == None:
            self.keywords = keywordsA
        elif keywordsA == None and keywordsB != None:
            self.keywords = keywordsB
        else:
            self.keywords = None

        # check language and translate keywords and abstract if not english
        if self.abstract != None:
            languageSample = ' '.join(self.abstract.split(' ')[0:5])
            self.language = identify(languageSample,self.gApi)
        
            if self.language != 'en':
                translationAB = translate(self.abstract,self.language,'en',self.gApi)
                self.abstractEN = to_unicode(translationAB)
                translationKW = translate(self.abstract,self.language,'en',self.gApi)
                self.keywordsEN = to_unicode(translationKW)
            else:
                self.abstractEN = self.abstract
                self.keywordsEN = self.keywords
        else:
            self.language = None
            self.abstractEN = None
            self.keywordsEN = None

    def getHTMLTable(self):
        """Get html table on webpage."""
        try:
            entry = urllib2.urlopen(self.entryurl).read()
            soup = BeautifulSoup(entry)
            table = soup.find('table')
            return table
        except:
            return None

    def getFieldList(self,table):
        """Get list with all fields in the html table."""
        try:
            fields = table.findAll('th')
            fieldList = []
            for th in fields:
                temp = str(th)
                out = temp.strip('\/<th>:')
                out = to_unicode(out)
                fieldList.append(out)
            return fieldList
        except:
            return None

    def getEntryList(self,table):
        """Get list with all entries in the html table."""
        try:
            entries = table.findAll('td')
            entryList = []
            for td in entries:
                temp = str(td)
                out = temp.strip('\/<td>')
                out = to_unicode(out)
                entryList.append(out)
            return entryList
        except:
            return None

    def getEntry(self,field,fieldList,entryList):
        """Get defined entry from html table."""
        try:
            position = fieldList.index(field)
            entry = entryList[position]
            return entry
        except:
            return None

    def getUrl(self,field,fieldList,entryList):
        """Get fulltext link from html table."""
        try:
            raw = self.getEntry(field,fieldList,entryList)
            temp = raw.split('"')
            return temp[1]
        except:
            return None

#toDo:
# check why there are so few translations after including the exceptions
# make sure the translator passes unicode instead of encoding it here (this leads to 'None' if no translation is passed.
        
