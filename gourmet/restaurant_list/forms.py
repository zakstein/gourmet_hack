from django import forms


class UploadRestaurantFileForm(forms.Form):
    input_spreadsheet = forms.FileField()


class BaseRestaurantForm(forms.Form):
    restaurant_name = forms.CharField()
    has_been = forms.BooleanField(required=False)
    rating = forms.IntegerField(required=False, min_value=1, max_value=100)
    notes = forms.CharField()

    def clean(self):
        cleaned_data = self.cleaned_data
        has_been_to_restaurant = cleaned_data['has_been']

        if 'rating' in cleaned_data:
            restaurant_rating = cleaned_data['rating']

        if has_been_to_restaurant and not restaurant_rating:
            raise forms.ValidationError('Need to rate the restaurant if you have been there')

        return cleaned_data


class EditRestaurantForm(BaseRestaurantForm):
    restaurant_list_element_id = forms.IntegerField()


class AddRestaurantForm(BaseRestaurantForm):
    restaurant_id = forms.CharField()
