from django.shortcuts import render,HttpResponse

# Create your views here.
def baseview(request):
    return render(request,'base.html')