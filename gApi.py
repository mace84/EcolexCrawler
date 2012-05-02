## Matthias Orlowski
## 04/28/2012
## Project: Ecolex crawler	
## Python script to initiate and test Google apis

import urllib
try:
    import simplejson
except ImportError:
    import json as simplejson

    
class GApi(object):

    def __init__(self,gApi=None,service="translate"):
	self.error = None
	if gApi == None:
	    self.gApi = self.getAuthorization()
	else:
	    self.gApi = gApi

	if service == "translate":
	    self.baseurl = "https://www.googleapis.com/language/translate/v2"

	self.valid = self.testAuthorization()
	
	if not self.valid:
	    self.printMessages(1)
	    self.gApi = None
	    self.printMessages(2)


    def __str__(self):
	return self.gApi

			    
    def userPrompts(self,types):
        if types == 1:
            return "Please enter your Google API key >> "


    def printMessages(self,types):
	if types == 1:
	    print "You cannot access the service you chose with the API key you entered.\nThe reason google reports for this is:\n%s " % self.error
	elif types == 2:
	    print "Please try again with a valid google API key for the service you want to use."


    def getAuthorization(self):
        """User prompt for authorization keys."""
        prompt = self.userPrompts(1)
        gApiKey = raw_input(prompt )
        return gApiKey

    
    def testAuthorization(self):
	"""Tests validity of Google API."""
	request = '%s/detect?key=%s&q=test' %(self.baseurl,self.gApi)
	content = urllib.FancyURLopener().open(request)
	json = simplejson.load(content)
	if json.has_key('data'):
		return True
	elif json.has_key('error'):
		self.error = json['error']['errors'][0]['reason']
		return False


def defineApi(gApi = None):
	myApi = GApi(gApi)
	return myApi.gApi
