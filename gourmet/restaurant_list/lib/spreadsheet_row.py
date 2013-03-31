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
        self.list_model_element_instance = list_element_model()
        self.list_element_model_fields = list_element_model._meta.get_all_field_names()
        self.header_column_map = header_column_map
        self.required_columns = required_columns
        self.unclassified_info = {}

        self.list_model_element_instance.set_list(list_model_instance)

    def parse_row(self):
        """
        Parses the raw spreadsheet row into the list_model class and unclassified info
        """
        required_columns_count = dict(zip(
            self.required_columns,
            [0] * len(self.required_columns)
        ))

        for idx, cell in enumerate(self.row):
            header_name = self.header_column_map[idx].lower()
            if header_name in self.list_element_model_fields:
                self._update_required_column_count_with_header_name(
                    header_name,
                    required_columns_count
                )
                self.list_model_element_instance.set_field_from_spreadsheet_cell(
                    header_name,
                    cell.value
                )
            else:
                self.unclassified_info[header_name] = cell.value

        if not self._check_required_columns_are_present(required_columns_count):
            raise RequiredColumnNotFound('Required column not populated')

    def _check_required_columns_are_present(self, required_columns_count):
        """
        Checks if the required columns are present and returns true if they are
        """
        for required_column, count in required_columns_count.items():
            if count != 1:
                return False

        return True


    def _update_required_column_count_with_header_name(self, header_name, required_columns_count):
        if header_name in self.required_columns:
            required_columns_count[header_name.lower()] += 1
