try:
    import simplejson as json
except:
    import json

import urllib2

def trim(trim_to=False):
    """
    Decorator to shorten the JSON output of each API method.
    Trim will always be set to True unless specified otherwise.
    """
    def wrap(func):
        def wrapped_f(*args, **kwargs):
            if 'trim' in kwargs:
                trim = kwargs.pop('trim')
            else:
                trim = True
            response = func(*args, **kwargs)
            if trim and 'error' not in response:
                response = response['result']
                if trim_to:
                    response = response[trim_to]
            return response
        return wrapped_f
    return wrap


class SaploError(Exception):
        """
        Is thrown when an request to the Saplo API for some reason fails

        All requests to the SaploJSOnClient should catch this exception, and handle it
        """
        def __init__(self, value):
                super(SaploError, self).__init__(value)
                self.value = value
        def __str__(self):
                return repr(self.value)

class SaploJSONClient:
        """
         Saplo JSON Client.
         Handles authentication and json-requests to the saplo API Server.

         All requests to the SaploJSONClient should catch the SaploError that is thrown if a request fails

         Example of request usage: All these requests returns a dictionary that you can use to retrieve data
         try:
                client = SaploJSONClient()
                client.createCorpus("My new Corpus", "Some description text", "sv")
                client.addArticle(corpusId, TitleString, LeadString, BodyString, Date, "someurl.com", "some author")
                client.getEntityTags(corpusId, articleId, waittime)
                client.getSimilarArticles(corpusId, articleId, wait, numberOfResults, minThreshold, maxThreshold)
                client.getCorpusPermission()
        except SaploError, err:
                print err.__str__()
                
        """
        url         = "http://api.saplo.com/rpc/json?access_token={token}"
        apikey      = ''
        secretkey   = ''
        token       = ''
                        
        def __init__(self,apikey, secretkey, token=None):
                """
                Initiates the Saplo JSONClient using the secret & api keys
                @type String
                @param Saplo API key
                @type String
                @param Saplo Secret key
                """
                self.apikey     = apikey
                self.secretkey  = secretkey
                self.token      = token
                self.__createSession(self.apikey, self.secretkey)
                
                self.collection = Collection(self)
                self.text = Text(self)
                self.group = Group(self)
                self.account = Account(self)

        def __createSession(self, apiKey, secretKey):
                """
                Creates a session towards the Saplo API

                @type String
                @param apikey - The apikey to access the Saplo API
                @type String
                @param secretkey - The secret key to access the Saplo API
                """
                #Request a new session
                response = self.doRequest('auth.accessToken', {'api_key':apiKey, 'secret_key':secretKey})
               
                # Get the response
                jsonresponse = response.read()
                # If our request fails, raise an SaploException
                try:
                        self.handleJSONResponse(jsonresponse)
                except SaploError, err:
                        raise err
                # Decode the JSON request and retrieve the token, establishing it as our given token.
                result = json.loads(jsonresponse)

                token  = result['result']['access_token']
                self.__setTokenTo(token)
                
        def doRequest(self, meth, param,sapid=0):
                
                '''
                Creates an JSON request to the server from the params
                '''
                #HTTP params
                options = json.dumps(dict(
                        method = meth,
                        params = param,
                        id=sapid))
                
                #Parse the url-string to contain our session-token
                url = self.url.format(token = self.token)
                
                #Create HTTP request
                request  = urllib2.Request(url,options)
                response = urllib2.urlopen(request)
                return response
                
        def __setTokenTo(self, t):
                '''
                Sets the class token string to the given param
                '''
                self.token = t;
                
        def handleJSONResponse(self, jsonresponse):
                response = json.loads(jsonresponse)
                #If errors, handle them
                if "error" in response:
                        errormsg  =  "Unknown error" if ('msg' not in response['error']) else response['error']['msg']
                        errorcode =  "" if ('code' not in response['error']) else response['error']['code']                    
                        
                        #Create a readable error message
                        msg = "An error has occured: '{errormessage}' With code = ({errorcode})".format(
                                        errormessage = errormsg,
                                        errorcode    = errorcode,
                                        );
                        #Raise an SaploError
                        raise SaploError(msg)
                ##Otherwise we have a sucessfull response
                return response
                
                
class Account:
    def __init__(self, api):
        self.api = api

    @trim()
    def get(self, **kwargs):
        response = self.api.doRequest('account.get', kwargs)
        return self.api.handleJSONResponse(response.read())
                
class Collection:
    def __init__(self, api):
        self.api = api

    @trim()
    def create(self, **kwargs):
            response = self.api.doRequest('collection.create', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def get(self, **kwargs):
            response = self.api.doRequest('collection.get', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def update(self, **kwargs):
            response = self.api.doRequest('collection.update', kwargs)
            return self.api.handleJSONResponse(response.read())
        
    @trim()
    def delete(self, **kwargs):
            response = self.api.doRequest('collection.delete', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def list(self, **kwargs):
            response = self.api.doRequest('collection.list', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def reset(self, **kwargs):
            response = self.api.doRequest('collection.reset', kwargs)
            return self.api.handleJSONResponse(response.read())


class Group:
    def __init__(self, api):
        self.api = api

    @trim()
    def create(self, **kwargs):
            response = self.api.doRequest('group.create', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def get(self, **kwargs):
            response = self.api.doRequest('group.get', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def update(self, **kwargs):
            response = self.api.doRequest('group.update', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def delete(self, **kwargs):
            response = self.api.doRequest('group.delete', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def list(self, **kwargs):
            response = self.api.doRequest('group.list', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def list_texts(self, **kwargs):
            response = self.api.doRequest('group.listTexts', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def add_text(self, **kwargs):
            response = self.api.doRequest('group.addText', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def delete_text(self, **kwargs):
            response = self.api.doRequest('group.deleteText', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def related_groups(self, **kwargs):
            response = self.api.doRequest('group.relatedGroups', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def related_texts(self, **kwargs):
            response = self.api.doRequest('group.relatedTexts', kwargs)
            return self.api.handleJSONResponse(response.read())

class Text:
    def __init__(self, api):
        self.api = api

    @trim()
    def create(self, **kwargs):
            response = self.api.doRequest('text.create', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def get(self, **kwargs):
            response = self.api.doRequest('text.get', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def update(self, **kwargs):
            response = self.api.doRequest('text.update', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def delete(self, **kwargs):
            response = self.api.doRequest('text.delete', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def tags(self, **kwargs):
            response = self.api.doRequest('text.tags', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def related_texts(self, **kwargs):
            response = self.api.doRequest('text.relatedTexts', kwargs)
            return self.api.handleJSONResponse(response.read())

    @trim()
    def related_groups(self, **kwargs):
            response = self.api.doRequest('text.relatedGroups', kwargs)
            return self.api.handleJSONResponse(response.read())