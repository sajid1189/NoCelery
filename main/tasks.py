from main.models import Foo
from main.task_decorators import task
from main.fifo_task_decorators import fifo_task


@task
def add(x, y):
    print("I am adding")
    return x + y


@task
def incr_foo(f_id, d):
    f = Foo.objects.get(id=f_id)
    f.value += 100
    f.save()
    print("updated on ", d)


def test_func(a=1, b=2):
    print(a, b)


@fifo_task
def create_foo(value: int):
    foo = Foo.objects.create(value=value)
    print(f"created: {foo}")
