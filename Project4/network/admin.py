from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("follows",)

admin.site.register(User, UserAdmin)
admin.site.register(Post)




# Register your models here.
