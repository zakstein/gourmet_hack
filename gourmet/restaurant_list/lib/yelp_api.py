import oauth2
import re

from api import API
from api_search_results import Api_Search_Results


# Usage:
#>>> restaurant = Yelp_API ()
#>>> restaurant.search(name, location)
#
#Key fields --> number_of_responses (if this is 0, the API call yielded no results), top_match, alt_matches (both contain 'name', 'url', and 'address'), match_confidence (True indicates that the restaurant is probably the right one


class Yelp_API(API):
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

        path = ""
        CONSUMER_KEY = "pz_fQdRGcSi900RmV9vgKQ"
        CONSUMER_SECRET = "c1XQmeyrbjlGVux5VsRd7xr0ZVo"
        TOKEN =	"QGWeXgOtqTfGDWHdJZTkqyzQZFQ-hEMB"
        TOKEN_SECRET = "NIJ2I1e2Wmqy0lOaRJhIC-vj4E0"

        def _parse_search_response(self, response):
            businesses = []
            for business in response['businesses']:
                businesses.append(self._extract_business_information(business))

            return businesses

        def _extract_business_information(self, business):
            return {
                'name': business['name'],
                'address': business['location'],
                'url': business['url'],
                'api_id': business['id']
            }

        def search(self, name, location):
            if name is "" or location is "":
                return None

            self.path = 'http://api.yelp.com/v2/search'

            # Remove parens
            name = re.sub('\(.*\)', '', name)
            name = name.lower()
            location = re.sub('\(.*\)', '', location)

            self.url_params = {
                'term': name,
                'location': location,
                'limit': self.MAX_RESULTS,
                'category_filter': self.CATEGORIES
            }

            response = self._request()
            if not 'total' in response:
                return None

            if response['total'] == 0:
                return Api_Search_Results([], 0, name)

            return Api_Search_Results(self._parse_search_response(response), response['total'], name)

        def fetch_restaurant_info(self, restaurant_id):
            """
            :param restaurant_id:
            :return:
            """
            self.path = 'http://api.yelp.com/v2/business/' + restaurant_id

            self.url_params = {}

            response = self._request()

            return self._extract_business_information(response)



def main():
        name = "AQ"
        location = "1085 Mission, San Francisco"
        yelp_api = Yelp_API()
        api_result = yelp_api.search(name,location)
        print api_result.top_match
        print api_result.match_confidence

        print yelp_api.fetch_restaurant_info(api_result.top_match['api_id'])


if __name__ == '__main__':
        main()
