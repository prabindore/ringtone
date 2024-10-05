from django.contrib import admin
from .models import CustomUser, Ringtone, State, City, Ringtone_Language, Notification

# Custom admin for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'user_name', 'user_type', 'status', 'created_at', 'last_activity']
    search_fields = ['email', 'user_name']
    list_filter = ['user_type', 'status', 'user_gender', 'created_at']
    readonly_fields = ['last_activity', 'created_at', 'updated_at']

# Custom admin for Ringtone Language
class RingtoneLanguageAdmin(admin.ModelAdmin):
    list_display = ['language_name', 'status', 'created_at', 'updated_at']
    search_fields = ['language_name']
    list_filter = ['status']

# Custom admin for Ringtone
class RingtoneAdmin(admin.ModelAdmin):
    list_display = ['ringtone_title', 'ringtone_language', 'status', 'created_at', 'get_total_download', 'get_total_views', 'is_hyped']
    search_fields = ['ringtone_title', 'ringtone_language__language_name', 'user__user_name']
    list_filter = ['status', 'ringtone_language', 'created_at', 'is_hyped', 'is_all']
    readonly_fields = ['get_total_views', 'get_total_download', 'created_at', 'updated_at']

    # Add callable methods for total_download and total_views
    def get_total_download(self, obj):
        # Placeholder logic, adjust based on how you store total downloads
        return obj.play_times  # Adjust this if you have a separate field for total downloads

    get_total_download.short_description = 'Total Downloads'

    def get_total_views(self, obj):
        # Placeholder logic, adjust based on how you store total views
        return obj.play_times  # Adjust this if you have a separate field for total views

    get_total_views.short_description = 'Total Views'

# Custom admin for Notification
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_title', 'user', 'notification_on']
    search_fields = ['notification_title', 'user__user_name']
    list_filter = ['notification_on']
    readonly_fields = ['notification_on']

# Register models to admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ringtone, RingtoneAdmin)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Ringtone_Language, RingtoneLanguageAdmin)
admin.site.register(Notification, NotificationAdmin)