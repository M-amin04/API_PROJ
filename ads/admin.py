from django.contrib import admin
from . import models


@admin.register(models.Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'publisher')
    list_filter = ('date_added',)
    search_fields = ('title',)
    list_per_page = 15
    readonly_fields = ('date_added',)
