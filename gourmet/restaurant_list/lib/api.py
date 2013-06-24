import oauth2
import json
import urllib2
import urllib
import urlparse
import difflib
import re


# Usage:
#>>> restaurant = MatchAPI (name,location)
#>>> restaurant.execute()
#
#Key fields --> number_of_responses (if this is 0, the API call yielded no results), top_match, alt_matches (both contain 'name', 'url', and 'address'), match_confidence (True indicates that the restaurant is probably the right one

class MatchAPI:
        #Information from user's spreadsheet
        name = ""
        location = ""

        CATEGORIES = "restaurants,bars"
        MAX_RESULTS = "5"
        url_params = ""

        #Objects matched from API call
        top_match = ""
        alt_matches = ""
        number_of_responses = ""

        #For the strength of the top match
        match_confidence = False
        TOTAL_NUMBER_OF_MATCHES_CONFIDENCE = 75
        RATIO_OF_KEY_WORDS_MATCHED_CONFIDENCE = 0.66

        #Yelp specific
        PATH = "http://api.yelp.com/v2/search"
        CONSUMER_KEY = "pz_fQdRGcSi900RmV9vgKQ"
        CONSUMER_SECRET = "c1XQmeyrbjlGVux5VsRd7xr0ZVo"
        TOKEN =	"QGWeXgOtqTfGDWHdJZTkqyzQZFQ-hEMB"
        TOKEN_SECRET = "NIJ2I1e2Wmqy0lOaRJhIC-vj4E0"

        def __init__(self, name, location):
            # Remove parens
            name = re.sub('\(.*\)', '', name)
            self.name = name.lower()
            print self.name.encode('utf-8')
            self.location = re.sub('\(.*\)', '', location)
            print self.location
            self.url_params = {'term': self.name, 'location': self.location, 'limit': self.MAX_RESULTS, 'category_filter': self.CATEGORIES}

        def request(self):

                #Sign the URL
                url_params = {}
                # oauth doesn't handle unicode very well, so I've done some of the url construction manually
                for k,v in self.url_params.iteritems():
                    if isinstance(v, unicode):
                        v = v.encode('utf-8')
                    url_params[k] = v
                url = self.PATH + '?' + urllib.urlencode(url_params)
                consumer = oauth2.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
                oauth_request = oauth2.Request('GET', url=url)
                oauth_request.update({
                    'oauth_nonce': oauth2.generate_nonce(),
                    'oauth_timestamp': oauth2.generate_timestamp(),
                    'oauth_token': self.TOKEN,
                    'oauth_consumer_key': self.CONSUMER_KEY
                })
                token = oauth2.Token(self.TOKEN, self.TOKEN_SECRET)
                oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
                signed_url = self.to_url(oauth_request)

                # Connect
                try:
                    conn = urllib2.urlopen(signed_url, None)
                    try:
                        response = json.loads(conn.read())
                    finally:
                        conn.close()
                except urllib2.HTTPError, error:
                    response = json.loads(error.read())
                return response

        def top_match_confidence_check(self):
                full_name_matcher = difflib.SequenceMatcher(None, self.name, self.top_match['name'].lower())
                ratio = full_name_matcher.ratio();
                self.match_confidence = ratio > .75

        def parse_response(self, response):
            businesses = []
            for business in response['businesses']:
                businesses.append({'name': business['name'], 'address': business['location'], 'url': business['url']})
            self.top_match = businesses[0]
            self.alt_matches = businesses[1:]


        def execute(self):
                if self.name is "" or self.location is "":
                                return
                response = self.request()
                if not 'total' in response:
                    return

                self.number_of_responses = int(response['total'])

                if response['total'] == 0:
                                return
                self.parse_response(response)
                self.top_match_confidence_check()

        def to_url(self, oauth_request):
            """
            I implemented this method because to_url is broken in the Oauth2 library for unicode
            """
            base_url = urlparse.urlparse(oauth_request.url)
            try:
                query = base_url.query
            except AttributeError:
                # must be python <2.5
                query = base_url[4]
            query = oauth2.parse_qs(query.encode('utf-8'))
            for k, v in oauth_request.items():
                query.setdefault(k.encode('utf-8'), []).append(oauth2.to_utf8_optional_iterator(v))

            try:
                scheme = base_url.scheme.encode('utf-8')
                netloc = base_url.netloc.encode('utf-8')
                path = base_url.path.encode('utf-8')
                params = base_url.params.encode('utf-8')
                fragment = base_url.fragment.encode('utf-8')
            except AttributeError:
                # must be python <2.5
                scheme = base_url[0].encode('utf-8')
                netloc = base_url[1].encode('utf-8')
                path = base_url[2].encode('utf-8')
                params = base_url[3].encode('utf-8')
                fragment = base_url[5].encode('utf-8')

            url = (scheme, netloc, path, params,
                   urllib.urlencode(query, True), fragment)
            return urlparse.urlunparse(url)


def main():
        name = "AQ"
        location = "1085 Mission, San Francisco"
        restaurant = MatchAPI(name,location)
        restaurant.execute()
        print restaurant.top_match
        print restaurant.match_confidence


if __name__ == '__main__':
        main()
