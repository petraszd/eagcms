from google.appengine.api import users
from django.shortcuts import redirect, render_to_response
from django.conf import settings

def admin_required(func):
    def newfunc(request, *args, **kwargs):
        if users.is_current_user_admin():
            return func(request, *args, **kwargs)

        user = users.get_current_user()
        if not user:
            return _toaccount(request)

        emails = (email for name, email in settings.ADMINS)
        if not user.email() in emails:
            return _noaccess(request)
        return func(request, *args, **kwargs)
    return newfunc

def _toaccount(request):
    uri = request.build_absolute_uri()
    return redirect(users.create_login_url(uri))

def _noaccess(request):
    return render_to_response('eagadmin/noaccess.html')

