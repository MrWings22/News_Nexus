from django.shortcuts import render


def Indexpage(request):
    return render(request, "index.html")

def Homepage(request):
    return render(request, "home.html")

def Detailedpage(request):
    return render(request, "detail-page.html")