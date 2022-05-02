from django.shortcuts import render


def handler404_view(request, *args, **kwargs):
    response = render(
        request,
        'jobsearch/error/404.html',
        context={
            'information': 'Эта информация не представлена на сайте :('
        }
    )
    response.status_code = 404
    return response


def handler500_view(request, *args, **kwargs):
    response = render(
        request,
        'jobsearch/error/500.html',
        context={
            'information': 'Ой-ей, скоро мы это исправим!'
        }
    )
    response.status_code = 500
    return response
