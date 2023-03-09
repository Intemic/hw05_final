from django.shortcuts import render


def page_not_found(request, exception):
    return render(
        request,
        'core/404_page_not_found.html',
        {'path': request.path}, status=404
    )


def csrf_failure(request, reason=''):
    return render(
        request,
        'core/403_csrf_failure.html'
    )


def access_denied(request, exception):
    return render(
        request,
        'core/403_permission_denied.html',
        {'path': request.path}, status=403
    )
