import oauth2
import json
import urllib2
import urllib
import sys


def request( path, url_params, consumer_key, consumer_secret, token, token_secret):
        #unsigned URL
        encoded_params = ''
        if url_params:
                encoded_params = urllib.urlencode(url_params)
        url = '%s?%s' % (path, encoded_params)
        print 'URL: %s' % (url,)

        #Sign the URL
        consumer = oauth2.Consumer(consumer_key, consumer_secret)
        oauth_request = oauth2.Request('GET', url, {})
        oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),'oauth_timestamp': oauth2.generate_timestamp(), 'oauth_token': token,'oauth_consumer_key': consumer_key})
        token = oauth2.Token(token, token_secret)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        signed_url = oauth_request.to_url()
        print 'Signed URL: %s\n' % (signed_url,)

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


def main():
        #if sys.argv[1].find('@') >=0:
        #	calendar_list.append(sys.argv[1])

        name = "landmark"
        category = "restaurants,bars"
        url = "http://api.yelp.com/v2/search"
        consumer_key = "pz_fQdRGcSi900RmV9vgKQ"
        consumer_secret = "c1XQmeyrbjlGVux5VsRd7xr0ZVo"
        token =	"QGWeXgOtqTfGDWHdJZTkqyzQZFQ-hEMB"
        token_secret = "NIJ2I1e2Wmqy0lOaRJhIC-vj4E0"

        params = {'term': name, 'location': '10 Columbus Circle', 'limit': '2', 'category_filter': category}
        response = request(url, params, consumer_key, consumer_secret, token, token_secret)

        print json.dumps(response, sort_keys=True, indent=2)


if __name__ == '__main__':
        main()
