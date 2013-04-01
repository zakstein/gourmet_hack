import oauth2
import json
import urllib2
import urllib
import sys


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
                        self.name = name
                        self.location = location
                        self.url_params = {'term': self.name, 'location': self.location, 'limit': self.MAX_RESULTS, 'category_filter': self.CATEGORIES}

        def request(self):
                #unsigned URL
                encoded_params = ''
                if self.url_params:
                                encoded_params = urllib.urlencode(self.url_params)
                url = '%s?%s' % (self.PATH, encoded_params)
                print 'URL: %s' % (url,)

                #Sign the URL
                consumer = oauth2.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
                oauth_request = oauth2.Request('GET', url, {})
                oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),'oauth_timestamp': oauth2.generate_timestamp(), 'oauth_token': self.TOKEN,'oauth_consumer_key': self.CONSUMER_KEY})
                token = oauth2.Token(self.TOKEN, self.TOKEN_SECRET)
                oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
                signed_url = oauth_request.to_url()
                #print 'Signed URL: %s\n' % (signed_url,)

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
                ignore_words = ['the','of','by','in','on']
                name_list = self.name.lower().split(' ')
                top_match_name = self.top_match['name'].lower()
                bool_name_match = False
                count_of_key_words = 0
                count_of_key_words_matched = 0

                for word in name_list:
                        if word not in ignore_words:
                                count_of_key_words += 1
                                if word in top_match_name:
                                        count_of_key_words_matched += 1
                if count_of_key_words_matched/count_of_key_words > self.RATIO_OF_KEY_WORDS_MATCHED_CONFIDENCE  and self.number_of_responses < self.TOTAL_NUMBER_OF_MATCHES_CONFIDENCE:
                        self.match_confidence = True
                print name_list
                print top_match_name
                print count_of_key_words
                print count_of_key_words_matched
                print self.number_of_responses

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
                self.number_of_responses = int(response['total'])
                print self.number_of_responses

                if response['total'] == 0:
                                return
                self.parse_response(response)
                self.top_match_confidence_check()

def main():
        name = "tia pol"
        location = "chelsea new york"
        restaurant = MatchAPI(name,location)
        restaurant.execute()
        print restaurant.top_match
        print restaurant.match_confidence


if __name__ == '__main__':
        main()
