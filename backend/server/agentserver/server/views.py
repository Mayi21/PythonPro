from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import User, Instance



def index(request):
    return HttpResponse("request path:{}".format(request.path))


def save_user(request):
    user = User(name='xiaohei', gender='m', age=10)
    user.save()
def get_user(request):
    data = User.objects.all()
    return HttpResponse(data)

