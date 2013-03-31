import oauth2 as oauth
import json
import urllib2
import urllib
import sys

class YelpAPI:
        token = ""
        consumer = ""
        search_url = "http://api.yelp.com/v2/search"
        biz_url = "http://api.yelp.com/v2/business/"
        request_url = ""
        oauth_request = ""


        def __init__(self, consumer_key, consumer_secret, token_key, token_secret):
                self.consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
                self.token = oauth.Token(key=token_key, secret=token_secret)

        def biz_search(self, biz_name):
                self.request_url = "%s%s" % (self.biz_url, biz_name)
                self.init_request()
                return self.send_request()

        def search(self, params):
                if not params:
                        raise Exception("No params specified")

                encoded_params = urllib.urlencode(params)
                print encoded_params
                self.request_url = "%s?%s" % (self.search_url, encoded_params)
                self.init_request()
                return self.send_request()

        def init_request(self):
                self.oauth_request = oauth.Request('GET', self.request_url, {})
                self.oauth_request.update({'oauth_none': oauth.generate_nonce(), 'oauth_timestamp': oauth.generate_timestamp(), 'oauth_token': self.token.key, 'oauth_consumer_key': self.consumer.key})
                self.oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
                self.request_url = self.oauth_request.to_url()

        def send_request(self):
                try:
                        print self.request_url
                        conn = urllib2.urlopen(self.request_url, None)
                        try:
                                respone = json.loads(conn.read())
                        finally:
                                conn.close()
                except urllib2.HTTPError, error:
                        raise Exception('HTTP Error: %s' % error)
                return response

def main():
        #if sys.argv[1].find('@') >=0:
        #	calendar_list.append(sys.argv[1])

        name = "esperpento"
        consumer_key = "pz_fQdRGcSi900RmV9vgKQ"
        consumer_secret = "c1XQmeyrbjlGVux5VsRd7xr0ZVo"
        token =	"QGWeXgOtqTfGDWHdJZTkqyzQZFQ-hEMB"
        token_secret = "NIJ2I1e2Wmqy0lOaRJhIC-vj4E0"

        yelp = YelpAPI(consumer_key, consumer_secret, token, token_secret)

        params = {'term' : name}
        responses = yelp.search(params)
        print reponse


if __name__ == '__main__':
        main()
