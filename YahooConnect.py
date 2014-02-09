import oauth2 as oauth
import urlparse
import webbrowser
from pycascade import cascade

from code import interact

GET_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_token'
AUTHORIZATION_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth'
REQUEST_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
CALLBACK_URL = 'oob'


def getConsumer():

    with open("consumer.txt", "r") as f:
        f = f.readlines()
        CONSUMER_KEY = f[0].strip()
        CONSUMER_SECRET = f[1].strip()

    return oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)


def writeAccessToken(consumer, verbose=True):


    # Step 1 : Sign up for a Yahoo api key


    client = oauth.Client(consumer)


    # Step 2: Get a request token


    # params = { # don't actually need these ! Request takes care of it
    #     'oauth_nonce': oauth.generate_nonce(),
    #     'oauth_timestamp': oauth.generate_timestamp(),
    #     "oauth_consumer_key": CONSUMER_KEY,
    #     "oauth_signature_method": "HMAC-SHA1",
    #     "oauth_signature": CONSUMER_SECRET,
    #     'oauth_version': '2.0',
    #     "xoauth_lang_pref": "en-us",
    #     "oauth_callback": CALLBACK_URL,
    # }
    # url = REQUEST_TOKEN_URL + "?" + "&".join([ k + "=" + str(v) for k, v in params.iteritems() ])

    url = REQUEST_TOKEN_URL + "?" + "oauth_callback" + "=" + CALLBACK_URL
    resp, content = client.request(url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))

    if verbose:
        print "\nRequest Token:"
        print "- oauth_token        = %s" % request_token['oauth_token']
        print "- oauth_token_secret = %s" % request_token['oauth_token_secret']
        print 


    # Step 3: Authenticate the user and get the user authorization for your application


    print "\nGo to the following link in your browser:\n%s\n" % request_token['xoauth_request_auth_url']
    webbrowser.open(request_token['xoauth_request_auth_url'], new=2)

    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized yet? (y/n) ')
    oauth_verifier = raw_input('What is the PIN? ')


    # Step 4: Get the access token that enables making API calls


    token = oauth.Token(
        request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(GET_TOKEN_URL, "POST")

    with open("access.txt", "w") as f:
        f.write(content)

    return


def getAccessToken(verbose=True):

    with open("access.txt", "r") as f:
        content = f.read()

    access_token = dict(urlparse.parse_qsl(content))

    if verbose:
        print "Access Token:"
        print "- oauth_token        = %s" % access_token['oauth_token']
        print "- oauth_token_secret = %s" % access_token['oauth_token_secret']
        print "- oauth_session_handle = %s" % access_token['oauth_session_handle']
        print "- xoauth_yahoo_guid = %s" % access_token['xoauth_yahoo_guid']

        print "\nYou may now access protected resources using the access tokens above.\n" 

    return access_token


def refreshAccessToken():



    return


def callAPI(consumer, access_token, method, params=[{}]):

    token = oauth.Token(
        access_token['oauth_token'],
        access_token['oauth_token_secret']
        )

    jc = cascade.JSON11Client(consumer, token)
    result = jc.call(method, params=params)

    return result


def callAPI2(access_token):
    """Not sure what I'm doing here"""

    url = "http://social.yahooapis.com/v1/user/%s/profile?format=json&" % access_token["xoauth_yahoo_guid"]

    params = {
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': oauth.generate_timestamp(),
        "oauth_consumer_key": CONSUMER_KEY,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_signature": CONSUMER_SECRET,
        'oauth_version': '1.0',
        "oauth_token": access_token["oauth_token"],
        "oauth_signature": access_token["oauth_token_secret"],
        "realm": "yahooapis.com",
    }
    url = url + "&".join([ k + "=" + str(v) for k, v in params.iteritems() ])

    token = oauth.Token(
        access_token['oauth_token'],
        access_token['oauth_token_secret'])
    client = oauth.Client(consumer, token)

    resp, content = client.request(url, "GET")
    print resp
    print content

    return


def main():

    consumer = getConsumer()

    try:
        access_token = getAccessToken(False)
    except pycascade.cascade.CascadeError, e:
        # instead I should just refresh it
        writeAccessToken(consumer)
        access_token = getAccessToken()

    folders = callAPI(consumer, access_token, "ListFolders")["result"]["folder"]
    for f in folders:
        fid = f["folderInfo"]["fid"]
        if fid == "Inbox":
            numMessages = f["total"]

    params = {
        "fid": "Inbox",
        "startMid": 0,
        "numMid": numMessages,
        "startInfo": 0,
        "numInfo": numMessages,
    }

    messages = callAPI(consumer, access_token, "ListMessages", params=[params])["result"]["messageInfo"]
    for i, m in enumerate(messages, 1):
        print i, m["subject"]
        # print m["mid"], "\n"
        if i == 1:
            mid = m["mid"]

    #read the first message
    params = {
        "fid": "Inbox",
        "mid": ["%s" % mid, ],
        "truncateAt": 1000,
    }

    messages = callAPI(consumer, access_token, "GetMessage", params=[params])["result"]["message"]

    for message in messages:
        m = message["part"]
        for dic in m:
            if dic["subtype"] == "plain":
                print "\n", dic["text"], "\n"

    return


if __name__ == '__main__':
    main()




