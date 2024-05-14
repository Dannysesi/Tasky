from django.contrib import admin
from .models import *
from user.models import *

# Register your models here.
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(Profile)