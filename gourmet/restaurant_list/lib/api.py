import oauth2
import json
import urllib2
import urllib
import urlparse

class API(object):
    """
    Abstract class to define API interface
    """

    def search(self, name, location):
        raise NotImplementedError("This should be implemented in a subclass")

    def fetch_restaurant_info(self, restaurant_id):
        raise NotImplementedError("This should be implemented in a subclass")


    def _request(self):
        """
        Creates a request for an API with oauth2
        """

        #Sign the URL
        url_params = {}
        # oauth doesn't handle unicode very well, so I've done some of the url construction manually
        for k,v in self.url_params.iteritems():
            if isinstance(v, unicode):
                v = v.encode('utf-8')
            url_params[k] = v
        url = self.path + '?' + urllib.urlencode(url_params)
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
        signed_url = self._to_url(oauth_request)

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

    def _to_url(self, oauth_request):
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


