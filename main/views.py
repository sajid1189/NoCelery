from django.http import HttpResponse
from datetime import datetime
from main.models import Foo
from main.tasks import incr_foo, create_foo


def home(request):
    f = Foo.objects.create(value=1)
    incr_foo(f.id, datetime.now().isoformat())
    return HttpResponse("Hello!")


def fifo(request):
    value = int(request.GET.get("value"))
    create_foo(value)
    return HttpResponse(f"created {value}")


