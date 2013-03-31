class SpreadsheetRow(object):
    """
    This class represents a row in a spreadsheet
    """
    def __init__(self, row, list_model, header_column_map, required_columns):
        self.row = row
        self.list_model_instance = list_model()
        self.list_model_fields = list_model._meta.get_all_field_names()
        self.header_column_map = header_column_map
        self.required_columns = required_columns
        self.unknown_information = {}

        self.parse_row()

    def parse_row(self):
        required_columns_count_list = [0] * len(self.required_columns)
        required_columns_count = dict(zip(self.required_columns, required_columns_count_list))
        for idx, cell in enumerate(self.row):
            header_name = self.header_column_map[idx]
            if header_name in self.list_model_fields:
                self._update_required_column_count_with_header_name(header_name.lower(), required_columns_count)
                setattr(self.list_model_instance, self.header_column_map[idx], cell.value)
            else:
                self.unknown_information[header_name] = cell.value

    def _update_required_column_count_with_header_name(self, header_name, required_columns_count):
        if header_name.lower() in self.required_columns:
            required_columns_count[header_name.lower()] += 1
