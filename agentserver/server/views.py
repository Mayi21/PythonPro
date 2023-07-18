
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .service import get_command_res






# index page
def index(request):
    return render(request, "index.html", {})

# get result of execute command
@csrf_exempt
def get_cmd_res(request):
    get_command_res(request)
