from django import forms

class UploadRestaurantFileForm(forms.Form):
    restaurant_file = forms.FileField()
