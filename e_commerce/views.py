from django.shortcuts import render 
# Create your views here. 
def sview(request): 
    return render(request, "index.html") 