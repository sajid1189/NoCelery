from django.db import models

# Create your models here.


class Foo(models.Model):
    value = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.value}"
