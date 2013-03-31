import oauth2
import json
import urllib2
import urllib
import sys

class MatchAPI:
        #Information from user's spreadsheet
        name = ""
        location = ""

        categories = "restaurants,bars"
        limit = "5"
        url_params = ""

        #Objects matched from API call
        top_match = ""
        alt_matches = ""

        #Yelp specific
        path = "http://api.yelp.com/v2/search"
        consumer_key = "pz_fQdRGcSi900RmV9vgKQ"
        consumer_secret = "c1XQmeyrbjlGVux5VsRd7xr0ZVo"
        token =	"QGWeXgOtqTfGDWHdJZTkqyzQZFQ-hEMB"
        token_secret = "NIJ2I1e2Wmqy0lOaRJhIC-vj4E0"


        def __init__(self, name, location):
                self.name = name
                self.location = location
                self.url_params = {'term': self.name, 'location': self.location, 'limit': self.limit, 'category_filter': self.categories}

        def request(self):
                #unsigned URL
                encoded_params = ''
                if self.url_params:
                        encoded_params = urllib.urlencode(self.url_params)
                url = '%s?%s' % (self.path, encoded_params)
                #print 'URL: %s' % (url,)

                #Sign the URL
                consumer = oauth2.Consumer(self.consumer_key, self.consumer_secret)
                oauth_request = oauth2.Request('GET', url, {})
                oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),'oauth_timestamp': oauth2.generate_timestamp(), 'oauth_token': self.token,'oauth_consumer_key': self.consumer_key})
                token = oauth2.Token(self.token, self.token_secret)
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

        def execute(self):
                if self.name is "" or self.location is "":
                        return
                response = self.request()
                if response['total'] == 0:
                        return

                businesses = []
                for business in response['businesses']:
                        businesses.append({'name': business['name'], 'address': business['location'], 'url': business['url']})

                self.top_match = businesses[0]
                self.alt_matches = businesses[1:]


def main():
        name = "landmarc"
        location = "10 Columbus Circle"
        restaurant = MatchAPI(name,location)
        restaurant.execute()
        print restaurant.alt_matches


if __name__ == '__main__':
        main()
