from django.contrib.auth import authenticate, login


def auto_login(get_response):

    def middleware(request):

        if not  request.user.is_authenticated:
            user = authenticate(username='admin', password='Lexa2010')
            login(request, user)

        return get_response(request)
    
    return middleware