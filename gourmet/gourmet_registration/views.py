from django.http import HttpResponse
from django.contrib.auth.models import User


"""def register(request,form_class=RegistrationForm, profile_callback=None,template_name='registration/registration_form.html'):

        if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(profile_callback=profile_callback)
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            return HttpResponseRedirect(success_url or reverse('registration_complete'))
    else:
        form = form_class()

    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context) Create your views here.

"""

from django.contrib.auth import authenticate, login

def gourmet_login(request):
            username = request.POST['username']
                password = request.POST['password']
                print username
                print password

                user = authenticate(username=username, password=password)
                if user is not None:
                        if user.is_active:
                                login(request, user)
                                # Redirect to a success page.
                                return HttpResponseRedirect(reverse('registration_complete'))
                        else:
                                # Return a 'disabled account' error message
                else:
                        # Return an 'invalid login' error message.
