import xlrd
import json
from lib.shortcuts import render_to_response
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from forms import UploadRestaurantFileForm
from models import restaurant_list_for_user
from decorators import json_view

@require_POST
@login_required
@json_view
def upload_restaurant_list_from_file(request):
    form = UploadRestaurantFileForm(request.POST, request.FILES)
    print form.is_valid()
    if form.is_valid():
        input_excel = request.FILES['input_spreadsheet']
        book = xlrd.open_workbook(file_contents=input_excel.read())

        restaurant_list = restaurant_list_for_user(request.user)
        results = restaurant_list.update_restaurant_list_with_file_data(book)
        print 'Got results!'
        print results

        return {'result': 'success'}

    return {'result': 'failure'}

def _get_restaurant_list_for_user(user):
    restaurant_elements = restaurant_list_for_user(user).restaurantlistelement_set.all()
    for restaurant_element in restaurant_elements:
        restaurant_element.raw_upload_info  = json.loads(restaurant_element.raw_upload_info)
        print restaurant_element.raw_upload_info

    return restaurant_elements

@login_required
def display_restaurant_list_and_upload(request):
    user = request.user

    restaurant_elements = _get_restaurant_list_for_user(user)

    return render_to_response(
        request,
        'restaurant_list/list_and_upload.html',
        {'restaurant_list': restaurant_elements},
    )

@login_required
def display_restaurant_list(request):
    user = request.user

    restaurant_elements = _get_restaurant_list_for_user(user)

    return render_to_response(
        request,
        'restaurant_list/list.html',
            {'restaurant_list': restaurant_elements},
    )

