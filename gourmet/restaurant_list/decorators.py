from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.mail import mail_admins
from django.utils.translation import ugettext as _
from lib.authorization_check import Authorization_Check
import sys


def json_view(func):
	"""
	Taken from http://djangosnippets.org/snippets/622/
	"""
	def wrap(request, *a, **kw):
		response = None
		try:
			response = func(request, *a, **kw)
			assert isinstance(response, dict)
			if 'result' not in response:
				response['result'] = 'success'
		except KeyboardInterrupt:
			# Allow keyboard interrupts through for debugging.
			raise
		except Exception, e:
			# Mail the admins with the error
			exc_info = sys.exc_info()
			subject = 'JSON view error: %s' % request.path
			try:
				request_repr = repr(request)
			except:
				request_repr = 'Request repr() unavailable'
			import traceback
			message = 'Traceback:\n%s\n\nRequest:\n%s' % (
			'\n'.join(traceback.format_exception(*exc_info)),
			request_repr,
			)
			mail_admins(subject, message, fail_silently=True)

			# Come what may, we're returning JSON.
			if hasattr(e, 'message'):
				msg = e.message
			else:
				msg = _('Internal error')+': '+str(e)
				response = {'result': 'error', 'text': msg}

		json = simplejson.dumps(response)
		return HttpResponse(json, mimetype='application/json')
	return wrap

def authorization_required(authorization_type):

    def decorator(func):
        user_to_display = None
        def wrap(request, *args, **kwargs):
            if 'user' in kwargs:
                user_to_display = kwargs['user']
            else:
                user_to_display = request.user

            auth_check = Authorization_Check(authorization_type)
            if not auth_check.is_authorized(request.user, user_to_display):
                return HttpResponseRedirect('/')

            return func(request, *args, **kwargs)

        return wrap
    return decorator

