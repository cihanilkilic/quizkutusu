from django.contrib import admin
from.models import Profile, Classroom, School,UserSubscribeEdit
admin.site.register(Profile)
admin.site.register(Classroom)
admin.site.register(School)
admin.site.register(UserSubscribeEdit)


from django.contrib.auth.models import User

# Customizing User admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser')


# Register User model with custom admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)