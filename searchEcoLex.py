## Matthias Orlowski
## 04/19/2012
## Script to define search on ecolex.org and parse links to individual results

#!/opt/local/bin/python2.7

from selenium import webdriver
import re
    
class EcoLexSearch(object):

    def __init__(self):
        self.typeCheck = False
        self.countryCheck = False
        self.subjectCheck = False
        
        self.legType = None
        self.countries = None # change default to searching all countries
        self.subject = None
        self.searchUrl = None
        
        self.defineSearch()
        self.entrylinks = self.parseEntryLinks()


    def __str__(self):
        self.printSearchInput()

        
    def printSearchInput(self):
        "Generates output witch search specification."""
        print "You are searching ecolex.org with the following specification:\n"
        print "Subject: %s \n" % self.subject
        print "Document type: %s \n" % self.legType
        printCountries = self.countries.replace('; ','\n')
        print "Countries: %s \n" % printCountries
        

    def defineSearch(self):
        """Calls functions to define search terms."""
        self.defineLegType()
        self.defineSubject()
        self.countryDefault()
        self.generateSearchUrl()


# Functions to define the ecolex search
    def defineLegType(self):
        """Prompts user to define type of documents to be searched."""
        while self.typeCheck == False:
            prompt = self.userPrompts(1)
            typeid = raw_input(prompt )
            self.checkType(typeid)
            

    def checkType(self,typeid):
        """Checks whether input for document type is correct."""
        legtypes = ['common','courtdecisions','legislation','treaties','literature'] # this only works for legislation.
        if typeid not in ['1','2','3','4','5']:
            prompt = self.userPrompts(2)
            print prompt
            self.defineLegType()
        else:
            temp = int(typeid)-1
            self.legType = legtypes[temp]
            self.typeCheck = True


    def countryDefault(self):
        """Prompts user to define countries to be searched."""
        while self.countryCheck == False:
            prompt = self.userPrompts(4)
            countryDef = raw_input(prompt )
            self.checkCountries(countryDef)        


    def checkCountries(self,countries):
        """Checks whether input for countries is correct."""
        defaultCountires =  'Australia; Austria; Belgium; Canada; Cyprus; Czech Republic; Denmark; Bulgaria; Estonia; European Union; Finland; France; Germany; Greece; Hungary; Iceland; Ireland; Israel; Italy; Japan; Korea, Republic of; Latvia; Lithuania; Luxembourg; Malta; Mexico; Moldova, Republic of; Monaco; Netherlands; New Zealand; Norway; Poland; Portugal; Romania; Serbia; Serbia and Montenegro; Slovakia; Slovenia; Spain; Sweden; Switzerland; Turkey; Ukraine; United Kingdom; United States of America'
        if countries not in ['1','2','3']:
            prompt = self.userPrompts(2)
            print prompt
            self.countryDefault()
        elif countries == '1':
            self.countries = defaultCountires
            self.countryCheck = True
        elif countries == '2':
            self.defineCountries()
            self.countryCheck = True
        else:
            printCountries = defaultCountires.replace('; ','\n')
            print printCountries
            self.countryDefault()
            

    def defineCountries(self):
        """Prompts user to define type of documents to be searched."""
        prompt = self.userPrompts(3)
        countries = raw_input(prompt )
        self.countries = countries


    def defineSubject(self): # add more subjects
        """Prompts user to define subject to be searched."""
        while self.subjectCheck == False:
            prompt = self.userPrompts(5)
            subjectid = raw_input(prompt )
            self.checkSubject(subjectid)


    def checkSubject(self,typeid):
        """Checks whether user input for subject is correct."""
        subjects = ['Agriculture']
        if typeid not in ['1']:
            prompt = self.userPrompts(2)
            print prompt
            self.defineSubject()
        else:
            temp = int(typeid)-1
            self.subject = subjects[temp]
            self.subjectCheck = True

            
    def generateSearchUrl(self):
        """Generates url with specified search terms."""
        baseUrl = 'http://www.ecolex.org'
        resultsUrl = '/ecolex/ledge/view/SearchResults;'
        sessionUrl = 'DIDPFDSIjsessionid=788AAD9AED21D53066AD4A4ADF662CF3'
        dummyUrl = '?action=table.SetPage' # what's this?
        wordsUrl = '&allFields=&allFields_allWords=allWords'
        basinUrl = '&basin=&basin_allWords=allWords'
        countries = self.countries.replace('; ','%22+%22')
        countries = countries.replace(', ','%2C+')
        countries = countries.replace(' ','+')
        countryUrl = '&country=+%22' + countries + '%22&country_allWords=anyWord'
        indexUrl = '&index=documents'
        keywordUrl = '&keyword=&keyword_allWords=allWords'
        listingsUrl = '&listingField=&page=1'
        regionUrl = '&region=&region_allWords=allWords'
        screenUrl = '&screen=Legislation'
        dateEndUrl = '&searchDate_end='
        dateStartUrl = '&searchDate_start='
        sortUrl = '&sortField=searchDate'
        subjectUrl = '&subject=' + self.subject + '&subject_allWords=allWords'
        tableUrl = '&tableId=1'
        subdivisionUrl = '&territorialSubdivision=&territorialSubdivision_allWords=allWords'
        titleUrl = '&titleOfText=&titleOfText_allWords=allWords'
        typeUrl = '&typeOfText=' + self.legType
    
        self.searchUrl = baseUrl + resultsUrl + sessionUrl + dummyUrl + wordsUrl + basinUrl + countryUrl + indexUrl + keywordUrl + listingsUrl + regionUrl + screenUrl + dateEndUrl + dateStartUrl + sortUrl + subjectUrl + tableUrl + subdivisionUrl + titleUrl + typeUrl


    def userPrompts(self,types):
        """Generates user prompts."""
        if types == 1:
            return "What type of documents do you want to search for? 1.'All', 2.'Court Decisions', 3.'Legislation', 4.'Treaties', or 5.'Literature' >> "
        elif types == 2:
            return "Please enter your choice as an integer."
        elif types == 3:
            return "Which countries do you want to search? (Please enter english country names, separated by a semicolon, with the first letter capitalized.) >> "
        elif types == 4:
            return "Do you want to search the default set of countries? 1.'Yes', 2.'No', 3.'Show default countries' >> "
        elif types == 5:
            return "Which subject do you want to search for? 1.'Agriculture' >> "


# Functions to parse search results. This requires firefox to render dynamic urls

    def parseEntryLinks(self):
        """Open search url in Firefox and screen scrape all links to single entries."""
        entrylinks = []
        driver = webdriver.Firefox()
        driver.get(self.searchUrl)
        idx = 1
        while True:
            links = driver.find_elements_by_partial_link_text('')
            for l in links:
                href = l.get_attribute('href')
                match = re.search( 'id=LEX', href )
                if match != None:
                    entrylinks.append(href)
            idx = idx + 1
            nextpage = driver.find_elements_by_link_text( str(idx) )
            if nextpage == []:
                break
            else:
                nextpage[0].click()
        driver.close()
        return entrylinks

# toDos:
# add search by keywords, date etc.
# add more default subjects
# correct document type (only works for legislation now)
# include user prompt for browser selection
