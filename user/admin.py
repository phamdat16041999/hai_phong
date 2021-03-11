from django.contrib import admin
from .models import Album, Cart, Category, Music, Group_music
# Register your models here.
class InlineGroup_music(admin.TabularInline):
    model = Group_music
class AlbumAdmin(admin.ModelAdmin):
    inlines = [InlineGroup_music]
    list_display = ['Name', 'Description']
    list_filter = ['Name']
    search_fields = ['Name']
admin.site.register(Album, AlbumAdmin)
class Group_musicAdmin(admin.ModelAdmin):
    list_display = ['AlbumID', 'Music_ID']
    list_filter = ['AlbumID']
    search_fields = ['AlbumID']
admin.site.register(Group_music, Group_musicAdmin)
class MusicAdmin(admin.ModelAdmin):
    inlines = [InlineGroup_music]
    list_display = ['Name', 'Singer', 'CategoryID']
    list_filter = ['Singer']
    search_fields = ['Name']
admin.site.register(Music, MusicAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Description']
    list_filter = ['Name']
    search_fields = ['Name']
admin.site.register(Category, CategoryAdmin)