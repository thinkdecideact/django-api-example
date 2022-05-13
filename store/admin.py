from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'priority', 'ctime', 'mtime', 'is_active', 'is_del')
    list_editable = ('name', 'address', 'priority', )
    search_fields = ('name',)
    readonly_fields = ('id',)

    fields = ('name', 'address', 'priority', )
    # exclude = ('ctime', 'mtime',)

    list_per_page = 30