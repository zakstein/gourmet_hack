import xlrd
import json
from lib.shortcuts import render_to_response
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from forms import UploadRestaurantFileForm
from models import restaurant_list_for_user, RestaurantListElement
from decorators import json_view,authorization_required
from lib.authorization_check import Authorization_Check, DELETE_ACTION, VIEW_ACTION, EDIT_ACTION

@require_POST
@login_required
@json_view
def upload_restaurant_list_from_file(request):
    form = UploadRestaurantFileForm(request.POST, request.FILES)
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

def _render_restaurant_list_response_with_template(request, template_name, restaurant_elements, user_to_display):
    return render_to_response(
        request,
        template_name,
            {
            'restaurant_list': restaurant_elements,
            'can_edit_rows': Authorization_Check(EDIT_ACTION).is_authorized(request.user, user_to_display),
            },
    )

@login_required
@authorization_required(VIEW_ACTION)
def display_restaurant_list_and_upload_for_user(request, user_to_display):
    user = request.user
    if not user_to_display:
        user_to_display = user

    restaurant_elements = _get_restaurant_list_for_user(user_to_display)

    return _render_restaurant_list_response_with_template(
        request,
        'restaurant_list/list_page.html',
        restaurant_elements,
        user_to_display
        )


def display_restaurant_list_and_upload_for_current_user(request):
    return display_restaurant_list_and_upload_for_user(request, request.user)

@login_required
@authorization_required(VIEW_ACTION)
def display_restaurant_list_for_user(request, user_to_display):
    user = request.user
    if not user_to_display:
        user_to_display = user

    restaurant_elements = _get_restaurant_list_for_user(user_to_display)

    return _render_restaurant_list_response_with_template(
        request,
        'restaurant_list/list.html',
        restaurant_elements,
        user_to_display
    )

@login_required
def show_restaurant_search(request, restaurant_list_element_id):
    restaurant_list_element = None
    if restaurant_list_element_id:
        restaurant_list_element = RestaurantListElement.objects.get(pk=restaurant_list_element_id)
    return render_to_response(
        request,
        'restaurant_list/search.html',
        {
            'restaurant_list_element': restaurant_list_element,
        }
    )

@login_required
def restaurant_search(request, query, restaurant_list_element_id):
    pass
