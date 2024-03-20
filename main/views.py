from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from main.tasks import add, test_func, incr_foo
from main.models import Foo

# Create your views here.


def home(request):
    f = Foo.objects.create(value=3)
    incr_foo(f.id, datetime.now().isoformat())
    return HttpResponse("Hello!")
