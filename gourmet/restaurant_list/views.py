import xlrd
from forms import UploadRestaurantFileForm
from models import restaurant_list_for_user

def upload_restaurant_list_from_file(request):
    form = UploadRestaurantFileForm(request.POST, request.FILES)
    if form.is_valid():
        input_excel = request.FILES['input_excel']
        book = xlrd.open_workbook(file_contents=input_excel)

        restaurant_list = restaurant_list_for_user(request.user)
        restaurant_list.update_restaurant_list_with_file_data(book)

def display_restaurant_list(request):
    pass
