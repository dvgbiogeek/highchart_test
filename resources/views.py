from django.shortcuts import render


def resource(request):
    return render(request, 'resource.html')
