from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Goal, Expense, Challenge

admin.site.register(User, UserAdmin)
admin.site.register(Goal)
admin.site.register(Expense)
admin.site.register(Challenge)