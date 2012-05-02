## Matthias Orlowski
## 04/29/2012
## Script to crawl ecolex.org

#!/opt/local/bin/python2.7

__author__ = 'Matthias Orlowski'
__email__ = 'mace84@gmail.com'

import searchEcoLex
from searchEcoLex import EcoLexSearch

import makeEcoLexEntry
from makeEcoLexEntry import EcoLexResult

import addEcoLexEntry
from addEcoLexEntry import addEntry, startSession

from gApi import defineApi


class EcoLexCrawl(object):
    def __init__(self, gApi = None):
        if gApi != None:
            self.gApi = defineApi(gApi)
        else:
            self.gApi = gApi
        while self.gApi == None:
            self.gApi = defineApi()

        self.firstTime()
        self.search = EcoLexSearch()
        self.entriesAdded = 0
        self.enterNewResults()


    def firstTime(self):
        """Prompts user about creating a new data base."""
        first = raw_input("Is this the first time you run EcoLex Crawler? 1. 'Yes', 2. 'No' >> " )
        if first == '1':
            self.firsttime = True
        else:
            self.firsttime = False

    def enterResults(self,links):
        """Pass results to database"""
        for link in links:
            newentry = EcoLexResult(link,self.gApi)
            addEntry(newentry,self.firsttime)
            if self.firsttime == True:
                self.firsttime = False
            self.entriesAdded = self.entriesAdded + 1
        
    def enterNewResults(self):
        """Checks whether scraped entries are in database already and passes new ones to database"""
        links = self.search.entrylinks
        if not self.firsttime:
            for link in links:
                start = link.rfind('id=') + 3
                end = link.rfind('&',start)
                ecolexID = link[start:end]
                session = startSession()
                check = session.query(addEcoLexEntry.EcoLexEntry).filter(addEcoLexEntry.EcoLexEntry.ecolex_id == ecolexID ).count()
                session.commit()
                if check == 1:
                    links.remove(link)
                else:
                    pass
                
        self.enterResults(links)

    def printReport(self):
        """Prints a report of the specified search."""
        self.search.printSearchInput()
        print "This specification led to %i new entries in your data base." % self.entriesAdded
        
        
def startEcoLexCrawler():
    """Initiates Ecolex crawler."""
    newSearch = EcoLexCrawl()
    newSearch.printReport()
    return newSearch
    

# toDos:
# make using google translate optional
# prompt about whether to create new data base or use existing one
# specify path for where data base is created
# reduce the number of times writing on disc to speed things up
# generate relational database with keywords and ecolex identifiers in one, keywords and google analytics results in another, and the one created here without keywords
# get relational data for amentments, 
