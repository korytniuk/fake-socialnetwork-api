from django.utils.timezone import now


def last_request_middleware(get_response):
    def middleware(request):

        response = get_response(request)

        if request.user.is_authenticated:
            user = request.user
            user.last_request = now()
            user.save()

        return response

    return middleware
