from django.contrib import admin
from .models import Genre, Movie, Review

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'rating')
    list_filter = ('genres', 'release_year')
    search_fields = ('title', 'description')
    filter_horizontal = ('genres',)
    readonly_fields = ('rating',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('text', 'movie__title', 'user__username')
    readonly_fields = ('created_at',)

admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)