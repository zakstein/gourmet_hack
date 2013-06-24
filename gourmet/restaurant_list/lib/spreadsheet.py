from spreadsheet_row import SpreadsheetRow
from exceptions import RequiredColumnNotFound

class Spreadsheet(object):

    MAX_SPREADSHEET_ROW_COUNT = 1000

    def __init__(self, list_model_instance, data, required_headers):
        """
        Takes in a list model to translate to and the raw spreadsheet data
        The required headers are headers that if we don't find, we will throw an error
        """
        self.list_model_instance = list_model_instance
        self.data = data
        self.required_headers = required_headers
        self.header_to_column_index_map = {}

    def parse(self, list_element_model):
        """
        The main function in the module: We parse the spreadsheet into list_element_model
        objects
        """

        # For now, we assume that each data set only has one sheet
        sheet = self.data.sheet_by_index(0)
        headers = self._get_headers_from_sheet(sheet)
        if not self._check_headers_have_required_headers(headers):
            raise Exception('Required headers were not found')

        self._map_header_name_to_column_index(headers)

        row_results = []

        print sheet.nrows
        print sheet.row(1)
        print list_element_model
        for i in range(1, min(self.MAX_SPREADSHEET_ROW_COUNT, sheet.nrows)):
            try:
                print "Trying row " + str(i)
                row = SpreadsheetRow(
                    sheet.row(i),
                    list_element_model,
                    self
                )
                row.parse_row()
                row_results.append(row)
                if i > 3:
                    break
            except RequiredColumnNotFound:
                print "Required column not found"
            except ValueError:
                print "Error saving values"


        return row_results


    def _get_headers_from_sheet(self, sheet):
        """
        Gets headers from the given excel sheet. Assumes that the headers are in row 0
        """
        header_row = sheet.row(0)
        return header_row

    def _check_headers_have_required_headers(self, headers):
        """
        Checks the given headers against the required headers
        Returns true if the required headers are present
        """
        required_headers_found_count = 0
        for header in headers:
            if header.value.lower() in self.required_headers:
                required_headers_found_count += 1

        return required_headers_found_count == len(self.required_headers)

    def _map_header_name_to_column_index(self, headers):
        """
        Maps the header column indexes to their values
        """

        for idx, header in enumerate(headers):
            self.header_to_column_index_map[idx] = header.value

