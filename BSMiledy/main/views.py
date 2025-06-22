from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def politics(request):
    return render(request, 'main/politics.html')

def contacts(request):
    return render(request, 'main/contacts.html')