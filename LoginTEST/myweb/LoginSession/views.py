from django.shortcuts import render,HttpResponse
from LoginSession.models import MyUser
# Create your views here.
def baseview(request):
    return render(request,'base.html')


def indextest(request):
     pass