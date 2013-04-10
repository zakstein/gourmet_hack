from exceptions import RequiredColumnNotFound

class SpreadsheetRow(object):
    """
    This class represents a row in a spreadsheet
    """
    def __init__(self,
                 row,
                 list_element_model,
                 header_column_map,
                 required_columns,
                 list_model_instance
    ):
        self.row = row
        self.list_element_model_instance = list_element_model()
        self.header_column_map = header_column_map
        self.required_columns = required_columns
        self.unclassified_info = {}

        self.list_element_model_instance.set_list(list_model_instance)

    def parse_row(self):
        """
        Parses the raw spreadsheet row into the list_model class and unclassified info
        """
        self.unclassified_info = self.list_element_model_instance.set_all_fields_from_spreadsheet_row_and_save(
            self.row,
            self.header_column_map,
        )

        if not self._check_required_columns_are_present():
            raise RequiredColumnNotFound('Required column not populated')

    def _check_required_columns_are_present(self):
        """
        Checks if the required columns are present and returns true if they are
        """
        required_columns_count = dict(zip(
            self.required_columns,
            [0] * len(self.required_columns)
        ))
        for idx, cell in enumerate(self.row):
            self._update_required_column_count_with_header_name(
                self.header_column_map[idx].lower(),
                required_columns_count
            )
        for required_column, count in required_columns_count.items():
            if count != 1:
                return False

        return True


    def _update_required_column_count_with_header_name(self, header_name, required_columns_count):
        if header_name in self.required_columns:
            required_columns_count[header_name.lower()] += 1
