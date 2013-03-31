

class Spreadsheet(object):

    def __init__(self, list_model, data):
        """
        Takes in a list model to translate to and the raw spreadsheet data
        """

    def _get_headers_from_sheet(self, sheet):
        """
        Gets headers from the given excel sheet. Assumes that the headers are in row 0
        """
        header_row = sheet.row(0)
