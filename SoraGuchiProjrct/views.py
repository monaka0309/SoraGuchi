from django.shortcuts import render # type: ignore

def page_not_found(request, exception):
    print(exception)
    return render(request, "404.html", status=404)