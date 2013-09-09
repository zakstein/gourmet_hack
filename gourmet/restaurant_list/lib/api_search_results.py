import difflib

class Api_Search_Results(object):
    """
    Encapsulates a search result
    """

    def __init__(self, matches, total_number_of_matches, search_term):

        self.total_number_of_matches = total_number_of_matches
        self.search_term = search_term

        if total_number_of_matches > 0:
            self.top_match = matches[0]
            self.alt_matches = matches[1:]
            self.matches = matches
            self._top_match_confidence_check()


    def _top_match_confidence_check(self):
        full_name_matcher = difflib.SequenceMatcher(None, self.search_term, self.top_match['name'].lower())
        ratio = full_name_matcher.ratio();
        self.match_confidence = ratio > .75

    def format_matches_for_display(self):
        if len(self.matches) == 0:
            return []

        return [{'label': match['name'], 'value': match['api_id']} for match in self.matches]


