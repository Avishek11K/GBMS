# here models imported and the imported model along with registered are shown in-
# admin site i.e. the registered models like Home,Application,landlord are registered

from django.contrib import admin
from pyapp.models import Contact, Home, availablerent, landlord, RoomSeekerProfile, Application, HomeImage


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


class HomeImageInline(admin.TabularInline):
    model = HomeImage
    extra = 1


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'landlord', 'is_available', 'created_at')
    list_filter = ('is_available', 'location')
    search_fields = ('title', 'location')
    inlines = [HomeImageInline]


admin.site.register(availablerent)


@admin.register(landlord)
class LandlordAdmin(admin.ModelAdmin):
    # admin page for managing landlords: username, email and contact phone in one place
    list_display = ('user', 'get_email', 'phone')
    search_fields = ('user__username', 'user__email', 'phone')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(RoomSeekerProfile)
class RoomSeekerProfileAdmin(admin.ModelAdmin):
    # admin page for managing roomseekers: username, email and contact phone in one place
    list_display = ('user', 'get_email', 'phone')
    search_fields = ('user__username', 'user__email', 'phone')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'house', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'house__title')


admin.site.register(HomeImage)
