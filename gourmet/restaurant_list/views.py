import xlrd
import json
from lib.shortcuts import render_to_response
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.forms import ValidationError
from django.db.models import Q
from forms import UploadRestaurantFileForm, AddRestaurantForm, EditRestaurantForm
from models import restaurant_list_for_user, RestaurantListElement, fetch_restaurant_from_database_or_api
from models import sort_by_options_for_restaurant_list, sort_direction_options_for_restaurant_list
from decorators import json_view, authorization_required
from lib.authorization_check import Authorization_Check, DELETE_ACTION, VIEW_ACTION, EDIT_ACTION
from restaurant_list.lib.yelp_api import Yelp_API
from taggit.models import Tag


def display_home_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/list/')
    else:
        return render(request, 'home.html', content_type="text/html")


@require_POST
@login_required
@json_view
def upload_restaurant_list_from_file(request):
    form = UploadRestaurantFileForm(request.POST, request.FILES)
    if form.is_valid():
        print 'Valid form!'
        input_excel = request.FILES['input_spreadsheet']
        book = xlrd.open_workbook(file_contents=input_excel.read())

        restaurant_list = restaurant_list_for_user(request.user)
        results = restaurant_list.update_restaurant_list_with_file_data(book)
        print 'Got results!'
        print results

        return {'result': 'success'}

    raise ValidationError('Invalid form!')


def _get_restaurant_list_elements_for_user(user):
    restaurant_list = restaurant_list_for_user(user)
    order_direction_sign = '-' if restaurant_list.sort_direction == 'DESC' else ''

    restaurant_elements = restaurant_list.restaurantlistelement_set.all().order_by(
        order_direction_sign + restaurant_list.sort_by
    )
    for restaurant_element in restaurant_elements:
        restaurant_element.raw_upload_info = json.loads(restaurant_element.raw_upload_info)
        restaurant_element.tags = [{'id': tag.name, 'name': tag.name} for tag in restaurant_element.tags.all()]

    return restaurant_elements


def _render_restaurant_list_response_with_template(request, template_name, restaurant_elements, user_to_display):
    restaurant_list = restaurant_list_for_user(user_to_display)
    return render_to_response(
        request,
        template_name,
        {
            'modals_to_include': ['edit', 'add'],
            'sort_by_options': sort_by_options_for_restaurant_list(),
            'sort_by_for_list': restaurant_list.sort_by,
            'sort_direction_for_list': restaurant_list.sort_direction.lower(),
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

    restaurant_elements = _get_restaurant_list_elements_for_user(user_to_display)

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

    restaurant_elements = _get_restaurant_list_elements_for_user(user_to_display)

    return _render_restaurant_list_response_with_template(
        request,
        'restaurant_list/list.html',
        restaurant_elements,
        user_to_display
    )


@require_POST
@login_required
def update_restaurant_list_sorting_for_user_and_return_updated_list(request):
    user = request.user
    sort_by = request.POST['sort_by']
    sort_direction = request.POST['sort_direction']
    sort_direction_is_correct = sort_direction.upper() in sort_direction_options_for_restaurant_list()
    sort_by_is_correct = sort_by in sort_by_options_for_restaurant_list()
    if sort_by_is_correct and sort_direction_is_correct:
        restaurant_list = restaurant_list_for_user(user)
        restaurant_list.sort_by = sort_by
        restaurant_list.sort_direction = sort_direction.upper()
        restaurant_list.save()

    return display_restaurant_list_for_user(request, user)


def display_restaurant_list_for_current_user(request):
    return display_restaurant_list_for_user(request, request.user)


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
@json_view
def restaurant_search(request):
    search_term = request.GET.get('term')
    location = request.GET.get('location')

    yelp_api = Yelp_API()
    api_result = yelp_api.search(search_term, location)

    return api_result.format_matches_for_display()


def _get_restaurant_list_element_fields_from_form(form_data):
    list_element_fields = {
        'has_been': form_data['has_been'],
    }
    if 'notes' in form_data:
        list_element_fields['notes'] = form_data['notes']
    if 'rating' in form_data:
        list_element_fields['rating'] = form_data['rating']
    return list_element_fields


@require_POST
@login_required
@json_view
@authorization_required(EDIT_ACTION)
def add_restaurant_to_list(request):
    form = AddRestaurantForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        yelp_api = Yelp_API()
        restaurant_info = yelp_api.fetch_restaurant_info(form_data['restaurant_id'])
        restaurant = fetch_restaurant_from_database_or_api(restaurant_info)

        list_element_fields = _get_restaurant_list_element_fields_from_form(form_data)

        list_element_fields['restaurant'] = restaurant

        list_element = RestaurantListElement()

        list_element.set_list(restaurant_list_for_user(request.user))
        list_element.set_all_fields_from_restaurant_and_element_info(list_element_fields, restaurant, {})

        return {'result': 'success'}

    # TODO (zak): Throw exception that is handled by JSON
    return {'result': 'error'}


@require_POST
@login_required
@json_view
@authorization_required(EDIT_ACTION)
def delete_restaurant_from_list(request):
    id = request.POST['id']
    RestaurantListElement.objects.get(pk=id).delete()
    return {'result': 'success'}


@require_POST
@login_required
@json_view
@authorization_required(EDIT_ACTION)
def edit_restaurant_list_element(request):
    form = EditRestaurantForm(request.POST)
    print "HASDLAKSJDLAKSDJLAKSDJ"
    print form.is_valid()
    if form.is_valid():
        form_data = form.cleaned_data
        list_element = RestaurantListElement.objects.get(pk=form_data['restaurant_list_element_id'])

        list_element_fields = _get_restaurant_list_element_fields_from_form(form_data)

        list_element.set_all_fields_from_restaurant_and_element_info(list_element_fields, None, {})

        if 'tags' in form_data:
            list_element.tags.set(form_data['tags'])

        return {'result': 'success'}

    # TODO (zak): Throw exception that is handled by JSON
    return {'result': 'error'}


@require_POST
@login_required
@authorization_required(EDIT_ACTION)
def set_tags_for_restaurant_list_element(request):
    tags = request.POST['tags']
    restaurant_list_element = RestaurantListElement.objects.get(pk=request.POST['restaurant_list_element_id'])

    restaurant_list_element.tags.set(tags)


@login_required
@json_view
def get_filtered_tags_for_current_user(request, filter_term=''):
    user = request.user
    if filter_term:
        tags = Tag.objects.filter(Q(name__startswith=filter_term), restaurantlistelement__restaurantList__owner=user).distinct()
    else:
        tags = Tag.objects.filter(restaurantelement__owner=user).distinct()
    return [{'id': tag.name, 'name': tag.name} for tag in tags]
