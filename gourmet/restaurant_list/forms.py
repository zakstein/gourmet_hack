from django import forms

class UploadRestaurantFileForm(forms.Form):
    input_spreadsheet = forms.FileField()
